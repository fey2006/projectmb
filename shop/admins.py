from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from django.contrib.auth import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


import warnings

from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy #as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy

ERROR_MESSAGE = ugettext_lazy("Please enter the correct %(username)s and password "
        "for a staff account. Note that both fields may be case-sensitive.")

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.

    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("Please log in again, because your session has expired.")})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
        params = {'username': self.username_field.verbose_name}

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = ("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message, code='invalid', params=params)
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message, code='invalid', params=params)
        return self.cleaned_data

from datetime import timedelta
class CustomUserAdmin(AdminSite):
    # Anything we wish to add or override
    login_form = UserAdminAuthenticationForm
    def has_permission(self, request):
        #Removed check for is_staff.
        if request.user.is_staff:
            if request.user.last_login + timedelta(seconds=1) >= request.user.date_joined:
                obj = request.user
                from django.contrib.contenttypes.models import ContentType
                from django.contrib.auth.models import Permission
                permissionlist = ['change_vendor',
                                      'add_category',
                                      'change_category',
                                      'delete_category',
                                      'add_product',
                                      'change_product',
                                      'delete_product',
                                      'add_optiongroup',
                                      'change_optiongroup',
                                      'delete_optiongroup',
                                      'add_option',
                                      'change_option',
                                      'delete_option',
                                      'add_productoptiongroup',
                                      'change_productoptiongroup',
                                      'delete_productoptiongroup',
                                      'change_order',
                                      'change_booking',
                                      'change_comment'
                                      ]


                for item in permissionlist:
                    pos = item.find('_')
                    if pos == -1:
                        continue
                    name = item[pos + 1:]
                    print name
                    content = ContentType.objects.filter(model = name)
                    permission = Permission.objects.get(content_type = content, codename = item)
                    obj.user_permissions.add(permission)
                    obj.save()

        from .models import Vendor
        if not request.user.is_active or  not request.user.is_staff:
            return False
        queryset = Vendor.objects.filter(owner = request.user)
        if len(queryset) > 0:
            return True
        else:
            return False

        #return request.user.is_active & request.user.is_staff



user_admin_site = CustomUserAdmin(name='usersadmin')


from django.contrib import admin
import models
# Register your models here.

from shop.models import Vendor
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('owner','name','updateDate','order')
    def has_change_permission(self, request, obj=None):
        return True



    def has_add_permission(self, request):
        """
        Returns True if the given request has permission to add an object.
        Can be overridden by the user in subclasses.
        """

        return True

    def has_change_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to change the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to change *any* object of the given type.
        """
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        #user = request.user
        #vendor = Vendor.objects.get(owner = user)
        #form.base_fields['owner'].initial = vendor
        return form

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        user = request.user
        vendor = Vendor.objects.get(owner = user)
        obj.owner = vendor
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('owner',)
        return self.readonly_fields

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        user = request.user
        vendor = Vendor.objects.get(owner = user)

        return qs.filter(owner = vendor)
    list_display = ('name', 'description', 'owner')
    list_per_page = 50
user_admin_site.register(models.Category, CategoryAdmin)
#admin.site.register(models.Category, CategoryAdmin)




from shop.models import Category


class OptionGroupInProductAdmin(admin.TabularInline):
    #list_display = ('order', 'product', 'quantity', 'price',)
    fields = ('productid', 'optiongroupid',)
    #readonly_fields = ('product', 'quantity', 'price',)
    #inline = (OrderItemDetailAdmin,)
    #fk_name = ''
    model = models.ProductOptionGroup


class OptionGroupAdmin2(admin.TabularInline):
    fields = ('name','description')
    model = models.OptionGroup


class ProductOptionGroupAdmin(admin.ModelAdmin):

    inlines = (OptionGroupAdmin2,)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category','vendor')
    list_per_page = 50
    readonly_fields = ('userlikes',)
    #list_filter = ['category']
    inlines = (OptionGroupInProductAdmin,)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category':
            user = request.user
            vendor = Vendor.objects.get(owner = user)
            kwargs['queryset'] = Category.objects.filter(owner = vendor)

        return db_field.formfield(**kwargs)


    exclude = ('vendor',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        #user = request.user
        #vendor = Vendor.objects.get(owner = user)
        #form.base_fields['owner'].initial = vendor
        return form

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        user = request.user
        vendor = Vendor.objects.get(owner = user)
        obj.vendor = vendor
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('vendor',)
        return self.readonly_fields

    def queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        user = request.user
        vendor = Vendor.objects.get(owner = user)

        return qs.filter(vendor = vendor)


import urllib2
import urllib
import json

def getLatLon(address):
    try:
        curUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (urllib.quote_plus(address + ' Singapore') , 'AIzaSyAe50PasAkJ_JS4hJZfFnrIKqqmprjp1Lc')
        print curUrl
        j = urllib2.urlopen(curUrl)
        js = json.load(j)

        print js
        ourResult = js['results'][0]['geometry']['location']
        return (ourResult['lat'], ourResult['lng'])
    except Exception as ex:
        return (0,0)

class ShopOwnerAdmin(admin.ModelAdmin):
    #list_display = ('name', 'address', 'postcode', 'email','logo','phone','description','openhour','closehour')
    readonly_fields = ('owner', 'latitude', 'longitude')
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(ShopOwnerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'owner':
            kwargs['queryset'] = User.objects.filter(is_staff = True)

        return db_field.formfield(**kwargs)

    def queryset(self, request):
        qs = super(ShopOwnerAdmin, self).queryset(request)
        user = request.user
        return qs.filter(owner = user)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        try:
            (lat,lon) = getLatLon(obj.address)
            obj.latitude = lat
            obj.longitude = lon
        except Exception as ex:
            print ex
            obj.latitude = 0
            obj.longitude = 0
        obj.save()



user_admin_site.register(models.Product, ProductAdmin)
user_admin_site.register(models.Vendor, ShopOwnerAdmin)
user_admin_site.register(models.ProductOptionGroup)
user_admin_site.register(models.Option)
#user_admin_site.register(models.OptionGroup)






class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date','persons','vendor',)
    list_per_page = 50
    readonly_fields = ('user','date','persons','vendor','phone','userdetail')

    def userdetail(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)

    def phone(self, obj):
        from .models import RegistrationProfile
        profile = RegistrationProfile.objects.get(user = obj.user)
        if profile:
            return profile.phone
        else:
            return '0'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(BookingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        return db_field.formfield(**kwargs)


    exclude = ('vendor',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)
        #user = request.user
        #vendor = Vendor.objects.get(owner = user)
        #form.base_fields['vendor'].initial = vendor
        return form

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        user = request.user
        vendor = Vendor.objects.get(owner = user)
        obj.vendor = vendor
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('vendor',)
        return self.readonly_fields

    def queryset(self, request):
        qs = super(BookingAdmin, self).queryset(request)
        user = request.user
        vendor = Vendor.objects.get(owner = user)

        return qs.filter(vendor = vendor)

user_admin_site.register(models.Booking, BookingAdmin)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','address')
    list_per_page = 50


    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        try:
            (lat,lon) = getLatLon(obj.address)
            obj.latitude = lat
            obj.longitude = lon
        except Exception as ex:
            print ex
            obj.latitude = 0
            obj.longitude = 0
        obj.save()


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(VendorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'owner':
            kwargs['queryset'] = User.objects.filter(is_staff = True)

        return db_field.formfield(**kwargs)


admin.site.register(Vendor,VendorAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'updated','vendor')
    readonly_fields = ('content','updated','user')
    list_per_page = 50

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(CommentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category':
            user = request.user
            vendor = Vendor.objects.get(owner = user)
            kwargs['queryset'] = Category.objects.filter(owner = vendor)

        return db_field.formfield(**kwargs)


    exclude = ('vendor',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(CommentAdmin, self).get_form(request, obj, **kwargs)
        #user = request.user
        #vendor = Vendor.objects.get(owner = user)
        #form.base_fields['owner'].initial = vendor
        return form

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        user = request.user
        vendor = Vendor.objects.get(owner = user)
        obj.vendor = vendor
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('vendor',)
        return self.readonly_fields

    def queryset(self, request):
        qs = super(CommentAdmin, self).queryset(request)
        user = request.user
        vendor = Vendor.objects.get(owner = user)

        return qs.filter(vendor = vendor)

user_admin_site.register(models.Comment, CommentAdmin)


class OrderItemDetailAdmin(admin.TabularInline):
    fields = ('name', 'value',)
    model = models.OrderItemDetail


class OrderItemAdmin(admin.TabularInline):
    #list_display = ('order', 'product', 'quantity', 'price',)
    fields = ('order', 'product', 'quantity', 'price',)
    readonly_fields = ('product', 'quantity', 'price',)
    #inline = (OrderItemDetailAdmin,)
    #fk_name = ''
    can_delete = False
    max_num = 1
    model = models.OrderItem

#user_admin_site.register(models.OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

    def userdetail(self, obj):
        return 'hello'



    readonly_fields = ('vendor', 'date', 'user', 'totalPrice', 'status', 'last_updated', 'deliverUser', 'payment_method','shippingAddress', 'postcode','shippingDistance','deliverTime','deliverFee','totalPrice','comments')
    list_display = ('date', 'status', 'user', 'totalPrice', 'userdetail' )
    list_per_page = 50
    inlines = (OrderItemAdmin,)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        return db_field.formfield(**kwargs)


    exclude = ('vendor',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        #user = request.user
        #vendor = Vendor.objects.get(owner = user)
        #form.base_fields['vendor'].initial = vendor
        return form

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        user = request.user
        vendor = Vendor.objects.get(owner = user)
        obj.vendor = vendor
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('vendor',)
        return self.readonly_fields

    def queryset(self, request):
        qs = super(OrderAdmin, self).queryset(request).select_related('orderitem')
        user = request.user
        vendor = Vendor.objects.get(owner = user)

        return qs.filter(vendor = vendor)

user_admin_site.register(models.Order, OrderAdmin)
#user_admin_site.register(models.Booking, BookingAdmin)

class VendorAdmin2(admin.ModelAdmin):
    pass


class OptionAdmin(admin.TabularInline):
    #list_display = ('order', 'product', 'quantity', 'price',)
    fields = ('name', 'value', 'price',)
    #readonly_fields = ('product', 'quantity', 'price',)
    #inline = (OrderItemDetailAdmin,)
    #fk_name = ''
    model = models.Option


class OptionGroupAdmin(admin.ModelAdmin):
    #readonly_fields = ('vendor', 'date', 'user', 'totalPrice', 'status', 'last_updated', 'deliverUser', 'payment_method','shippingAddress', 'postcode','shippingDistance','deliverTime','deliverFee','totalPrice','comments')
    list_display = ('name', 'description', )
    list_per_page = 50


    inlines = (OptionAdmin,)


class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone','address')
    readonly_fields = ('user','activation_key',)
    list_per_page = 50

admin.site.register(models.RegistrationProfile, RegistrationProfileAdmin)


#admin.site.register(models.ProductOptionGroup)
#admin.site.register(models.Option)
admin.site.register(models.OptionGroup, OptionGroupAdmin)
user_admin_site.register(models.OptionGroup, OptionGroupAdmin)






from django.db.models import Q
from .models import Customer
from .models import Staff
from django.contrib.auth.admin import UserAdmin
class StaffAdmin(UserAdmin):

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
        return qs


    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """


        obj.is_staff = True
        obj.save()







class CustomerAdmin(StaffAdmin):

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
        return qs

admin.site.unregister(User)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Customer, CustomerAdmin)

#AdminSite.register(Vendor, VendorAdmin2)

from django.contrib.gis import admin
import django.contrib.gis.admin
from django.contrib.gis.geos import GEOSGeometry
from models import Vendor

from django.contrib.gis import gdal
gdal.HAS_GDAL = True


from django.contrib.gis import  admin
#from django.contrib.gis.admin.options import OSMGeoAdmin
#class GoogleAdmin(admin.OSMGeoAdmin):
#    g = GEOSGeometry('POINT (9.191884 45.464254)') # Set map center
#    g.set_srid(4326)
#    g.transform(900913)
#    default_lon = int(g.x)
#    default_lat = int(g.y)
#    default_zoom = 7
#    extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"]
#    map_template = 'gmgdav3.html'

#admin.site.register(Vendor, GoogleAdmin)
#admin.site.register(point, GoogleAdmin)

# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users

# Run admin.site.register() for each model we wish to register
# with the REAL django admin!