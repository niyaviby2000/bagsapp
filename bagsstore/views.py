from django.shortcuts import render,redirect

# Create your views here.

from bagsstore.forms import SignUpform,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from bagsstore.models import Bag,Size,BasketItem,Order

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpform()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpform(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # data=form_instance.cleaned_data

            # User.objects.create(**data) // password to get encrypted

            return redirect("register")
        
        return render(request,"register.html",{"form":form_instance})
    
class LoginInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("login success")

                return redirect("index")
            
        print("failed")

        return render(request,"login.html",{"form":form_instance})
    
class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Bag.objects.all()

        return render(request,"index.html",{"data":qs})
    

class BagDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Bag.objects.get(id=id)

        return render(request,"bag_detail.html",{"data":qs})
    
class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Bag.objects.get(id=id)

        size_name=request.POST.get("size")

    # colour_name=request.POST.get("colour")
        qty=request.POST.get("qty")
    # basket_obj=basket.objects.get(owner=request.user)
        basket_obj=request.user.cart  #using related name for parent reference

        size_obj=Size.objects.get(name=size_name)

        basket_item_obj=BasketItem.objects.filter(basket_object=basket_obj,product_object=product_obj,size_object=size_obj,is_order_placed=False)

        if basket_item_obj: #filter gives a list thatis y [0]

            basket_item_obj[0].quantity+=int(qty)

            basket_item_obj[0].save()

        else:

        # colour_obj=Colour.objects.get(name=colour_name)
        # basket item object

            BasketItem.objects.create(

            basket_object=basket_obj,

            size_object=size_obj,
            
            product_object=product_obj,

            quantity=qty,

            # colour_object=colour_obj,

        )

        print("item added to cart")

        # print(product_obj,size_obj)

        return redirect ("index")

    
    
class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False) #if related name is not there then basket_obj=basket.objects.get(owner=request.user) qs=basketitem.objects.filter(basket_object=basket_obj,is_order_placed=false)

        return render(request,"cart_items.html",{"data":qs})
    
class CartDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")
    
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        # action=request.POST.get("action") #increment/decrement

        id=kwargs.get("pk")

        basket_item_obj=BasketItem.objects.get(id=id)

        action=request.POST.get("action") 


        if action=="increment":

            basket_item_obj.quantity+=1

        else:

            basket_item_obj.quantity-=1

        basket_item_obj.save()
        
        return redirect("cart-summary")    
    
class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        delivery_address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False).order_by("-created_date")

        if payment_mode=="cod":

            order_obj=Order.objects.create(

                user_object=user_obj,

                email=email,

                phone=phone,

                delivery_address=delivery_address,

                pin=pin,

                payment_mode=payment_mode
            )

            for bi in cart_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()
                
        # print(email,phone,delivery_address,pin,payment_mode)
        
        return redirect("index")
    
class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order_summary.html",{"data":qs})

