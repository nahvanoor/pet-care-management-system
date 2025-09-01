from django.shortcuts import render
from pet_app. models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType

# Create your views here.
def home(request):
    return render(request,"index.html")

def login(request):
    if request.method=='POST' and 'submit' in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=Login.objects.get(username=username,password=password)
            request.session['login_id']=user.id
            
            if user.usertype=="admin":
                return HttpResponse ('<script>alert("Welcome Admin");window.location="/admin_home"</script>')
            
            if user.usertype=="user":
                return HttpResponse ('<script>alert("Welcome User");window.location="/user_home"</script>')
            
            if user.usertype=="trainer":
                return HttpResponse ('<script>alert("Welcome Trainer");window.location="/trainer_home"</script>')
            
            elif user.usertype=="petstore":
                return HttpResponse ('<script>alert("Welcome Petstore");window.location="/petstore_home"</script>')
            
            else:
                return HttpResponse('Unknown Usertype')
            
        except Login.DoesNotExist:
            return HttpResponse ('<script>alert("invalid username or password");window.location="/login"</script>')
    return render(request,"login.html")

def register(request): 
    if request.method=='POST' and 'submit' in request.POST:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        gender=request.POST['gender']
        phone_number=request.POST['phone_number']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        usertype=request.POST['usertype']
        if Register.objects.filter(email=email).exists():
            return HttpResponse ('<script>alert("email already exists);window.location="/register"</script>')
        
        if Register.objects.filter(phone_number=phone_number).exists():
            return HttpResponse ('<script>alert("phone number already exists);window.location="/register"</script>')
        
        if Login.objects.filter(username=username).exists():
            return HttpResponse ('<script>alert("username already exists);window.location="/Login"</script>')
        
        logi=Login(username=username,password=password,usertype=usertype)
        logi.save()
        
        reg=Register(LOGIN=logi,firstname=firstname,lastname=lastname,gender=gender,phone_number=phone_number,email=email)
        reg.save()
        return HttpResponse ('<script>alert("Registered successfully");window.location="/login"</script>')
    return render(request,"register.html")

def admin_home(request):
    id=request.session['login_id']
    user=Register.objects.get(id=id)
    return render(request,"admin_home.html",{'user':user})

def user_home(request):
    pet=Pet.objects.all()
    food=PetFoods.objects.all()
    accessories=PetAccessories.objects.all()
    return render(request,"user_home.html",{'pet':pet,'food':food,'accessories':accessories})

def trainer_home(request):
    id=request.session['login_id']
    user=Register.objects.get(id=id)
    return render(request,"trainer_home.html",{'user':user})

def petstore_home(request):
    id=request.session['login_id']
    pet=Pet.objects.filter(REGISTER__LOGIN=id)
    food=PetFoods.objects.filter(REGISTER__LOGIN=id)
    accessories=PetAccessories.objects.filter(REGISTER__LOGIN=id)
    return render(request,"petstore_home.html",{'pet':pet,'food':food,'accessories':accessories})

def profile(request):
    id = request.session['login_id']
    login = Login.objects.get(id=id)
    user = Register.objects.get(LOGIN=login)
    return render(request,'profile.html',{'user':user,'login':login})

def edit_profile(request,id):
    login=Login.objects.get(id=id)
    user=Register.objects.get(LOGIN=login)
    if request.method=="POST" and 'update' in request.POST:
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        gender=request.POST.get('gender')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user.firstname=firstname
        user.lastname=lastname
        user.gender=gender
        user.phone_number=phone_number
        user.email=email
        login.username=username
        login.password=password
        user.save()
        login.save()
        return HttpResponse('<script>alert("Profile updated successfully"); window.location="/profile/"</script>')
    return render(request,'edit_profile.html',{'user':user, 'login':login})

def add_pets(request):
    if request.method=='POST' and 'submit' in request.POST:
        pet_name=request.POST['pet_name']
        age=request.POST['age']
        type=request.POST['type']
        price=request.POST['price']
        image=request.FILES['image']
        pet=Pet(pet_name=pet_name,age=age,type=type,price=price,image=image,REGISTER=Register.objects.get(LOGIN=request.session['login_id']))
        pet.save()
        return HttpResponse ('<script>alert("Pet added successfully");window.location="/petstore_home"</script>')
    return render(request,"add_pets.html")

def add_pet_foods(request):
    if request.method=='POST' and 'submit' in request.POST:
        food_name=request.POST['food_name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        image=request.FILES['image']
        food=PetFoods(food_name=food_name,quantity=quantity,price=price,image=image,REGISTER=Register.objects.get(LOGIN=request.session['login_id']))
        food.save()
        return HttpResponse ('<script>alert("Pet Food added successfully");window.location="/petstore_home"</script>')
    return render(request,"add_pet_foods.html")

def add_pet_accessories(request):
    if request.method=='POST' and 'submit' in request.POST:
        accessories_name=request.POST['accessories_name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        image=request.FILES['image']
        accessories=PetAccessories(accessories_name=accessories_name,quantity=quantity,price=price,image=image,REGISTER=Register.objects.get(LOGIN=request.session['login_id']))
        accessories.save()
        return HttpResponse ('<script>alert("Pet Accessories added successfully");window.location="/petstore_home"</script>')
    return render(request,"add_pet_accessories.html")

def edit_pets(request,id):
    pet=Pet.objects.get(id=id)
    if request.method=='POST' and 'update' in request.POST:
        pet_name=request.POST['pet_name']
        age=request.POST['age']
        type=request.POST['type']
        price=request.POST['price']
        if 'image' in request.FILES:
            image=request.FILES['image']
            pet.image=image
        pet.pet_name=pet_name
        pet.age=age
        pet.type=type
        pet.price=price
        pet.save()
        return HttpResponse ('<script>alert("Pet updated successfully");window.location="/petstore_home"</script>')
    return render(request,"edit_pets.html",{'pet':pet})

def delete_pets(request,id):
    pet=Pet.objects.get(id=id)
    pet.delete()
    return HttpResponse ('<script>alert("Pet deleted successfully");window.location="/petstore_home"</script>')

def edit_foods(request,id):
    food=PetFoods.objects.get(id=id)
    if request.method=='POST' and 'update' in request.POST:
        food_name=request.POST['food_name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        if 'image' in request.FILES:
            image=request.FILES['image']
            food.image=image
        food.food_name=food_name
        food.quantity=quantity
        food.price=price
        food.save()
        return HttpResponse ('<script>alert("Pet Food updated successfully");window.location="/petstore_home"</script>')
    return render(request,"edit_foods.html",{'food':food})

def delete_foods(request,id):
    food=PetFoods.objects.get(id=id)
    food.delete()
    return HttpResponse ('<script>alert("Pet Food deleted successfully");window.location="/petstore_home"</script>')

def edit_accessories(request,id):
    accessories=PetAccessories.objects.get(id=id)
    if request.method=='POST' and 'update' in request.POST:
        accessories_name=request.POST['accessories_name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        if 'image' in request.FILES:
            image=request.FILES['image']
            accessories.image=image
        accessories.accessories_name=accessories_name
        accessories.quantity=quantity
        accessories.price=price
        accessories.save()
        return HttpResponse ('<script>alert("Pet Accessories updated successfully");window.location="/petstore_home"</script>')
    return render(request,"edit_accessories.html",{'accessories':accessories})

def delete_accessories(request,id):
    accessories=PetAccessories.objects.get(id=id)
    accessories.delete()
    return HttpResponse ('<script>alert("Pet Accessories deleted successfully");window.location="/petstore_home"</script>')


def get_user_cart(request):
    user_id = request.session.get('login_id')
    if not user_id:
        return None  # Or redirect to login page
    user = get_object_or_404(Register, id=user_id)
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# Add item to cart
def add_to_cart(request, type, item_id):
    cart = get_user_cart(request)
    if not cart:
        return redirect('login')  # fallback if user not logged in

    # Select the product model
    if type == 'pet':
        product = get_object_or_404(Pet, id=item_id)
    elif type == 'food':
        product = get_object_or_404(PetFoods, id=item_id)
    elif type == 'accessory':
        product = get_object_or_404(PetAccessories, id=item_id)
    else:
        return redirect('user_home')  # fallback

    # Create or update cart item
    content_type = ContentType.objects.get_for_model(product)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=product.id,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

# View cart
def view_cart(request):
    cart = get_user_cart(request)
    if not cart:
        return render(request, 'cart.html', {'cart': None})
    return render(request, 'cart.html', {'cart': cart})

# Remove item from cart
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')

# Update cart quantity
def update_cart_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect('view_cart')