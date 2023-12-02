# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.wfadaptations import PLONE_VERSION
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestInstall(unittest.TestCase):
    """Test installation of collective.wfadaptations into Plone."""

    layer = COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if PLONE_VERSION >= '5.1':
            from Products.CMFPlone.utils import get_installer  # noqa
            self.installer = get_installer(self.portal, self.layer["request"])
            self.ipi = self.installer.is_product_installed
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')  # noqa
            self.ipi = self.installer.isProductInstalled

    def test_product_installed(self):
        """Test if collective.wfadaptations is installed."""
        self.assertTrue(self.ipi('collective.wfadaptations'))

    def test_uninstall(self):
        """Test if collective.wfadaptations is cleanly uninstalled."""
        if PLONE_VERSION >= '5.1':
            self.installer.uninstall_product('collective.wfadaptations')
        else:
            self.installer.uninstallProducts(['collective.wfadaptations'])
        self.assertFalse(self.ipi('collective.wfadaptations'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveWfadaptationsLayer is registered."""
        from collective.wfadaptations.interfaces import ICollectiveWfadaptationsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveWfadaptationsLayer, utils.registered_layers())
