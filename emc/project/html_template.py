# -*- coding: utf-8 -*-

message = """<html>
<body>
<p>%(from)s</p>

%(message)s

<hr/>
<p><a href="%(url)s">%(url_text)s</a></p>
</body>
</html>
"""
# dummy i18n helper for workflow states
#from zope.i18nmessageid import MessageFactory
from Products.CMFPlone import PloneMessageFactory as _p
#workflow status
dummy = _p("fangan")


