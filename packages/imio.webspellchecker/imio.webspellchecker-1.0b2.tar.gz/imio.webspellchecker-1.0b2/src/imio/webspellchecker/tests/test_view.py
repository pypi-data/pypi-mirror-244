from imio.webspellchecker.tests import WSCIntegrationTest
from plone import api
from plone.testing._z2_testbrowser import Browser

import transaction


class TestView(WSCIntegrationTest):
    def setUp(self):
        super(TestView, self).setUp()
        app = self.layer["app"]
        self.browser = Browser(app)
        self.INIT_SCRIPT_URL = "{}/wscinit.js".format(self.portal.absolute_url())

    def test_js_view_doesnt_fail(self):
        self.browser.open(self.INIT_SCRIPT_URL)

    def test_js_view_include_all_info(self):
        self.browser.open(self.INIT_SCRIPT_URL)

        self.assertIn("window.WEBSPELLCHECKER_CONFIG", self.browser.contents)
        self.assertIn("enableGrammar", self.browser.contents)
        self.assertIn("serviceHost", self.browser.contents)
        self.assertIn("wsc.fake", self.browser.contents)
        self.assertIn("servicePath", self.browser.contents)
        self.assertIn("/wscservice/api/scripts/ssrv.cgi", self.browser.contents)
        self.assertIn("theme", self.browser.contents)
        self.assertIn("default", self.browser.contents)

    def test_js_view_is_disabled(self):
        api.portal.set_registry_record(
            "imio.webspellchecker.browser.controlpanel.IWebspellcheckerControlPanelSchema.enabled",
            False,
        )
        transaction.commit()
        self.browser.open(self.INIT_SCRIPT_URL)
        self.assertEqual(
            b"",
            self.browser.contents,
        )

    def test_js_view_headers(self):
        self.browser.open(self.INIT_SCRIPT_URL)

    def test_scripts_viewlet(self):
        self.browser.open(self.portal.absolute_url())
        self.assertIn("wscinit.js", self.browser.contents)
        self.assertIn("wscbundle", self.browser.contents)

    def test_scripts_viewlet_disabled(self):
        api.portal.set_registry_record(
            "imio.webspellchecker.browser.controlpanel.IWebspellcheckerControlPanelSchema.enabled",
            False,
        )
        transaction.commit()
        self.browser.open(self.portal.absolute_url())
        self.assertNotIn("wscinit.js", self.browser.contents)
        self.assertNotIn("wscbundle", self.browser.contents)

    def test_scripts_viewlet_timestamps(self):
        pass
