
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
    'privateGroup': 'GRITSPriv'  # Users in this group get extra data

}


class DiagnoseHandler(Resource):

    @access.user
    def submit(self, params):
        url = params.get('url')
        content = params.get('content')
        user = self.getCurrentUser()

        # check permissions
        group = ModelImporter().model('group').find({'name': config['group']})

        print 'count = %i' % group.count()
        if group.count():
            # the group must exist
            group = group[0]

            # the user must have read access to the group
            ModelImporter().model('group').requireAccess(group, user, AccessType.READ)

        else:
            raise AccessException('Invalid group name configured')

        statusMethod = server_support.handleDiagnosis(content=content, url=url)

        status = statusMethod()
        maxLoops = 300
        iloop = 0
        while status['status'] == 'pending' and iloop < maxLoops:
            iloop += 1
            time.sleep(1)
            status = statusMethod()

        if status['status'] == 'pending':
            raise RestException("Task timed out.")

        if status['status'] == 'failure':
            raise RestException(status['message'])

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
    )


def load(info):
    diagnoseHandler = DiagnoseHandler()
    info['apiRoot'].resource.route('POST', ('diagnose',), diagnoseHandler.submit)
