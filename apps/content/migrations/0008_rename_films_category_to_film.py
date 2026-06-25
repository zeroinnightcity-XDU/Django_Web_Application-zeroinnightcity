from django.db import migrations, models


def rename_films_category_to_film(apps, schema_editor):
    MediaItem = apps.get_model("content", "MediaItem")
    MediaItem.objects.filter(category="films").update(category="film")


def rename_film_category_to_films(apps, schema_editor):
    MediaItem = apps.get_model("content", "MediaItem")
    MediaItem.objects.filter(category="film").update(category="films")


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0007_mediaitem_release_year"),
    ]

    operations = [
        migrations.RunPython(
            rename_films_category_to_film,
            rename_film_category_to_films,
        ),
        migrations.AlterField(
            model_name="mediaitem",
            name="category",
            field=models.CharField(
                choices=[("music", "Music"), ("film", "Film")],
                max_length=20,
                verbose_name="类别",
            ),
        ),
    ]
