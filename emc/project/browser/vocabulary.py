from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import directlyProvides

from emc.policy.patch.zh import normalizer
from emc.project.interface import IDocTypeSettings

def DocTitle(context):
    """Context source binder to provide a vocabulary of document's title.
    """

    settings = getUtility(IRegistry).forInterface(IDocTypeSettings)

    terms = []
    pttl = context.title        
    for item in settings.types:
        docttl = "%s%s" %(pttl,item)
        asciittl = normalizer.normalize(docttl)           
        terms.append(SimpleVocabulary.createTerm(docttl, asciittl, docttl))
    return SimpleVocabulary(terms)
    
directlyProvides(DocTitle, IContextSourceBinder)

def makingDocTitle(context):
    """Context source binder to provide a vocabulary of document's title.
    """

    settings = getUtility(IRegistry).forInterface(IMaking)

    terms = []
    pttl = context.title        
    for item in settings.types:
        docttl = "%s%s" %(pttl,item)
        asciittl = normalizer.normalize(docttl)           
        terms.append(SimpleVocabulary.createTerm(docttl, asciittl, docttl))
    return SimpleVocabulary(terms)
    
directlyProvides(makingDocTitle, IContextSourceBinder)    