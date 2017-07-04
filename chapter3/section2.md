# 学员管理系统

这一节让我们来快速的过一下Django的各个模块，在上一节内容中，你可能了解了Django所提供的功能，这一节我们来切实体会一下。你最好打开你熟悉的IDE，一起写起来。

## 需求

一句话就能描述清楚的需求：提供一个学员管理系统，一个前台页面，展示现有学员，并供新学员提交申请，一个后台，能够处理申请。over

## 初始化环境

首先，创建虚拟环境: ``mkvirtualenv student-env -p `which python2.7` `` (最后的-p是指明虚拟环境使用的python版本2.7)。不熟悉的可以看这里: [使用virtualenv创建虚拟python环境](https://www.the5fire.com/virtualenv-python-env.html)

然后激活虚拟环境: ``workon student-env``，接着我们安装django，目前的最新版1.11.2: ``pip install django==1.11.2``。


## 创建项目

虽然可以不创建虚拟环境就安装Django，但是我还是建议你在虚拟环境中安装，因为在实际的开发中，你可能需要维护不止一个项目。不同项目的所依赖库的版本也不同，如果你都安装到root下或者user下，会出现冲突的问题。

好了，cd到你喜欢的目录中，比如``/home/the5fire/workspace/``，创建项目根目录: ``mkdir student_house``，这是我们的项目目录，然后再我们创建项目结构: ``cd student_house && django-admin startproject student_sys``，我们能得到下面的结构:

TODO:



## 创建APP

进入`student_house/student_sys`中，通过上一步创建好的manage.py创建一个app: ``python manage.py startapp student``。现在目录结构如下:


TODO:



## 编写代码

我们可以在Model层开始写代码了，这是一个简单的需求，我们只需要一个Model就可以满足。

student_house/student_sys/student/models.py:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models


    class Student(models.Model):
        SEX_ITEMS = [
            (1, '男'),
            (2, '女'),
            (0, '未知'),
        ]
        STATUS_ITEMS = [
            (0, '申请'),
            (1, '通过'),
            (2, '拒绝'),
        ]
        name = models.CharField(max_length=128, verbose_name="姓名")
        sex = models.IntegerField(choices=SEX_ITEMS, verbose_name="性别")
        profession = models.CharField(max_length=128, verbose_name="职业")
        email = models.EmailField(verbose_name="Email")
        qq = models.CharField(max_length=128, verbose_name="QQ")
        phone = models.CharField(max_length=128, verbose_name="电话")

        status = models.IntegerField(choices=STATUS_ITEMS, verbose_name="审核状态")

        created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")

        def __unicode__(self):
            return '<Student: {}>'.format(self.name)

        class Meta:
            verbose_name = verbose_name_plural = "学员信息"

再来写admin.py:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.contrib import admin

    from .models import Student


    class StudentAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'sex', 'profession', 'email', 'qq', 'phone', 'status', 'created_time')
        list_filter = ('sex', 'status', 'created_time')
        search_fields = ('name', 'profession')
        fieldsets = (
            (None, {
             'fields': (
                     'name',
                     ('sex', 'profession'),
                     ('email', 'qq', 'phone'),
                     'status',
                     )
             }),
        )


    admin.site.register(Student, StudentAdmin)

写完这两个配置，model和admin的界面就ok了，接下来我们把这个``student``app放到settings.py中。

我们只需要在INSTALLED_APPS配置的最后，或者最前面增加'student'即可:

settings.py文件:

    INSTALLED_APPS = [
        'student',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

好了，后台部分就完成了，我们来创建下表以及超级用户，通过下面命令:

* ``cd student_house/student_sys/``
* ``python manage.py makemigrations``  创建迁移文件
* ``python manage.py migrate``  创建表
* ``python manage.py createsuperuser`` 根据提示，输出用户名，邮箱，密码

启动项目: ``python manage.py runserver``，访问: http://127.0.0.1:8000，看到一个提示页，这是因为我们还没开发首页。我们可以进入到admin的页面: http://127.0.0.1:8000/admin/。用你创建好的账户登录，就能看到一个完整的带有CURD的后台了。


## 基础配置（中文）

通过上面的配置，你看到的界面应该是英文的，并且时区也是UTC时区。所以我们需要进一步配置。

在settings中有如下配置:

    LANGUAGE_CODE = 'zh-hans'  # 语言

    TIME_ZONE = 'Asia/Shanghai'  # 时区

    USE_I18N = True  # 语言

    USE_L10N = True  # 数据和时间格式

    USE_TZ = True  # 启用时区

修改完这些之后，刷新下试试。你可以尝试修改上面的配置，看看分别对应什么功能。

到这一部分我们基本上完成了admin的部分。下一节我们来完成页面提交数据的部分，看下如何使用Form。
