from django.db import models
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
# Create your models here.

from django.contrib.auth.models import User
#from django.contrib.gis.db import models as geomodels
from datetime import datetime
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
import geocoder
DB_LENGTH = 32

class Vendor(models.Model):
    name = models.CharField(max_length=DB_LENGTH, db_index=True)
    address = models.CharField(max_length=128)
    postcode = models.PositiveIntegerField()
    email = models.EmailField()
    logo = models.ImageField(upload_to='images/Vendors/main/')
    phone = models.CharField(max_length=16)
    description = models.CharField(max_length=512)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    openhour = models.TimeField()
    closehour = models.TimeField()
    owner = models.ForeignKey(User,null=True)


    #location = gis_models.PointField(u"longitude/latitude",
    #                                 geography=True)

    #gis = gis_models.GeoManager()
    #objects = models.Manager()


    def __unicode__(self):
        return self.name


#class UserProfile(models.Model):
#    user = models.OneToOneField(User,related_name='reg')
#    phone = models.CharField(max_length=16)
#    address = models.CharField(max_length=64)




from django.utils.text import slugify
import datetime

from django.utils.encoding import smart_text
from django.utils.encoding import smart_unicode
from urllib import quote
class Category(models.Model):
    owner = models.ForeignKey(Vendor)
    #name = models.CharField(max_length=16, db_index=True)
    name = models.SlugField(max_length=16)
    title = models.CharField(max_length=DB_LENGTH)
    description = models.CharField(max_length=256)
    #created = models.IntegerField()
    order = models.IntegerField(default=0)
    updateDate = models.DateTimeField(datetime.datetime.now())



    def save(self,*args,**kwargs):
        self.name = self.title
        self.updateDate = datetime.datetime.now()
        self.order = 0
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s|%s' % (self.owner.name, self.name)

    class Meta:
        unique_together = ('owner','name')

class Product(models.Model):
    vendor = models.ForeignKey(Vendor)
    category = models.ForeignKey(Category, related_name='products')
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    name = models.CharField(max_length=50)
    userlikes = models.BigIntegerField(default=0)
    description = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='images/product_photo', blank=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class OptionGroup(models.Model):
    """
    A set of options that can be applied to an item.
    Examples - Size, Color, Shape, etc
    """
    vendor = models.ForeignKey(Vendor, verbose_name=_('Vendor'))
    name = models.CharField(_("Name of Option Group"), max_length=50,
        help_text=_("This will be the text displayed on the product page."))
    description = models.CharField(_("Detailed Description"), max_length=100,
        blank=True,
        help_text=_("Further description of this group (i.e. shirt size vs shoe size)."))
    sort_order = models.IntegerField(_("Sort Order"),
        help_text=_("The display order for this group."), default=0)

    #objects = OptionGroupManager()

    def __unicode__(self):
        if self.description:
            return u"%s - %s" % (self.name, self.description)
        else:
            return self.name

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = _("Option Group")
        verbose_name_plural = _("Option Groups")




class Option(models.Model):
    """
    These are the actual items in an OptionGroup.  If the OptionGroup is Size, then an Option
    would be Small.
    """
    option_group = models.ForeignKey(OptionGroup,related_name='options')
    name = models.CharField(_("Display value"), max_length=50, )
    value = models.CharField(_("Stored value"), max_length=50)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)


class ProductOptionGroup(models.Model):
    productid = models.ForeignKey(Product)
    optiongroupid = models.ForeignKey(OptionGroup)


#class Deliver(models.Model):
#    fromAddr = models.ForeignKey(User)
#    toAddr = models.ForeignKey(User)
#    orders = models.ManyToManyField(Order)



class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product)

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def augment_quantity(self, quantity):
        self.quantity += int(quantity)
        self.save()

import decimal
class Order(models.Model):
    #each individual status
    #pending , open, doing, billing, closed
    PROCESSING = 1
    UNDERWAY = 2
    UNPAID = 3
    PAID = 4
    ORDER_STATUSES = ((PROCESSING, 'Processing'),
                      (UNDERWAY, 'Underway'),
                      (UNPAID, 'Unpaid'),
                      (PAID, 'Paid'),)
    vendor = models.ForeignKey(Vendor)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=PROCESSING)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, related_name='customer')
    deliverUser = models.ForeignKey(User, null=True, related_name='deliverman')
    #transaction_id = models.CharField(max_length=20)

    #contact info
    shippingAddress = models.CharField(max_length=128,null=True)
    postcode = models.CharField(max_length=16, default='000000')
    shippingDistance = models.FloatField(default=0)
    deliverTime = models.DateTimeField(null=True)

    deliverFee = models.DecimalField(max_digits=9, decimal_places=2,default=0)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)
    comments = models.CharField(max_length=256,default='')


    CASH_ON_DELIVER = 1
    NETS = 2
    PAYPAL = 3

    PAY_METHODS = (
        (CASH_ON_DELIVER, 'Cash'),
        (NETS, 'Nets'),
        (PAYPAL, 'Paypal')
    )

    payment_method = models.IntegerField(choices=PAY_METHODS, default=CASH_ON_DELIVER)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='lineitems')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def show(self):
        return self.option_values.all()

    def __unicode__(self):
        queryset = self.option_values.all()
        if not queryset:
            return self.product.name
        else:
            res = ''
            for item in queryset:
                res = res + '%s:%s\n' % (item.name, item.value)
            return res

    @property
    def total(self):
        return self.quantity * self.price

class OrderItemDetail(models.Model):
    orderitem = models.ForeignKey(OrderItem, related_name='option_values')
    value = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

class DeliveryAddressReport(models.Model):
    order = models.ForeignKey(Order)
    deliverMan = models.ForeignKey(User)


import datetime

class Feedback(models.Model):
    content = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now_add=datetime.datetime.now())

class CompanyProfile(models.Model):
    email = models.EmailField()
    bookingNo = models.CharField(max_length=32)
    businessNo = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    terms = models.CharField(max_length=1024)
    published = models.BooleanField()

class Favourite(models.Model):
    user = models.ForeignKey(User,db_index=True)
    product = models.ForeignKey(Product)
    updated = models.DateTimeField(auto_now=True)

from django.db import models
#from django_comments.models import Comment

#class CommentWithTitle(Comment):
#    title = models.CharField(max_length=300)
#    vendor = models.ForeignKey(Vendor)


class Booking(models.Model):
    vendor = models.ForeignKey(Vendor)
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    persons = models.IntegerField()



#from django.contrib import admin

#admin.site.register(Vendor)

#from django.contrib.gis import admin




#admin.Vendor.register(Product)
#admin.Vendor.register(Category)
#admin.site.register(CartItem)

#from shop.admins import user_admin_site




import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import now as datetime_now
from django.utils.translation import ugettext_lazy as _


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    """
    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True, verbose_name=_('user'), related_name='reguser')
    activation_key = models.CharField(_('activation key'), max_length=40)


    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=64)
    is_deliver = models.BooleanField(default=False)

    class Meta:
        app_label = 'shop'

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        Key expiration is determined by a two-step process:
        1. If the user has already activated, the key will have been
        reset to the string constant ``ACTIVATED``. Re-activating
        is not permitted, and so this method returns ``True`` in
        this case.

        2. Otherwise, the date the user signed up is incremented by
        the number of days specified in the setting
        ``REGISTRATION_API_ACCOUNT_ACTIVATION_DAYS`` (which should be
        the number of days after signup during which a user is allowed
        to activate their account); if the result is less than or
        equal to the current date, the key has expired and this method
        returns ``True``.

        """

        # utils imported here to avoid circular import
        import utils

        expiration_date = datetime.timedelta(
            days=utils.get_settings('REGISTRATION_API_ACCOUNT_ACTIVATION_DAYS'))
        return self.activation_key == self.ACTIVATED or \
            (self.user.date_joined + expiration_date <= datetime_now())


class DeliverReport(models.Model):
    order = models.ForeignKey(Order)
    user = models.ForeignKey(User)
    lon = models.FloatField()
    lat = models.FloatField()
    location = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         unique_together = ('order','user','updated')


class Comment(models.Model):
    user = models.ForeignKey(User)
    vendor = models.ForeignKey(Vendor)
    content = models.CharField(max_length=256)
    updated = models.DateTimeField(auto_now=True)


class Customer(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Customer account'
        verbose_name_plural = 'Customer accounts'

class Staff(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Staff account'
        verbose_name_plural = 'Staff accounts'