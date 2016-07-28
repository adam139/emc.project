#-*- coding: UTF-8 -*-
from five import grok
from plone.directives import dexterity
from emc.project.content.document import IDocument

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView

class DocAddForm(DefaultAddForm):

    def update(self):
        DefaultAddForm.update(self)

    def updateWidgets(self):
        """ """
        DefaultAddForm.updateWidgets(self)
        self.widgets['IRichText.report'].rows = 3
        self.widgets['IRichText.report'].addClass('report')
        



class AddView(DefaultAddView):
    form = DocAddForm

class DocEditForm(dexterity.EditForm):

    grok.context(IDocument)

    def updateWidgets(self):
        """ """
        dexterity.EditForm.updateWidgets(self)
        
#         import pdb
#         pdb.set_trace()
        self.widgets['IRichText.report'].rows = 3
        self.widgets['IRichText.report'].addClass('report')