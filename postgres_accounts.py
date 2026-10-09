"""云端 PostgreSQL 适配层；继续使用原有密码、会话和资料逻辑。"""
from collections import defaultdict, deque
from contextlib import contextmanager
import secrets
from threading import Lock
from urllib.parse import urlsplit, parse_qs
import psycopg
from psycopg.rows import dict_row
from accounts import Accounts


class Connection:
    def __init__(self, connection):self.connection=connection
    def execute(self, sql, params=None):
        # All statements are application-owned SQL. User values are bound separately.
        return self.connection.execute(sql.replace('?', '%s'), params)


class PostgresAccounts(Accounts):
    def __init__(self, dsn):
        parsed=urlsplit(dsn)
        if parsed.scheme not in ['postgres','postgresql'] or not parsed.hostname:
            raise RuntimeError('DATABASE_URL 需要有效的 PostgreSQL 连接地址。')
        if parse_qs(parsed.query).get('sslmode',[''])[0] not in ['require','verify-ca','verify-full']:
            raise RuntimeError('云数据库连接需要 sslmode=require 或证书验证模式。')
        self.database=dsn
        self.attempts=defaultdict(deque);self.lock=Lock()
        self.dummy_salt=secrets.token_bytes(16)
        self.dummy_hash=self.hash_password('not-an-account-password',self.dummy_salt)
        schema='''
            CREATE SCHEMA IF NOT EXISTS atlas;
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY, username TEXT NOT NULL,
                username_key TEXT NOT NULL UNIQUE, salt BYTEA NOT NULL,
                password_hash BYTEA NOT NULL, iterations INTEGER NOT NULL,
                created_at BIGINT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at BIGINT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS preferences (
                user_id BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                data TEXT NOT NULL DEFAULT '{"favorites":[],"gear":{}}'
            );
            CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires_at)
        '''
        with self.connect() as db:
            for statement in schema.split(';'):
                if statement.strip():db.execute(statement)

    @contextmanager
    def connect(self):
        with psycopg.connect(self.database,connect_timeout=10,row_factory=dict_row) as db:
            db.execute('SET LOCAL search_path TO atlas')
            yield Connection(db)

    def register(self, data, old_cookie):
        try:return super().register(data,old_cookie)
        except psycopg.errors.UniqueViolation:
            from accounts import AccountError
            raise AccountError(409,'这个用户名已被注册，请换一个，或直接登录。') from None
