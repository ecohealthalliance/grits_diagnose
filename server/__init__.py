
import time

import importlib
server_support = importlib.import_module('.server_support', 'grits-api')

from girder.api.rest import Resource, RestException
from girder.api.describe import Description
from girder.utility.model_importer import ModelImporter
from girder.constants import AccessType
from girder.models.model_base import AccessException

try:
    from girder.api import access
except ImportError:
    def access():
        pass

    access.user = lambda x: x

config = {
    'group': 'GRITS',  # Users must have read access in this group to hit the api.
    'privateGroup': 'GRITSPriv',  # Users in this group get extra data
    'maxTaskWait': 300,  # The maximum number of seconds to wait for the diagnosis task
    'pollingInterval': 0.1  # The interval in seconds to check the diagnosis task status
}


class DiagnoseHandler(Resource):

    def __init__(self):
        self.resourceName = 'grits'

    @access.user
    def submit(self, params):
        url = params.get('url')
        content = params.get('content')
        user = self.getCurrentUser()

        # check permissions
        group = ModelImporter().model('group').find({'name': config['group']})

        if group.count():
            # the group must exist
            group = group[0]

            # the user must have read access to the group
            ModelImporter().model('group').requireAccess(group, user, AccessType.READ)

        else:
            raise AccessException('Invalid group name configured')

        # Create the diagnosis task
        statusMethod = server_support.handleDiagnosis(content=content, url=url)

        # Get the initial status
        status = statusMethod()

        # Get the maximum number of times to poll the task
        maxLoops = config['maxTaskWait']/config['pollingInterval']

        # Loop until the task is finished
        iloop = 0
        while status['status'] == 'pending' and iloop < maxLoops:
            iloop += 1
            time.sleep(config['pollingInterval'])
            status = statusMethod()

        # Get status and report errors
        if status['status'] == 'pending':
            raise RestException("Task timed out.", code=408)

        if status['status'] == 'failure':
            raise RestException(status['message'], code=400)

        # check access to private data
        group = ModelImporter().model('group').find({'name': config['privateGroup']})
        hasAccess = False
        if group.count():
            group = group[0]
            try:
                ModelImporter().model('group').requireAccess(group, user, AccessType.READ)
                hasAccess = True
            except AccessException:
                pass

        # Append content data if the user has access
        if hasAccess:
            status["result"]["scrapedData"] = status["content"]

        return status["result"]

    submit.description = (
        Description(
            "Diagnose an article."
        )
        .notes(
            "Either a URL or text content must be provided."
        )
        .param(
            "content",
            "The article text",
            required=False
        )
        .param(
            "url",
            "A url containing the article to be scraped",
            required=False
        )
        .errorResponse('Error in diagnosis task', 400)
        .errorResponse('Permission denied', 403)
        .errorResponse('Diagnosis task timeout', 408)
    )


def load(info):
    diagnoseHandler = DiagnoseHandler()
    diagnoseHandler.route('POST', ('diagnose',), diagnoseHandler.submit)
    info['apiRoot'].grits = diagnoseHandler
