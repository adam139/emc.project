#!/bin/sh
PRODUCTNAME='plone'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# ../../../../bin/i18ndude --merge  locales/${PRODUCTNAME}.pot  locales/${PRODUCTNAME}-manual.pot 

# Synchronise the resulting .pot with the .po files
../../../../bin/i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/zh_CN/LC_MESSAGES/${PRODUCTNAME}.po
