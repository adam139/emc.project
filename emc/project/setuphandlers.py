# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from logging import getLogger

logger = getLogger(__name__)


STRUCTURE = [
    {
        'type': 'emc.project.projectFolder',
        'title': u'项目容器',
        'id': 'project_folder',
        'description': u'项目容器',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'emc.project.project',
            'title': u'笔记本E210',
            'id': 'notebooke210',
            'description': u'笔记本E210EMC项目',
            'layout': 'ajax_listings',
            'children': [
                         {'type': 'emc.project.team',
                          'title': u'主板',
                          'id': 'motherboard',
                          'description': u'主板组',
                          'security_level':'public',
                          'task_type':'train',
                          'layout': 'ajax_listings',                          
                                             } ,  
                         {'type': 'emc.project.team',
                          'title': u'显卡',
                          'id': 'displaycard',
                          'description': u'显卡',
                          'security_level':'public',
                          'task_type':'train',
                          'layout': 'ajax_listings',
                           'children': [
                                        {'type': 'emc.project.analysisDoc',
                                         'title': u'显卡分析',
                                         'id': 'analysis',
                                         'description': u'显卡分析文档',
                                         'security_level':'public',
                                         'task_type':'train',                          
                                                                             } ,  
                                        {'type': 'emc.project.designDoc',
                                         'title': u'显卡设计',
                                         'id': 'design',
                                         'description': u'显卡设计文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,    
                                        {'type': 'emc.project.auditDoc',
                                         'title': u'显卡审核',
                                         'id': 'audit',
                                         'description': u'显卡审核文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,  
                                        {'type': 'emc.project.diagnoseDoc',
                                         'title': u'故障诊断',
                                         'id': 'diagnose',
                                         'description': u'故障诊断文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,                                                                                       
                         
                                                                        ]
                                             } ,                                                
                         {'type': 'emc.project.team',
                          'title': u'网卡',
                          'id': 'network',
                          'description': u'网卡',
                          'security_level':'public',
                          'task_type':'train',
                          'layout': 'ajax_listings',
                           'children': [
                                        {'type': 'emc.project.analysisDoc',
                                         'title': u'网卡分析',
                                         'id': 'analysis',
                                         'description': u'网卡分析文档',
                                         'security_level':'public',
                                         'task_type':'train',                          
                                                                             } ,  
                                        {'type': 'emc.project.designDoc',
                                         'title': u'网卡设计',
                                         'id': 'design',
                                         'description': u'网卡设计文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,    
                                        {'type': 'emc.project.auditDoc',
                                         'title': u'网卡审核',
                                         'id': 'audit',
                                         'description': u'网卡审核文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,  
                                        {'type': 'emc.project.diagnoseDoc',
                                         'title': u'故障诊断',
                                         'id': 'diagnose',
                                         'description': u'故障诊断文档',
                                         'security_level':'public',
                                         'task_type':'train',
                                                                         } ,                                                                                       
                         
                                                                        ]
                                             } ,                            
                                            ]
                      },
           
                ]
    },   
]


def isNotCurrentProfile(context):
    return context.readDataFile('ploneconfsite_marker.txt') is None


def post_install(context):
    """Setuphandler for the profile 'default'
    """
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
#     portal = api.portal.get()
#     members = portal.get('Members', None)
#     if members is not None:
#         api.content.delete(members)


def content(context):
    """Setuphandler for the profile 'content'
    """
    if context.readDataFile('emc_content_marker.txt') is None:
        return
    portal = api.portal.get()
    for item in STRUCTURE:
        _create_content(item, portal)
#     from plone import api
    for i in range(1,10): 
        user = api.user.create(
                               username='test%s' % i,
                               email='test%s@plone.org' % i,
                               password='secret',
                               )


def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:
        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
