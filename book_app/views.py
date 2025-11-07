#Use of HttpResponse to print response in web page
import random
import razorpay, time
from django.shortcuts import render,HttpResponse,redirect
from django.views import View # Class base view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import book,cart,order,Contact
from django.db.models import Q
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings


# Create your views here.

def home(request):
    context={}
    p = book.objects.filter(is_active=True)
    context['book']=p
    #print(p)
    return render(request,"index.html",context)

def books(request):
    context={}
    p = book.objects.filter(is_active=True)
    context['book']=p
    #print(p)
    return render(request,"books.html",context)

def bdetails(request,pid):
    p=book.objects.filter(id=pid)
    context={}
    context['book']=p
    return render(request, "book_detail.html",context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="Field Cannot be empty"
            return render(request, 'register.html', context)
        
        elif upass!=ucpass:
            context={}
            context['errmsg']="Password did not match"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass)
                u.save()
                context={}
                context['success']="User Created Successfully"
                return render(request,'register.html',context)
            
            except Exception:
                context={}
                context['errmsg']="Username already Exists"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
        

def user_login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context={}
            context['errmsg']="Field Cannot be empty"
            return render(request, 'login.html', context)
        else:
            u=authenticate(username=uname, password=upass)
            if u is not None:           #USER NAME & PASS IS NOT NULL
                login(request,u)
                return redirect('/')
            else:
                context={}
                context['errmsg']='Invalid Username or Password'
                return render(request,"login.html",context)
        
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

#9/1/24
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=book.objects.filter(q1&q2)
    context={}
    context['book']=p
    return render(request, 'books.html', context)

def sort(request,sv):
    if sv == '0':
        col = 'price' #asc
        
    else:
        col = '-price' #dec
        
    p=book.objects.order_by(col)
    context={}
    context['book']=p
    return render(request, 'books.html', context)

def range(request):
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    
    q = Q(is_active=True)
    
    if min_price:
        q &= Q(price__gte=min_price)
    
    if max_price:
        q &= Q(price__lte=max_price)
        
    p = book.objects.filter(q)
    context = {'book': p}
    return render(request, 'books.html', context)

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        context={}
        context['success']="Your Query is Submited Successfully"
    return render(request,"contact.html", context)

def addtocart(request,pid):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    print(u[0])
    p=book.objects.filter(id=pid)
    print(p[0])
    q1 = Q(uid = u[0])
    q2 = Q(pid = p[0])
    c = cart.objects.filter(q1 and q2)
    n = len(c)
    print(n)
    context = {}
    context['book'] = p
    
    if n == 1:
        context['msg'] = "Product Already exists in the cart"
    else:
        c=cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        context['success']="Book Added Successfully"
    #print(pid)
    #print(userid)
    #return HttpResponse("Id is fetched")
    return render(request, 'book_detail.html', context)



def viewcart(request):
    if request.user.is_authenticated:
        c = cart.objects.filter(uid = request.user.id)
        # print(c)
        # print(c[0].uid)
        # print(c[0].pid.name)
        # print(c[1].pid.name)
        # print(c[0].uid.is_superuser)
        # print(len(c))
        np = len(c)
        s = 0
        for x in c:
            # print(x)
            # print(x.pid.price)
            s = s + (x.pid.price * x.qty)
        print(s)
        context = {}
        context['book'] = c
        context['totalprice'] = s
        context['totalitem'] = np
        return render(request, 'cart.html', context)
    else:
        return redirect('/login')
    
def remove(request, cid):
    c = cart.objects.filter(id = cid)
    c.delete()
    return redirect('/viewcart')


def updateqty(request, qv, cid):
    c = cart.objects.filter(id = cid)
    # print(c[0].pid)
    # print(c[0].qty)
    
    if qv == "1":
      newqty  = c[0].qty + 1
      c.update(qty = newqty)
    else:
        if c[0].qty > 1:
            newqty = c[0].qty - 1
            c.update(qty = newqty)
    return redirect('/viewcart')


def placeorder(request):
    userid = request.user.id
    c = cart.objects.filter(uid=userid)
    oid = random.randrange(1000, 9999)

    for x in c:
        order.objects.create(orderid=oid, pid=x.pid, uid=x.uid, qty=x.qty)

    np = len(c)
    s = sum(item.pid.price * item.qty for item in c)

    context = {
        'book': c,
        'totalprice': s,
        'totalitem': np,
    }
    return render(request, 'placeorder.html', context)


def makepayment(request):
    """
    Compute total from cart items, convert to paise, create single Razorpay order,
    and render pay.html with the razorpay order dict in context (orders).
    """
    # Use your cart model name — file used 'cart' in repo
    cart_items = cart.objects.filter(uid=request.user.id)
    if not cart_items.exists():
        # nothing to pay for
        return redirect('cart')   # change target if your cart url name different

    # compute total safely using Decimal
    total_inr = Decimal('0.00')
    for item in cart_items:
        # assume item.pid.price exists and is numeric
        price = Decimal(item.pid.price)
        qty = int(item.qty)
        total_inr += (price * qty)

    # convert to paise (Razorpay expects integer paise)
    paise_amount = int((total_inr * Decimal('100')).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    # create razorpay client using settings (don't hardcode keys)
    client = razorpay.Client(auth=(getattr(settings, 'RZP_KEY_ID', ''), getattr(settings, 'RZP_KEY_SECRET', '')))

    # unique receipt per attempt
    receipt = f"rcpt_{request.user.id}_{int(time.time())}"

    DATA = {
        "amount": paise_amount,
        "currency": "INR",
        "receipt": receipt,
        "notes": {"user": request.user.username}
    }

    # Create razorpay order ONCE
    payment = client.order.create(data=DATA)

    # Optionally: log payment or create a PaymentAttempt record here
    # Example: PaymentAttempt.objects.create(user=request.user, rzp_order_id=payment['id'], amount=paise_amount, receipt=receipt, status='created')

    context = {
        'orders': payment,      # call it orders to match existing template usage
        'uname': request.user.username,
        'total_inr': total_inr
    }
    return render(request, 'pay.html', context)