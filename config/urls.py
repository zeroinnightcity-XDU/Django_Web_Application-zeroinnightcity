"""项目级 URL 配置。

Step1 仅保留后台入口，并在开发环境下补充媒体文件访问能力。
静态资源由 `django.contrib.staticfiles` 在开发环境中自动处理，
因此此处无需额外拼接静态资源路由。
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.content.urls')),
]

if settings.DEBUG:
    # 仅在开发环境下暴露媒体文件，便于本地预览上传内容。
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
