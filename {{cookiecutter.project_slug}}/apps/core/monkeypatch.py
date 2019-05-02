from wagtail.admin.edit_handlers import EditHandler, FieldPanel


def _edit_handler_repr(self):
    return "<%s with model=%s instance=%s request=%s form=%s>" % (
        self.__class__.__name__,
        self.model,
        self.instance,
        self.request,
        self.form.__class__.__name__,
    )


def _field_panel_repr(self):
    return "<%s '%s' with model=%s instance=%s request=%s form=%s>" % (
        self.__class__.__name__,
        self.field_name,
        self.model,
        self.instance,
        self.request,
        self.form.__class__.__name__,
    )


EditHandler.__repr__ = _edit_handler_repr
FieldPanel.__repr__ = _field_panel_repr
