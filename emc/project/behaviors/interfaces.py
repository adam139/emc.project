#-*- coding: UTF-8 -*-
from zope.interface import Interface


# Database event
class IChannel_numberLocator(Interface):
    def IsChannel(self,newAttr):
        """判断是否为 channel,返回True 或者 False
        """
    def AddChannel(self,num):
        """添加一条渠道记录
        """
        