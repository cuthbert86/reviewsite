"""
URL configuration for productreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from reviews.forms import NewPasswordChangeForm
from reviews.views import (
    contact_submission,
    home_page,
    new_category,
    new_product,
    product_details,
    product_list,
    register_new_user,
    review_product,
    update_product,
    update_profile,
    user_profile,
)


app_name = 'reviews'

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy(settings.LOGIN_URL),
        ),
        name='logout',
    ),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('home'),
            template_name='registration/change_password.html',
            form_class=NewPasswordChangeForm,
        ),
        name='change_password',
    ),
    path('register/', register_new_user, name='register_new_user'),
    path('admin/', admin.site.urls, name='admin'),
    path('contact/', contact_submission, name ='contact'),
    path('profile/edit/', update_profile, name='update_user_profile'),
    path('profile/', user_profile, name='user_profile'),
    path('new-category/', new_category, name='new_category'),
    path('new-product/', new_product, name='new_product'),
    path('product/<int:pk>/', product_details, name='product_details'),
    path('product/<int:pk>/update/', update_product, name='update_product'),
    path('product/<int:pk>/review/', review_product, name='review_product'),
    path('product-list/', product_list, name='product_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
