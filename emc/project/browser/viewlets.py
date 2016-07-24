# encoding=utf-8
from plone import api
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName
from emc.memberArea import DoFavorite

viewUsersRoles = "emc.project:View projectsummary"

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

    def output(self):
        
        
        if not self.hasRoles: return ""
        lr = self.context.__ac_local_roles__
        out = ""
        import pdb
        pdb.set_trace()
        for i in lr.keys():
            user = api.user.get(userid=i).fullname or i
            rolelist = lr[i]
            if len(rolelist) == 0:
                rlist = ""
            else:
                startstr =""
                for j in rolelist:
                    rl = self.tranVoc(j)
                    tmp = u"%s%s，" % (startstr,rl)
                    startstr = tmp
                rlist = startstr.rsplit(u"，")[0]                                       
            
            op = """<tr class="row">
                  <td class="col-md-2 text-center">%(name)s</td>                
                  <td class="col-md-10 text-left">%(rlist)s</td></tr>""" % dict(name=user,
                                                                                rlist=rlist)
            out = "%s%s" % (out,op)
        return out
 