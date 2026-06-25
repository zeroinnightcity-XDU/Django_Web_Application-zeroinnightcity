from types import MethodType

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Fragment, MediaItem, Post, SiteProfile

admin.site.site_title = "网站管理后台"
admin.site.site_header = "网站管理后台"
admin.site.index_title = "请按内容类型分类上传和管理"

ADMIN_INDEX_MODEL_ORDER = {
    "MediaItem": 0,
    "Fragment": 1,
    "Post": 2,
    "SiteProfile": 3,
}


def _get_app_list_with_custom_model_order(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = sorted(app_dict.values(), key=lambda app: app["name"].lower())

    for app in app_list:
        if app["app_label"] == "content":
            app["models"].sort(
                key=lambda model: (
                    ADMIN_INDEX_MODEL_ORDER.get(
                        model["object_name"],
                        len(ADMIN_INDEX_MODEL_ORDER),
                    ),
                    model["name"],
                )
            )
        else:
            app["models"].sort(key=lambda model: model["name"])

    return app_list


admin.site.get_app_list = MethodType(_get_app_list_with_custom_model_order, admin.site)


class ImagePreviewAdminMixin:
    preview_width = 220
    empty_value_display = "暂无"

    class Media:
        css = {"all": ("content/admin.css",)}

    def _build_image_preview(self, image_field, width=None, height=160):
        if not image_field:
            return "未上传图片"
        return format_html(
            '<img src="{}" alt="图片预览" style="max-width:{}px; max-height:{}px; '
            'border-radius:6px; border:1px solid #d9d9d9; object-fit:cover;" />',
            image_field.url,
            width or self.preview_width,
            height,
        )


class FragmentAdminForm(forms.ModelForm):
    class Meta:
        model = Fragment
        fields = "__all__"
        help_texts = {
            "image": "上传后可直接在下方预览",
            "title": "选填，用于后台识别和后续详情页展示",
            "summary": "简单介绍这张照片，或写下按下快门时的感受",
            "people_info": "标记照片中的人物信息，支持在后台按人物筛选照片",
            "shot_at": "网站将以拍摄时间降序展示，后台可按拍摄时间筛选照片。",
            "location": "后台可按地点标签筛选照片",
        }


class SiteProfileAdminForm(forms.ModelForm):
    class Meta:
        model = SiteProfile
        fields = "__all__"
        help_texts = {
        }


@admin.register(MediaItem)
class MediaItemAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "creator",
        "release_year",
        "has_external_url",
        "created_at",
    )
    list_filter = ("category", "release_year", "created_at")
    search_fields = ("title", "creator", "summary", "body", "external_url")
    ordering = ("category", "-created_at", "-id")
    readonly_fields = ("cover_preview", "created_at")
    list_per_page = 20
    date_hierarchy = "created_at"
    empty_value_display = "暂无"
    fieldsets = (
        (
            "基础信息",
            {
                "description": "在此录入作品的名称、类别和艺术家等基础信息",
                "fields": ("title", "category", ("creator", "release_year")),
            },
        ),
        (
            "图片与简介",
            {
                "description": "上传一张该作品的封面/海报，以及关于它的简单介绍",
                "fields": ("cover", "cover_preview", "summary"),
            },
        ),
        (
            "更多内容",
            {
                "description": "可补充更多信息、资料或感想，并上传外部网站链接",
                "fields": ("body", "external_url"),
            },
        ),
        (
            "系统信息",
            {
                "description": "系统将自动记录该条目的创建时间，后台仅供查看。",
                "fields": ("created_at",),
            },
        ),
    )

    @admin.display(description="图片预览")
    def cover_preview(self, obj):
        return self._build_image_preview(getattr(obj, "cover", None))

    @admin.display(description="外部链接")
    def has_external_url(self, obj):
        return "有" if obj.external_url else "无"


@admin.register(Fragment)
class FragmentAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = FragmentAdminForm
    list_display = (
        "fragment_preview_small",
        "title",
        "people_info",
        "location",
        "shot_at",
        "created_at",
    )
    list_filter = ("people_info", "shot_at", "created_at", "location")
    search_fields = ("title", "summary", "people_info", "location")
    ordering = ("-shot_at", "-created_at", "-id")
    readonly_fields = ("image_preview", "created_at")
    list_per_page = 24
    date_hierarchy = "shot_at"
    empty_value_display = "暂无"
    fieldsets = (
        (
            "图片与预览",
            {
                "description": "先上传照片并核对预览，再补充说明信息。",
                "fields": ("image", "image_preview"),
            },
        ),
        (
            "内容说明",
            {
                "description": "名称和简介用于内容辨识，人物信息可作为后台筛选标签。",
                "fields": ("title", "summary", "people_info"),
            },
        ),
        (
            "拍摄信息",
            {
                "description": "补充拍摄时间与地点，方便后续检索和排序。",
                "fields": ("shot_at", "location"),
            },
        ),
        (
            "系统信息",
            {
                "description": "系统将自动记录该条目的上传时间，后台仅供查看。",
                "fields": ("created_at",),
            },
        ),
    )

    @admin.display(description="图片预览")
    def image_preview(self, obj):
        return self._build_image_preview(getattr(obj, "image", None))

    @admin.display(description="缩略图")
    def fragment_preview_small(self, obj):
        return self._build_image_preview(getattr(obj, "image", None), width=72, height=72)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("content/admin.css",)}

    list_display = ("title", "summary_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "summary", "body")
    ordering = ("-created_at", "-id")
    readonly_fields = ("created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"
    empty_value_display = "暂无"
    fieldsets = (
        (
            "标题与摘要",
            {
                "fields": ("title", "summary"),
            },
        ),
        (
            "正文内容",
            {
                "fields": ("body",),
            },
        ),
        (
            "系统信息",
            {
                "description": "系统将自动记录该条目的创建时间，后台仅供查看。",
                "fields": ("created_at",),
            },
        ),
    )

    @admin.display(description="摘要")
    def summary_preview(self, obj):
        if obj.summary:
            return obj.summary
        return obj.body[:60] + ("..." if len(obj.body) > 60 else "")


@admin.register(SiteProfile)
class SiteProfileAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = SiteProfileAdminForm
    list_display = (
        "about_name",
        "about_nickname",
        "about_region",
        "has_home_background",
        "updated_at",
    )
    search_fields = (
        "about_name",
        "about_nickname",
        "about_region",
        "about_bio",
        "elsewhere_email_label",
        "elsewhere_github_label",
        "elsewhere_bilibili_label",
        "elsewhere_netease_label",
    )
    ordering = ("-updated_at", "-id")
    readonly_fields = (
        "home_background_preview",
        "about_avatar_preview",
        "created_at",
        "updated_at",
    )
    list_per_page = 10
    empty_value_display = "暂无"
    fieldsets = (
        (
            "首页主视觉",
            {
                "fields": ("home_background", "home_background_preview"),
            },
        ),
        (
            "个人资料",
            {
                "description": "个人资料页面当前展示名字、昵称、地区、头像和简介。",
                "fields": (
                    ("about_name", "about_nickname"),
                    "about_region",
                    "about_avatar",
                    "about_avatar_preview",
                    "about_bio",
                ),
            },
        ),
        (
            "Elsewhere",
            {   "fields": (
                    "elsewhere_email_url",
                    ("elsewhere_github_label", "elsewhere_github_url"),
                    ("elsewhere_bilibili_label", "elsewhere_bilibili_url"),
                    ("elsewhere_netease_label", "elsewhere_netease_url"),
                ),
            },
        ),
        (
            "系统信息",
            {
                "description": "系统将自动记录创建与更新时间，后台仅供查看。",
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    @admin.display(description="背景图预览")
    def home_background_preview(self, obj):
        return self._build_image_preview(getattr(obj, "home_background", None))

    @admin.display(description="个人资料头像预览")
    def about_avatar_preview(self, obj):
        return self._build_image_preview(getattr(obj, "about_avatar", None), width=160, height=160)

    @admin.display(description="背景图")
    def has_home_background(self, obj):
        return "有" if obj.home_background else "无"
