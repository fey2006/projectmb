__author__ = 'yef'

from models import Vendor
from models import Product
from models import Category
from models import RegistrationProfile
from models import Feedback
from models import CartItem
from models import Booking
from models import Order
from models import CompanyProfile
from models import Favourite
from models import ProductOptionGroup
from django.contrib.auth.models import User
from django.db.models import Q

def getVendorList():
    try:
        return Vendor.objects.all()
    except Exception as ex:
        print ex


def getProductList(vendorid):
    try:
        return Product.objects.filter(vendor_id = vendorid).all()

    except Exception as ex:
        return None

def getProductByCate(cateid):
    try:
        return Product.objects.filter(category_id = cateid).all()

    except Exception as ex:
        return None


def getVendor(vendorid):
    try:
        return Vendor.objects.get(pk = vendorid)
    except Exception as ex:
        return None

def getCategoryList(vendorid):
    try:
        return Category.objects.filter(owner_id = vendorid)
    except Exception as ex:
        return None

def getProductsByCate(cateid):
    try:
        return Product.objects.filter(category_id = cateid)
    except Exception as ex:
        return None


def getUserProfile(userid):
    try:
        return RegistrationProfile.objects.get(pk = userid)
    except Exception as ex:
        return None

def getUser(userid):
    try:
        return User.objects.get(pk = userid)
    except Exception as ex:
        return None

def addFeedback(user, content):
    try:
        obj, created = Feedback.objects.get_or_create(user = user, content = content)
        obj.save()
        return True

    except Exception as ex:
        return False


def getCompanyProfile():
    try:
        obj = CompanyProfile.objects.get(published = True)
        return obj
    except Exception as ex:
        return None

def getBookings(uid):
    try:
        return Booking.objects.filter(user_id = uid)
    except Exception as ex:
        return None

def getBookingByid(id):
    try:
        obj = Booking.objects.get(pk = id)
        return obj
    except Exception as ex:
        return None


def getProductByid(pid):
    try:
        return Product.objects.get(pk = pid)
    except Exception as ex:
        return None

def removelike(pid, uid):
    try:
        obj = Favourite.objects.get(Q(product_id = pid) and Q(user_id = uid))
        obj.delete()
    except Exception as ex:
        return

def addlike(pid, uid):
    try:
        obj, created = Favourite.objects.get_or_create(product_id = pid, user_id = uid)
        obj.save()
    except Exception as ex:
        return


import random
def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

def getOrderById(orderid):
    try:
        return Order.objects.get(pk = orderid)
    except Exception as ex:
        return None

def getOrdersByUser(user):
    try:
        return Order.objects.filter(user = user ).order_by('last_updated')
    except Exception as ex:
        return None


def getPendingOrder():
    try:
        return Order.objects.filter(status = Order.PENDING)
    except Exception as ex:
        return None


from models import DeliverReport

def getOrderLocation(orderid):
    try:
        return DeliverReport.objects.filter(order_id = orderid)
    except Exception as ex:
        return None

from models import Comment
def getCommentsByVendor(vendorid):
    try:
        return Comment.objects.filter(vendor_id = vendorid).order_by('updated')
    except Exception as ex:
        return None

def getFavouriteByUser(userid):
    try:
        return Favourite.objects.filter(user_id = userid).order_by('updated')
    except Exception as ex:
        return None