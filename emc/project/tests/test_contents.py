import unittest as unittest

from emc.bokeh.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('emc.bokeh.fearture', 'fearture1')

        self.portal = portal
    
    def test_item_types(self):
        self.assertEqual(self.portal['fearture1'].id,'fearture1')
    
        