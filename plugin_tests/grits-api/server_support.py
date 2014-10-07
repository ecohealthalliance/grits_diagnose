

# Simple mocking of the grits-api package
def handleDiagnosis(*arg, **kw):

    def response():
        response.ncalls += 1
        if response.ncalls <= 3:
            return {
                'status': 'pending',
                'result': None,
                'content': 'Some data'
            }
        else:
            return {
                'status': 'success',
                'result': {'data': 'Something'},
                'content': 'Some data'
            }
    response.ncalls = 0

    return response
