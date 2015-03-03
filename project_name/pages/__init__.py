import blanc_pages

default_app_config = '{{ project_name }}.pages.apps.PagesConfig'


class DefaultLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/default.html'
    title = 'Default Page'
    columns = {
        'Intro': {
            'width': 1069,
        },
        'Content': {
            'width': 1069,
        },
    }


class PageLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/page.html'
    title = 'Page with submenu'
    columns = {
        'Intro': {
            'width': 1069,
        },
        'Content': {
            'width': 1069,
        },
    }


blanc_pages.register_template(DefaultLayout)
blanc_pages.register_template(PageLayout)
