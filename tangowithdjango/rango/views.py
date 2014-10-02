from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse



# import rango model

from rango.models import Category, Page

# import rango forms

from rango.forms import CategoryForms, PageForms


def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {"categories": category_list}

    page_list = Page.objects.order_by("-views")[:5]

    context_dict["pages"] = page_list

    for category in category_list:
        category.url = category.name.replace(" ", "_")

    return render_to_response('rango/index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    context_dict = {"boldmessage": " i am bold font from the context"}

    return render_to_response('rango/about.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    context_dict = {'category_name': category_name}

    try:

        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)

        context_dict['category_name_url'] = category.name
        context_dict['pages'] = pages

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)


def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        print "hello this is post"
        form = CategoryForms(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            print form.errors
    else:
        form = CategoryForms()

    return render_to_response('rango/add_category.html', {'form': form}, context)


def decode_url(category_name_url):
    """

    :rtype : object
    """
    category_name = category_name_url.replace('_', ' ')
    return category_name


def add_page(request,category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForms(request.POST)

        if form.is_valid:
            page = form.save(commit = False)
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html',{},context)

            page.views = 0

            page.save()

            return category(request,category_name_url)
        else:
            print form.errors

    else:
        form = PageForms()

    return render_to_response('rango/add_page.html',
            {'category_name_url':category_name_url,
              'category_name':category_name, 'form':form},
            context)
