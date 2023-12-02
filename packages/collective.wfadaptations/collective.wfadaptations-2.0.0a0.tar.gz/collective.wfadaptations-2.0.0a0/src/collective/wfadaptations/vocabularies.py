# -*- coding: utf-8 -*-
"""Vocabularies."""
from collective.wfadaptations.interfaces import IWorkflowAdaptation
from zope.component import getUtilitiesFor
from zope.schema.vocabulary import SimpleVocabulary


class WorkflowAdaptationsVocabulary(object):

    """List available workflow adaptations."""

    def __call__(self, context):
        adaptations = getUtilitiesFor(IWorkflowAdaptation)
        terms = [SimpleVocabulary.createTerm(klass, name, name)
                 for name, klass in adaptations]

        return SimpleVocabulary(terms)
