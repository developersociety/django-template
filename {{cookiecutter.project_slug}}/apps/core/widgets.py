import json

from django.template.loader import render_to_string

from wagtail.admin.widgets import AdminChooser


class ModelChooser(AdminChooser):
    choose_one_text = "Choose a "
    choose_another_text = "Choose another "

    def __init__(self, target_model, **kwargs):
        self.target_model = target_model
        name = self.target_model._meta.verbose_name
        self.choose_one_text = "Choose %s" % name
        self.choose_another_text = "Choose another %s" % name
        self.link_to_chosen_text = "Edit this %s" % name

        super().__init__(**kwargs)

    def render_html(self, name, value, attrs):
        model_class = self.target_model

        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super().render_html(name, value, attrs)

        # Edit link
        edit_link = "{app_label}_{model_name}_modeladmin_edit".format(
            app_label=model_class._meta.app_label, model_name=model_class._meta.model_name
        )

        return render_to_string(
            "wagtailadmin/widgets/model_chooser.html",
            {
                "widget": self,
                "original_field_html": original_field_html,
                "attrs": attrs,
                "value": value,
                "item": instance,
                "edit_link": edit_link,
            },
        )

    def render_js_init(self, id_, name, value):
        model = self.target_model

        return "createModelChooser({id}, {model});".format(
            id=json.dumps(id_),
            model=json.dumps(
                "{app}/{model}".format(app=model._meta.app_label, model=model._meta.model_name)
            ),
        )

    class Media:
        js = ["wagtailadmin/chooser/model-chooser.js"]
