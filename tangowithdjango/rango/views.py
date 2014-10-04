from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# import rango model

from rango.models import Category, Page

# import rango forms

from rango.forms import CategoryForms, PageForms, UserForm, UserProfileForm


def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {"categories": category_list}

    page_list = Page.objects.order_by("-views")[:5]

    context_dict["pages"] = page_list

    for category in category_list:
        category.url = category.name.replace(" ", "_")

    response =  render_to_response('rango/index.html', context_dict, context)
    visits = int(request.COOKIES.get('visits', '0'))
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).days > 0:
            response.set_cookie('visits', visits+1)
            response.set_cookie('last_visit', datetime.now())
    else:
        response.set_cookie('last_visit', datetime.now())
    return response
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

        context_dict['category_name_url'] = category_name_url
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
    print category_name_url+":"+category_name
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
        print("hello")
        form = PageForms()

    return render_to_response('rango/add_page.html',
            {'category_name_url':category_name_url,
              'category_name':category_name, 'form':form},
            context)

def register(request):

    context = RequestContext(request)
    registered =False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'rango/register.html',
            {'user_form':user_form,'profile_form':profile_form,
            'registered':registered}, context)

def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return render_to_response('/rango/',{},context)
            else:
                return HttpResponse('Your rango account is disabled')
        else:
            print('invalid login details {0}, {1}'.format(username, password))
            return HttpResponse("invalid login details supplied")

    else:
        return render_to_response('rango/login.html',{},context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


