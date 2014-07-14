__author__ = 'yef'


from rest_framework import serializers
from models import Vendor
from models import Product
from models import Category
from models import Comment
from models import RegistrationProfile
import models

from rest_framework import serializers
from rest_framework import pagination

class NextPageField(serializers.Field):
    def to_native(self, value):
        if value.has_next():
            return True
        else:
            return False

class PageNumField(serializers.Field):
    def to_native(self, value):
        return value.count()


class CustomPaginationSerializer(pagination.BasePaginationSerializer):
    hasnext = NextPageField(source='*')
    pagenum = serializers.Field(source='paginator.count')
    #contextData = ContexDataField(source='*')


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        #fields = ('id', 'name', 'description', 'location')
        fields = ('id', 'name', 'description', 'address', 'phone', 'logo','openhour','closehour')

class SimpleVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        #fields = ('id', 'name', 'description', 'location')
        fields = ('id', 'name', 'logo', 'latitude', 'longitude')

class CommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name')
    class Meta:
        model = Comment
        #fields = ('id', 'name', 'description', 'location')
        fields = ('id', 'content', 'updated','name')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        #fields = ('id', 'name', 'description', 'location')
        fields = ('id', 'name', 'description', 'price')

class SimpleProductSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(source='vendor.latitude')
    lon = serializers.FloatField(source='vendor.longitude')

    class Meta:
        model = Product
        #fields = ('id', 'name', 'description', 'location')
        fields = ('id', 'name', 'description', 'price', 'lat','lon','photo','description')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'description',)

class CateListResponse(CustomPaginationSerializer):
    results_field = 'catelist'
    class Meta:
        object_serializer_class = CategorySerializer


class CateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'description',)


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')


    class Meta:
        model = RegistrationProfile
        fields = ('id', 'phone', 'address', 'first_name', 'last_name', 'email')


class OrderItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItemDetail
        fields = ('name', 'value',)


class OrderItemSerializer(serializers.ModelSerializer):
    option_values = OrderItemDetailSerializer(source='option_values', many=True)


    class Meta:
        model = models.OrderItem
        fields = ('product', 'quantity', 'price', 'option_values')

class OrderSerializer(serializers.ModelSerializer):
    lineitems = OrderItemSerializer(source='lineitems', many=True)

    class Meta:
        model = models.Order
        fields = ('id', 'lineitems', 'date', 'status')

class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Option
        fields = ('id','name','value','price')

class OptionGroupSerializer(serializers.ModelSerializer):
    options = OptionSerializer(source='options',many=True)

    class Meta:
        model = models.OptionGroup
        fields = ('name','description','options')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CompanyProfile
        fields = ('email','bookingNo','businessNo','address','terms')

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Booking
        fields = ('user','date','persons','vendor')


class BookingInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Booking
        fields = ('date','persons','vendor')

from django.contrib.auth import get_user_model


from rest_framework import serializers



from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import _resolve_model
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)


class TokenSerializer(serializers.ModelSerializer):

    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)


class UserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for UserProfile model.
    """

    user = UserDetailsSerializer()

    class Meta:
        # http://stackoverflow.com/questions/4881607/django-get-model-from-string
        model = _resolve_model(getattr(settings, 'REST_PROFILE_MODULE', None))


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    """
    ModelSerializer that allows fields argument to control fields
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserUpdateSerializer(DynamicFieldsModelSerializer):

    """
    User model w/o username and password
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name')


from shop.models import RegistrationProfile

class UserProfileUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer for updating User and UserProfile model.
    """

    user = UserUpdateSerializer()

    class Meta:
        # http://stackoverflow.com/questions/4881607/django-get-model-from-string
        model = RegistrationProfile



class SimpleOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ('id', 'status',)


class OrderItemSerailzer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        field = ('product','quantity', 'price')


class Order2Serializer(serializers.ModelSerializer):

    products = OrderItemSerializer(source='lineitems', many=True)

    class Meta:
        model = models.Order
        fields = ('status', 'user', 'shippingAddress', 'postcode', 'shippingDistance','deliverTime','deliverFee','totalPrice','comments', 'products')


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeliverReport
        fields = ('lat','lon','location')