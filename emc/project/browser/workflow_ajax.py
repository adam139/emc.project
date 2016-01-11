#-*- coding: UTF-8 -*-
from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
import json
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
import datetime

from emc.project import _
from Products.CMFPlone import PloneMessageFactory as _p
from zope.interface import Interface
from emc.project.content.project import IProject


try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ImportError: # py24
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
from emc.project import html_template

class Workflow(grok.View):
    "接受前台ajax 事件，处理工作流基类"
    grok.name('workflow')   
    grok.require('zope2.View')
    grok.context(Interface)
    
    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
    
    def wf(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_workflow')
        
    def sendMail(self,subject,mailbody,send_to,send_to_bcc=[],sender=None,debug_mode=False):
        notify_encode = 'utf-8'
        object = aq_inner(self.context)
        portal = getToolByName(object,"portal_url").getPortalObject()
        portal_transforms = getToolByName(object, "portal_transforms")
        if sender ==None:
            send_from = portal.getProperty('email_from_address')
        else:
            send_from = sender
        if send_from and type(send_from)==tuple:
            send_from = send_from[0]
        
        translation_service = getToolByName(object,'translation_service')
        
        html_body = mailbody
        here_url = object.absolute_url()
        url_text = u"%s-%s年度-年检报告" % (object.title,object.year) 
        text = html_template.message % ({'from': send_from ,                                 
                                     'message': html_body,
                                     'url': here_url,
                                     'url_text': url_text,
                                     })        
                            
        if notify_encode:
            text = text.encode(notify_encode)
        try:
            data_to_plaintext = portal_transforms.convert("html_to_web_intelligent_plain_text", text)
        except:
            # Probably Plone 2.5.x
            data_to_plaintext = portal_transforms.convert("html_to_text", text)
        plain_text = data_to_plaintext.getData()
    
        msg = MIMEMultipart('alternative')
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(plain_text, 'plain', _charset=notify_encode)
        part2 = MIMEText(text, 'html', _charset=notify_encode)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)    
        mail_host = getToolByName(object, 'MailHost')
        try:
            if debug_mode:
                print "Message subject: %s" % subject
                print "Message text:\n%s" % text
                print "Message sent to %s (and to %s in bcc)" % (", ".join(send_to) or 'no-one',
                                                             ", ".join(send_to_bcc) or 'no-one')
            else:
                try:
                    mail_host.secureSend(msg, mto=send_to, mfrom=send_from,
                                     subject=subject, charset=notify_encode, mbcc=send_to_bcc)
                except TypeError:
                    # BBB: Plone 2.5 has problem sending MIMEMultipart... fallback to normal plain text email
                    mail_host.secureSend(plain_text, mto=send_to, mfrom=send_from,
                                     subject=subject, charset=notify_encode, mbcc=send_to_bcc)                
        except Exception, inst:
            putils = getToolByName(object,'plone_utils')
            putils.addPortalMessage(_(u'Not able to send notifications'))
            object.plone_log("Error sending notification: %s" % str(inst))
    
    def render(self):
        """
        workflow process ,this function should be subclass override.
        every subclass link to workflow transition.
        """
class ProjectWorkfow(Workflow):
    "接受前台ajax 事件，处理工作流，提交状态转换"
    
    grok.context(IProject)
    grok.name('workflow_ajax')
    
    def getChildrens(self,context):
        query = {'path': '/'.join(context.getPhysicalPath())}
        brains = self.catalog()(query)
        return [brain for brain in brains if brain.id !=context.id]    
          

    def render(self):
        """
            项目状态转换按钮 后台响应逻辑。

        input:{subject:'please approve';actionid:'chuyang'}
        output:{result,status,message}
        """
        data = self.request.form
        subject = data['subject']
        #workflow transition id
        actionid = data['actionid']
        transition = "submit2%s" % actionid
        context = aq_inner(self.context)
        brains = self.getChildrens(context)
#         import pdb
#         pdb.set_trace()
        for bn in brains:
            try:
                obj = bn.getObject()
                self.wf().doActionFor(obj, transition, comment=subject )
            except:
                continue

        try:
            self.wf().doActionFor(context, transition, comment=subject )
            newstatus = self.context.translate(_p(actionid))
            ajaxtext = u"%(project)s项目已成功切换到：<strong>%(status)s</strong>状态。" % ({"project":context.title,
                                                           "status":newstatus})
            callback = {"result":True,"status":newstatus,"message":ajaxtext}
        except:
            callback = {"result":False,"status":"","message":""}
            
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(callback)
    

