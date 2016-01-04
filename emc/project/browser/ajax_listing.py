#-*- coding: UTF-8 -*-
from zope.interface import Interface
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

# from collective.gtags.source import TagsSourceBinder
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.gtags.interfaces import ITagSettings
from emc.project import viewReport
grok.templatedir('templates') 

class BaseView(grok.View):
    "social organizations list page"
    grok.context(Interface)
    grok.template('ajax_listings')
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
        
    def splitTag(self,value):
            """Split a tag into (category, tag) parts. category may be None.
            """
            parts = value.split("-")        
    
            if len(parts) == 1:
                return value
            else:
                return parts[1:][0]
    
        
    def getAllTags(self):
        """fetch system all predefine tags"""
        settings = getUtility(IRegistry).forInterface(ITagSettings)

#         source = TagsSourceBinder(allow_uncommon=False)
        tags = [self.splitTag(value) for value in settings.tags]
        return tags
    def getAllTagsHtml(self):
        """
                        <span data-name="1"><a href="javascript:void(0)">分析</a></span>
                        <span data-name="2"><a href="javascript:void(0)">设计</a></span>
                        <span data-name="3"><a href="javascript:void(0)">实验</a></span>
                        <span data-name="4"><a href="javascript:void(0)">仿真</a></span> 
                        <span data-name="5"><a href="javascript:void(0)">培训</a></span>  
        """
        out = ""
        i = 1
        for tag in self.getAllTags():
            num = str(i)                       
            out2 = """<span data-name="%s"><a class="btn btn-default" href="javascript:void(0)" role="button">%s</a></span>""" % (num,tag)
            out = "%s%s" %(out,out2)
            i = i + 1
        return out

class SiteRootajaxListingView(BaseView):
    """
    AJAX 查询，返回分页结果
    """
    grok.context(Interface)
    grok.template('ajax_listings')
    grok.name('ajax_listings')
     
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)                
        
    def canbeRead(self):
#        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission(viewReport,self.context)

        return canbe is not None

    def hasSummaryView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"summary_view")
        except:
            sview = None
        return  sview is not None
    
    def hasListingView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"listing_view")
        except:
            sview = None
        return  sview is not None 
    
    def buildAjaxViewName(self):
        "根据当前上下文，构建ajax view 名称"
        context = aq_inner(self.context)
        if ISiteRoot.providedBy(context):return "oajaxsearch"
        else:return "xiangtanshisearch"        
        
    def getPathQuery(self):
 
        """返回 all organizations
        """
        query = {}
        query['path'] = "/".join(self.context.getPhysicalPath())
        return query
#任务类型属性：分析/设计/实验/仿真/培训          
    def getTaskType(self,typekey):
        if typekey == 1:
            return "analysis"
        elif typekey == 2:
            return "design"
        elif typekey == 3:
            return "experiment"
        elif typekey == 4:
            return "simulation"                
        else:
            return "train"
         
#密级属性：公开/内部/机密 
    def getSecurityLevel(self,key):
        if key == 1:
            return "public"
        elif key == 2:
            return "inner"
        else:
            return "secret"
         
    def search_multicondition(self,query):  
        return self.catalog()(query)        

   



        

 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """    
    grok.context(Interface)
    grok.name('ajaxsearch')
    grok.require('zope2.View')    
#     grok.require('emc.project.view_projectsummary')

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
        searchview = getMultiAdapter((self.context, self.request),name=u"ajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
#         import pdb
#         pdb.set_trace()
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
        tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = searchview.getPathQuery()
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if securitykey != 0:
            origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)           
        if tasktypekey != 0:
            origquery['task_type'] = searchview.getTaskType(tasktypekey)
        all = u"所有".encode("utf-8")
#         import pdb
#         pdb.set_trace()
        if tag !=all and tag !="0":
            rule = {"query":tag,"operator":"or"}
            origquery['Subject'] = rule
                      
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
          
            out = """<tr class="text-left">
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>
                                <td class="col-md-2">%(date)s</td>                                
                            </tr> """% dict(objurl="%s/@@view" % i.getURL(),
                                            num=str(k + 1),
                                            title=i.Title,
                                            description= i.Description,
                                            date = i.created.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        


