# Django框架

https://www.djangoproject.com/

the5fire使用Django的时间比Tornado还久，在我从Java开发转到Python开发时直接是从Java的SSH(Struts、Spring、Hibernate)框架逃离到了Django上。一开始使用Django的感觉就是，这玩意太轻便了，比SSH轻太多了。但是没想到的是在Python社区Django也算是比较重的框架了。

对于Django框架，我的评价是这个是一个全功能的Web开发框架。Web开发所需要的一切它都包含了，你不需要去选择，只需要去熟悉，然后使用。

## 新手友好程度

前面介绍的两个框架：Flask和Tornado，你从文档上直接把代码copy到server.py文件中，然后直接`Python server.py`就能看到界面。但是到Django中，你发现新手指导需要写好多代码才能看到界面。所以大部分人觉得Django对新手并不友好，或者说它有一定的门槛。

其实我们换个角度来看，你在写完Flask和Tornado的第一个Python文件之后，接下来应该怎么做呢？就拿开发一个Blog来说吧，你要怎么组织你的代码，组织你的项目结构？这些搞定了之后，接下来你要怎么选择一个适合你的ORM，然后把它配置到项目中。你的配置文件要怎么共享给其他模块？你要怎么来处理用户登录？如果要放到外网访问的话，你怎么保证系统安全？

这些都是接下来要面对的问题。所以我的看法是，微框架让你能够快速的做些小的应用，比如就是几个页面，整个项目只需要三四个Python文件（模块）就搞定了。稍微大一些的项目，那就是考验Python能力了。这对于初学者来说，并不那么友好。

而Django提供了更完善的新手指导。你一开始可能无法写一个文件就让代码run起来，但是这一套新手招数打完之后，你可以基于此来完成一个稍微大点的项目。并且Django也会帮你处理好我上面提到的那些问题。


## 内置功能

一开始我也说到了，Django是作为全功能的Web开发框架出现的。这意味着它提供的可能远多于你想要的。我们简单列下常用的功能。

* HTTP的封装-request和response
* ORM
* Admin
* form
* template
* session和cookie
* 权限
* 安全
* Cache
* Logging
* Sitemap
* RSS

上面列出了常用的部分，也是我们这次需求需要的部分，都能满足我们的需求。Django再次之外还提供了更多的功能，比如i18n（多语言的支持），gis的支持等。

我的观点是，如果你掌握了Django，那么你就是掌握了Web开发中的大部分知识。因为这个框架涉及到了Web开发的所有层面。


## 总结

对于Web开发来说，尤其是基于内容驱动的项目，我推荐用Django来做，因为即便你选择了Flask或者其他的微框架，然后把插件拼装起来，最终也是做了一个类Django的框架，基于松散的配置。还不如Django在整体上的整合。

Django作为一个从新闻系统生成环境中诞生的框架，是直接面向企业级开发的。无论是从社区的发展，还是整体的生态（比如Django大会，Django基金会）来看Django都是十分成熟的框架，并有有十分完善的周边生态。

另外我们也可以看看基于它开发的那些我们耳熟能详的产品，如Instagram， Disqus，Sentry，Open Stack等，这些都证明了Django在企业开发中的地位。


## 参考
* https://www.djangoproject.com/start/overview/
* https://docs.djangoproject.com/en/1.11/
* [Django第三方插件](https://djangopackages.org/)
* [Django Sites](https://www.djangosites.org/)
