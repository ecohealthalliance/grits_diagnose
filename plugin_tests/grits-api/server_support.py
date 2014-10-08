
global grits_diagnose_next_status
grits_diagnose_next_status = 'success'


def make_next_test_fail():
    global grits_diagnose_next_status
    grits_diagnose_next_status = 'failure'


# Simple mocking of the grits-api package
def handleDiagnosis(*arg, **kw):

    global grits_diagnose_next_status
    stat = grits_diagnose_next_status
    grits_diagnose_next_status = 'success'

    def response():
        response.ncalls += 1
        if response.ncalls <= 3:
            return {
                'status': 'pending',
                'message': 'a status message',
                'result': None,
                'content': 'Some data'
            }
        else:
            return {
                'status': stat,
                'message': 'a status message',
                'result': {'data': 'Something'},
                'content': 'Some data'
            }
    response.ncalls = 0

    return response
