import os
import tempfile

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import emc.project
#        import xtshzz.policy
#        self.loadZCML(package=xtshzz.policy)
  
        xmlconfig.file('configure.zcml', emc.project, context=configurationContext)        
#        xmlconfig.file('configure.zcml', xtshzz.policy, context=configurationContext)
                      
    def tearDownZope(self, app):
        pass
    
    def setUpPloneSite(self, portal):
     
        applyProfile(portal, 'emc.project:test')
#        applyProfile(portal, 'xtshzz.policy:default')
     

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="emcproject:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="emcproject:Functional")
