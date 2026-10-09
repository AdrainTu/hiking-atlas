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


公开 Git 仓库 URL 部署不支持自动发布；后续代码提交后需触发 Render 手动部署，并确认新部署的 commit 与 GitHub main 一致。线路讨论保存在 atlas.comments 表，应用启动自动执行可重复初始化。


足迹与社交：已走过线路保存在账号 preferences.completed 数组，兼容旧客户端不传此字段的写入；公开主页仅返回用户名、用户 ID、已走过线路与关注计数。关注关系保存在 atlas.follows 表，唯一约束防止重复关注。


用户投稿：atlas.route_submissions 持久保存标准化线路与作者。登录后表单投稿，支持客户端解析 1 MB 内单段 GPX，采样最多 300 个展示点；原始 GPX 文件与设备元数据不上传。公开内容具有社区投稿标识，未作独立路线核验；支持评论、收藏及已走过足迹。公开列表每页 50 条，可继续加载，分享链接支持按 ID 加载。

国内资料新增 24 条，维护数据位于 domestic-additions.json，由 build_china.py 合并。暂缺已授权照片的线路明确保留空相册；不把其他地点的照片当作线路实拍。


线路照片：route_photos 表持久保存重编码 JPEG 与审核记录，单图压缩后最多 240 KB，全站图片上限 50 MB；每账号最多 10 张待审核，5 分钟最多 5 次提交。原图前端缩放，服务端解码验证、尺寸限制、再次重编码并去除 EXIF。所有照片初始 pending，仅上传者与审核员能访问，approved 才公开；审核员可拒绝并填原因，也可将 approved 下架为 rejected。ATLAS_MODERATOR_IDS 为明确授权的网站用户 ID 逗号列表，默认空，不会自动赋予首位注册用户权限。

此免费方案采用基础文件检查加人工内容审核，没有接入色情/暴力/违法内容 AI 分类服务，不能保证自动识别全部违规内容。审核员检查线路关联、内容、版权与隐私后再批准。审核权限需用户明确指定网站账号。
