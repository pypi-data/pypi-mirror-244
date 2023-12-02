# -*- coding: utf-8 -*-
"""List workflow adaptations."""
from collective.wfadaptations.api import get_applied_adaptations
from Products.Five import BrowserView


class ListWorkflowAdaptations(BrowserView):

    """View that lists applied workflow adaptations."""

    def adaptations(self):
        """Return applied adaptations."""
        return get_applied_adaptations()
