#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import ISiteRoot
from plone.directives import dexterity
from plone.memoize.instance import memoize
from emc.project import _
from emc.project.content.projectfolder import IProjectFolder
from emc.project.content.project import IProject
from emc.project.content.team import ITeam



grok.templatedir('templates') 

class BaseView(grok.View):
    "social organizations list page"
    grok.context(IProjectFolder)
    grok.template('allorgnization_listings_b3')
    grok.name('listview')
    grok.require('zope2.View')    
    

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

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
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context) 

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')

        title = translation_service.translate(
                                                  value,
                                                  domain='emc.project',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
       
        
        brains = self.catalog()({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
        
    def pendingDefault(self):
        "计算缺省情况下，还剩多少条"
        total = len(self.allitems())
        if total > 10:
            return total -10
        else:
            return 0    
    
    
    @memoize         
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})
        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath        
        



class SiteRootAllOrgnizationListingView(BaseView):
    """
    AJAX 查询，返回分页结果
    """
    grok.context(ISiteRoot)
    grok.template('allorgnization_listings_b3')
    grok.name('allorgnization_listings')
     
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)                
        

    
    def buildAjaxViewName(self):
        "根据当前上下文，构建ajax view 名称"
        context = aq_inner(self.context)
        if ISiteRoot.providedBy(context):return "oajaxsearch"

        else:return "xiangtanshisearch"        
        
    def getorgnizations(self):
 
        """返回 all organizations
        """

        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})
#翻译 社团，民非，基金会          
    def getType(self,typekey):
        if typekey == 1:
            return "shetuan"
        elif typekey ==2:
            return "minfei"
        else:
            return "jijinhui"
         
#翻译 成立公告，变更，注销公告  
    def getProvince(self,provincekey):
        if provincekey == 1:
            return "chengli"
        elif provincekey ==2:
            return "biangeng"
        else:
            return "zhuxiao"
         
    def search_multicondition(self,query):  
        return self.catalog()(query)        

   


class yuhuquorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(ISiteRoot)     
#    grok.template('yuhuqu_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all organizations
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'yuhuqu',
                             'sort_order': 'reverse',
                             'sort_on':'created'})
        

 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """    
    grok.context(ISiteRoot)
    grok.name('oajaxsearch')
    grok.require('zope2.View')

    def Datecondition(self,key):        
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)       
       
    def output(self,start,size,totalnum,braindata):
        "根据参数total,braindata,返回jason 输出"
        outhtml = ""      
        k = 0
        for i in braindata:
#            objurl = i.getURL()
#            objtitle = i.Title
#            address = i.orgnization_address
#            register_code = i.orgnization_registerCode
#            legal_person = i.orgnization_legalPerson
#            objdate = i.orgnization_passDate.strftime('%Y-%m-%d')
#            sponsor = i.orgnization_supervisor            
#            numindex = str(k + 1)            
            out = """<tr class="text-left">
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-1">%(code)s</td>
                                <td class="col-md-3 text-left">%(address)s</td>
                                <td class="col-md-2 text-left">%(sponsor)s</td>
                                <td class="col-md-1 text-left">%(legal_person)s</td>
                                <td class="col-md-2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=i.getURL(),
                                            num=str(k + 1),
                                            title=i.Title,
                                            code= i.orgnization_registerCode,
                                            address=i.orgnization_address,
                                            sponsor=i.orgnization_supervisor,
                                            legal_person = i.orgnization_legalPerson,
                                            pass_date = i.orgnization_passDate.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        


####################################################3333333333
class OrgAdminListAjax(ajaxsearch):
    grok.name('org_admin_list')
    
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
#        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
#        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
#        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
 
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
                 
        del origquery 
        del totalquery,totalbrains
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
######################################################                              
class yuhuqusearchlist(ajaxsearch):
    grok.name('yuhuqusearch')
    
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'yuhuqu'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
                 
        del origquery 
        del totalquery,totalbrains
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)             
                   