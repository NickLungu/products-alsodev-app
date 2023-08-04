from rest_framework import serializers
from .models import Product, Feature, Image

import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG)

# Create a logger instance
logger = logging.getLogger('my_logger')


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Custom method to get the image URL

    class Meta:
        model = Image
        fields = ['image_url']

    def get_image_url(self, obj):
        # obj represents the current Image instance
        # Get the URL of the associated image file
        request = self.context.get('request')  # Get the request from context
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['value', 'key']


class ProductSerializer(serializers.ModelSerializer):

    feature = FeatureSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id','slug','author','price','create_date','feature','images']