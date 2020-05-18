from django.utils.html import format_html

from wagtail.admin.edit_handlers import EditHandler


class ReadOnlyFieldPanel(EditHandler):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )

    def _get_value(self):
        value = getattr(self.instance, self.attr)
        is_callable = callable(value)
        if is_callable:
            value = value()
        return value

    def render(self):
        return format_html('<div style="padding-top: 1.2em;">{}</div>', self._get_value())

    def render_as_object(self):
        return format_html(
            f"""
            <fieldset><legend>{self.heading}</legend>
            <ul class="fields"><li><div class="field">{self.render()}</div></li></ul>
            </fieldset>
            """
        )

    def render_as_field(self):
        return format_html(
            f"""
            <div class="field">
            <label>{self.heading}:</label>
            <div class="field-content">{self.render()}</div>
            </div>
            """
        )
