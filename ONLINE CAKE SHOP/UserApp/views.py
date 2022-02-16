from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import Category,Cake
from UserApp.models import UserInfo,MyCart,MyAccount,OrderMaster
from datetime import datetime 
from django.contrib import messages 
# Create your views here.
def home(request):
    cats = Category.objects.all()
    cakes = Cake.objects.all()
    return render(request,"master.html",{"cats":cats,"cakes":cakes})

def showCakes(request,cid):
    cats = Category.objects.all()
    cakes = Cake.objects.filter(category=cid)
    cat = Category.objects.get(id=cid)
    return render(request,"master.html",{"cats":cats,"cakes":cakes,"cname":cat.cat_name})

def ViewDetails(request,cakeid):
    cake = Cake.objects.get(id=cakeid)
    return render(request,"ViewDetails.html",{"cake":cake})


def SignUp(request):
    if(request.method == "GET"):
        return render(request,"SignUp.html",{})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        try:
            u1 = UserInfo.objects.get(username=uname,password=pwd)
        except:
            u1  = UserInfo(uname,pwd)
            u1.save()        
            return redirect(Login)
            #return HttpResponse("User created successfuly..")
        else:
            redirect(home)

            #return HttpResponse("User already exists..")

def Login(request):
    if(request.method == "GET"):
        return render(request,"Login.html",{})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        try:
            u1 = UserInfo.objects.get(username=uname,password=pwd)
        except:
            #return HttpResponse("Invalid Credentials..")
            return redirect(Login)
        else:
            #If login is successful, create the session and redirect to home page
            request.session["uname"]  = uname
            return redirect(home)

def logout(request):
    request.session.clear()
    return redirect(home)

def addToCart(request):
    if("uname" in request.session):        
        cid = request.POST["cid"]
        qty = request.POST["qty"]
        cake = Cake.objects.get(id=cid)
        user = UserInfo.objects.get(username = request.session["uname"])
        #Check if item already added in cart
        try:
            m1 = MyCart.objects.get(user = user,cake=cake)
        except:
            cart1 = MyCart()
            cart1.user = user
            cart1.cake = cake
            cart1.cake = Cake.objects.get(id=cid)
            cart1.qty = qty
            cart1.save()
            return HttpResponse("Item added successfully to cart")
        else:
            return HttpResponse("Item already present in cart")
        
    else:
        return redirect(Login)

def showAllCartItems(request):
    u1 = UserInfo.objects.get(username = request.session["uname"])
    if(request.method == "GET"):
        #Get the items from cart based on user       
        items = MyCart.objects.filter(user = u1)
        total = 0

        for item in items:
            total += item.cake.price * item.qty

        request.session["total"] = total
        return render(request,"showAllCartItems.html",{"items":items})
    else:
        action = request.POST["action"]
        cakeid = request.POST["cakeid"]
        c1 = Cake.objects.get(id=cakeid)
        cart = MyCart.objects.get(user = u1,cake=c1)
        if(action == "update"):
            qty = request.POST["qty"]
            cart.qty = qty
            cart.save()
        else:
            cart.delete()
        return redirect(showAllCartItems)


def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = MyAccount.objects.get(cardno = cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            owner = MyAccount.objects.get(cardno = '111',cvv='111',expiry='12/2025')
            owner.balance += request.session["total"]
            buyer.balance -= request.session["total"]

            owner.save()
            buyer.save()

            user = UserInfo.objects.get(username = request.session["uname"])
            items = MyCart.objects.filter(user=user)
            details = ""
            for item in items:
                details+=item.cake.cname + ","
                item.delete()
            
            order = OrderMaster()
            order.order_date = datetime.now()
            order.user = user 
            order.amount = request.session["total"]
            order.order_details = details
            order.save()

            

            return redirect(home)