import django.forms

from .models import Product
from django.forms import ModelForm, formset_factory


class FeatureForm(django.forms.Form):
    key = django.forms.CharField(max_length=100)
    value = django.forms.CharField(max_length=100)



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['slug','price','images']
        widgets = {
            'slug': django.forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "name"
            }),
            'price': django.forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "price"
            }),
            'images': django.forms.ClearableFileInput(attrs={
                'multiple': True,
                'placeholder':'image'
            }),
        }

