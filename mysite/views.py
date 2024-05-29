from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import *
from .forms import RegisterForm

def index(r):
    return render(r, "index.html")

def contact(r):
    return render(r, "contact.html")

def about(r):
    return render(r, "about.html")

def login_view(r):
    if r.method == 'POST':
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(r, username=username, password=password)
        if user is not None:
            login(r, user)
            return redirect('/catalog')

def logout_view(r):
    logout(r)
    Session.objects.filter(session_key=r.session.session_key).delete()
    return redirect("/")

def register(r):
    if r.method == 'POST':
        form = RegisterForm(r.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            return login_view(r)

def catalog(r):
    if r.method == 'POST':
        image = r.FILES.get('image')
        name = r.POST.get('name')

        try:
            category = Category(
                name=name,
                image=image,
            )

            category.save()

            messages.success(r, 'Категория добавлена!')

        except Exception as e:
            messages.error(r, f'Неизвестная ошибка: {e}')


    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(r, "catalog.html", context=context)

def catalog_category(r, id):
    if r.method == 'POST':
        category_id = r.POST.get('category')
        image = r.FILES.get('image')
        name = r.POST.get('name')
        code = r.POST.get('code')
        barcode = r.POST.get('barcode')
        description = r.POST.get('description')
        provider = r.POST.get('provider')
        purchase_price = r.POST.get('purchase_price')
        selling_price = r.POST.get('selling_price')
        amount = r.POST.get('amount')

        try:
            category = Category.objects.get(id=category_id)

            product = Product(
                category=category,
                image=image,
                name=name,
                code=code,
                barcode=int(barcode),
                description=description,
                provider=provider,
                purchase_price=int(purchase_price),
                selling_price=int(selling_price),
                amount=int(amount)
            )
            product.save()

            messages.success(r, 'Продукт добавлен!')

        except Category.DoesNotExist:
            messages.error(r, 'Категория не найдена')
        except Exception as e:
            messages.error(r, f'Неизвестная ошибка: {e}')

    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)
    context = {
        "categories": categories,
        "category": category,
        "products": products,
    }
    return render(r, "catalog_category.html", context=context)

def editproduct(r):
    if r.method == 'POST':
        pid = r.POST.get('pid')
        category_id = r.POST.get('category')
        image = r.FILES.get('image')
        print(image, r.FILES)
        name = r.POST.get('name')
        code = r.POST.get('code')
        barcode = int(float(r.POST.get('barcode', None)))
        description = r.POST.get('description')
        provider = r.POST.get('provider')
        purchase_price = int(float(r.POST.get('purchase_price', None)))
        selling_price = int(float(r.POST.get('selling_price', None)))
        amount = int(float(r.POST.get('amount', None)))

        try:
            category = Category.objects.get(id=category_id)

            product = Product.objects.get(id=pid)

            if category is not "" and product.category != category:
                product.category = category
            if image:
                print(image)
                product.image = image
            if name is not "" and product.name != name:
                product.name = name
            if code is not "" and product.code != code:
                product.code = code
            if barcode is not "" and product.barcode != barcode:
                product.barcode = barcode
            if description is not "" and product.description != description:
                product.description = description
            if provider is not "" and product.provider != provider:
                product.provider = provider
            if purchase_price is not "" and product.purchase_price != purchase_price:
                product.purchase_price = purchase_price
            if selling_price is not "" and product.selling_price != selling_price:
                product.selling_price = selling_price
            if amount is not "" and product.amount != amount:
                product.amount = amount

            product.save()

            messages.success(r, 'Данные изменены!')

        except Category.DoesNotExist:
            messages.error(r, 'Категория не найдена')
        except Exception as e:
            messages.error(r, f'Неизвестная ошибка: {e}')

    return redirect(f"/catalog/{ category_id }")

def delete_product(r, id, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    return redirect(f"/catalog/{ id }")