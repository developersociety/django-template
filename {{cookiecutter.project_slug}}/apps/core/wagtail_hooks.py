from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.core import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("dist/css/admin.css"))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("dist/js/admin.js"))


@hooks.register("register_rich_text_features")
def register_pre_feature(features):
    feature_name = "pre"
    type_ = "PRE"
    tag = "pre"

    control = {"type": type_, "label": "code", "description": "Preformatted Text"}

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)


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


@hooks.register("register_rich_text_features")
def register_align_center_feature(features):
    feature_name = "align_center"
    type_ = "TEXTALIGNCENTER"
    tag = "div"

    control = {
        "type": type_,
        "icon": "fa-align-center",
        "description": "Align center",
        "style": {"display": "block", "text-align": "center"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {'div[class="text-center"]': InlineStyleElementHandler(type_)},
            "to_database_format": {
                "style_map": {type_: {"element": tag, "props": {"class": "text-center"}}}
            },
        },
    )


@hooks.register("register_rich_text_features")
def register_align_left_feature(features):
    feature_name = "align_left"
    type_ = "TEXTALIGNLEFT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "fa-align-left",
        "description": "Align Left",
        "style": {"display": "block", "text-align": "left"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {'div[class="text-left"]': InlineStyleElementHandler(type_)},
            "to_database_format": {
                "style_map": {type_: {"element": tag, "props": {"class": "text-left"}}}
            },
        },
    )


@hooks.register("register_rich_text_features")
def register_align_right_feature(features):
    feature_name = "align_right"
    type_ = "TEXTALIGNRIGHT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "fa-align-right",
        "description": "Align Right",
        "style": {"display": "block", "text-align": "right"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {'div[class="text-right"]': InlineStyleElementHandler(type_)},
            "to_database_format": {
                "style_map": {type_: {"element": tag, "props": {"class": "text-right"}}}
            },
        },
    )
