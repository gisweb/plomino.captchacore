# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plomino.captchacore.testing import PLOMINO_CAPTCHACORE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that plomino.captchacore is properly installed."""

    layer = PLOMINO_CAPTCHACORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plomino.captchacore is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('plomino.captchacore'))

    def test_browserlayer(self):
        """Test that IPlominoCaptchacoreLayer is registered."""
        from plomino.captchacore.interfaces import IPlominoCaptchacoreLayer
        from plone.browserlayer import utils
        self.assertIn(IPlominoCaptchacoreLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLOMINO_CAPTCHACORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['plomino.captchacore'])

    def test_product_uninstalled(self):
        """Test if plomino.captchacore is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('plomino.captchacore'))
