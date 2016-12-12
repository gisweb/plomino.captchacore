# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import plomino.captchacore


class PlominoCaptchacoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=plomino.captchacore)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plomino.captchacore:default')


PLOMINO_CAPTCHACORE_FIXTURE = PlominoCaptchacoreLayer()


PLOMINO_CAPTCHACORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLOMINO_CAPTCHACORE_FIXTURE,),
    name='PlominoCaptchacoreLayer:IntegrationTesting'
)


PLOMINO_CAPTCHACORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLOMINO_CAPTCHACORE_FIXTURE,),
    name='PlominoCaptchacoreLayer:FunctionalTesting'
)


PLOMINO_CAPTCHACORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLOMINO_CAPTCHACORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PlominoCaptchacoreLayer:AcceptanceTesting'
)
