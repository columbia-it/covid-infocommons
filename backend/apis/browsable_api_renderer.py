from rest_framework.renderers import BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx['display_edit_forms'] = False
        return ctx