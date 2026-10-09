"""本地 SQLite 账号、密码散列与会话；不需要第三方依赖。"""
import hashlib
import hmac
import json
import re
import secrets
import sqlite3
import time
from collections import defaultdict, deque
from http.cookies import SimpleCookie, CookieError
from threading import Lock
from contextlib import contextmanager

ITERATIONS = 600_000
SESSION_SECONDS = 7 * 24 * 60 * 60
COOKIE = 'atlas_session'


class AccountError(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


class Accounts:
    def __init__(self, database):
        self.database = database
        database.parent.mkdir(parents=True, exist_ok=True)
        self.attempts = defaultdict(deque)
        self.lock = Lock()
        self.dummy_salt = secrets.token_bytes(16)
        self.dummy_hash = self.hash_password('not-an-account-password', self.dummy_salt)
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    username_key TEXT NOT NULL UNIQUE,
                    salt BLOB NOT NULL,
                    password_hash BLOB NOT NULL,
                    iterations INTEGER NOT NULL,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS preferences (
                    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                    data TEXT NOT NULL DEFAULT '{"favorites":[],"gear":{}}'
                );
                CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires_at);
            ''')
        from comments import initialize
        initialize(self)
        from social import initialize as initialize_social
        initialize_social(self)
        from submissions import initialize as initialize_submissions
        initialize_submissions(self)
        from route_photos import initialize as initialize_photos
        initialize_photos(self)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.database, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def hash_password(password, salt, iterations=ITERATIONS):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)

    def rate_limit(self, address, limit=20):
        now = time.monotonic()
        with self.lock:
            if address not in self.attempts and len(self.attempts) >= 5000:
                expired=[key for key,values in self.attempts.items() if not values or values[-1]<now-300]
                for key in expired:del self.attempts[key]
                if len(self.attempts)>=5000:raise AccountError(429, '操作太频繁，请稍后重试。')
            attempts = self.attempts[address]
            while attempts and attempts[0] < now - 300:
                attempts.popleft()
            if len(attempts) >= limit:
                raise AccountError(429, '操作太频繁，请在 5 分钟后重试。')
            attempts.append(now)

    @staticmethod
    def credentials(data, registering=False):
        username, password = data.get('username'), data.get('password')
        if not isinstance(username, str) or not isinstance(password, str):
            raise AccountError(400, '请填写用户名和密码。')
        username = username.strip()
        if not re.fullmatch(r'[A-Za-z0-9_\u4e00-\u9fff]{3,24}', username):
            raise AccountError(400, '用户名需为 3–24 位中文、字母、数字或下划线。')
        if len(password) > 128 or not password:
            raise AccountError(400, '密码最长 128 个字符，不能为空。')
        if registering and len(password) < 12:
            raise AccountError(400, '密码至少需要 12 个字符，可使用易记的长口令。')
        return username, password

    @staticmethod
    def token_from_cookie(header):
        try:
            cookie = SimpleCookie()
            cookie.load(header or '')
            return cookie[COOKIE].value if COOKIE in cookie else ''
        except CookieError:
            return ''

    @staticmethod
    def token_hash(token):
        return hashlib.sha256(token.encode()).hexdigest()

    def user(self, header):
        token = self.token_from_cookie(header)
        if not token or len(token) > 100:
            return None
        with self.connect() as db:
            row = db.execute('''SELECT users.id, username FROM sessions JOIN users
                ON users.id=sessions.user_id WHERE token_hash=? AND expires_at>?''',
                (self.token_hash(token), int(time.time()))).fetchone()
            return dict(row) if row else None

    def create_session(self, db, user_id, old_cookie):
        old_token = self.token_from_cookie(old_cookie)
        db.execute('DELETE FROM sessions WHERE expires_at<=? OR token_hash=?',
                   (int(time.time()), self.token_hash(old_token)))
        token = secrets.token_urlsafe(32)
        db.execute('INSERT INTO sessions VALUES (?,?,?)',
                   (self.token_hash(token), user_id, int(time.time()) + SESSION_SECONDS))
        return token

    def register(self, data, old_cookie):
        username, password = self.credentials(data, registering=True)
        salt = secrets.token_bytes(16)
        password_hash = self.hash_password(password, salt)
        with self.connect() as db:
            try:
                cursor = db.execute('''INSERT INTO users
                    (username,username_key,salt,password_hash,iterations,created_at)
                    VALUES (?,?,?,?,?,?) RETURNING id''',
                    (username, username.casefold(), salt, password_hash, ITERATIONS, int(time.time())))
            except sqlite3.IntegrityError:
                raise AccountError(409, '这个用户名已被注册，请换一个，或直接登录。') from None
            user = {'id': cursor.fetchone()['id'], 'username': username}
            db.execute('INSERT INTO preferences (user_id) VALUES (?)', (user['id'],))
            token = self.create_session(db, user['id'], old_cookie)
        return user, token

    def login(self, data, old_cookie):
        username, password = self.credentials(data)
        with self.connect() as db:
            row = db.execute('SELECT * FROM users WHERE username_key=?', (username.casefold(),)).fetchone()
            salt, expected, iterations = (row['salt'], row['password_hash'], row['iterations']) if row else (self.dummy_salt, self.dummy_hash, ITERATIONS)
            actual = self.hash_password(password, salt, iterations)
            if not hmac.compare_digest(actual, expected) or not row:
                raise AccountError(401, '用户名或密码不正确。')
            token = self.create_session(db, row['id'], old_cookie)
            return {'id': row['id'], 'username': row['username']}, token

    def logout(self, header):
        with self.connect() as db:
            db.execute('DELETE FROM sessions WHERE token_hash=?',
                       (self.token_hash(self.token_from_cookie(header)),))

    def preferences(self, user, data=None):
        if not user:
            raise AccountError(401, '请先登录。')
        with self.connect() as db:
            if data is None:
                row = db.execute('SELECT data FROM preferences WHERE user_id=?', (user['id'],)).fetchone()
                value=json.loads(row['data']) if row else {'favorites': [], 'gear': {}}
                value.setdefault('completed',[])
                return value
            # Account ID prevents delayed writes after switching accounts.
            if data.get('userId') != user['id']:
                raise AccountError(409, '账号已切换，请刷新后重试保存。')
            favorites, gear = data.get('favorites'), data.get('gear')
            valid_id = lambda value: isinstance(value, str) and re.fullmatch(r'[a-z0-9-]{1,50}', value)
            if not isinstance(favorites, list) or len(favorites) > 200 or not all(valid_id(x) for x in favorites):
                raise AccountError(400, '收藏格式不正确。')
            if not isinstance(gear, dict) or len(gear) > 200:
                raise AccountError(400, '装备清单格式不正确。')
            for key, checks in gear.items():
                if not valid_id(key) or not isinstance(checks, list) or len(checks) > 100 or not all(type(i) is int and 0 <= i < 100 for i in checks):
                    raise AccountError(400, '装备清单格式不正确。')
            existing=db.execute('SELECT data FROM preferences WHERE user_id=?',(user['id'],)).fetchone()
            completed=data.get('completed',json.loads(existing['data']).get('completed',[]) if existing else [])
            from submissions import valid_ids
            if not isinstance(completed,list) or len(completed)>200 or not all(isinstance(item,str) for item in completed) or len(valid_ids(self,completed))!=len(set(completed)):
                raise AccountError(400,'已走过线路格式不正确。')
            value = {'favorites': list(dict.fromkeys(favorites)), 'gear': gear, 'completed':list(dict.fromkeys(completed))}
            db.execute('INSERT INTO preferences VALUES (?,?) ON CONFLICT(user_id) DO UPDATE SET data=excluded.data',
                       (user['id'], json.dumps(value, ensure_ascii=False)))
            return value
