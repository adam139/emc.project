# -*- coding: utf-8 -*-
from emc.project.interface import IProjectContent
from plone.app.contenttypes.content import File
from zope.interface import implementer


class IFile(IProjectContent):
    """
    emc project file mark interface
    """


@implementer(IFile)
class ProjectFile(File):
    """ProjectFile inharit from plone.app.contenttypes's File"""