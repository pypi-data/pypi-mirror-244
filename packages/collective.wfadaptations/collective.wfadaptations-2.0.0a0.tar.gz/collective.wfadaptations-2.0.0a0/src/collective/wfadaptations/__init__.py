# -*- coding: utf-8 -*-
"""Init and utils."""

from plone import api
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.wfadaptations')

PLONE_VERSION = api.env.plone_version()[:3]
