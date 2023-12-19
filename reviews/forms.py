from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.urls import reverse

from reviews.models import Category, ContactSubmission, Product, Profile, Review


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'address', 'city', 'country', 'photo']


class RegiserNewProfileForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class RegisterNewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class NewPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Contact Us',
                'name',
                'email',
                'subject',
                'message',
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'branch',
            'average_cost',
            'category',
            'release_date',
            'description',
            'product_photo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_category_url = reverse('new_category')
        self.fields['category'].help_text = (
            f'<a href="{new_category_url}" class="btn btn-sm btn-secondary">Add new category</a>'
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'description']

    def __init__(self, user, product, *args, **kwargs):
        self.user = user
        self.product = product
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super().save(commit=False)
        review.product = self.product
        review.user = self.user
        if commit:
            review.save()

        return review
