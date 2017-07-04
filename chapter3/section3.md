# 学员管理系统- 前台

## 开发首页

有了上一节的Model和Admin的部分，我们接着来做一个简单的用户提交申请的表单页面。

首先在student/views.py文件中编写下面的代码:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.shortcuts import render


    def index(request):
        words = 'World!'
        return render(request, 'index.html', context={'words': words})

上面的代码中，我们用了django提供的一个快捷的方法``render()``来渲染页面，使用模板``index.html``文件。我们需要在student目录下创建``templates``文件夹，这个文件夹是Django在渲染页面时会默认查找的。

这部分需要多说几句的是，Django查找会去每个App下，也就是我们的settings.py文件中配置的``INSTALLED_APPS``中的app下的``templates``文件夹中查找你在``render``上用到的模板，并且是顺序查找。这意味着，如果你有两个app，比如studentA, studentB，而这两个app中都存在``templates/index.html``，那么Django会加载位置在前的那个App的index.html文件。这个你可以自行尝试下。通过这种方式我们也可以重写admin的模板。

创建好``templates/index.html``之后，我们编写页面代码。简单来做:

    <!DOCTYPE html>
    <html>
        <head>
            <title>学员管理系统-by the5fire</title>
        </head>
        <body>
            Hello {{ words }}!
        </body>
    </html>


接着我们需要再配置下url，也就是提供一个url映射，可以让用户访问url时把数据发送到我们定义的``index`` 这个view上。

我们直接来修改student_sys目录下的urls.py文件:

    # coding:utf-8

    from django.conf.urls import url
    from django.contrib import admin

    from student.views import index

    urlpatterns = [
        url(r'^$', index, name='index'),
        url(r'^admin/', admin.site.urls),
    ]

这样改完，我们再次启动项目: ``python manage.py runserver``，访问:http://127.0.0.1:8000就能看到我们输出的``Hello World!!' 了。


## 输出数据

接下来的工作就是把数据从表里面取出来，渲染到页面上了。你可以现在admin后台创建几条学员数据，以便于我们测试。

我们需要修改views.py中的代码:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.shortcuts import render

    from .models import Student


    def index(request):
        students = Student.objects.all()
        return render(request, 'index.html', context={'students': students})

接着修改index.html中的代码:

    <!DOCTYPE html>
    <html>
        <head>
            <title>学员管理系统-by the5fire</title>
        </head>
        <body>
            <ul>
            {% for student in students %}
                <li>{{ student.name }} - {{ student.get_status_display }}</li>
            {% endfor %}
            </ul>
        </body>
    </html>

这样我们就输出了一个简单的列表，展示学员名称和目前状态。这里有一个地方需要注意的是``{{ student.get_status_display }}``，在Model中我们只定义了``status``字段，并未定义这样的字段，为什么能通过这种方式取到数据呢。并且我们在Admin中，也没有使用这样的字段。

原因就是，对于设置了choices的字段，Django会帮我们提供一个方法（注意，是方法），用来获取这个字段对应的要展示的值。回头看下我们``status``的定义:

    ## 省略上下文代码

    STATUS_ITEMS = [
        (0, '申请'),
        (1, '通过'),
        (2, '拒绝'),
    ]

    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name="审核状态")

    ## 省略上下文代码

在admin中，展示带有choices属性的字段时，Django会自动帮我们调用``get_status_display``方法，所以我们不用配置。而在我们自己写的模板中，我们需要自己来写。并且在模板中不支持函数/方法调用，你只需要写方法名称即可，后面的括号不需要写。Django会自行帮你调用(如果是方法的话)。

## 提交数据

输出数据之后，我们再来开发提交数据的功能。这部分我们用一下Form。

首先我们先创建一个forms.py的文件，跟views.py同级。编写如下代码:

	# coding:utf-8
	from __future__ import unicode_literals

	from django import forms

	from .models import Student


	class StudentForm(forms.Form):
		name = forms.CharField(label='姓名', max_length=128)
		sex = forms.ChoiceField(label='性别', choices=Student.SEX_ITEMS)
		profession = forms.CharField(label='职业', max_length=128)
		email = forms.EmailField(label='邮箱', max_length=128)
		qq = forms.CharField(label='QQ', max_length=128)
		phone = forms.CharField(label='手机', max_length=128)

看这个``StudentForm``的定义是不是很熟悉，跟Model的定义类似，那么我们能不能复用Model的代码呢。答案是可以。还记得我们上节文档介绍的部分吗？有一个ModelForm可以用。我们来改下。

    # coding:utf-8
    from __future__ import unicode_literals

    from django import forms

    from .models import Student


    class StudentForm(forms.ModelForm):
        class Meta:
            model = Student
            fields = (
                'name', 'sex', 'profession',
                'email', 'qq', 'phone'
            )

只需要这么改就ok，不需要重复定义N多个字段。如果有修改对应字段类型的需求，比如把qq改成``IntegerField``用来做数字校验，也是可以声明出来。也可以通过定义``clean``方法的方式来做，我们来改下代码，增加QQ号必须为纯数字的校验:

	# coding:utf-8
	from __future__ import unicode_literals

	from django import forms

	from .models import Student


	class StudentForm(forms.ModelForm):
		def clean_qq(self):
			cleaned_data = self.cleaned_data['qq']
			if not cleaned_data.isdigit():
				raise forms.ValidationError('必须是数字！')

			return int(cleaned_data)

		class Meta:
			model = Student
			fields = (
				'name', 'sex', 'profession',
				'email', 'qq', 'phone'
			)

其中``clean_qq``就是Django的form会自动调用，来处理每个字段的方法，比如在这个form中你可以通过定义``clean_phone``来处理电话号码，可以定义``clean_email``来处理邮箱等等。如果验证失败，可以通过``raise forms.ValidationError('必须是数字！')``的方式返回错误信息，这个信息会存储在form中，最终会被我们渲染到页面上。


有了form，我们接下来需要做的就是在页面中展示form，让用户能够填写信息提交表单。同时对于提交的数据，我们需要先做校验，通过后可以保存到数据库中。来看下views.py中的文件最终的样子：

	# -*- coding: utf-8 -*-
	from __future__ import unicode_literals

	from django.http import HttpResponseRedirect
	from django.urls import reverse
	from django.shortcuts import render

	from .models import Student
	from .forms import StudentForm


	def index(request):
		students = Student.objects.all()
		if request.method == 'POST':
			form = StudentForm(request.POST)
			if form.is_valid():
				cleaned_data = form.cleaned_data
				student = Student()
				student.name = cleaned_data['name']
				student.sex = cleaned_data['sex']
				student.email = cleaned_data['email']
				student.profession = cleaned_data['profession']
				student.qq = cleaned_data['qq']
				student.phone = cleaned_data['phone']
				student.save()
				return HttpResponseRedirect(reverse('index'))
		else:
			form = StudentForm()

		context = {
			'students': students,
			'form': form,
		}
		return render(request, 'index.html', context=context)

里面有一个``form.cleaned_data``，这个对象是Django的form对用户提交的数据根据字段类型做完转换之后的结果。另外还有``reverse``的使用，我们在urls.py中定义``index``的时候，声明了``name='index'``，所以我们这里可以通过``reverse``来拿到对应的url。这么做的好处是，不需要硬编码url到代码中，这意味着如果以后有修改url的需求，只要index的名称不变，这个地方的代码就不用改。

写完views.py中的代码之后，我们要把form传到模板中，这样用户才能最终看到一个可以填写数据的表单。要在模板中加form，是相当简单的一件事。最终模板(index.html)代码如下:

	<!DOCTYPE html>
	<html>
		<head>
			<title>学员管理系统-by the5fire</title>
		</head>
		<body>
			<h3><a href="/admin/">Admin</a></h3>
			<ul>
				{% for student in students %}
				<li>{{ student.name }} - {{ student.get_status_display }}</li>
				{% endfor %}
			</ul>
			<hr/>
			<form action="/" method="post">
				{% csrf_token %}
				{{ form }}
				<input type="submit" value="Submit" />
			</form>
		</body>
	</html>

其中 ``{% csrf_token %}``是Django对提交数据安全性做的校验，这意味着，如果没有这个token，提交过去的数据是无效的。这是用来防止跨站伪造请求攻击的一个手段。

只需要这么写，Django就会帮我们自动把所有字段列出来。当然，如果需要调整样式，那就要自己来增加css样式文件解决了。

不过到此为止，功能上已经完备。你可以再次通过命令: ``python manage.py runserver``，访问: http://localhost:8000测试下页面功能是否可用。
