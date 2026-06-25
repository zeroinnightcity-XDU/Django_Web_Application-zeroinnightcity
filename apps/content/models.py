from django.db import models


class MediaItem(models.Model):
    class Category(models.TextChoices):
        MUSIC = "music", "Music"
        FILM = "film", "Film"

    title = models.CharField("标题", max_length=200)
    creator = models.CharField("艺术家", max_length=200)
    category = models.CharField("类别", max_length=20, choices=Category.choices)
    cover = models.ImageField("图片", upload_to="content/media_items/covers/")
    release_year = models.PositiveSmallIntegerField("发行年份", null=True, blank=True)
    summary = models.TextField("简介")
    body = models.TextField("更多信息", blank=True)
    external_url = models.URLField("外部链接", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "音乐/电影"
        verbose_name_plural = "音乐/电影"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"


class Fragment(models.Model):
    image = models.ImageField("图片", upload_to="content/fragments/")
    title = models.CharField("名称", max_length=200, blank=True, default="")
    summary = models.TextField("简介", blank=True, default="")
    people_info = models.CharField("人物信息", max_length=100, blank=True, default="")
    shot_at = models.DateTimeField("拍摄时间", null=True, blank=True)
    location = models.CharField("地点标签", max_length=255, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "照片墙"
        verbose_name_plural = "照片墙"
        ordering = ["-shot_at", "-created_at", "-id"]

    def __str__(self):
        if self.title:
            return self.title
        location = self.location or "未标注地点"
        return f"{location} @ {self.shot_at:%Y-%m-%d}" if self.shot_at else location


class Post(models.Model):
    title = models.CharField("标题", max_length=200)
    summary = models.CharField("摘要", max_length=255, blank=True)
    body = models.TextField("正文")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = "博客"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title


class SiteProfile(models.Model):
    home_background = models.ImageField(
        "首页背景图",
        upload_to="content/site_profile/home/",
        blank=True,
    )
    about_name = models.CharField("名字", max_length=100, blank=True, default="")
    about_nickname = models.CharField(
        "昵称",
        max_length=100,
        blank=True,
        default="",
    )
    about_region = models.CharField("地区", max_length=100, blank=True, default="")
    about_bio = models.TextField(
        "简介",
        blank=True,
        default="",
    )
    about_avatar = models.ImageField(
        "头像",
        upload_to="content/site_profile/about/",
        blank=True,
    )
    elsewhere_email_label = models.CharField(
        "Email 名称",
        max_length=100,
        blank=True,
        default="Email",
    )
    elsewhere_email_url = models.CharField(
        "Email 地址",
        max_length=255,
        blank=True,
        default="",
    )
    elsewhere_github_label = models.CharField(
        "GitHub 名称",
        max_length=100,
        blank=True,
        default="GitHub",
    )
    elsewhere_github_url = models.URLField(
        "GitHub 链接",
        blank=True,
        default="",
    )
    elsewhere_bilibili_label = models.CharField(
        "哔哩哔哩 名称",
        max_length=100,
        blank=True,
        default="Bilibili",
    )
    elsewhere_bilibili_url = models.URLField(
        "哔哩哔哩 链接",
        blank=True,
        default="",
    )
    elsewhere_netease_label = models.CharField(
        "网易云音乐 名称",
        max_length=100,
        blank=True,
        default="Netease Music",
    )
    elsewhere_netease_url = models.URLField(
        "网易云音乐 链接",
        blank=True,
        default="",
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "首页与个人资料"
        verbose_name_plural = "首页与个人资料"
        ordering = ["-updated_at", "-id"]

    def __str__(self):
        return self.about_name or self.about_nickname or f"首页与个人资料 #{self.pk}"
