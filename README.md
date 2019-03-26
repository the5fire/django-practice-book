# 《Django企业开发实战》初版草稿 -- by the5fire

* 博客: https://www.the5fire.com  
* github: https://github.com/the5fire/django-practice-book
* 配套视频: [视频版](course.md)
* 进阶视频: [Django源码分析视频](https://www.the5fire.com/django-source-inside-catalog-by-the5fire.html)

## 纸质版已上市

* [图灵社区-目录和试读](http://www.ituring.com.cn/book/2663)

* [![Django企业开发实战](http://file.ituring.com.cn/SmallCover/19014dfb7e0e331be8db)](https://book.douban.com/subject/30434690/)

* [图灵社区购买](http://www.ituring.com.cn/book/2663)
* [京东购买](https://item.jd.com/12537842.html)
* [当当网购买](http://product.dangdang.com/26509799.html)
* [亚马逊购买](https://www.amazon.cn/dp/B07N3PVGZK/ref=sr_1_1?ie=UTF8&qid=1550195346&sr=8-1&keywords=Django%E4%BC%81%E4%B8%9A%E5%BC%80%E5%8F%91)

## 疑惑解答

* 问：视频和图书有什么差别
* 答：
    * 图书是在视频之后产出的，基于Python3.6 和 Django 1.11（LTS版本），在书最后会升级到Django 2.0，内容上会更加细致。
    * 视频是基于Python 2.7和Django 1.11（LTS版本） 的版本，最终会升级到 Python3.6 和 Django2.0，内容上会更加动态，信息量会更大，毕竟书上不能带着你写代码，视频是可以非常直观的演示代码编写的。

## 提交勘误

如果你发现*纸质书籍*中存在问题，欢迎提交勘误，步骤如下:
* 指明具体「章节」「页码」出错的部分代码或者相关信息
* 点击[创建 Issues](https://github.com/the5fire/django-practice-book/issues/new) 来填些上面的信息。

## 随书源码 && 随视频源码

本书对应源码和相关视频对应源码都在：

[https://github.com/the5fire/typeidea](https://github.com/the5fire/typeidea)

通过分支名来区分是视频还是图书，以及对应的章节，比如：

分支 ``book/05-initproject`` 就是对应的图书的第五章的代码，``book/06-admin`` 就是对应的第六章的代码。
而对应的 ``chapter7``、``chapter8``这样的是视频章节对应的代码。


## 前言

从JavaWeb开发转行到PythonWeb开发已经有6年多了，一开始就是从SSH框架转到Django，我觉得这玩意太轻便了，比SSH好用太多了。但是熟悉了Python社区之后，发现在Python中，Django确实算是一个比较重的框架。主要的原因在于它的定位：企业级开发框架，或者说全功能的Web开发框架。Web系统涉及到的方面它都有提供。这也是导致它学习成本看起来有点高的原因。

在用Django的几年中，我和我们的小伙伴们用它做了N多个系统，有对内的，也有对外的，都能够很好的满足我们的需求。所以今年我就在考虑，能不能总结出来一些东西，对大家有所帮助，主要是想学习Django，但是不得其门者。

于是就有了这个开始，包括这本教程，也包括配套的[视频教程](course.md)。

希望对你有所帮助。关于Django的问题可以加我的QQ群:111054501(Django企业开发实践)进行交流。


## 目标读者

* 学完Python基础想要继续学习Web开发的同学
* 想要学习Django的同学


## Power by Django

https://www.djangoproject.com/start/overview/

前几天比较火的Instagram就是基于Django开发的，从官网上也能看到其他我们耳熟能详的产品，比如：Disqus，Pinterest，Mozilla，Sentry。


## 生态

Django之所有被广泛应用，除了本身是提供了完备的功能之外， 也得益于它的成熟生态，框架本身没有提供的功能，会有优秀的第三方插件来补足。比如Django-rest-framework，比如Django Debug toolbar。


## 学习曲线

相对于Flask、web.py、bottle这一类的微框架来说，Django的上手确实有点复杂，但是并不难。因为官网的新手指导写的很清晰。在众多框架中，Django的文档算是相当不错的了。

你需要花比学习微框架更多的时间来学习Django，是因为Django提供的内容远多于其他框架。刚开始可能会觉得很多地方不明白，但是等你熟悉了之后，会发现Django每个层所提供的功能都很清晰，什么样的需求，在哪一层来处理，会有清晰的认识。

Django的学习曲线是先陡，然后平缓上升的。先陡主要是新手需要一下子接受很多东西，但是随着之后的不断使用，不断了解，你会发现，学习所耗费的时间完全值得。你可以更快的做出完善的系统，这会是一笔很划算的投资。


## 这本书的目的

把我知道的东西、开发项目中总结的经验，融到一个Blog系统中，写出来。让后来者可以参考我的经验快速成长。


## 勘误和提问

欢迎到github上给我提Issues: https://github.com/the5fire/django-practice-book
