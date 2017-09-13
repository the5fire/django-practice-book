## 定制admin

上一节我们完成了基础的admin代码编写，已经得到了一个基本可用的内容管理系统，这一节我们来说下常用的定制行的操作。让大家有一个初步的认识，后面在实现需求时还会做更多的讲解。

框架为了达到更高的通用性，只会抽象出通用的逻辑。因此有些特性的东西需要我们自己来做。不过一个好的框架，提供给我们定制的能力。比如这一节我们会看到如何定制admin的界面，来达到我们的需求。


## 定制site

重写Django自带的adminsite，实现自己的admin页面。


## 定义list页面

第一个我们需要定制的就是list页面，如果你确实把自己当做用户，去写几篇文章之后，你会发现，这个页面是会频繁操作到的页面，因此这个页面能提供的功能，对于用户的使用效率来说至关重要。

关于列表展示的几个配置：

    list_display = ['title', 'category', 'status', 'owner', 'created_time']
    list_filter = ['category']
    search_fields = ['title', 'category__name', 'owner__username']
    show_full_result_count = True
    # 补充
    list_display_links = ['category', 'status']
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'created_time'
    list_editable = ('title', )

## 刨源码来看上节课的问题
实际项目开发中经常会遇到与期望不符的结果，因此排查问题是必备技能，对于Python来说，看源码也是相对容易的，这一节我们来通过源码看下上节课的问题所在。


## 编辑页面配置

    save_on_top = True
    fields = ('title', 'category')
    fields = (('category', 'title'), 'content')  # 布局
    exclude = ('owner',)

    fieldsets = (  # 跟fields互斥
        ('基础配置', {
            'fields': (('category', 'title'), 'content')
        }),
        ('高级配置', {
            'classes': ('collapse', 'addon'),
            'fields': ('tags', ),
        }),
    )
    filter_horizontal = ('tags', )
    filter_vertical = ('tags', )


## 自定义字段展示

增加编辑、删除操作：

    from django.utils.html import format_html

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
            )
    # operator.allow_tags = True  # 用format_html替代
    operator.show_description = '操作'
    operator.empty_value_display = '???'


## 自定义form

还是只针对postadmin来增加form, 在blog目录下增加文件（模块）adminforms.py  这里要命名为adminforms而不是forms，只为了跟前台针对用户输入进行处理的form区分开来。里面编写代码，定义form。关于form的作用，我们之前有讲到，form跟model其实是耦合在一起的，或者说form跟model的逻辑是一致的，model是对数据库中字段的抽象，form是对用户输入以及model中要展示数据的抽象。具体作用我们还是通过代码来看看。

我们通过form来定制下status这个字段的展示

    # adminforms.py
    from django import forms


    class PostAdminForm(forms.ModelForm):
        status = forms.BooleanField(label="是否删除", required=True)
        desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)


    # admin.py
    from .adminforms import PostAdminForm

    form = PostAdminForm


## 同时编辑外键和数据inline

我们有个需求，需要在分类页面直接编辑文章。当然这是个伪需求。因为这种内置(inline)的admin更适合的场景是针对字段较少的model，进行内联的操作。我们这里只是演示下它的用法。

    from django.contrib import admin

    class PostInline(admin.TabularInline):  # StackedInline  样式不同
        fields = ('title', 'desc')
        extra = 1  # 控制额外多几个
        model = Post


    class CategoryAdmin(admin.ModelAdmin):
        inlines = [PostInline, ]

## 重写form的clean_status方法

    def clean_status(self):
        if self.cleaned_data['status']:
            return 1
        else:
            return 3



## 重写admin的save_model方法

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)


## 参考
1. https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#customizing-the-adminsite-class
2. https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.html.format_html
