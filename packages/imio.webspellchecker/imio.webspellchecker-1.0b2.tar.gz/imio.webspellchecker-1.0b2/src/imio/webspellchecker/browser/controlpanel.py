from DateTime import DateTime
from imio.webspellchecker import _
from imio.webspellchecker.interfaces import IIWebspellcheckerControlPanelSettings
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from Products.CMFPlone.utils import safe_unicode
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IWebspellcheckerControlPanelSchema(Interface):
    """ """

    enabled = schema.Bool(
        title=_("Enabled"),
        description=_("Enable or disable Webspellchecker."),
        required=False,
        default=False,
    )
    hide_branding = schema.Bool(
        title=_("Hide branding"),
        description=_("Note: only available for server version."),
        required=False,
        default=False,
    )
    enable_grammar = schema.Bool(
        title=_("Enable grammar"),
        description=_(""),
        required=False,
        default=True,
    )
    theme = schema.Choice(
        title=_("Theme"),
        description=_(""),
        required=True,
        vocabulary="imio.webspellchecker.vocabularies.Themes",
        default="default",
    )
    js_bundle_url = schema.TextLine(
        title=_("WSC JS bundle URL"),
        description=_(""),
        required=True,
        default="",
    )
    service_url = schema.TextLine(
        title=_("WSC service URL"),
        description=_(""),
        required=True,
        default="",
    )
    service_id = schema.TextLine(
        title=_("Service ID"),
        description=_(""),
        required=False,
        default="",
    )


@implementer(IIWebspellcheckerControlPanelSettings)
class WebspellcheckerControlPanelEditForm(RegistryEditForm):
    schema = IWebspellcheckerControlPanelSchema
    label = _("Webspellchecker settings")
    description = _("Webspellchecker settings control panel")


class WebspellcheckerSettings(ControlPanelFormWrapper):
    form = WebspellcheckerControlPanelEditForm


def handle_configuration_changed(records, event):
    """Event subscriber that is called every time the configuration changed."""
    api.portal.set_registry_record(
        "imio.webspellchecker.scripts_timestamp",
        safe_unicode(str(DateTime().timeTime())),
    )
