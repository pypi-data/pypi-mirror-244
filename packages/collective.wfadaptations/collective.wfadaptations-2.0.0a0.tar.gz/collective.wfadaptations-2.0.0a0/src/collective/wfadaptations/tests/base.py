# -*- coding: utf-8 -*-
from collective.wfadaptations.interfaces import IWorkflowAdaptation
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IDummySchema(Interface):

    param = schema.TextLine(
        title=u"Dummy parameter",
        required=True)


@implementer(IWorkflowAdaptation)
class DummyWorkflowAdaptation(object):

    schema = IDummySchema
    multiplicity = False
    reapply = False

    def patch_workflow(self, workflow_name, **parameters):
        self.patched = "{};{};{}".format(workflow_name, parameters['param'], self.reapply)  # noqa
        return True, ''


@implementer(IWorkflowAdaptation)
class AnotherWorkflowAdaptation(object):

    schema = None

    def patch_workflow(self, workflow_name, **parameters):
        return True, ''
