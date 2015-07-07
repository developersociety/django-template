import blanc_pages

default_app_config = 'pages.apps.PagesConfig'


class DefaultLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/default.html'
    title = 'Default'
    columns = {
        'Content': {
            'width': 960,
            'image_width': 960,
        },
    }


blanc_pages.register_template(DefaultLayout)
