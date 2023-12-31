from django.conf import settings
from django.shortcuts import render
from .models import About , Resume , Services ,CategoryService, MySkills
from projects.models import Projects
from blog.models import Post
from django.core.mail import send_mail
from django.views.generic import  ListView, DetailView
from django.db.models.query_utils import Q
from django.db.models import Count




# Create your views here.

def home(request):
    about = About.objects.last()
    project_count = Projects.objects.all().count() 
    awards = project_count+2
    Cups_of_coffee = project_count*60
    resume = Resume.objects.all()
    service = Services.objects.all()
    recent_project = Projects.objects.all().order_by('-created_at')[:6]
    recent_blog = Post.objects.all().order_by('-created_at')[:3]
    skills = MySkills.objects.all()




    return render(request,'home.html', {
        'about':about  , 
        'project_count':project_count,
        'resume':resume ,
        'service':service,
        'recent_project':recent_project,
        'recent_blog':recent_blog,
        'awards':awards,
        'Cups_of_coffee':Cups_of_coffee,
        'skills':skills
    })


class ServiceList(ListView):
    model = Services
    def get_queryset(self) :
        name = self.request.GET.get('q','')
        service_list = Services.objects.filter(
                Q(name__icontains = name) |
                Q(description__icontains = name)
            )
        return service_list

class ServiceDetail(DetailView):
    model = Services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryService.objects.all().annotate(service_count=Count('service_category'))
        context["other_services"] = Services.objects.all().order_by('-created_at')[:4]
        return context
    
class ServiceByCategory(ListView):
    model = Services

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Services.objects.filter(
            Q(category__name__icontains = slug)
        )
        return object_list