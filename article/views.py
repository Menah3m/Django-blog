from django.shortcuts import render,redirect
from .models import ArticlePost
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import markdown
from django.db.models import Q
from comment.models import Comment

# 视图函数，用于从url映射文章列表
def article_list(request):
    # 根据GET请求中查询条件返回对应顺序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            # 用Q对象进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()


    # 每页显示1篇文章
    paginator = Paginator(article_list, 1)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给template的对象
    context = {'articles': articles, 'order': order, 'search':search}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc':md.toc ,'comments':comments }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中id=1的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form':article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新tittle，body字段
    GET方法进入初始表单页面
    id：文章的id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为POST提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改的文章中。需要传入文章的id值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户GET请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以提取旧的内容
        context = {'article':article,'article_post_form':article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


