from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    CategoryForm,
    ContactForm,
    ProductForm,
    ProfileForm,
    RegiserNewProfileForm,
    ReviewForm,
)
from .models import Product, Profile


def home_page(request):
    return render(request, 'welcome.html')


@login_required
def contact_submission(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    
    return render(request, 'contact.html', {'form': form})


def register_new_user(request):
    user_form = UserCreationForm(request.POST or None)
    profile_form = RegiserNewProfileForm(request.POST or None)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect('login')
    
    return render(
        request,
        'new_user.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        },
    )


@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)

    return render(request, 'profile.html', {'profile': profile})


@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})


@login_required
def new_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('new_product')

    return render(
        request,
        'crispy_form_template.html',
        {
            'form': form,
            'title': 'New Category',
        },
    )


@login_required
def new_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(
        request,
        'update_product.html',
        {
            'form': form,
            'verb': 'Create',

        },
    )


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_details', pk=product.pk)

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'update_product.html',
        {
            'form': form,
            'verb': 'Update',

        },
    )


@login_required
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_details.html', {'product': product})


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def review_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(data=request.POST, user=request.user.profile, product=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    
    else:
        form = ReviewForm(user=request.user, product=product)

    return render(
        request,
        'update_product.html',
        {'form': form, 'verb': 'Review'},
    )
