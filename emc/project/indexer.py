from plone.indexer.decorator import indexer
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFPlone.utils import safe_unicode
from plone.app.contenttypes.indexers import _unicode_save_string_concat,SearchableText
from zope.interface import Interface
from emc.project.interface import IProjectContent
from emc.project.content.project import IProject
from emc.project.content.team import ITeam
from emc.project.content.document import IDocument
from emc.project.content.file import IFile
from emc.project.content.image import IImage


@indexer(IProject)
def SearchableText_project(obj):
    return _unicode_save_string_concat(SearchableText(obj))

@indexer(IFile)
def SearchableText_file(obj):
    return _unicode_save_string_concat(SearchableText(obj))

@indexer(IImage)
def SearchableText_image(obj):
    return _unicode_save_string_concat(SearchableText(obj))

@indexer(ITeam)
def SearchableText_team(obj):
    return _unicode_save_string_concat(SearchableText(obj))

@indexer(IDocument)
def SearchableText_document(obj):
#     if obj.text is None or obj.text.output is None:
#             return _unicode_save_string_concat(SearchableText(obj))
    return _unicode_save_string_concat(SearchableText(obj), obj.text.output)

# @indexer(IProjectContent)
# def indexer_security_level(obj, **kw):
#     return obj.security_level
# 
# @indexer(IProjectContent)
# def indexer_task_type(obj, **kw):
#     return obj.task_type

# @indexer(IProjectContent)
# def indexer_report(obj, **kw):
#     return obj.report

