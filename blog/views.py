from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Post , Category
from taggit.models import Tag
from django.db.models import Count
from django.db.models.query_utils import Q




class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 2
    def get_queryset(self) :
        name = self.request.GET.get('q','')
        object_list = Post.objects.filter(
            Q(title__icontains = name) |
            Q(description__icontains = name)
        )
        return object_list

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().annotate(post_count=Count('post_category'))
        context["tags"] = Tag.objects.all()
        context["recent_posts"] = Post.objects.all()[:3]
        return context