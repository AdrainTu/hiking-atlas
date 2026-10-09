# 免费公网部署：Render + Neon

当前状态：GitHub 仓库 AdrainTu/hiking-atlas 已上传部署代码。Render 免费服务 hiking-atlas 已上线，区域为新加坡；公网地址 https://hiking-atlas.onrender.com 。Neon 加密连接和 atlas 专用 schema 初始化已验证。数据库连接串仅保存在本机 .env 和 Render 环境变量中。验收结果记录在 .deployment/neon.json。

## 部署内容

- Python 生产入口为 `production.py`（Flask + Waitress），不对外开放本机演示服务器。
- 云端使用 Neon PostgreSQL 的 `atlas` 专用 schema；保留原有密码散列、会话和账号资料逻辑。
- 注册、登录使用 HTTPS Secure / HttpOnly Cookie；校验公网域名、请求来源和 JSON 自定义请求头。
- 免费部署缺少 `DATABASE_URL` 会明确失败，避免误把用户数据存入临时文件。
- 本机 `start.bat` 与 SQLite 模式继续保留。

## 需要本人完成的账号步骤

1. 登录或创建 [GitHub](https://github.com/)、[Neon](https://console.neon.tech/) 与 [Render](https://dashboard.render.com/) 账号。平台条款、账号验证和授权由本人确认；选择免费套餐，不添加付费资源。
2. 在 Neon 创建专用于野途的免费 PostgreSQL 项目，尽量选择与 Render 接近的区域。连接字符串需包含 `sslmode=require`（或更严格证书验证模式）。连接字符串是秘密，不要发到聊天、提交 Git 或放进网页代码。
3. 建立私有 GitHub 仓库，将部署包解压后的文件作为仓库根目录上传；不要上传整个电脑工作目录。包内不含本机数据库、会话、日志、私钥或 `.env`。
4. 在 Render 用该仓库创建 Blueprint，配置文件为根目录 `render.yaml`，实例计划为 `free`。仅授权指定仓库。把 Neon 连接字符串填入 `DATABASE_URL` 的保密环境变量。
5. Render 提供 `RENDER_EXTERNAL_URL`，程序自动用它作为站点地址。自定义域名时把 `PUBLIC_URL` 设置为确切的 HTTPS 域名，且在平台完成域名验证。不要使用通配域名。
6. 等待构建通过、健康检查成功，使用 Render 实际返回的 `https://…onrender.com` 地址；不能根据项目名猜测可用网址。

免费套餐有资源额度和休眠机制，首次请求可能冷启动。Neon 免费数据库与 Render 免费文件系统不同，数据库内容不会依赖 Web 实例的临时目录。具体额度以平台当前页面为准。

## 部署后验收

- 公网首页与全部核心 JS / 图片元数据可加载。
- 用临时测试账号完成注册、错误密码、正确登录、退出。
- 收藏和装备在重登、服务重启后仍保留；两个账号不能相互读取或覆盖。
- 验证真实 Neon TLS 连接、PostgreSQL 初始化、唯一用户名冲突和会话到期。
- 不把密码、数据库 URL 或会话令牌放进日志及截图。

已完成真实公网 HTTPS + Neon PostgreSQL 联调：注册、登录、退出、错误密码、重复用户名、收藏与装备重登保存、账号隔离及私有文件访问保护均通过。临时验收账号已清理；verify_public.py 可重新执行验收。

## 资料

- [Render 免费服务与临时文件系统](https://render.com/docs/free)
- [Render Blueprint 配置](https://render.com/docs/blueprint-spec)
- [Neon 免费计划](https://neon.com/docs/introduction/free-tier)
- [Waitress 生产服务](https://flask.palletsprojects.com/en/stable/deploying/waitress/)
