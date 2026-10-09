"""公网入口：Waitress + Flask，HTTPS 托管平台终止 TLS，数据库单独持久保存。"""
import os
from pathlib import Path
import sqlite3
from urllib.parse import urlsplit
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException
from accounts import Accounts, AccountError, COOKIE, SESSION_SECONDS

ROOT=Path(__file__).resolve().parent


def create_app(public_url=None,database_path=None,testing=False):
    public_url=public_url or os.environ.get('PUBLIC_URL') or os.environ.get('RENDER_EXTERNAL_URL')
    if not public_url:raise RuntimeError('请配置 PUBLIC_URL 或使用 Render 提供的 RENDER_EXTERNAL_URL。')
    origin=public_url.rstrip('/')
    parsed=urlsplit(origin)
    if not parsed.hostname or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:
        raise RuntimeError('PUBLIC_URL 应为单一站点地址，不包含路径或账号。')
    if parsed.scheme!='https' and not (testing and parsed.scheme=='http'):
        raise RuntimeError('公网注册登录必须使用 HTTPS。')
    if database_path is not None and testing:
        store=Accounts(Path(database_path));database_errors=(sqlite3.Error,)
    elif os.environ.get('DATABASE_URL'):
        import psycopg
        from postgres_accounts import PostgresAccounts
        store=PostgresAccounts(os.environ['DATABASE_URL']);database_errors=(psycopg.Error,)
    elif os.environ.get('ATLAS_ALLOW_SQLITE')=='1' and os.environ.get('ATLAS_DATABASE'):
        store=Accounts(Path(os.environ['ATLAS_DATABASE']));database_errors=(sqlite3.Error,)
    else:
        raise RuntimeError('需要 DATABASE_URL 云数据库；免费托管不能保存到临时 SQLite 文件。')
    app=Flask(__name__,static_folder=None)
    app.config.update(TESTING=testing,MAX_CONTENT_LENGTH=65536,TRUSTED_HOSTS=[parsed.hostname,'127.0.0.1','localhost'])
    app.extensions['accounts']=store

    @app.before_request
    def validate_request():
        # The platform may probe health through an internal host. Health exposes no account data.
        if request.path!='/api/health' and request.host!=parsed.netloc:
            raise AccountError(403,'请通过本站公开地址访问。')
        if request.method=='POST':
            if request.headers.get('X-Atlas-Request')!='1' or request.headers.get('Origin')!=origin:
                raise AccountError(403,'请求来源不合法，请在项目页面操作。')
            if not request.is_json:raise AccountError(415,'请发送 JSON 格式。')

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
        if parsed.scheme=='https':response.headers['Strict-Transport-Security']='max-age=31536000'
        if request.path.startswith('/api/'):response.headers['Cache-Control']='no-store'
        return response

    @app.errorhandler(AccountError)
    def account_error(error):return jsonify(error=error.message),error.status

    @app.errorhandler(HTTPException)
    def http_error(error):
        messages={400:'请求格式不正确。',404:'接口或文件不存在。',405:'请求方法不支持。',413:'请求内容过大。'}
        return jsonify(error=messages.get(error.code,'请求未成功。')),error.code

    for error_type in database_errors:
        @app.errorhandler(error_type)
        def database_error(error):
            # Never print a database URL, SQL parameters or credentials to a public response.
            app.logger.error('Database operation unavailable (%s)',type(error).__name__)
            return jsonify(error='数据库暂时不可用，请稍后重试。'),503

    def body():
        data=request.get_json()
        if not isinstance(data,dict):raise AccountError(400,'请求格式不正确。')
        return data

    def current_user():return store.user(request.headers.get('Cookie'))

    @app.get('/api/health')
    def health():return jsonify(app='trail-atlas',status='ok')

    @app.get('/api/auth/me')
    def me():return jsonify(user=current_user())

    @app.post('/api/auth/<action>')
    def authenticate(action):
        if action=='logout':
            body();store.logout(request.headers.get('Cookie'))
            response=jsonify(user=None);response.delete_cookie(COOKIE,path='/',secure=parsed.scheme=='https',httponly=True,samesite='Strict');return response
        if action not in ['register','login']:raise AccountError(404,'接口不存在。')
        data=body();username,_=store.credentials(data,registering=action=='register')
        # Do not trust caller-supplied forwarding headers for authentication throttling.
        store.rate_limit('peer:'+str(request.remote_addr),limit=1000)
        store.rate_limit('account:'+username.casefold())
        method=store.register if action=='register' else store.login
        user,token=method(data,request.headers.get('Cookie'))
        response=jsonify(user=user);response.status_code=201 if action=='register' else 200
        response.set_cookie(COOKIE,token,max_age=SESSION_SECONDS,path='/',secure=parsed.scheme=='https',httponly=True,samesite='Strict')
        return response

    @app.route('/api/preferences',methods=['GET','POST'])
    def preferences():return jsonify(store.preferences(current_user(),body() if request.method=='POST' else None))

    @app.route('/api/routes/<route>/comments',methods=['GET','POST'])
    def comments(route):
        from comments import discuss
        result=discuss(store,route,current_user(),body() if request.method=='POST' else None,request.args.get('before'))
        return jsonify(result),201 if request.method=='POST' else 200

    @app.route('/api/submissions',methods=['GET','POST'])
    def submissions():
        from submissions import listing,publish
        if request.method=='POST':return jsonify(publish(store,current_user(),body())),201
        return jsonify(listing(store,request.args.get('before')))

    @app.get('/api/submissions/<rid>')
    def submitted_route(rid):
        from submissions import get_route
        return jsonify(get_route(store,rid))

    @app.get('/api/users')
    def people():
        from social import people
        return jsonify(people(store,request.args.get('search',''),request.args.get('after')))

    @app.get('/api/users/<int:uid>')
    def profile(uid):
        from social import profile
        return jsonify(profile(store,uid,current_user()))

    @app.get('/api/users/<int:uid>/<kind>')
    def connections(uid,kind):
        from social import people
        return jsonify(people(store,before=request.args.get('after'),uid=uid,kind=kind))

    @app.post('/api/users/<int:uid>/follow')
    def follow(uid):
        from social import follow
        return jsonify(follow(store,uid,current_user(),body()))

    @app.route('/',defaults={'path':'index.html'})
    @app.route('/<path:path>')
    def static_file(path):
        if path.startswith('api/') or any(part.startswith('.') for part in Path(path).parts):raise AccountError(404,'接口或文件不存在。')
        return send_from_directory(ROOT/'web',path)

    return app


if __name__=='__main__':
    from waitress import serve
    try:application=create_app()
    except Exception as error:
        # Connection errors may include credentials: report configuration status without their text.
        raise SystemExit('公网服务初始化失败，请检查站点地址、云数据库配置与连接权限。') from None
    serve(application,host='0.0.0.0',port=int(os.environ.get('PORT','8080')),threads=4,max_request_body_size=65536,connection_limit=100,channel_timeout=30)
