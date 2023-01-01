from functools import reduce
from django.urls import path
from .views import *
from shop import views

urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('product/',Product_List.as_view(), name = 'productlist'),
    path('category_lists/<slug>',Category_list.as_view(), name = 'name'),
    path('Productdetail/<slug>',Product_Detail.as_view(), name = 'productdetail'),
    path('Productreview/<slug>',Productreview, name = "productreview"),
    path('search/',SearchView.as_view(), name = 'search'),
    path('cart/',CartView.as_view(), name = 'cart'),
    path('check/',Check.as_view(),name = "check"),
    path('setting/',setting, name = 'setting'),
    path('statement/', statment, name = "statement"),
    path('sdetail/',sdetail, name = "sdetail"),
    path('reduce/<slug>',reduce, name ='redcue'),
    path('addto/<slug>',add_to, name = 'addto'),
    path('delete/<slug>',delete, name = 'delete'),
    path('signup',signup,name = 'signup'),
    path('signin',signin,name = 'signin'),
    path('signout',signout, name='signout'),
    #path('change/<token>/',change, name='reset'),
    path('change/', change, name = "change"),
    path('reset/', reset, name = "reset"),
    #path('sucess/',sucess,name = "sucess"),
    #path('identity/',indentity, name = 'identity'),
    path('addlike/<slug>',addlike,name = "like"),
    path('like/',LikeView.as_view(),name = "like"),
    path('deletelike/<slug>',deletelike,name = "deletelike"),
    path('order/',views.order, name = "order"),
    path('show/',Show.as_view(), name = "show")
]
