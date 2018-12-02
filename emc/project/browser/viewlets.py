# encoding=utf-8
from plone import api
from Acquisition import aq_inner
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName
from emc.project.behaviors.security_level import ISecurityLevel
from emc.project.behaviors.localroles import Ilocalroles
from borg.localrole.interfaces import ILocalRoleProvider
from emc.memberArea import DoFavorite

viewUsersRoles = "emc.project:View projectsummary"


class SecurityLevel(base.ViewletBase):
    "render the current object's security level"
    
    output = None
    context = None

    def update(self):
        super(SecurityLevel, self).update()
        if self.output is None:
            self.output = self.output()
        if self.context is None:
            self.context = self.output()            
                
    def isEnabled(self):
        """
        @return: Should this viewlet be rendered on this page.
        """
        context = aq_inner(self.context)
        has = ISecurityLevel.providedBy(context)
        if has:       
            return True
        else:
            return False
        
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = api.portal.get_tool(name='translation_service')

        title = translation_service.translate(value,
                                              domain='emc.project',
                                              mapping={},
                                              target_language='zh_CN',
                                              context=self.context,
                                              default='')
        return title 
    def output(self):
        """ Render viewlet only if it is enabled.
                <tr class="row">
                    <td class="col-md-4">李四</td>
                    <td class="col-md-4">重要人员</td>
                    <td class="col-md-4">秘密</td>                    
                </tr>
        """
        context = aq_inner(self.context)

        user = api.user.get_current()
        username = api.user.get(userid=user.id).getProperty('fullname') or user.id
        ulevel = api.user.get(userid=user.id).getProperty('safe_level') or 'secure'
        ulevel = self.tranVoc(ulevel)
        rlevel = ISecurityLevel(context).security_level
        rlevel = self.tranVoc(rlevel)
        op = """<tr class="row">
                  <td class="col-md-4 text-center">%(name)s</td>                
                  <td class="col-md-4 text-left">%(ulevel)s</td>
                  <td class="col-md-4 text-left">%(rlevel)s</td></tr>""" % dict(name=username,
                                                                                ulevel=ulevel,
                                                                                rlevel=rlevel)

        return op                        

class UsersRoles(base.ViewletBase):

    output = None
    hasRoles = None
    can_view = None

    # Update methods are guaranteed to be called before rendering for
    # Viewlets and Portlets (Because they are IContentProvider objects)
    # and for z3c.forms and formlib forms. But *not* for normal Browser Pages
    def update(self):
        super(UsersRoles, self).update()
        if self.output is None:
            self.output = self.output()
        
        if self.hasRoles is None:
            self.hasRoles = self.hasRoles()

        if self.can_view is None:
            user = api.user.get_current().id
            self.can_view = api.user.has_permission(viewUsersRoles, username=user, obj=self.context)
#             self.can_view = self.pm.checkPermission(
#                 viewUsersRoles, self.context)

    def hasRoles(self):
        lr = self.context.__ac_local_roles__
        return len(lr)
        
        
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = api.portal.get_tool(name='translation_service')

        title = translation_service.translate(value,
                                              domain='plone',
                                              mapping={},
                                              target_language='zh_CN',
                                              context=self.context,
                                              default='')
        return title

    def node_users(self):
        "get current node local roles that come from Ilocalroles behavior"
        context = self.context

        allroles = ILocalRoleProvider(context).getAllRoles()
        return allroles
        
    
    def output(self):        
        
        if not self.hasRoles: return ""
        lr = self.context.__ac_local_roles__
        roles = list(self.node_users())

        def lst2dic(lt):
            loop = dict()
            user = lt[0]
            rl = list(lt[1])
            loop[user] = rl
            return loop
        result = map(lst2dic,roles)
        result.append(lr)
        out = ""        
        for i in result:
            item = i.keys()
            user = api.user.get(userid=item[0]).getProperty('fullname') or item[0]
            rolelist = i.values()[0]
            if len(rolelist) == 0:
                rlist = ""
            else:
#                 startstr =""
                def tran(value):
                    if "Site Administrator" in value:value= "EMCDesigner"
                    elif "Contributor" in value:value ="Designer"
                    return self.tranVoc(value)
                outtran = map(tran,rolelist)
                #join all roles
                div = u"，"
                rlist = div.join(outtran)                                    
            
            op = """<tr class="row">
                  <td class="col-md-2 text-center">%(name)s</td>                
                  <td class="col-md-10 text-left">%(rlist)s</td></tr>""" % dict(name=user,
                                                                                rlist=rlist)
            out = "%s%s" % (out,op)
        return out
 