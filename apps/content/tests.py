import datetime
import re

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

from .models import Fragment, MediaItem, Post, SiteProfile


class SiteProfileViewTests(TestCase):
    NAV_ITEMS = ("Music", "Film", "Fragments", "Thoughts", "About")
    HOME_SITE_TITLE = "zeroinnightcity"
    HOME_OWNER_NAME = "Wentong Zou"
    HOME_TAGLINE = "收纳日常偏爱的内容、短句与缓慢整理出来的个人注脚。"

    def _extract_markup(self, content, pattern):
        match = re.search(pattern, content, re.S)
        self.assertIsNotNone(match)
        return match.group(0)

    def _assert_minimal_navigation(self, markup):
        self.assertEqual(markup.count("data-nav-link"), len(self.NAV_ITEMS) + 1)
        self.assertIn(">Home<", markup)
        for label in self.NAV_ITEMS:
            self.assertIn(f">{label}<", markup)
        self.assertIn(self.HOME_OWNER_NAME, markup)
        self.assertIn(str(timezone.now().year), markup)
        self.assertNotIn(">Films<", markup)
        self.assertNotIn(self.HOME_SITE_TITLE, markup)
        self.assertNotIn(self.HOME_TAGLINE, markup)
        self.assertNotIn("Explore", markup)
        self.assertNotIn("Welcome", markup)
        self.assertNotIn("Quote", markup)

    def _assert_home_navigation_with_brand(self, markup):
        self.assertEqual(markup.count("data-nav-link"), 5)
        for label in self.NAV_ITEMS:
            self.assertIn(f">{label}<", markup)
        self.assertIn('data-home-brand="true"', markup)
        self.assertRegex(
            markup,
            r'font-display[^>]*>\s*%s\s*</p>\s*<p class="font-english[^"]*">\s*%s\s*</p>'
            % (re.escape(self.HOME_SITE_TITLE), re.escape(self.HOME_OWNER_NAME)),
        )
        self.assertIn(self.HOME_SITE_TITLE, markup)
        self.assertIn(self.HOME_OWNER_NAME, markup)
        self.assertIn(self.HOME_TAGLINE, markup)
        self.assertIn(str(timezone.now().year), markup)
        self.assertNotIn(">Films<", markup)
        self.assertNotIn("Explore", markup)
        self.assertNotIn("Welcome", markup)
        self.assertNotIn("Quote", markup)

    def test_home_uses_fallback_context_without_site_profile(self):
        response = self.client.get(reverse("content:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/home.html")
        self.assertIsNone(response.context["home_background"])
        self.assertEqual(response.context["home_site_title"], self.HOME_SITE_TITLE)
        self.assertEqual(response.context["home_owner_name"], self.HOME_OWNER_NAME)
        self.assertEqual(response.context["home_tagline"], self.HOME_TAGLINE)
        self.assertContains(response, 'aria-label="首页主视觉图像"', html=False)
        self.assertContains(response, 'data-home-nav="true"', html=False)
        self.assertContains(response, 'data-home-brand="true"', html=False)
        self.assertContains(response, 'data-home-hero="fullscreen"', html=False)
        self.assertNotContains(response, 'aria-label="展开主导航"', html=False)
        self.assertNotContains(response, "border border-white/20 bg-[#e2eadc]/14", html=False)
        self.assertContains(response, "首页主视觉图像采用全屏铺满模式")
        self.assertContains(response, ">Film<", html=False)
        self.assertContains(response, self.HOME_SITE_TITLE)
        self.assertContains(response, self.HOME_OWNER_NAME)
        self.assertContains(response, self.HOME_TAGLINE)
        self.assertNotContains(response, ">Films<", html=False)
        self.assertNotContains(response, ">Welcome<", html=False)
        self.assertNotContains(response, ">Quote<", html=False)
        self.assertNotContains(response, ">Explore<", html=False)
        self.assertNotContains(response, "home-cargo-grid")

    def test_home_navigation_restores_brand_info_while_keeping_menu_and_stamp(self):
        response = self.client.get(reverse("content:home"))
        markup = self._extract_markup(
            response.content.decode("utf-8"),
            r'<div\s+data-home-nav="true"[\s\S]*?</div>\s*</header>',
        )

        self._assert_home_navigation_with_brand(markup)

    def test_home_reads_latest_site_profile(self):
        SiteProfile.objects.create()
        latest_profile = SiteProfile.objects.create(
            home_background=SimpleUploadedFile(
                "hero.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            )
        )

        response = self.client.get(reverse("content:home"))

        self.assertEqual(
            response.context["home_background"].name,
            latest_profile.home_background.name,
        )

    def test_about_uses_fallback_context_without_site_profile(self):
        response = self.client.get(reverse("content:about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/about.html")
        self.assertEqual(response.context["about_name"], "Quiet Archive")
        self.assertEqual(response.context["about_nickname"], "Quiet Archive")
        self.assertEqual(response.context["about_region"], "")
        self.assertContains(response, "Quiet Archive")
        self.assertContains(response, "这里用来收纳日常偏爱的内容")
        self.assertContains(response, 'data-nav-toggle', html=False)
        self.assertContains(response, 'data-expandable-nav="true"', html=False)
        self.assertContains(response, 'aria-hidden="true"', html=False)
        self.assertContains(response, "pointer-events-none invisible", html=False)
        self.assertContains(response, "-translate-x-[calc(100%+1.5rem)]", html=False)
        self.assertContains(response, ">Film<", html=False)
        self.assertNotContains(response, ">Films<", html=False)
        self.assertNotContains(response, 'data-home-nav="true"', html=False)
        self.assertEqual(response.context["elsewhere_links"], [])
        self.assertNotContains(response, ">Elsewhere<", html=False)
        self.assertNotContains(response, "Portrait Pending")
        self.assertNotContains(response, "简介状态")
        self.assertNotContains(response, "页面优先读取后台维护的站点资料")
        self.assertNotContains(response, "hello@example.com")
        self.assertNotContains(response, "@yourname")

    def test_about_expandable_navigation_keeps_home_plus_five_menu_items_and_name_year_stamp(self):
        response = self.client.get(reverse("content:about"))
        markup = self._extract_markup(
            response.content.decode("utf-8"),
            r'<aside[\s\S]*?id="site-nav-panel"[\s\S]*?</aside>',
        )

        self._assert_minimal_navigation(markup)

    def test_base_template_uses_muted_blue_theme_tokens(self):
        response = self.client.get(reverse("content:about"))

        self.assertContains(response, 'mist: "#eef3f8"', html=False)
        self.assertContains(response, 'panel: "#f5f8fc"', html=False)
        self.assertContains(response, 'sage: "#d7e1eb"', html=False)
        self.assertContains(response, 'moss: "#70879c"', html=False)
        self.assertContains(response, 'ink: "#243242"', html=False)
        self.assertContains(response, 'line: "#becbd8"', html=False)
        self.assertContains(response, "background-color: #eef3f8;", html=False)
        self.assertContains(response, "rgba(232, 239, 247, 0.9)", html=False)

    def test_about_reads_latest_site_profile(self):
        SiteProfile.objects.create(about_name="旧名字", about_nickname="旧昵称", about_bio="旧简介")
        latest_profile = SiteProfile.objects.create(
            about_name="站点主人",
            about_nickname="Archive Owner",
            about_region="杭州",
            about_bio="这是后台维护的 About 简介。",
            about_avatar=SimpleUploadedFile(
                "avatar.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            elsewhere_email_label="邮箱",
            elsewhere_email_url="hello@example.com",
        )

        response = self.client.get(reverse("content:about"))

        self.assertEqual(response.context["about_name"], "站点主人")
        self.assertEqual(response.context["about_nickname"], "Archive Owner")
        self.assertEqual(response.context["about_region"], "杭州")
        self.assertEqual(response.context["about_bio"], "这是后台维护的 About 简介。")
        self.assertEqual(response.context["about_avatar"].name, latest_profile.about_avatar.name)
        self.assertEqual(len(response.context["elsewhere_links"]), 1)
        self.assertContains(response, "站点主人")
        self.assertContains(response, "Archive Owner")
        self.assertContains(response, "杭州")
        self.assertContains(response, "这是后台维护的 About 简介。")
        self.assertContains(response, 'alt="站点主人 的个人资料头像"', html=False)
        self.assertContains(response, f'src="{latest_profile.about_avatar.url}"', html=False)
        self.assertContains(response, "Portrait")
        self.assertContains(response, "hello@example.com")
        self.assertNotContains(response, 'href="hello@example.com"', html=False)
        self.assertNotContains(response, 'href="mailto:hello@example.com"', html=False)
        self.assertContains(response, "Email")
        self.assertNotContains(response, "邮箱")
        self.assertNotContains(response, "GitHub")
        self.assertEqual(response.context["elsewhere_links"][0]["label"], "Email")
        self.assertEqual(
            response.context["elsewhere_links"][0]["value"],
            "hello@example.com",
        )
        self.assertTrue(response.context["elsewhere_links"][0]["is_plain_text"])

    def test_about_keeps_avatar_and_restores_elsewhere_links_section(self):
        latest_profile = SiteProfile.objects.create(
            about_name="站点主人",
            about_nickname="Archive Owner",
            about_bio="这是后台维护的 About 简介。",
            about_avatar=SimpleUploadedFile(
                "avatar.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            elsewhere_email_label="邮箱",
            elsewhere_email_url="hello@example.com",
            elsewhere_github_label="GitHub",
            elsewhere_github_url="https://github.com/example",
        )

        response = self.client.get(reverse("content:about"))
        content = response.content.decode("utf-8")

        self.assertContains(response, "Portrait")
        self.assertContains(response, f'src="{latest_profile.about_avatar.url}"', html=False)
        self.assertContains(response, ">Elsewhere<", html=False)
        self.assertContains(response, "hello@example.com")
        self.assertNotContains(response, 'href="hello@example.com"', html=False)
        self.assertNotContains(response, 'href="mailto:hello@example.com"', html=False)
        self.assertContains(response, 'href="https://github.com/example"', html=False)
        self.assertContains(response, "Email")
        self.assertNotContains(response, "邮箱")
        self.assertContains(response, "GitHub")
        self.assertEqual(content.count(">Visit<"), 1)


class AdminExperienceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-pass-123",
        )
        self.client.force_login(self.user)

    def _admin_request(self):
        request = self.factory.get("/admin/")
        request.user = self.user
        return request

    def _flatten_fieldsets(self, fieldsets):
        flattened_fields = []
        for _, options in fieldsets:
            for field in options["fields"]:
                if isinstance(field, tuple):
                    flattened_fields.extend(field)
                else:
                    flattened_fields.append(field)
        return flattened_fields

    def test_fragment_admin_add_page_loads_with_reworked_sections(self):
        response = self.client.get(reverse("admin:content_fragment_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "图片与预览")
        self.assertContains(response, "内容说明")
        self.assertContains(response, "拍摄信息")
        self.assertContains(response, "人物信息")
        self.assertContains(response, "未上传图片")

    def test_fragment_admin_configuration_highlights_people_info(self):
        model_admin = admin.site._registry[Fragment]
        request = self._admin_request()
        fieldsets = model_admin.get_fieldsets(request)
        form = model_admin.get_form(request)()

        self.assertEqual(
            [section_name for section_name, _ in fieldsets],
            ["图片与预览", "内容说明", "拍摄信息", "系统信息"],
        )
        self.assertIn("people_info", model_admin.list_filter)
        self.assertIn("people_info", self._flatten_fieldsets(fieldsets))
        self.assertIn("后台列表页按人物筛选", form.fields["people_info"].help_text)

    def test_mediaitem_admin_configuration_exposes_release_year(self):
        model_admin = admin.site._registry[MediaItem]
        request = self._admin_request()
        fieldsets = model_admin.get_fieldsets(request)
        form = model_admin.get_form(request)()

        self.assertIn("release_year", model_admin.list_display)
        self.assertIn("release_year", model_admin.list_filter)
        self.assertIn("release_year", self._flatten_fieldsets(fieldsets))
        self.assertIn(
            ("creator", "release_year"),
            dict(fieldsets)["基础信息"]["fields"],
        )
        self.assertEqual(
            form.fields["category"].choices,
            [
                ("", "---------"),
                (MediaItem.Category.MUSIC, "Music"),
                (MediaItem.Category.FILM, "Film"),
            ],
        )

    def test_mediaitem_admin_add_page_uses_singular_film_and_fieldbox_layout_for_release_year(self):
        response = self.client.get(reverse("admin:content_mediaitem_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="film"', html=False)
        self.assertContains(response, ">Film</option>", html=False)
        self.assertNotContains(response, 'value="films"', html=False)
        self.assertContains(response, "fieldBox field-release_year", html=False)

    def test_admin_index_lists_models_in_content_order(self):
        app_list = admin.site.get_app_list(self._admin_request())
        content_app = next(app for app in app_list if app["app_label"] == "content")

        self.assertEqual(
            [model["name"] for model in content_app["models"]],
            ["音乐/电影", "照片墙", "博客", "首页与个人资料"],
        )

    def test_siteprofile_admin_add_page_only_shows_current_profile_fields(self):
        response = self.client.get(reverse("admin:content_siteprofile_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "首页主视觉")
        self.assertContains(response, "个人资料")
        self.assertContains(response, "Elsewhere")
        self.assertNotContains(response, "欢迎语")
        self.assertNotContains(response, "Quote")
        self.assertContains(response, "个人资料头像")
        self.assertContains(response, "个人资料头像预览")

    def test_siteprofile_admin_configuration_uses_label_and_url_pairs(self):
        model_admin = admin.site._registry[SiteProfile]
        request = self._admin_request()
        fieldsets = model_admin.get_fieldsets(request)
        form = model_admin.get_form(request)()
        flattened_fields = self._flatten_fieldsets(fieldsets)
        elsewhere_fields = dict(fieldsets)["Elsewhere"]["fields"]

        self.assertEqual(
            [section_name for section_name, _ in fieldsets],
            ["首页主视觉", "个人资料", "Elsewhere", "系统信息"],
        )
        self.assertIn("about_avatar", flattened_fields)
        self.assertIn("about_avatar_preview", flattened_fields)
        self.assertNotIn("elsewhere_email_label", flattened_fields)
        self.assertNotIn("elsewhere_email_label", form.fields)
        self.assertEqual(
            elsewhere_fields,
            (
                "elsewhere_email_url",
                ("elsewhere_github_label", "elsewhere_github_url"),
                ("elsewhere_bilibili_label", "elsewhere_bilibili_url"),
                ("elsewhere_netease_label", "elsewhere_netease_url"),
            ),
        )
        self.assertIn("旧首页文案字段", form.fields["about_bio"].help_text)
        self.assertIn("简洁头像卡片形式展示", form.fields["about_avatar"].help_text)
        self.assertIn("hello@example.com", form.fields["elsewhere_email_url"].help_text)
        self.assertIn("前台仅展示，不会跳转", form.fields["elsewhere_email_url"].help_text)


class ContentDetailViewTests(TestCase):
    def test_film_list_uses_singular_name_and_detail_only_entry_points(self):
        film = MediaItem.objects.create(
            title="Perfect Blue",
            creator="Satoshi Kon",
            category=MediaItem.Category.FILM,
            cover=SimpleUploadedFile(
                "perfect-blue.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=1997,
            summary="偶像与身份在镜像之间不断错位。",
            body="补充一些观影笔记。",
            external_url="https://example.com/perfect-blue",
        )

        response = self.client.get(reverse("content:film-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_title"], "Film")
        self.assertEqual(response.context["section_slug"], "film")
        self.assertContains(response, ">Film<", html=False)
        self.assertNotContains(response, ">Films<", html=False)
        self.assertContains(response, reverse("content:film-detail", args=[film.pk]))
        self.assertContains(
            response,
            'src="%s"' % film.cover.url,
            html=False,
        )
        self.assertNotContains(
            response,
            'href="https://example.com/perfect-blue"',
            html=False,
        )
        self.assertNotContains(
            response,
            'href="%s"' % film.cover.url,
            html=False,
        )
        self.assertContains(response, "1997")
        self.assertNotContains(
            response,
            'class="font-english text-[0.78rem] font-light uppercase tracking-[0.38em] text-moss/76"',
            html=False,
        )
        self.assertNotContains(response, "偶像与身份在镜像之间不断错位。")
        self.assertContains(response, "View Detail")
        self.assertEqual(response.content.decode("utf-8").count("View Detail"), 1)
        self.assertNotContains(response, "View Original")

    def test_music_list_keeps_detail_only_entry_points(self):
        track = MediaItem.objects.create(
            title="花样年华",
            creator="梅林茂",
            category=MediaItem.Category.MUSIC,
            cover=SimpleUploadedFile(
                "in-the-mood-for-love.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=2000,
            summary="适合反复回听的电影配乐。",
            external_url="https://example.com/in-the-mood-for-love",
        )

        response = self.client.get(reverse("content:music-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("content:music-detail", args=[track.pk]))
        self.assertContains(
            response,
            'src="%s"' % track.cover.url,
            html=False,
        )
        self.assertNotContains(
            response,
            'href="https://example.com/in-the-mood-for-love"',
            html=False,
        )
        self.assertNotContains(
            response,
            'href="%s"' % track.cover.url,
            html=False,
        )
        self.assertContains(response, "2000")
        self.assertNotContains(
            response,
            'class="font-english text-[0.78rem] font-light uppercase tracking-[0.38em] text-moss/76"',
            html=False,
        )
        self.assertNotContains(response, "适合反复回听的电影配乐。")
        self.assertContains(response, "View Detail")
        self.assertEqual(response.content.decode("utf-8").count("View Detail"), 1)
        self.assertNotContains(response, "View Original")

    def test_film_list_shows_newer_added_items_first_instead_of_release_year(self):
        first_film = MediaItem.objects.create(
            title="First Added Film",
            creator="Director A",
            category=MediaItem.Category.FILM,
            cover=SimpleUploadedFile(
                "first-film.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=2024,
            summary="先添加的电影。",
        )
        second_film = MediaItem.objects.create(
            title="Second Added Film",
            creator="Director B",
            category=MediaItem.Category.FILM,
            cover=SimpleUploadedFile(
                "second-film.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=1990,
            summary="后添加的电影。",
        )

        response = self.client.get(reverse("content:film-list"))
        items = list(response.context["items"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item.pk for item in items], [second_film.pk, first_film.pk])
        content = response.content.decode("utf-8")
        self.assertLess(content.index("Second Added Film"), content.index("First Added Film"))

    def test_music_list_shows_newer_added_items_first_instead_of_release_year(self):
        first_track = MediaItem.objects.create(
            title="First Added Track",
            creator="Artist A",
            category=MediaItem.Category.MUSIC,
            cover=SimpleUploadedFile(
                "first-track.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=2023,
            summary="先添加的音乐。",
        )
        second_track = MediaItem.objects.create(
            title="Second Added Track",
            creator="Artist B",
            category=MediaItem.Category.MUSIC,
            cover=SimpleUploadedFile(
                "second-track.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=1988,
            summary="后添加的音乐。",
        )

        response = self.client.get(reverse("content:music-list"))
        items = list(response.context["items"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item.pk for item in items], [second_track.pk, first_track.pk])
        content = response.content.decode("utf-8")
        self.assertLess(content.index("Second Added Track"), content.index("First Added Track"))

    def test_media_detail_includes_original_image_entry(self):
        film = MediaItem.objects.create(
            title="Fallen Angels",
            creator="Wong Kar-wai",
            category=MediaItem.Category.FILM,
            cover=SimpleUploadedFile(
                "fallen-angels.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            release_year=1995,
            summary="夜色、速度和疏离感交织在一起。",
            external_url="https://example.com/fallen-angels",
        )

        response = self.client.get(reverse("content:film-detail", args=[film.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Original")
        self.assertEqual(response.content.decode("utf-8").count("View Original"), 1)
        self.assertContains(response, "1995")
        self.assertContains(response, "夜色、速度和疏离感交织在一起。")
        self.assertContains(
            response,
            'href="%s"' % film.cover.url,
            html=False,
        )
        self.assertContains(
            response,
            'href="https://example.com/fallen-angels"',
            html=False,
        )

    def test_fragments_list_links_to_detail_page(self):
        fragment = Fragment.objects.create(
            image=SimpleUploadedFile(
                "fragment.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="奈良美智",
            summary="展厅里的一瞬。",
            people_info="奈良美智",
            location="上海",
        )

        response = self.client.get(reverse("content:fragments-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("content:fragments-detail", args=[fragment.pk]),
            count=2,
        )
        self.assertNotContains(response, 'aria-label="查看原图"', html=False)
        self.assertNotContains(response, "View Detail")
        self.assertNotContains(response, "View Original")
        self.assertContains(response, 'aria-label="查看详情"', html=False)
        self.assertNotContains(response, "展厅里的一瞬。")

    def test_fragments_list_uses_fragment_model_default_ordering(self):
        older_shot = Fragment.objects.create(
            image=SimpleUploadedFile(
                "older-shot.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="较早拍摄",
            shot_at=timezone.make_aware(datetime.datetime(2026, 1, 1, 8, 0, 0)),
        )
        same_shot_older_created = Fragment.objects.create(
            image=SimpleUploadedFile(
                "same-shot-older-created.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="同拍摄时间-较早创建",
            shot_at=timezone.make_aware(datetime.datetime(2026, 1, 2, 8, 0, 0)),
        )
        same_shot_newer_created = Fragment.objects.create(
            image=SimpleUploadedFile(
                "same-shot-newer-created.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="同拍摄时间-较晚创建",
            shot_at=timezone.make_aware(datetime.datetime(2026, 1, 2, 8, 0, 0)),
        )
        same_timestamp_first = Fragment.objects.create(
            image=SimpleUploadedFile(
                "same-timestamp-first.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="同时间戳-先创建",
            shot_at=timezone.make_aware(datetime.datetime(2026, 1, 3, 8, 0, 0)),
        )
        same_timestamp_second = Fragment.objects.create(
            image=SimpleUploadedFile(
                "same-timestamp-second.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="同时间戳-后创建",
            shot_at=timezone.make_aware(datetime.datetime(2026, 1, 3, 8, 0, 0)),
        )
        null_shot = Fragment.objects.create(
            image=SimpleUploadedFile(
                "null-shot.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="未填写拍摄时间",
        )

        Fragment.objects.filter(pk=older_shot.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 1, 5, 8, 0, 0))
        )
        Fragment.objects.filter(pk=same_shot_older_created.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 1, 3, 8, 0, 0))
        )
        Fragment.objects.filter(pk=same_shot_newer_created.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 1, 4, 8, 0, 0))
        )
        shared_created_at = timezone.make_aware(datetime.datetime(2026, 1, 2, 8, 0, 0))
        Fragment.objects.filter(pk=same_timestamp_first.pk).update(created_at=shared_created_at)
        Fragment.objects.filter(pk=same_timestamp_second.pk).update(created_at=shared_created_at)
        Fragment.objects.filter(pk=null_shot.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 1, 6, 8, 0, 0))
        )

        response = self.client.get(reverse("content:fragments-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item.pk for item in response.context["items"]],
            [
                same_timestamp_second.pk,
                same_timestamp_first.pk,
                same_shot_newer_created.pk,
                same_shot_older_created.pk,
                older_shot.pk,
                null_shot.pk,
            ],
        )

        content = response.content.decode("utf-8")
        ordered_links = [
            reverse("content:fragments-detail", args=[same_timestamp_second.pk]),
            reverse("content:fragments-detail", args=[same_timestamp_first.pk]),
            reverse("content:fragments-detail", args=[same_shot_newer_created.pk]),
            reverse("content:fragments-detail", args=[same_shot_older_created.pk]),
            reverse("content:fragments-detail", args=[older_shot.pk]),
            reverse("content:fragments-detail", args=[null_shot.pk]),
        ]
        self.assertEqual(
            sorted(content.index(link) for link in ordered_links),
            [content.index(link) for link in ordered_links],
        )

    def test_fragments_detail_renders_complete_metadata(self):
        fragment = Fragment.objects.create(
            image=SimpleUploadedFile(
                "detail.jpg",
                b"fake-image-content",
                content_type="image/jpeg",
            ),
            title="蓦然回首",
            summary="安静的展厅角落。",
            people_info="藤本树",
            location="杭州",
        )

        response = self.client.get(reverse("content:fragments-detail", args=[fragment.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/fragment_detail.html")
        self.assertContains(response, "蓦然回首")
        self.assertContains(response, "安静的展厅角落。")
        self.assertContains(response, "藤本树")
        self.assertContains(response, "杭州")
        self.assertContains(response, "View Original")
        self.assertEqual(response.content.decode("utf-8").count("View Original"), 1)
        self.assertEqual(response.content.decode("utf-8").count("藤本树"), 1)
        self.assertContains(
            response,
            'href="%s"' % fragment.image.url,
            html=False,
        )

    def test_thoughts_list_shows_newer_added_posts_first_instead_of_created_at_desc(self):
        first_post = Post.objects.create(
            title="第一篇",
            summary="先添加的文章",
            body="记录第一篇文章。",
        )
        second_post = Post.objects.create(
            title="第二篇",
            summary="后添加的文章",
            body="记录第二篇文章。",
        )
        Post.objects.filter(pk=first_post.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 6, 20, 8, 0, 0))
        )
        Post.objects.filter(pk=second_post.pk).update(
            created_at=timezone.make_aware(datetime.datetime(2026, 6, 19, 8, 0, 0))
        )

        response = self.client.get(reverse("content:thoughts-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item.pk for item in response.context["items"]],
            [second_post.pk, first_post.pk],
        )
        content = response.content.decode("utf-8")
        self.assertLess(content.index("第二篇"), content.index("第一篇"))

    def test_thoughts_list_shows_metadata_and_links(self):
        post = Post.objects.create(
            title="六月散步记录",
            summary="写给黄昏和晚风的短记。",
            body="今天的风很轻。\n我在河边走了很久。",
        )

        response = self.client.get(reverse("content:thoughts-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("content:thoughts-detail", args=[post.pk]))
        self.assertContains(response, "写给黄昏和晚风的短记。")
        self.assertContains(response, "星期")
        self.assertContains(response, "字")
        self.assertContains(response, "View Detail")

    def test_thoughts_detail_renders_weekday_and_word_count(self):
        post = Post.objects.create(
            title="博客详情页",
            summary="补齐文章详情链路。",
            body="雨停以后，街道重新亮了起来。",
        )
        fixed_created_at = timezone.make_aware(datetime.datetime(2026, 6, 19, 8, 0, 0))
        Post.objects.filter(pk=post.pk).update(created_at=fixed_created_at)

        response = self.client.get(reverse("content:thoughts-detail", args=[post.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/thought_detail.html")
        self.assertEqual(response.context["item"].weekday_label, "星期五")
        self.assertEqual(response.context["item"].word_count, 14)
        self.assertContains(response, "博客详情页")
        self.assertContains(response, "补齐文章详情链路。")
        self.assertContains(response, "星期五")
        self.assertContains(response, "14 字")
