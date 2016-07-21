#-*- coding: UTF-8 -*-
from zope.interface import Interface
from persistent.list import PersistentList
from plone.dexterity.interfaces import IDexterityContent
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer


from emc.memberArea import _

SENDED_KEY = 'emc.memberArea.senders'


class ISending(Interface):

    def available(userToken):
        """Determine the userToken  whether to be sent todoitem event,ture:will send
        """
                       
    def addSender(userToken):
        """add userid to user list.
        """
        
    def delSender(userToken):
        """delete user id from user list.
        """  
class ISendable(Interface):
    "mark interface for saving user list behavior"

@implementer(ISending)
@adapter(IDexterityContent)
class Send(object):
    """the self.sent list saved all id of users that had been sended todoitem create event """

    
    def __init__(self, context):
        self.context = context
        
        annotations = IAnnotations(context)
        if SENDED_KEY not in annotations.keys():
            annotations[SENDED_KEY] = PersistentList()          
        self.sent = annotations[SENDED_KEY]
    

        
    #Determine the userToken  whether to be sent todoitem event,ture:will send
    def available(self, userToken):
        return not(userToken in self.sent)
#         return self.sent.has_key(userToken) 
    #Editing statistics concern the number of               
    def addSender(self, userToken):
        if self.available(userToken):
            self.sent.append(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)
    #Editing statistics concern the number of               
    def delSender(self, userToken):
        if not self.available(userToken):
            self.sent.remove(userToken)
        else:
            raise KeyError("The %s is not concerned about" % userToken)