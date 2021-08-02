from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Locale = apps.get_model('wagtailcore.Locale')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('pages.HomePage')

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, __ = ContentType.objects.get_or_create(
        model='homepage', app_label='pages'
    )

    # Default locale - there should only be one locale in the database at this point, so a .get
    # should work
    locale = Locale.objects.get()

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Home",
        draft_title="Home",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
        locale=locale,
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=homepage, is_default_site=True
    )


def remove_homepage(apps, schema_editor):
    # Get models
    HomePage = apps.get_model('pages.HomePage')

    # Delete the default homepage
    # Page and Site objects CASCADE
    HomePage.objects.filter(slug='home', depth=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pages', '0001_initial'),
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
