from imio.webspellchecker.testing import IMIO_WEBSPELLCHECKER_FUNCTIONAL_TESTING
from zope.globalrequest import setLocal

import unittest


class WSCIntegrationTest(unittest.TestCase):
    """Base class for integration browser tests."""

    layer = IMIO_WEBSPELLCHECKER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setLocal("request", self.portal.REQUEST)
        super(WSCIntegrationTest, self).setUp()
