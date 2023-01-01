# Create your views here.
# from cProfile import Profile
# from email import message
# import email
# from multiprocessing import context
# from re import L
# from sre_parse import State
# from unicodedata import name
# from urllib import request
from django.db.models import Count
from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from .help import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.db.models import Sum
# from Ecom import settings
# from django.core.mail import send_mail
from .help import sendmail
import uuid
import random
# Create your views here.
class Base(View):
    context = {}
    # context['brands']=Brand.objects.all()
    brand_count = []
    # users = User.objects.all().count()
    # context={'users':users}
    for i in Brand.objects.all():
         ids = Brand.objects.get(name = i).id
         print(ids)
         product = Product.objects.filter(brand = ids).count()
         brand_count.append({'ids':ids,'product_count':product})
    context['counts'] = brand_count

    def get(request):
        context = {}
        username = request.user.username
        like_count = Like.objects.get(username = username).count()
        add_tocart = Cart.objects.get(username = username).coun()
        count = []
        count.append({'like_count': like_count,'add_tocart':add_tocart })
        context['counting'] = count


class Index(Base):
    def get(self,request):
        username = request.user.username
        self.context['categorys'] = Category.objects.all()
        self.context['sliders'] = Slider.objects.all()
        self.context['hots'] = Product.objects.filter(label = 'hot')
        self.context['news'] = Product.objects.filter(label = 'new')
        self.context['sales'] = Product.objects.filter(label = 'sale')
        self.context['reviews'] = Review.objects.all()
        self.context['services'] = Service.objects.all()
        self.context['ads'] = Ads.objects.all()
        self.context['brands'] = Brand.objects.all()
        self.context['use']=User.objects.filter(username = username)
        return render(request,'index.html',self.context)

#-------------------------------------Category-------------------------
class Category_list(Base):
    def get(self,request,slug): 
        ids = Category.objects.get(slug = slug).id
        self.context['cata_pro'] = Product.objects.filter(category_id = ids)
        return render(request,'category_list.html',self.context)

#--------------------------------------Product list =------------------
class Product_List(Base):
    def get(self,request):
        self.context['products'] = Product.objects.all()
        return render(request,'product-list.html',self.context) 

#-----------------------------------------Product_Detail----------------
class Product_Detail(Base):
    def get(self,request,slug):
        self.context['Pro_detail'] = Product.objects.filter(slug = slug)
        self.context['comments'] = Comment.objects.filter(slug = slug)
        return render(request,'product-detail.html',self.context)

def Productreview(request,slug):
    username = request.user.username
    if request.method == 'POST':
        review = request.POST['comments'] 
        rate = request.POST['rate']
        rdata = Comment.objects.create(
            username = username,
            slug = slug,
            Comment = review,
            rate = rate
        )
        rdata.save()
        return redirect(f'/Productdetail/{slug}')
    return redirect(f'/Productdetail/{slug}')

#..................................................Search field..................
class SearchView(Base):
    def get(self,request):
        if request.method == 'GET':
            query = request.GET['querys']
            if query is not None:
                self.context['searches'] = Product.objects.filter(name__icontains = query)
            else:
                return redirect('/')
        
        return render(request,'search.html',self.context)
#---------------------------------------------------Signup/register----------------------------------
def signup(request):
    username = request.user.username
    if request.method =='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mail = request.POST['email']
        pword = request.POST['pass1']
        rpword = request.POST['pass2']
        if pword == rpword: 
            if User.objects.filter(username = username).exists():
                messages.error(request,'This user name already taken')
                return redirect('/signup')
            elif User.objects.filter(email = mail).exists():
                messages.error(request,'this email is already taken')
                return redirect('/signup')
            else:
              
                users = User.objects.create_user(
                    first_name = fname,
                    last_name = lname,
                    username = username,
                    email = mail,
                    password = pword,
                )
                users.save()
                sendmail(users.email,users.first_name)
        else:
            messages.error(request,'The password do not match')
            return redirect('/signup')
        return redirect("/signin")
    return render(request,'register.html')
#------------------------------------------------------------Login/signin------------------------------------------
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
        else:
            messages.error(request,"bad credentilas ")
            return redirect("/signin")
        return redirect("/")
    return render(request,'authentication/login.html')

    # it was done in the main project urls file
#-----------------------------------------------------------------------LIKE--------------------------------------- 
class LikeView(Base):
    def get(self,request):
        username = request.user.username
        self.context['likes'] = Like.objects.filter(username = username)
        return render(request,'like.html',self.context)
    
def addlike(request,slug):
    username = request.user.username
    if Like.objects.filter(slug = slug,username = username).exists():
         return redirect("/like/")
    if not Cart.objects.filter(slug = slug,username = username ).exists():
        price = Product.objects.get(slug = slug).price
        discount_price = Product.objects.get(slug = slug).discount_price
        if discount_price > 0:
            original_price = discount_price
        else:
            original_price = price
        like_add = Like.objects.create(
            username = username,
            total = original_price,
            slug = slug,
            items = Product.objects.get(slug = slug)
        )
        like_add.save()
    return redirect('/like/')

def deletelike(request,slug):
    username = request.user.username
    if Like.objects.filter(username = username, slug=slug).delete():
        return redirect("/like/")

#---------------------------------------------------------Checkout----------------------------------------------
class Check(Base):
    def get(self,request):
        username = request.user.username
        self.context['cartitem'] = Cart.objects.filter(username = username)
        self.context['checkview'] = CheckOut.objects.filter(username = username)
        user_cart = Cart.objects.filter(username = request.user.username)
        grand_total = 0
        for item in user_cart:
            grand_total += item.total
        # ids = Cart.objects.filter(username = request.user.username).id
        # user_cart_add = Cart.objects.filter(ids = id)
        # cart_obj = user_cart_add.create(
        #     grandtotal = grand_total
        # )
        # cart_obj.save()
        self.context['grand_total'] = grand_total

        return render(request,"checkout.html",self.context)

def order(request): 
    username = request.user.username
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        city = request.POST['city']
        zip_c = request.POST['zip_code']
        state = request.POST['state']
        country = request.POST['country']
        address = request.POST['address']
        email = request.POST['email']
        order_data = CheckOut.objects.create(
            username = username,
            first_name = fname,
            last_name = lname,
            country =country,
            email = email,
            address = address,
            state = state,
            city = city,
            zip_code = zip_c,
            phone = phone
        )
        order_data.save()
    #messages.success(request,"Your order is successfully placed")
    return redirect('/show/')
class Show(Base):
    def get(self,request):
        username = request.user.username
        self.context ['cartitem']=Cart.objects.filter(username = username)
        self.context ['info']=CheckOut.objects.filter(username = username)
        return render(request,"order.html",self.context)
#------------------------------------------------------------Cart-----------------------------------------------
class CartView(Base):
    def get(self,request):
        username = request.user.username
        print(username)
        self.context['my_cart'] = Cart.objects.filter(username = username )
        return render(request,'cart.html',self.context)

def add_to(request,slug):
    username = request.user.username
    if Product.objects.filter(slug = slug ).exists():
        if Cart.objects.filter(slug = slug, username = username, checkout = False).exists():
            price = Product.objects.get(slug = slug).price
            quentity = Cart.objects.get(slug = slug, username = username, checkout = False).quentity
            discount_price = Product.objects.get( slug = slug).discount_price
            grand_price = Cart.objects.get( slug = slug).grandtotal
            if discount_price > 0 :
                original_price = discount_price
            else:
                original_price= price
            quentity = quentity + 1   
            total_price = original_price * quentity
            #grand_price = grand_price + total_price 
            Cart.objects.filter(slug = slug, username = username, checkout = False ).update(total = total_price, quentity = quentity)
            return redirect('/cart')
        else:
            price = Product.objects.get(slug = slug).price
            discount_price = Product.objects.get(slug = slug).discount_price
            if discount_price > 0:
                original_price = discount_price
            else:
                original_price = price
            carts = Cart.objects.create(
                username = username,
                total = original_price,
                slug = slug,
                items = Product.objects.filter(slug = slug)[0]
            )
            carts.save()
            # grand = 0
            # for i in Cart.objects.get(username = username):
            #     grand = grand + i.total
            # cart_total = Cart.objects.create(
            #     grandtotal = grand
            # )
            # cart_total.save()
        return redirect('/cart/')
    return redirect('cart/')

def reduce(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug = slug, username= username, checkout = False).exists():
        price = Product.objects.get(slug = slug).price
        discount_price = Product.objects.get(slug = slug).discount_price
        quentity = Cart.objects.get(slug = slug, username = username, checkout = False).quentity
        if discount_price > 0:
            original_price = discount_price
        else:
            original_price = price
        quentity = quentity - 1
        if quentity == 0:
            Cart.objects.filter(slug = slug, username = username, checkout = False).delete()
        total_price = original_price * quentity
        Cart.objects.filter(slug =slug, username = username, checkout = False ).update(total = total_price,quentity =quentity)
        return redirect('/cart/')

def delete(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug = slug, username = username, checkout = False).delete():
        return redirect('/cart/')  
        

#----------------------------------------------------------Setting---------------------------------------------
def setting(request):
    return render (request,'setting.html')
    #from django.contrib.auth.models import User
def statment(request):
    username = request.user.username
    statements = CheckOut.objects.filter(username = username)
    context = {'statements' : statements}
    return render(request,"statement.html",context)

def sdetail(request):
    username = request.user.username
    state = CheckOut.objects.get(username = username)
    context = {'state':state}
    return render(request,"sdetail.html",context)

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         firstname = request.POST['fname']
#         lastname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']

#         myuser = User.objects.create(
#         username = username,
#         email = email,
#         password = pass1,
#         first_name = firstname,
#         last_name = lastname
#         )
#         myuser.save()
#         messages.success(request,"your accout is succesfully created")
#         return redirect ('/signin')

#     return render(request,'register.html')

def signout(request):
    logout(request)
    return redirect ("/")

#--------------------------------------------------Identity-------------------------------------
# def indentity(request):
#     try:
#         if request.method == "POST":
#             uname = request.POST['username']
#             if not User.objects.filter(username = uname).first():
#                 messages.error(request,"No such user is found")
#                 return redirect('/identity/') 
#             # email = User.objects.get(username = uname).email 
#             # token = str(uuid.uuid4())
#             # pro_obj = Profile.objects.filter(user = user_obj)
#             # pro_obj.forget_password_token = token
#             # pro_obj.save()
#             # email = user_obj.email
#             # forgetpassword( email, token)
#             # messages.error(request,"an email has been sent")
#             # pro_obj = Profile.objects.get(user = User.objects.get(username = uname))
#             # pro_obj.forget_password_token = token
#             # pro_obj.save()
#             return redirect('/change/')

#     except Exception as e:
#         print(e)
#     return render(request,"authentication/identity.html")

#.......................................................Change..........................................
def change(request):
    try:
        username = request.user.username
        if request.method == "POST":
            password = request.POST['pass1']
            password_con = request.POST['pass2']
            if password != password_con :
                messages.error(request,"Password do not matches")
                return redirect('/change/')
            else:
                user_obj = User.objects.get(username = username )
                user_obj.set_password(password)
                user_obj.save()
                return redirect('/')
    except Exception as e:
        print(e)
    return render(request,"authentication/change.html")

def reset(request):
    try:
        if request.method == "POST":
            username = request.POST['name']
            password = request.POST['pass1']
            password_con = request.POST['pass2']
            if password != password_con :
                messages.error(request,"Password do not matches")
                return redirect('/change/')
            else:
                user_obj = User.objects.get(username = username )
                user_obj.set_password(password)
                user_obj.save()
                return redirect('/signin')
    except Exception as e:
        print(e)
    return render(request,"authentication/reset.html")