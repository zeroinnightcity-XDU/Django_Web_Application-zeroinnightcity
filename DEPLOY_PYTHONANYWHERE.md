# PythonAnywhere 部署步骤

这份文档按“期末作业可稳定展示”的目标整理，默认你使用 PythonAnywhere 付费版。

## 1. 本地准备

在项目根目录执行：

```bash
python -m pip install -r requirements.txt
python manage.py check
python manage.py collectstatic
```

说明：

- `db.sqlite3` 和 `media/` 建议保留并提交到 GitHub，这样部署后能直接看到你当前的演示数据和图片。
- `staticfiles/` 是部署时重新收集出来的目录，不需要提交。

## 2. 推送到 GitHub

如果项目还不是 Git 仓库，在项目根目录执行：

```bash
git init
git add .
git commit -m "Prepare project for PythonAnywhere deployment"
```

然后在 GitHub 新建仓库，复制仓库地址后执行：

```bash
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

## 3. 在 PythonAnywhere 创建环境

登录 PythonAnywhere 后：

1. 打开 `Consoles`，创建一个 `Bash` 控制台。
2. 克隆你的仓库：

```bash
git clone <你的仓库地址>
cd <你的仓库目录名>
```

3. 创建虚拟环境：

```bash
mkvirtualenv --python=/usr/bin/python3.13 mysite-venv
pip install -r requirements.txt
```

如果 `mkvirtualenv` 不可用，也可以：

```bash
python3.13 -m venv ~/.virtualenvs/mysite-venv
source ~/.virtualenvs/mysite-venv/bin/activate
pip install -r requirements.txt
```

## 4. 配置 Django 环境变量

在 Bash 控制台里先生成一个密钥：

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

记下输出结果，然后设置环境变量：

```bash
export DJANGO_SECRET_KEY='<替换成上一步生成的密钥>'
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS='<你的用户名>.pythonanywhere.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://<你的用户名>.pythonanywhere.com'
```

说明：

- 这一步只是临时设置，后面还要把同样内容写进 WSGI 文件，确保网站重启后仍然生效。

## 5. 初始化数据库和静态资源

仍在项目目录下执行：

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

如果你把本地的 `db.sqlite3` 一并提交上去了，`migrate` 一般不会破坏已有内容。

## 6. 创建 Web App

在 PythonAnywhere 后台：

1. 打开 `Web`
2. 点击 `Add a new web app`
3. 选择域名：先用 `your-username.pythonanywhere.com`
4. 选择 `Manual configuration`
5. Python 版本选择与你虚拟环境一致的版本，例如 `Python 3.13`

## 7. 配置虚拟环境和代码路径

在 `Web` 页面里填写：

- `Source code`: `/home/<你的用户名>/<你的仓库目录名>`
- `Working directory`: `/home/<你的用户名>/<你的仓库目录名>`
- `Virtualenv`: `/home/<你的用户名>/.virtualenvs/mysite-venv`

## 8. 修改 WSGI 文件

打开 PythonAnywhere 自动生成的 WSGI 文件，把核心内容改成下面这种结构：

```python
import os
import sys

path = '/home/<你的用户名>/<你的仓库目录名>'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DJANGO_SECRET_KEY'] = '<你的密钥>'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = '<你的用户名>.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://<你的用户名>.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 9. 配置静态文件和媒体文件

在 `Web` 页面中的 `Static files` 区域新增两条映射：

- URL: `/static/`
  Directory: `/home/<你的用户名>/<你的仓库目录名>/staticfiles`
- URL: `/media/`
  Directory: `/home/<你的用户名>/<你的仓库目录名>/media`

## 10. 重载并检查

点击 `Reload`，然后访问：

- `https://<你的用户名>.pythonanywhere.com/`
- `https://<你的用户名>.pythonanywhere.com/admin/`

如果报错，优先看：

- `Web` 页面的 `Error log`
- `Server log`

## 11. 后续更新代码

以后每次更新都可以在 PythonAnywhere Bash 控制台执行：

```bash
cd <你的仓库目录名>
source ~/.virtualenvs/mysite-venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

然后回到 `Web` 页面点击 `Reload`。
