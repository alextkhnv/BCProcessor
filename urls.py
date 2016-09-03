
from django.conf.urls import url

from blog.views import (home, about, show_article, show_product, parse, all_category, difference, set_difference,
                        all_product, show_merchant_product, all_merchant_product, sync)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^all_merchant_product/(\d+)/$', all_merchant_product, name='all_merchant_product'),
    url(r'^show_merchant_product/(\d+)/$', show_merchant_product, name='show_merchant_product'),
    url(r'^about/$', about, name='about'),
    url(r'^articles/(?P<article_id>[0-9]+)/$', show_article, name='article'),
    url(r'^show_product/(?P<id>[0-9]+)/$', show_product, name='show_product'),
    url(r'^all_product/$', all_product, name='all_product'),
    url(r'^all_product/page/(\d+)/$', all_product, name='all_product_page'),
    url(r'^difference/$', difference, name='difference'),
    url(r'^difference/page/(\d+)/$', difference, name='difference_page'),
    url(r'^all_category/$', all_category, name='all_category'),
    url(r'^all_category/page/(\d+)/$', all_category, name='all_category_page'),
    url(r'^parse$', parse, name='parse'),
    url(r'^sync$', sync, name='sync'),
    url(r'^set_difference$', set_difference, name='set_difference'),
]
