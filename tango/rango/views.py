#-*-coding:utf-8-*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'Bağlamdan gelen ve kalın gözükecek mesaj burada'}
    return render_to_response('rango/about.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name = category_name)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)

def add_category(request):
    # İstemden bağlamı alıyor
    context = RequestContext(request)
    # method post olduğu durumda veriyi forma bağlıyor
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # gelen verinin geçerlilik sınamasını yapıyor
        if form.is_valid():
            # geçerli veriyi veritabanına kaydediyor ve 
            # index() işlevini, request nesnesini teslim 
            # ederek çalıştırıyor. 
            form.save(commit = True)
            return index(request)
        else:
            # form geçerlilik testi sonunda hatalar çıkarsa 
            # hataları konsola yazdırıyor. 
            print form.errors
    else:
        # request yönteminin post olmadığı durumlarda 
        # CategoryForm nesnesi bağlı olmayan bir form 
        # örneği olarak oluşturuluyor. 
        form = CategoryForm()
    return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit = False)
            try:
                cat = Category.objects.get(name = category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html', {'category_name_url': category_name_url, 'category_name': category_name, 'form': form}, context)

