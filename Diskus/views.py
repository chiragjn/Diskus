from django.shortcuts import render,Http404
from django.views.defaults import page_not_found
from Diskus.models import *
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def home(request):
    context_dict = {}
    categories = Category.objects.annotate(num_threads=Count('thread')).order_by('-num_threads')
    context_dict['categories'] = categories
    top_threads = {}
    for category in categories:
        top_threads[str(category.pk)] = [[thread ,str(thread.post_set.count() - 1)] for thread in Thread.objects.filter(category=category).order_by('-last_modified')[:2]]
    context_dict['top_threads'] = top_threads
    return render(request, 'home.html', context_dict)


def getAllCategoryThreads(request, slug):
    context_dict = {}
    category = Category.objects.filter(slug=slug)
    if category:
        page = request.GET.get('page')
        context_dict['categories'] = category
        threads = Thread.objects.filter(category=category).order_by('-last_modified')
        paginator = Paginator(threads, 15) # Show 25 contacts per page
        try:
            threads = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            threads = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            threads = paginator.page(paginator.num_pages)
        context_dict['threads'] = [[thread,str(thread.post_set.count() - 1)] for thread in threads]
        context_dict['paginated_threads'] = threads
    else:
        return page_not_found(request)
    return render(request,'category.html',context_dict)