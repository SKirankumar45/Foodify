from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import Customer,Restaurant,Item
# Create your views here.
def index(request):
    return render(request, 'index.html')

def open_singin(request):
    return render(request, 'signin.html')

def open_signup(request):
    return render(request, 'signup.html')

def signup(request):
    #return HttpResponse("Response recieved")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('phone')
        address = request.POST.get('address')
        try:
            Customer.objects.get(username = username)
            return HttpResponse("username already exists")
        except:
            Customer.objects.create(
                username = username,
                password = password,
                email = email,
                mobile = mobile,
                address = address
            )

            return render(request, 'signin.html')
    
def signin(request):
        #return HttpResponse('received')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    try:
        Customer.objects.get(username = username, password = password)
        if(username=='admin'):
            return render(request, 'admin_home.html')
        else:
            restaurant = Restaurant.objects.all()
            return render(request, 'customer_home.html',{"restaurants": restaurant,
                                                         "username":username})
    except Customer.DoesNotExist:
        return render(request, 'failure.html')
    
def open_add_restaurant(request):
    return render(request,'add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('url')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name = name,
                                  pictureurl = picture,
                                  cuisine = cuisine,
                                  rating = rating)
        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {'restaurants':restaurants})

def open_show_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {'restaurants':restaurants})

def open_update_restaurant(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    return render(request,'update_restaurant.html',{'restaurant':restaurant})

def update_restaurant(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.pictureurl = request.POST.get('pictureurl')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()
        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html',{'restaurants':restaurants})
    

def delete_restaurant(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, id = restaurant_id)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('open_show_restaurant')
    

def open_update_menu(request,restaurant_id):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'update_menu.html', 
{"itemList": itemList, "restaurant": restaurant})


def update_menu(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id = restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        picture = request.POST.get('picture')
        is_veg = request.POST.get('is_veg') == 'on'
        price = request.POST.get('price')

        Item.objects.create(
            restaurant = restaurant,
            name = name,
            description = description,
            price= price,
            is_veg = is_veg,
            picture = picture
        )

        return redirect('open_show_restaurant')
    
def view_menu(request,restaurant_id,username):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'customer_menu.html', 
{"itemList": itemList, "restaurant": restaurant, "username":username})