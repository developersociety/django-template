from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.html import format_html

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail.core import hooks


@hooks.register("insert_editor_js")
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.modelChooser = '{0}';
        </script>
        """,
        reverse("models_choose_generic"),
    )


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("dist/css/admin.css"))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("dist/js/admin.js"))


@hooks.register("register_rich_text_features")
def register_blockquote_feature(features):
    feature_name = "blockquote"
    type_ = "blockquote"
    tag = "blockquote"

    control = {"type": type_, "label": "❝", "description": "Blockquote", "element": "blockquote"}

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {tag: BlockElementHandler(type_)},
            "to_database_format": {"block_map": {type_: tag}},
        },
    )
