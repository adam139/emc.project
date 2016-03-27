from plone.app.registry.browser import controlpanel
from emc.project.interface import IDocTypeSettings
from emc.project import _

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

class DocTypeSettingsEditForm(controlpanel.RegistryEditForm):
    
    schema = IDocTypeSettings
    label = _(u"Document types settings")
#     schema_prefix = "projectconf" 
    description = _(u"Please enter details of available types")
    
    def updateFields(self):
        super(DocTypeSettingsEditForm, self).updateFields()
        self.fields['types'].widgetFactory = TextLinesFieldWidget
    
    def updateWidgets(self):
        super(DocTypeSettingsEditForm, self).updateWidgets()
        self.widgets['types'].rows = 8
    
class DocTypeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DocTypeSettingsEditForm
  



# DocTypeSettingsView = layout.wrap_form(
#     DocTypeSettingsEditForm, controlpanel.ControlPanelFormWrapper)    
    
    