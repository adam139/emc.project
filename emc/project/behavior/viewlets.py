# -*- coding: utf-8 -*-
from emc.project.behavior.belowcontentfile import IAttachFile
from plone.app.layout.viewlets import ViewletBase


class AttachFileViewlet(ViewletBase):
    """ A simple viewlet which renders attach file """

    def update(self):
        self.context = IAttachFile(self.context)
        self.available = True if self.context.attach else False
