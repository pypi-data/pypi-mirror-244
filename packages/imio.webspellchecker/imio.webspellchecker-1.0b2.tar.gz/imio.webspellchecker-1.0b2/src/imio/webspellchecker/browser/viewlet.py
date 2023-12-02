from imio.webspellchecker.browser.controlpanel import IWebspellcheckerControlPanelSchema
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


WSC_SCRIPTS_TEMPLATE = """
<script src="{plonesite}/wscinit.js?t={timestamp}"></script>
<script crossorigin="anonymous" src="{bundle}?t={timestamp}"></script>
"""


class WscJsViewlet(ViewletBase):
    def index(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IWebspellcheckerControlPanelSchema, check=False
        )
        if settings.enabled:
            return WSC_SCRIPTS_TEMPLATE.format(
                plonesite=api.portal.get().absolute_url(),
                timestamp=api.portal.get_registry_record(
                    "imio.webspellchecker.scripts_timestamp"
                ),
                bundle=settings.js_bundle_url,
            )
        return ""
