#-*- coding: UTF-8 -*-
from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
#import unicodedata
#from incf.countryutils import data as countrydata
from emc.project import _

#任务类型属性：分析/设计/实验/仿真/培训
task_type=[    ('analysis','analysis',_(u'analysis')),
                  ('design','design',_(u'design')),           
                  ('train','train',_(u'train')),           
                  ('simulation','simulation',_(u'simulation')),
                  ('experiment','experiment',_(u'experiment')),
                        ]
task_type_terms = [SimpleTerm(value, token, title) for value, token, title in task_type ]

class taskType(object):

    def __call__(self, context):
        return SimpleVocabulary(task_type_terms)

grok.global_utility(taskType, IVocabularyFactory,
        name="emc.project.vocabulary.tasktype")

#密级属性：内部/秘密/机密/绝密
# 公开/内部/普通商业秘密/秘密/核心商业秘密/机密
security_level=[  
                  ('public','public',_(u'public')),
                  ('inner','inner',_(u'inner')),                              
                  ('low','low',_(u'normal business secret')),
                  ('secret','secret',_(u'secret')),
                  ('high','high',_(u'high business secret')),
                  ('highest','highest',_(u'highest secret')),
                        ]
security_level_terms = [SimpleTerm(value, token, title) for value, token, title in security_level ]

class SecurityLevel(object):

    def __call__(self, context):
        return SimpleVocabulary(security_level_terms)

grok.global_utility(SecurityLevel, IVocabularyFactory,
        name="emc.project.vocabulary.securitylevel")

