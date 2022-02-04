from wagtail.core import hooks


@hooks.register("register_icons")
def register_fontawesome_icons(icons):
    # Find more icons https://github.com/FortAwesome/Font-Awesome/tree/master/svgs
    # or https://github.com/allcaps/wagtail-font-awesome-svg/
    return icons + [
        "wagtailfontawesomesvg/solid/share.svg",
    ]
