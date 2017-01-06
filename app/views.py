from django.views.generic import ListView,DeleteView
from django.views.generic.edit import FormView
from models import Article,Category,Tag,BlogComment
import markdown2
from django.shortcuts import get_object_or_404,HttpResponseRedirect,render
from .forms import BlogCommentForm

class IndexView(ListView):
    template_name = "lw-index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(IndexView,self).get_context_data(**kwargs)

class ArticleDetailView(DeleteView):
    model = Article
    template_name = "app/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body)
        return obj
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = "app/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['category_id'],status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView,self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = 'app/index.html'
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'],status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body)
        return  article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(TagView,self).get_context_data(**kwargs)


class ArchiveView(ListView):
    template_name = 'app/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year,created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return  super(ArchiveView,self).get_context_data(**kwargs)

class CommentPostView(FormView):
    form_class = BlogComment
    template_name = 'app/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.artcle = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return  render(self.request,'app/detail.html',{
            'form':form,
            'artcle': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })

