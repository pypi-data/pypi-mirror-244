# -*- coding: utf-8 -*-
"""API for workflow adaptations."""
from collective.wfadaptations.interfaces import IWorkflowAdaptation
from plone import api
from zope.component import getUtility

import json
import logging
import six


try:
    from zope.component.interfaces import ComponentLookupError
except ImportError:
    from zope.interface.interfaces import ComponentLookupError

RECORD_NAME = 'collective.wfadaptations.applied_adaptations'
logger = logging.getLogger('collective.wfadaptations')


class AdaptationAlreadyAppliedException(Exception):
    pass


def get_applied_adaptations():
    """Get applied adaptations for all workflows.

    :returns: The list of applied adaptations
    :rtype: list
    """
    record = api.portal.get_registry_record(RECORD_NAME, default=None)
    if record is None:
        return []

    # deserialize parameters
    return [{u'workflow': info['workflow'],
             u'adaptation': info['adaptation'],
             u'parameters': json.loads(info['parameters'])} for info in record]


def add_applied_adaptation(adaptation_name, workflow_name, multiplicity, **parameters):
    """Add an applied adaptation to registry record.

    :param adaptation_name: [required] name of the applied adaptation
    :type adaptation_name: Unicode object
    :param workflow_name: [required] name of the workflow on which the adaptation is applied
    :type workflow_name: Unicode object
    :param multiplicity: [required] can the same adaptation be applied multiple times
    :type multiplicity: boolean
    """
    by_workflow = get_applied_adaptations_by_workflows()
    if not multiplicity and workflow_name in by_workflow and adaptation_name in by_workflow[workflow_name]:
        raise AdaptationAlreadyAppliedException

    serialized_params = json.dumps(parameters, sort_keys=True)
    value = {
        u'workflow': six.text_type(workflow_name),
        u'adaptation': six.text_type(adaptation_name),
        u'parameters': six.text_type(serialized_params),
        }

    record = api.portal.get_registry_record(RECORD_NAME)
    if record is None:
        record = []

    record.append(value)
    api.portal.set_registry_record(RECORD_NAME, record)


def get_applied_adaptations_by_workflows():
    """Return a list of applied adaptations for each workflow.

    :returns: A dict which keys are workflow names and values are the list of
    applied workflow adaptations for this workflow.
    :rtype: dict
    """
    applied_adaptations = api.portal.get_registry_record(RECORD_NAME)
    if applied_adaptations is None:
        return {}

    result = {}
    for adaptation in applied_adaptations:
        workflow = adaptation['workflow']
        adaptation = adaptation['adaptation']
        if workflow not in result:
            result[workflow] = []

        result[workflow].append(adaptation)

    return result


def get_applied_adaptations_for_workflow(workflow_name):
    """Return the list of applied adaptations for workflow_name.

    :param workflow_name: [required] name of the workflow
    :type workflow_name: Unicode object

    :returns: A list of applied workflow adaptations for this workflow.
    :rtype: dict
    """
    all_applied = get_applied_adaptations_by_workflows()
    if workflow_name not in all_applied:
        return []
    else:
        return all_applied[workflow_name]


def apply_from_registry(reapply=False, name=None):
    """Apply workflow adaptations from registry settings.

    :param reapply: to indicate that the wf adaptations are reapplied after a workflow reset. Default to False.
    :param name: if given, only the same adaptation name string is reapplied
    :returns: The number of success and errors that occured during the process.
    :rtype: (int, int)
    """
    errors = 0
    success = 0
    logger.info("Apply workflow adaptations from registry.")
    for info in get_applied_adaptations():
        adaptation_name = info['adaptation']
        if name is not None and adaptation_name != name:
            continue
        try:
            adaptation = getUtility(IWorkflowAdaptation, adaptation_name)
            adaptation.reapply = reapply
        except ComponentLookupError:
            logger.error(
                "The adaptation '{}' has not been found.".format(
                    adaptation_name))
            errors += 1
            continue

        workflow_name = info['workflow']
        wtool = api.portal.get_tool('portal_workflow')
        if workflow_name not in wtool:
            logger.error("There is no '{}' workflow.".format(workflow_name))
            errors += 1
            continue

        parameters = info['parameters']
        result, message = adaptation.patch_workflow(workflow_name, **parameters)
        if result:
            success += 1
        else:
            logger.error("The patch has not been applied. {}".format(message))
            errors += 1

    logger.info(
        "Workflow adaptations applied from registry with {} success and {} "
        "errors".format(success, errors))
    return success, errors
