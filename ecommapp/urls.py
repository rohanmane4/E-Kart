

from django.urls import path
from ecommapp import views

urlpatterns = [
    path('',views.home),
    #path('login',views.login),
    path('contact',views.contact),
    path('about',views.about),
    path('base',views.reuse),
    path('index.html',views.home),
    path('productlist',views.productlist),
    path('sort/<sv>',views.sorting), # type: ignore
    path('catfilter/<catv>',views.catfilter),
    path('pricefilter/<pv>',views.pricefilter),
    path('pricerange',views.pricerange), # type: ignore
    path('pdetails/<pid>',views.product_details),
    path('addproduct',views.addproduct),
    path('delproduct/<rid>',views.delproduct),
    path('editproduct/<rid>',views.editproduct),
    path('djangoform',views.djangoform), # type: ignore
    path('modelform',views.modelform), # type: ignore
    path('user_register',views.user_register), # type: ignore
    path('login',views.user_login), # type: ignore
    path('setsession',views.setsession),
    path('getsession',views.getsession),
    path('cart/<pid>',views.addtocart), 
    path('logout',views.user_logout),
    path('viewcart',views.viewcart),
    path('changeqty/<pid>/<f>',views.changeqty),
    path('placeorder',views.placeorder), 
    path('payment',views.makepayment),
    path('store',views.storedetails),
]