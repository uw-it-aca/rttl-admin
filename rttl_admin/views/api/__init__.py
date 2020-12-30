from django.http import HttpResponse
import json


def error_response(status, message='', content={}):
    content['error'] = '{}'.format(message)
    return HttpResponse(json.dumps(content),
                        status=status,
                        content_type='application/json')


def json_response(content='', status=200):
    return HttpResponse(json.dumps(content, sort_keys=True),
                        status=status,
                        content_type='application/json')
