#-*- coding: UTF-8 -*-
from zope import schema
from plone.autoform import directives
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm

from emc.project.indexer import IProjectContent
from emc.project.browser.vocabulary import DocTitle

try:
    from plone.app.dexterity import _ as _p
except:
    from plone.app.dexterity import MessageFactory as _p


class IDocument(IProjectContent):
    """
    emc project  document content type
    """
    # self-defined title and description
#     title = schema.TextLine(
#         title=_(u'label_title', default=u'Title'),
#         required=True
#     )

    title = schema.Choice(
        title=_p(u'label_title'),
        source=DocTitle,
        required=True,
    )
    
    description = schema.Text(
        title=_p(u'label_description', default=u'Summary'),
        description=_p(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u'',
    )
    
    directives.order_before(description='*')
    directives.order_before(title='*')

    directives.omitted('title', 'description')
    directives.no_omit(IEditForm, 'description')
    directives.no_omit(IAddForm, 'title', 'description')        

