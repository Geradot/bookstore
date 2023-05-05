from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Sum, F
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
import json
from .models import *


def index(request):
    books = Book.objects.all()
    categories = BookCategory.objects.all().order_by('name')
    return render(request, "bookstore/index.html", {
        "books": books,
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookstore/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, "bookstore/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bookstore/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bookstore/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, "bookstore/register.html")


def book_page(request, id):
    try:
        book = Book.objects.get(pk=int(id))
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse("error404"))
    is_in_cart = False
    amount = 0
    purchase_item = None
    if request.user.is_authenticated:
        current_cart = Purchase.objects.filter(
            paid=False, user=request.user).first()
        if current_cart:
            purchase_item = PurchaseItem.objects.filter(
                book=book, purchase=current_cart).first()
            if purchase_item:
                is_in_cart = True
                amount = purchase_item.quantity

    return render(request, "bookstore/book.html", {
        "book": book,
        "is_in_cart": is_in_cart,
        "amount": amount,
        "purchase_item": purchase_item
    })


@login_required(login_url='/login')
def cart(request):
    purchase = Purchase.objects.filter(
        user=request.user, paid=False).first() or None
    cart = PurchaseItem.objects.filter(purchase=purchase) or None
    return render(request, "bookstore/cart.html", {
        "purchase": purchase,
        "cart": cart
    })


@csrf_exempt
def purchase_paid(request):
    if request.method == "PUT":
        current_cart = Purchase.objects.filter(
            user=request.user, paid=False).first()
        current_cart.paid = True
        current_cart.save()
        return JsonResponse({}, status=200)


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        bookId = int(data.get("bookId"))
        amount = int(data.get("amount"))

        book = Book.objects.get(pk=bookId)

        current_cart = Purchase.objects.filter(
            user=request.user, paid=False).first()
        if not current_cart:
            current_cart = Purchase.objects.create(user=request.user)

        purchase_item = PurchaseItem(
            purchase=current_cart,
            book=book,
            quantity=amount,
            subtotal=book.price * amount
        )
        purchase_item.save()
        recalculateTotalPrice(current_cart)

        return JsonResponse({"amount": purchase_item.quantity})


@csrf_exempt
def remove_from_cart(request, id):
    if request.method == "DELETE":
        current_cart = Purchase.objects.filter(
            user=request.user, paid=False).first()
        book = Book.objects.get(pk=int(id))
        purchase_item = PurchaseItem.objects.filter(
            purchase=current_cart, book=book).first()
        purchase_item.delete()
        recalculateTotalPrice(current_cart)
        return JsonResponse({}, status=204)


@csrf_exempt
def change_amount(request, id):
    print(request.user)
    if request.method == "PUT":
        data = json.loads(request.body)
        bookId = int(id)
        book = Book.objects.get(pk=bookId)
        amount = int(data.get("amount"))

        current_cart = Purchase.objects.filter(
            user=request.user, paid=False).first()

        purchase_item = PurchaseItem.objects.filter(
            purchase=current_cart, book=book).first()

        purchase_item.quantity = amount
        purchase_item.subtotal = amount * book.price
        purchase_item.save()

        recalculateTotalPrice(current_cart)

        return JsonResponse({"amount": purchase_item.quantity})

@login_required(login_url='/login')
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user, paid=True).order_by('-purchase_date')
    purchase_dict = {}
    for purchase in purchases:
        items = purchase.purchases.all()
        total_price = sum(item.subtotal for item in items)
        purchase_dict[purchase.pk] = {
            'items': items,
            'date': purchase.purchase_date,
            'total_price': total_price
        }

    return render(request, "bookstore/purchases.html", {
        "purchase_dict": purchase_dict,
        "favorite_category": get_popular_category(request.user) or None
    })


def recalculateTotalPrice(current_cart):
    total_price = PurchaseItem.objects.filter(purchase=current_cart).aggregate(
        total_price=Sum(F('quantity')*F('book__price')))['total_price'] or 0.0
    current_cart.total_price = total_price
    current_cart.save()

def get_popular_category(user):
    categories_count = defaultdict(int)
    for purchase in user.customers.filter(paid=True):
        for item in purchase.purchases.all():
            if item.book.category:
                categories_count[item.book.category.name] += item.quantity

    if not categories_count:
        return None

    max_count = max(categories_count.values())
    popular_categories = {k: v for k, v in categories_count.items() if v == max_count}

    return popular_categories

def handler404(request, exception):
    return render(request, "bookstore/404.html")

def handler500(request):
    return render(request, "bookstore/500.html")