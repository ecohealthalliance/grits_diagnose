
import time

import importlib
server_support = importlib.import_module('server_support', 'grits-api')

from girder.api.rest import Resource, RestException
from girder.api.describe import Description

try:
    from girder.api import access
except ImportError:
    def access():
        pass

    access.user = lambda x: x


@access.user
class DiagnoseHandler(Resource):

    def submit(self, params):
        url = params.get('url')
        content = params.get('content')

        # <- check permissions

        statusMethod = server_support.handleDiagnosis(content=content, url=url)

        status = statusMethod()
        maxLoops = 300
        iloop = 0
        while status == 'pending' and iloop < maxLoops:
            iloop += 1
            time.sleep(1)
            status = statusMethod()

        if status == 'pending':
            raise RestException("Task timed out.")

        if status == 'failure':
            raise RestException(status['message'])

        if False:  # <- check access to private data
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
