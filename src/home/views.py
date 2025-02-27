from django.shortcuts import render
from visits.models import PageVisit

def about_view(request, *args, **kwargs):
    return home_view(request, *args, **kwargs)

def home_view(request, *args, **kwargs):
    qs= PageVisit.objects.all()
    page_qs= PageVisit.objects.filter(path=request.path)
    my_title= "Hello Pial"
    html_template= "home.html"
    context= {"title": my_title, 
              "qs": qs.count(),
              "page_visits": page_qs.count(),
              "total_visits": qs.count(),
              "percent": (page_qs.count()*100)/qs.count(),
              }
    path=request.path

    PageVisit.objects.create(path=request.path)
    return render(request, html_template, context)

