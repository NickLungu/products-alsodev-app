from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer

from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView

from products.forms import ProductForm, FeatureForm
from products.models import Product, Feature, Image
from django.http import JsonResponse

import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG)

# Create a logger instance
logger = logging.getLogger('my_logger')


# Log a debug message


def add_product(request):
    FeatureFormSet = formset_factory(FeatureForm, extra=10)

    if request.method == 'POST':

        formset = FeatureFormSet(request.POST)
        if formset.is_valid():
            slug = request.POST.get('slug')
            price = request.POST.get('price')
            image_file = request.FILES['images']

            # Create a new Product instance
            product = Product(slug=slug, author=request.user, price=price)
            product.save()
            if image_file:
                logger.debug("image ok")
                image = Image(image=image_file)
                image.save()
                product.images.add(image)

            for feature_form in formset:

                key = feature_form.cleaned_data.get('key')
                value = feature_form.cleaned_data.get('value')
                logger.debug(key)
                logger.debug(value)
                if key and value:
                    feature = Feature(key=key, value=value)
                    feature.save()
                    product.feature.add(feature)
            logger.debug("go save")
            product.save()
            response_data = {'success': True}
            return JsonResponse(response_data)
    else:
        formset = FeatureFormSet()
        form = ProductForm()
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'products/add_product.html', context=context)


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    logger.debug(product_id)
    logger.debug(product)
    logger.debug(product.images.all())
    FeatureFormSet = formset_factory(FeatureForm, extra=1)

    if request.method == 'POST':
        formset = FeatureFormSet(request.POST)
        if formset.is_valid():
            slug = request.POST.get('slug')
            price = request.POST.get('price')
            image_file = request.FILES.get('images')

            # Update the existing Product instance
            product.slug = slug
            product.price = price
            if image_file:
                # Delete existing images and add the new one
                image = Image(image=image_file)
                image.save()
                product.images.add(image)

            # Delete existing features associated with the product
            product.feature.all().delete()

            for feature_form in formset:
                key = feature_form.cleaned_data.get('key')
                value = feature_form.cleaned_data.get('value')
                if key and value:
                    feature = Feature(key=key, value=value)
                    feature.save()
                    product.feature.add(feature)

            product.save()
            response_data = {'success': True}
            return JsonResponse(response_data)
    else:
        logger.debug("just update page.")
        form = ProductForm(instance=product)
        feature_queryset = product.feature.all()
        formset = FeatureFormSet(initial=[{'key': f.key, 'value': f.value} for f in feature_queryset])
        logger.debug(feature_queryset)
        context = {
            'form': form,
            'formset': formset,
            'product': product,
        }
        return render(request, 'products/update_product.html', context=context)


def delete_image(request, image_id):
    image_to_delete = get_object_or_404(Image, id=image_id)
    image_to_delete.delete()
    return JsonResponse({'success': True})


class ProductListView(ListView):
    paginate_by = 10
    model = Product
    template_name = "products/main.html"
    context_name = 'products'


class AddProduct(CreateView):
    # model = Comment
    form_class = ProductForm
    template_name = "products/add_product.html"
    # success_url = '/'


class ProductListApiView(APIView):
    def get(self, request):
        try:
            product_id = request.data.get('product_id')
            if not product_id is None:
                logger.debug(f'id {product_id} exist')
                queryset = Product.objects.get(id=product_id)
                serializer = ProductSerializer(queryset, context={'request': request})
            else:
                logger.debug(f'id {product_id} doesn\'t exist')
                queryset = Product.objects.all()
                serializer = ProductSerializer(queryset, many=True, context={'request': request})
        except Exception as e:
            logger.debug(f'error: {e}')
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True, context={'request': request})



        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

