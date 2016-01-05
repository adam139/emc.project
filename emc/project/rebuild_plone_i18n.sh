#!/bin/sh
PRODUCTNAME='plone'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
../../../../bin/i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --merge locales/${PRODUCTNAME}-manual.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
../../../../bin/i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/zh_CN/LC_MESSAGES/${PRODUCTNAME}.po