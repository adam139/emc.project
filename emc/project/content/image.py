# -*- coding: utf-8 -*-
from emc.project.interface import IProjectContent
from plone.app.contenttypes.content import Image
from zope.interface import implementer


class IImage(IProjectContent):
    """
    emc project image mark interface
    """
    

@implementer(IImage)
class ProjectImage(Image):
    """ProjectImage inharit from plone.app.contenttypes's Image"""