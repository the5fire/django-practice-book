# WSGI——Web框架基础

## 简介

WSGI，全称是Web Server Gateway Interface（Web服务网关接口）。

这是Python中的定义的一个网关协议，规定了Web Server如何跟应用程序进行交互。Web server可以理解为一个Web应用的容器，可以通过Web server来启动应用，进而提供http服务。而应用程序是指我们基于框架所开发的系统。

这个协议最主要的目的就是保证在Python中，所有Web Server程序或者说Gateway程序，能够通过统一的协议跟web框架，或者Web应用进行交互。这对于部署Web程序来说很重要，你可以选择任何一个实现了WSGI协议的Web Server来跑你的程序。

如果没有这个协议，那可能每个程序，每个Web Server都会各自实现各自的接口。

这一节我们来简单了解下WSGI协议是如何运作的，理解这一协议非常重要，因为在Python中大部分的Web框架都实现了此协议，在部署时也使用WSGI容器来进行部署。


## 简单的Web Server

在看WSGI协议之前，我们先来看一个通过socket编程实现的Web服务的代码。逻辑很简单，就是通过监听本地8080端口，接受客户端发过来的数据，然后返回对应的HTTP的响应。

    # 文件位置:/code/chapter2/section2/socket_server.py
	# coding:utf-8

	import socket

	EOL1 = '\n\n'
	EOL2 = '\n\r\n'
	body = '''Hello, world! <h1> from the5fire 《Django企业开发实战》</h1>'''
	response_params = [
		'HTTP/1.0 200 OK',
		'Date: Sat, 10 jun 2017 01:01:01 GMT',
		'Content-Type: text/plain; charset=utf-8',
		'Content-Length: {}\r\n'.format(len(body)),
		body,
	]
	response = b'\r\n'.join(response_params)


	def handle_connection(conn, addr):
		request = ""
		while EOL1 not in request and EOL2 not in request:
			request += conn.recv(1024)
		print(request)
		conn.send(response)
		conn.close()


	def main():
        # socket.AF_INET    用于服务器与服务器之间的网络通信
        # socket.SOCK_STREAM    基于TCP的流式socket通信
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口可复用，保证我们每次Ctrl C之后，快速再次重启
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind(('127.0.0.1', 8080))
        # 可参考：https://stackoverflow.com/questions/2444459/python-sock-listen
		serversocket.listen(1)
		print('http://127.0.0.1:8080')

		try:
			while True:
				conn, address = serversocket.accept()
				handle_connection(conn, address)
		finally:
			serversocket.close()


	if __name__ == '__main__':
		main()

代码的逻辑很简单，但是建议你在自己的电脑上敲一遍，然后Python2运行起来（用Python3的话需要做些调整），通过浏览器访问是否能收到正确响应。并且修改其中代码，观察结果。比如说修改上面`Content-Type: text/plain` 中的 `plain` 为 `html` ，然后Ctrl C结束进程，重新运行，刷新页面，看看结果。

理解这段代码很重要，这是Web服务最基本的模型，通过socket和HTTP协议，提供Web服务。建议你在理解上面的代码之前，不要继续往下学习。

## 简单的WSGI application

理解了上面的代码之后，我们继续看看WSGI协议，也就是我们一开头介绍的。WSGI协议分为两部分，其中一部分是Web Server或者Gateway，就像上面的代码一样，监听在某个端口上，接受外部的请求。另外一部分是Web Application，Web Server接受到请求之后会通过WSGI协议规定的方式把数据传递给Web Application，我们在Web Application中处理完之后，设置对应的状态和HEADER，之后返回body部分。Web Server拿到返回数据之后，再进行HTTP协议的封装，最终返回完整的HTTP Response数据。

这么说可能比较抽象，我们还是通过代码来演示下这个流程。我们先实现一个简单的application：

    # 文件位置：/code/chapter2/section2/wsgi_example/app.py
    # coding:utf-8


    def simple_app(environ, start_response):
        """Simplest possible application object"""
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world! -by the5fire \n']

这就是一个简单的application，那么我们要怎么运行它呢？我们先按照Python PEP3333文档上的实例代码来运行它。这是一个cgi的脚本。

    # 文件位置：/code/chapter2/section2/wsgi_example/gateway.py

    # coding:utf-8

    import os
    import sys

    from app import simple_app


    def run_with_cgi(application):
        environ = dict(os.environ.items())
        environ['wsgi.input'] = sys.stdin
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True

        if environ.get('HTTPS', 'off') in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        else:
            environ['wsgi.url_scheme'] = 'http'

        headers_set = []
        headers_sent = []

        def write(data):
            if not headers_set:
                raise AssertionError("write() before start_response()")

            elif not headers_sent:
                # Before the first output, send the stored headers
                status, response_headers = headers_sent[:] = headers_set
                sys.stdout.write('Status: %s\r\n' % status)
                for header in response_headers:
                    sys.stdout.write('%s: %s\r\n' % header)
                sys.stdout.write('\r\n')

            sys.stdout.write(data)
            sys.stdout.flush()

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        # Re-raise original exception if headers sent
                        raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None     # avoid dangling circular ref
            elif headers_set:
                raise AssertionError("Headers already set!")

            headers_set[:] = [status, response_headers]
            return write

        result = application(environ, start_response)
        try:
            for data in result:
                if data:    # don't send headers until body appears
                    write(data)
            if not headers_sent:
                write('')   # send headers now if body was empty
        finally:
            if hasattr(result, 'close'):
                result.close()

    if __name__ == '__main__':
        run_with_cgi(simple_app)

我们运行一下这个脚本: python gateway.py，在命令行上能够看到对应的输出：

    Status: 200 OK
    Content-type: text/plain

    Hello world! -by the5fire

对比下一开始我们通过socket写的server，这个就是一个最基本的HTTP响应了。如果输出给浏览器，浏览器会展示出`Hello world! -by the5fire`的字样。

我们再通过另外一种方式来运行我们的Application，用到的这个工具就是gunicorn。你可以先通过命令`pip install gunicorn`进行安装。

安装完成之后，进入到app.py脚本的目录。通过命令: `gunicorn app:simle_app` 来启动程序。这里的gunicorn就是一个Web Server。启动之后会看到如下输出:

    [2017-06-10 22:52:01 +0800] [48563] [INFO] Starting gunicorn 19.4.5
    [2017-06-10 22:52:01 +0800] [48563] [INFO] Listening at: http://127.0.0.1:8000 (48563)
    [2017-06-10 22:52:01 +0800] [48563] [INFO] Using worker: sync
    [2017-06-10 22:52:01 +0800] [48566] [INFO] Booting worker with pid: 48566

通过浏览器访问：http://127.0.0.1:8000 就能看到对应的页面了。


## 理解WSGI

通过上面的代码，你应该看到了简单的application中对WSGI协议的实现。你可以在`simple_app`方法中增加print语句来查看参数分别是什么。

WSGI协议规定，application必须是一个callable对象，这意味这个对象可以是Python中的一个函数，也可以是一个实现了``__call__``方法的类的实例。比如这个:

    # 文件位置：/code/chapter2/section2/wsgi_example/app.py

    class AppClass(object):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]

        def __call__(self, environ, start_response):
            print(environ, start_response)
            start_response(self.status, self.response_headers)
            return ['Hello AppClass.__call__\n']

    application = AppClass()


我们依然可以通过gunicorn这个WSGI Server来启动应用: ``gunicorn app:aplication``，再次访问 http://127.0.0.1:8000 看看是不是输出了同样的内容。

除了这种方式之外，我们可以通过另外一种方式实现WSGI协议，从上面 ``simple_app`` 和这里 ``AppClass.__call__``的返回值来看，WSGI Server中只需要一个可迭代的对象就行，callable也就是返回一个列表。那么我们可以用下面这种方式达到同样的结果:

    class AppClassIter(object):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]

        def __init__(self, environ, start_response):
            self.environ = environ
            self.start_response = start_response

        def __iter__(self):
            self.start_response(self.status, self.response_headers)
            yield 'Hello AppClassIter\n'


我们再次使用gunicorn来启动: ``gunicorn app:AppClassIter``，然后打开浏览器访问 http://127.0.0.1:8000，看看结果。

这里的启动命令并不是一个类的实例，而是类本身，为什么呢？通过上面两个代码，我们可以观察到能够被调用的方法会传environ和start_response过来，而现在这个实现，没有可调用的方式，所以就需要在实例化的时候通过参数传递进来，这样在返回body之前，可以先调用start_response方法。

所以我们可以推测出WSGI Server是如何调用WSGI Application的。大概代码如下:

    def start_response(status, headers):
        # 伪代码
        set_status(status)
        for k, v in headers:
            set_header(k, v)

    def handle_conn(conn):
        # 调用我们定义的application（也就是上面的simple_app或者是AppClass的实例或者是AppClassIter本身）
        app = application(environ, start_response)
        # 遍历返回的结果，生成response
        for data in app:
            response += data

        conn.sendall(response)

大概如此。


## WSGI中间件和Werkzeug（WSGI工具集）

理解了上面的逻辑，我们就可以继续行程了。

除了交互部分的定义，WSGI还定义了中间件部分的逻辑，这个中间件可以理解为Python中的一个装饰器，可以在不改变原方法的同时对方法的输入和输出部分进行处理。

比方说对返回body中的文字部分，把英文转换为中文等之类的操作。或者是一些更为易用的操作，比如对返回内容的封装，上面的例子我们是先调用start_response方法，然后再返回body，我们能不能直接封装一个Response对象呢，直接给对象设置header，而不是这种单独操作的逻辑。比如像这样:

    def simple_app(environ, start_response):
        response = Repsonse('Hello World', start_repsonse=start_response)
        response.set_header('Content-Type', 'text/plain')
        return response

这样不是更加自然。

因此就存在了Werkzeug这样的WSGI工具集。让你能够跟WSGI协议更加友好的交互。理论上我们可以直接通过WSGI协议的简单实现，也就是我们上面的代码，写一个Web服务。但是有了Werkzeug之后，我们可以写的更加容易。在很多Web框架中都是通过Werkzeug来处理WSGI协议的内容的。


## 参考文档

* [Python CGI](https://www.the5fire.com/python-project6-cgi.html)
* [gunicorn-sync源码](https://github.com/benoitc/gunicorn/blob/master/gunicorn/workers/sync.py#L176)
* [gunicorn-wsgi部分代码](https://github.com/benoitc/gunicorn/blob/master/gunicorn/http/wsgi.py#L241)
* [PEP3333中文](http://pep-3333-wsgi.readthedocs.io/en/latest/)
* [PEP3333英文](https://www.python.org/dev/peps/pep-3333/)
* [Werkzeug官网](http://werkzeug.pocoo.org/)
* [Werkzeug中文文档](http://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/)

## 扩展阅读

* [ASGI英文文档](https://channels.readthedocs.io/en/latest/asgi.html)
* [ASGI中文翻译](https://blog.ernest.me/post/asgi-draft-spec-zh)
* [Django SSE](https://www.the5fire.com/message-push-by-server-sent-event.html)
