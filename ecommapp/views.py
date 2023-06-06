from django.shortcuts import render,redirect
from django.http import HttpResponse
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
from ecommapp.forms import EmpForm,ProductModelForm,UserForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
import random
import razorpay,uuid
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.db import transaction


# Create your views here.

def home (request):
    #data=Product.objects.all() #select * from ecommapp_products;
    #print(data)
    data=Product.objects.filter(status=1) # type: ignore
    content={}
    content['products']=data
    return render (request,'index.html',content)

def delete (request,rid):
    print("ID to be deleted",rid)
    return HttpResponse("Id to be deleted:"+rid)

def addition(request,x,y):
    z=int(x)+int(y)
    print('Addition is:',z)
    return HttpResponse("Addition of numbers is:"+str(z)) # type: ignore

#def user_register(request):
    #return render(request,'register.html')

#def user_login(request):
    #return render(request,'login.html')

def edit(request,rid):
    print("ID to be edited",rid)
    return HttpResponse("Id to be edited:"+rid)


def product_list(request):

    context={}
    context['name']='Samsung'
    context['x']=100
    context['y']=200
    context['data']=[10,20,30,40]
    #context['plist']=['Samsung','Iphone','Nokia','Oppo']

    context['plist']=[
        {'name':'Samsung','pimage':'image of samsung','price':30000,'desc':'Product description'},
        {'name':'iphone','pimage':'image of iphone','price':85000,'desc':'Product description'},
        {'name':'Vivo','pimage':'image of vivo','price':35000,'desc':'Product description'},


    ]
    return render(request,'productlist.html',context)


def reuse(request):
    return render(request,'base.html')

#def login(request):
    #return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def productlist (request):
    return render(request,'productlist.html')

#Sorting start
def sorting(request,sv):
    if sv=='0':
        param='price'
    else:
       param='-price'

    data=Product.objects.order_by(param).filter(status=1) # type: ignore
    content={}
    content['products']=data
    return render(request, 'index.html',content)


def catfilter(request,catv):
    q1=Q(cat=catv)
    q2=Q(status=1)
    data=Product.objects.filter(q1 & q2) # type: ignore
    content={}
    content['products']=data
    return render(request, 'index.html',content)

def pricefilter(request,pv):
    q1=Q(status=1)
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)

    data=Product.objects.filter(q1 & q2) # type: ignore
    content={}
    content['products']=data
    return render(request, 'index.html',content)

def pricerange(request):

    low=request.GET['min']
    high=request.GET['max']
    #print(low)
    #print(high)
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)
    data=Product.objects.filter(q1 & q2 & q3) # type: ignore
    content={}
    content['products']=data
    return render(request, 'index.html',content)


def product_details(request,pid):
    #print("Id is",pid)
    data=Product.objects.filter(id=pid) # type: ignore
    content={}
    content['products']=data
    return render(request,'product_details.html',content)

def addproduct(request):
    print('The method is:',request.method)
    if request.method=='POST':
        print("Insert Record into database")
        #insert record into database product
        n=request.POST['pname']
        c=request.POST['pcat']
        amt=request.POST['pprice']
        s=request.POST['status']
        #print(n)
        #print(cat)
        #print(amt)
        #print(s)
        p=Product.objects.create(name=n,cat=c,price=amt,status=s) # type: ignore
        p.save()
        return redirect('/addproduct')
    
    else:
        print('In else part')
        p=Product.objects.all() # type: ignore
        #print(p)
        content={}
        content['products']=p
        return render(request,'addproduct.html',content)
    
def delproduct(request,rid):
    #print("ID to be deleted:",rid)
    #fetch record to be deleted
    p=Product.objects.filter(id=rid) # type: ignore
    p.delete()
    return redirect('/addproduct')

def editproduct(request,rid):
    if request.method=="POST":
        upname=request.POST['pname']
        ucat=request.POST['pcat']
        uprice=request.POST['pprice']
        ustatus=request.POST['status']

        #print(upname)
        p=Product.objects.filter(id=rid)
        p.update(name=upname,cat=ucat,price=uprice,status=ustatus)
        return redirect('/addproduct')

        
    else:
        p=Product.objects.filter(id=rid)
        content={}
        content['products']=p
        return render(request,'editproduct.html',content)
    

def djangoform(request):
    if request.method=="POST":
        ename=request.POST['name']
        dept=request.POST['dept']
        email=request.POST['email']
        esal=request.POST['salary']
        print("Employee Name:",ename)
        print("Dept Name:",dept)

    else:
        eobj=EmpForm()
        #print(eobj)
        content={}
        content['form']=eobj
        return render(request,'djangoform.html',content)


def modelform(request):
    if request.method=="POST":
        pass

    else:
        pobj=ProductModelForm()
        #print(pobj)
        content={}
        content['mform']=pobj
        return render(request,'modelform.html',content)
    
def user_register(request):
    regobj=UserForm()
    content={}
    content['userform']=regobj
    
    if request.method=="POST":
        regobj=UserForm(request.POST)
        if regobj.is_valid():
            regobj.save()
            content['success']="User Created Successfully"
            return render (request,'user_register.html',content)

    else:
        #regobj=UserCreationForm
        #print(regobj)
        return render (request,'user_register.html',content)
    

def user_login(request):
    if request.method=="POST":
        dataobj=AuthenticationForm(request=request,data=request.POST)
        #print(dataobj)
        if dataobj.is_valid():
            uname=dataobj.cleaned_data['username']
            upass=dataobj.cleaned_data['password']
            #print('Username:',uname)
            #print('Password:',upass)
            u=authenticate(username=uname,password=upass)
            if u:
                login(request,u)
                return redirect("/")

    else:
        uobj=AuthenticationForm()
        content={}
        content['loginform']=uobj
        return render (request,'user_login.html',content)
    

def setsession(request):
    request.session['name']='ITV'
    return render(request,'setsession.html')

def getsession(request):
    content={}
    content['data']=request.session['name']
    return render(request,'getsession.html',content)

def addtocart(request,pid):
    if request.user.is_authenticated:
       userid=request.user.id
       q1=Q(pid=pid)
       q2=Q(uid=userid)
       c=Cart.objects.filter(q1 & q2)
       p=Product.objects.filter(id=pid)
       content={}
       content['products']=p
       if c:
           content['msg']="Product Already exist in cart"
           return render (request,'product_details.html',content)

       else:
           #print("user id :",uid)
           u=User.objects.filter(id=userid)
           c=Cart.objects.create(uid=u[0],pid=p[0])
           c.save()
           content['success']='Product Added in cart'
           return render (request,'product_details.html',content)
    else:  
         return redirect('/login')
   
    
    
def user_logout(request):
    logout(request)
    return redirect('/login')


def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    #print(c[0])
    #print(c[0].pid)
    #print(c[0].uid)
    sum=0
    for x in c:
        #print(type(x.qty))
        #print(x.pid.price)
        sum=sum+(x.qty*x.pid.price)
        print("Total Product Price:",sum)
    content={}
    content['products']=c
    content['nitems']=len(c)
    content['total']=sum
    return render(request,'viewcart.html',content)


def changeqty(request,pid,f):
    content={}
    c=Cart.objects.filter(pid=pid)
    if f=='1':
        x=c[0].qty+1
    else:
        x=c[0].qty-1

    if x>0:
        c.update(qty=x)
        
    return redirect('/viewcart')


def placeorder(request):
    oid=random.randrange(1000,9999)
    #print(oid)
    user_id=request.user.id
    c=Cart.objects.filter(uid=user_id)
    #print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
        
    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)

    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum

    return render(request,'placeorder.html',content)


def makepayment(request):
    userid=request.user.id
    client = razorpay.Client(auth=("rzp_test_uJJpkZ8hkrGR1W","EJPtetoESQopJBPXmqba0Jnp"))
    o=Order.objects.filter(uid=userid)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    sum=sum*100
    oid=str(o[0].id) # type: ignore
    data = {"amount":sum, "currency":"INR", "receipt":oid} 
    payment = client.order.create(data=data)  # type: ignore
    print(payment)
    content={}
    content['payment']=payment

    return render(request,'pay.html',content)


def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id
    u=User.objects.filter(id=userid)
    #print(pay_id)
    #print(order_id)
    email=u[0].email
    msg='Order placed successfully.\n'  'Details are Payment ID:'+pay_id+"\nand order id is:"+order_id
    send_mail(
    "E-Kart Order Status",
    msg,
    settings.EMAIL_HOST_USER,
    ["rvm.scop@gmail.com"],
    fail_silently=False,
    )

    return render(request,'final.html')


