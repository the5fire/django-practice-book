# coding:utf-8

def simple_app(environ, start_response):
    """Simplest possible application object"""
    print(environ, start_response)
    print('\n\r')
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello simple_app world!\n']


class AppClass(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __call__(self, environ, start_response):
        print(environ, start_response)
        start_response(self.status, self.response_headers)
        return ['Hello AppClass.__call__\n']

application = AppClass()


class AppClassIter(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        print(self.environ, self.start_response)
        self.start_response(self.status, self.response_headers)
        yield 'Hello AppClassIter\n'
