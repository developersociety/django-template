from django import template

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-menu/


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return context['request'].site.root_page


def has_menu_children(page):
    # This is used by the navigation property
    # get_children is a Treebeard API thing
    # https://tabo.pe/projects/django-treebeard/docs/4.0.1/api.html
    return page.get_children().live().in_menu().exists()


def has_children(page):
    # Generically allow index pages to list their children
    return page.get_children().live().exists()


def is_active(page, current_page):
    # To give us active state on main navigation
    return (current_page.url_path.startswith(page.url_path) if current_page else False)


# Retrieves the navigation items - the immediate children of the parent page
# The has_menu_children method is necessary because the Foundation menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('includes/navigation_tags/navigation.html', takes_context=True)
def navigation(context, parent, calling_page=None):
    nav_items = parent.get_children().live().in_menu()
    for nav_item in nav_items:
        nav_item.show_dropdown = has_menu_children(nav_item)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        nav_item.active = (
            calling_page.url_path.startswith(nav_item.url_path) if calling_page else False
        )
    return {
        'calling_page': calling_page,
        'nav_items': nav_items,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the navigation items for the drop downs
@register.inclusion_tag('includes/navigation_tags/navigation_items.html', takes_context=True)
def navigation_items(context, parent, calling_page=None):
    nav_items = parent.get_children()
    nav_items = nav_items.live().in_menu()
    for nav_item in nav_items:
        nav_item.has_dropdown = has_menu_children(nav_item)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        nav_item.active = (
            calling_page.url_path.startswith(nav_item.url_path) if calling_page else False
        )
        nav_item.children = nav_item.get_children().live().in_menu()
    return {
        'parent': parent,
        'nav_items': nav_items,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
