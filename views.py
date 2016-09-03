import codecs
import json
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from blog.models import Article, OcProductDescription, OcProduct, OcCategory, OcCategoryDescription, OcProductImage, Product, DifferenceProduct
import urllib
import urllib2
import unidecode
import pytils
import re
from django.conf import settings
import os, sys, shutil


# Create your views here.

def all_product(request, page_number=1):
    #data = json.load(codecs.open('d:/Pyton/tutorialScrapy/scraped_items.json', 'r', 'utf-8-sig'))
    products = Product.objects.using('scrapy').all()
    current_page = Paginator(products, 10)
    context = {
        'products': current_page.page(page_number)
    }
    return render(request, 'blog/parse_list.html', context)


def show_product(request, id):
    #data = json.load(codecs.open('d:/Pyton/tutorialScrapy/scraped_items.json', 'r', 'utf-8-sig'))
    product = get_object_or_404(Product.objects.using('scrapy'), id=id)
    context = {
        'product': product
    }
    return render(request, 'blog/product.html', context)


def set_difference(request):
    #data = json.load(codecs.open('d:/Pyton/tutorialScrapy/scraped_items.json', 'r', 'utf-8-sig'))

    merchant_products = OcProduct.objects.using('shop').filter(status=1)
    merchant_names = set([product.name for product in merchant_products])

    parse_products = Product.objects.using('scrapy').all()
    parse_names = set([product.title for product in parse_products])

    difference_down = list(merchant_names - parse_names)
    difference_up = list(parse_names - merchant_names)

    #difference_products = [dict(name=product, is_parse=1) for product in list(difference_up)]
    #difference_products.extend([dict(name=product, is_parse=0) for product in list(difference_down)])

    #Product.objects.using('scrapy').bulk_create([Product() for product in difference_products])

    products_up = Product.objects.using('scrapy').filter(title__in=difference_up)

    #create_products = [DifferenceProduct(title=product.title, url=product.url, is_parse=1) for product in products_up]
    for product in products_up:
        difference_product = DifferenceProduct(title=product.title, url=product.url, is_parse=1)
        difference_product.save(using='scrapy')

    products_down = OcProduct.objects.using('shop').filter(name__in=difference_down)

    #create_products = [DifferenceProduct(title=product.name, is_parse=0) for product in products_down]
    #DifferenceProduct.objects.using('scrapy').bulk_create(create_products)
    for product in products_down:
        if product.name:
            difference_product = DifferenceProduct(title=product.name, is_parse=0)
            difference_product.save(using='scrapy')

    #return HttpResponse({}, content_type="application/json")
    return difference(request)


def difference(request, page_number=1):
    products = DifferenceProduct.objects.using('scrapy').all()
    current_page = Paginator(products, 10)
    context = {
        'difference_products': current_page.page(page_number)
    }
    return render(request, 'blog/difference_list.html', context)


def home(request):
    #articles = Article.objects.all()
    articles = OcCategory.objects.using('shop').filter(occategorydescription__language_id=1)
    context = {
        'articles': articles,
    }
    return render(request, 'blog/home.html', context)
    #response_data = serializers.serialize('json', articles)
    #return HttpResponse(response_data, content_type="application/json")


def show_merchant_product(request, product_id=0):
    product = get_object_or_404(OcProduct.objects.using('shop'), product_id=product_id)
    return render(request, 'blog/merchant_product.html', {'product': product})


def all_merchant_product(request, category_id=0):
    products = OcProduct.objects.using('shop').filter(ocproducttocategory__category=category_id)
    return render(request, 'blog/merchant_product_list.html', {'products': products})


def about(request):
    return render(request, 'blog/about.html', {'about': True})


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/article.html', {'article': article})


def all_category(request, page_number=1):
    data = json.load(codecs.open('d:/Pyton/tutorialScrapy/category.json', 'r', 'utf-8-sig'))
    current_page = Paginator(data, 10)
    context = {
        'categories': current_page.page(page_number)
    }
    return render(request, 'blog/category_list.html', context)


def parse(request):
    url = 'http://localhost:6800/schedule.json'
    values = {
        'project': 'tutorialScrapy',
        'spider': 'product'
    }
    run_spider(url, {'project': 'tutorialScrapy', 'spider': 'category'})
    result = run_spider(url, values)
    return HttpResponse(result, content_type="application/json")


def run_spider(url, values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = response.read()
    print result

    return result


def sync(request):
    data = json.load(codecs.open('d:/Pyton/tutorialScrapy/category.json', 'r', 'utf-8-sig'))
    img_dst = 'D:/OpenServer/domains/ocstore.local/image/catalog/images/'
    img_src = os.path.join(settings.BASE_DIR, 'blog/static/blog/images/')
    #data = data[17:18]
    for category_item in data:
        title = category_item.get('title')
        parent_category_title = category_item.get('main_category')

        parent_category = read_or_create(parent_category_title, 0, 1)
        category = read_or_create(title, parent_category.category_id, 0)


    #products = json.load(codecs.open('d:/Pyton/tutorialScrapy/scraped_items.json', 'r', 'utf-8-sig'))
    products = Product.objects.using('scrapy').all()
    #products = products[1:2]
    for product in products:
        title = product.title
        category = product.category
        description = product.description
        sku = product.sku
        cost_usd = product.cost_usd
        #cost_usd = re.findall("\d+\.\d+", cost_usd)[0]
        item_code = product.item_code
        #item_code = item_code[12:]

        images = json.loads(product.images)
        images = ['catalog/images/%s' % img['path'] for img in images]

        category = OcCategory.objects.using('shop').get(occategorydescription__name=category)
        product = OcProduct(
            model=item_code,
            name=title,
            sku=sku,
            quantity=2,
            stock_status_id=5,
            image=images.pop(0),
            price=cost_usd,
            tax_class_id=9,
            length_class_id=1,
            minimum=1,
            status=1
        )
        product.save(using='shop')
        product.ocproductdescription_set.create(
            language_id=1,
            name=title.replace('\"', '&quot;'),
            meta_title=title.replace('\"', '&quot;'),
            description=description.replace('\n', '&lt;p&gt;'),
        )
        product.ocproductdescription_set.create(
            language_id=2,
            name=title.replace('\"', '&quot;'),
            meta_title=title.replace('\"', '&quot;'),
            description=description.replace('\n', '&lt;p&gt;'),
        )
        product.ocproducttocategory_set.create(category=category)
        product.ocproducttostore_set.create(store_id=0)
        #for image in images.itervalues():
            #product.ocproductimage_set.create(image='catalg/images/' + image)

        product.ocproductimage_set.bulk_create([OcProductImage(image=img, product=product) for img in images])

    #copy_imgs(img_src, img_dst)

    return HttpResponse(data, content_type="application/json")


def read_or_create(title, parent_category_id, top):
    try:
        category_desc = OcCategoryDescription.objects.using('shop').get(name=title)
        category = OcCategory.objects.using('shop').get(category_id=category_desc.category_id)
    except OcCategoryDescription.DoesNotExist:
        category = OcCategory(status=1, parent_id=parent_category_id, top=top)
        category.save(using='shop')
        category.occategorydescription_set.create(language_id=1, name=title)
        category.occategorydescription_set.create(language_id=2, name=pytils.translit.translify(title))
        category.occategorytostore_set.create(store_id=0)

        if parent_category_id:
            category.occategorypath_set.create(path_id=parent_category_id)
            category.occategorypath_set.create(path_id=category.category_id, level=1)
        else:
            category.occategorypath_set.create(path_id=category.category_id)
    return category


def copy_imgs(src, dst):
    print ("copy tree " + src)
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                shutil.copytree(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error):
            print "Can't copy %s to %s" % (srcname, dstname)


#def read_or_create():

