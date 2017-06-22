# Tornado 框架

https://github.com/tornadoweb/tornado

在工作中使用Tornado到现在也有5年了。相对于上一节的Flask，我对Tornado非常熟悉。但是如果要总结Tornado的特性的话，那也只是`高性能`。除此之外没有什么可以介绍的。

不同于Flask或者其他的基于WSGI的框架，Tornado并不是基于WSGI协议的框架。虽然它提供了WSGI协议的支持，但是为了能够用到它的特性（异步、非阻塞），官方建议还是直接通过自带的HTTP Server进行部署，而不是WSGI。

因为WSGI协议是同步，Application端只需要处理上游的发送过来的environ（第二节我们有讲到）。当然现在的WSGIServer或者叫WSGI容器都支持多种启动方式，比如Gunicorn可以通过gevent/greenlet/gthread等来实现协程或者异步IO，但是这些都是WSGIServer中的，对于Application没有太多影响。所以对Tornado中的WSGI协议的适配也没太多作用，无法利用Tornado自身的特性，所以官方也不推荐使用WSGI的方式部署。


## 内置功能

对比flask来说，Tornado的特点十分明显，除了基本的Request和Response封装之外，就是基于io loop的特性。我们只来看下Web相关的功能。

* tornado.web — RequestHandler and Application classes （基础的Request的封装）
* tornado.template — Flexible output generation（简单的模板系统）
* tornado.routing — Basic routing implementation（基础的路由配置）
* tornado.escape — Escaping and string manipulation （转码和字符串的操作）
* tornado.locale — Internationalization support （国际化的支持）
* tornado.websocket — Bidirectional communication to the browser（Websocket的支持）

从整体上看，它并不如上一节我们介绍的Flask丰富，比如session的实现，比如文档友好程度，比如第三方插件的丰富程度。但是，这个差异其实是两个框架定位的不同，Flask更多的是对业务需求的满足，而Tornado针对的是高性能web系统。至于业务的部分，自己实现吧。

除了上述列出来的基础功能，tornado最大的卖点还是基于io loop（或者说基于event loop）的异步非阻塞的实现。就像文档中声称的:

> By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets, and other applications that require a long-lived connection to each user.

> 翻译一下就是：通过非阻塞的网络I/O，Tornado能够支撑成千上万的连接，这使它很适合对每个用户都需要建立长连接的需求，无论是是通过long polling(长轮询）Websockets，或者其他应用。

这也是我们选择它的原因，虽然我们的业务场景并非长连接，但能够承担更多的并发量正是我们需要的。

## 总结

在Python2.x的环境中，基于event loop模型的Tornado确实很有卖点。但是在Python3.x中，语言内部支持了event loop，这导致更多的框架可以很容易的开发出了异步非阻塞的模型。这对于Tornado确实是一个挑战。

但是，新兴的框架必然还要经受生成环境的考验，产生大量经验之后，其他人才可能放心使用。而Tornado基于多年的发展已经在生产环境中得到了证明，并且有大量的企业会分享出他们的最佳实践。

未来而言，哪种异步非阻塞的框架更加流行不好断言，但是从技术知识上来讲，都差不太多。
