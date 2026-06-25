import re

from django.shortcuts import get_object_or_404, render

from .models import Fragment, MediaItem, Post, SiteProfile

WEEKDAY_LABELS = [
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六",
    "星期日",
]

DEFAULT_HOME_CONTEXT = {
    "home_background": None,
    "home_site_title": "zeroinnightcity",
    "home_owner_name": "Wentong Zou",
    "home_tagline": "a place to showcase parts of my ordinary life",
}

DEFAULT_ABOUT_CONTEXT = {
    "about_name": "NOBODY",
    "about_nickname": "nobody",
    "about_region": "中国 北京",
    "about_bio": (
        "Hello World"
    ),
    "about_avatar": None,
    "elsewhere_links": [],
}


def _get_site_profile():
    return SiteProfile.objects.order_by("-updated_at", "-id").first()


def _home_context():
    profile = _get_site_profile()
    context = {
        "page_title": "Home",
        "section_slug": "home",
        **DEFAULT_HOME_CONTEXT,
    }
    if profile:
        context.update(
            {
                "home_background": profile.home_background or context["home_background"],
            }
        )
    return context


def _about_context():
    profile = _get_site_profile()
    context = {
        "page_title": "About",
        "section_slug": "about",
        **DEFAULT_ABOUT_CONTEXT,
    }
    if profile:
        elsewhere_links = [
            {
                "label": "Email",
                "value": profile.elsewhere_email_url,
                "is_plain_text": True,
            },
            {
                "label": profile.elsewhere_github_label or "GitHub",
                "url": profile.elsewhere_github_url,
                "is_plain_text": False,
            },
            {
                "label": profile.elsewhere_bilibili_label or "Bilibili",
                "url": profile.elsewhere_bilibili_url,
                "is_plain_text": False,
            },
            {
                "label": profile.elsewhere_netease_label or "Netease Music",
                "url": profile.elsewhere_netease_url,
                "is_plain_text": False,
            },
        ]
        visible_elsewhere_links = [
            link
            for link in elsewhere_links
            if link.get("value") or link.get("url")
        ]
        context.update(
            {
                "about_name": profile.about_name or context["about_name"],
                "about_nickname": profile.about_nickname or context["about_nickname"],
                "about_region": profile.about_region or context["about_region"],
                "about_bio": profile.about_bio or context["about_bio"],
                "about_avatar": profile.about_avatar or context["about_avatar"],
                "elsewhere_links": visible_elsewhere_links,
            }
        )
    return context


def home_view(request):
    return render(request, "content/home.html", _home_context())


def _media_list_context(category, page_title, section_slug):
    items = MediaItem.objects.filter(category=category).order_by("-id")
    return {
        "items": items,
        "page_title": page_title,
        "section_slug": section_slug,
    }


def _media_detail_context(item, page_title, section_slug):
    return {
        "item": item,
        "page_title": page_title,
        "section_slug": section_slug,
    }


def _weekday_label(value):
    return WEEKDAY_LABELS[value.weekday()]


def _content_length(text):
    return len(re.sub(r"\s+", "", text or ""))


def _decorate_post(post):
    post.weekday_label = _weekday_label(post.created_at)
    post.word_count = _content_length(post.body)
    return post


def music_list(request):
    context = _media_list_context(
        MediaItem.Category.MUSIC,
        "Music",
        "music",
    )
    return render(request, "content/media_list.html", context)


def music_detail(request, pk):
    item = get_object_or_404(
        MediaItem,
        pk=pk,
        category=MediaItem.Category.MUSIC,
    )
    context = _media_detail_context(item, "Music", "music")
    return render(request, "content/media_detail.html", context)


def film_list(request):
    context = _media_list_context(
        MediaItem.Category.FILM,
        "Film",
        "film",
    )
    return render(request, "content/media_list.html", context)


def film_detail(request, pk):
    item = get_object_or_404(
        MediaItem,
        pk=pk,
        category=MediaItem.Category.FILM,
    )
    context = _media_detail_context(item, "Film", "film")
    return render(request, "content/media_detail.html", context)


def fragments_list(request):
    context = {
        "items": Fragment.objects.all(),
        "page_title": "Fragments",
        "section_slug": "fragments",
    }
    return render(request, "content/fragments_list.html", context)


def fragments_detail(request, pk):
    item = get_object_or_404(Fragment, pk=pk)
    context = {
        "item": item,
        "page_title": "Fragments",
        "section_slug": "fragments",
    }
    return render(request, "content/fragment_detail.html", context)


def thoughts_list(request):
    context = {
        "items": [_decorate_post(item) for item in Post.objects.order_by("-id")],
        "page_title": "Thoughts",
        "section_slug": "thoughts",
    }
    return render(request, "content/thoughts_list.html", context)


def thoughts_detail(request, pk):
    item = get_object_or_404(Post, pk=pk)
    context = {
        "item": _decorate_post(item),
        "page_title": "Thoughts",
        "section_slug": "thoughts",
    }
    return render(request, "content/thought_detail.html", context)


def about_view(request):
    return render(request, "content/about.html", _about_context())
