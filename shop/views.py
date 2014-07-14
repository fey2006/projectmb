from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework import generics

import serializers

import logic
from serializers import VendorSerializer,ProductSerializer
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from geopy import distance
from geopy import Point
from geopy import Point
from geopy import distance
class VendorList(APIView):

    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        try:
            lat = request.DATA.get('lat',None)
            lon = request.DATA.get('lon',None)
            sorttype = request.DATA.get('sorttype', None)
            pagesize = request.DATA.get('pagesize', None)
            curpage = request.DATA.get('curpage', None)

            print '%s,%s,%s' % (sorttype,pagesize,curpage)

            if not sorttype or not pagesize or not curpage:
                return Response(self.ret)


            queryset = logic.getVendorList()

            if queryset == None:
                return Response(self.ret)

            paginator = Paginator(queryset, pagesize)
            try:
                vendors = paginator.page(curpage)
            except PageNotAnInteger:
                vendors = paginator.page(1)
            except EmptyPage:
                vendors = paginator.page(paginator.num_pages)

            serializer = serializers.SimpleVendorSerializer(vendors.object_list, many=True)

            response = {}
            response['vendor'] = serializer.data

            p1 = Point(latitude=lat, longitude=lon)
            for item in response['vendor']:
                lat = item['latitude']
                lon = item['longitude']

                p2 = Point(latitude=lat, longitude=lon)
                item['distance'] = distance.distance(p1, p2).km

            response['success'] = 0

            return Response(response)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print ex
            return Response(self.ret)



class NearVendorList(APIView):

    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        x = request.DATA.get('x')
        y = request.DATA.get('y')
        sorttype = request.DATA.get('sorttype', None)
        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        return Response(self.ret)




class PurchaseList(generics.ListAPIView):
    queryset = logic.getVendorList()
    serializer_class = VendorSerializer
    paginate_by = 1
    paginate_by_param = 'page_size'
    max_paginate_by = 100



class ProductDetail(APIView):
    ret = {
        'success': -1
    }
    def post(self, request, format = None):
        lat = request.DATA.get('lat',None)
        lon = request.DATA.get('lon',None)

        return Response(self.ret)


class ProductOption(APIView):

    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        productid = request.DATA.get('productid',None)

        from models import ProductOptionGroup

        objs = ProductOptionGroup.objects.filter(productid = productid)

        options = []
        for item in objs:
            options.append(item.optiongroupid)



        serializer = serializers.OptionGroupSerializer(options, many=True)


        response = serializer.data

        return Response(response)


class ProductByCategory(APIView):

    ret = {
        'success': -1
    }
    def post(self, request, format = None):

        categoryid = request.DATA.get('category', None)
        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        print '%s,%s,%s' % (categoryid, pagesize,curpage)

        if not categoryid or not pagesize or not curpage:
            return Response(self.ret)

        print 'yes'


        dataset = logic.getProductsByCate(categoryid)

        if dataset == None:
            return Response(self.ret)

        print 'es'

        paginator = Paginator(dataset, pagesize)
        try:
            queryset = paginator.page(curpage)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = serializers.SimpleProductSerializer(queryset.object_list, many=True)

        response = {}
        response['products'] = serializer.data
        response['success'] = 1

        return Response(response)



class ProductList(APIView):

    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        lat = request.DATA.get('lat',None)
        lon = request.DATA.get('lon',None)
        vendorid = request.DATA.get('vendorid', None)
        sorttype = request.DATA.get('sorttype', None)
        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        print '%s, %s,%s,%s' % (vendorid, sorttype,pagesize,curpage)

        if not vendorid or not sorttype or not pagesize or not curpage:
            return Response(self.ret)

        print 'yes'


        dataset = logic.getProductList(vendorid)

        if dataset == None:
            return Response(self.ret)

        print 'es'

        paginator = Paginator(dataset, pagesize)
        try:
            queryset = paginator.page(curpage)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = serializers.SimpleProductSerializer(queryset.object_list, many=True)

        p1 = Point(latitude=lat, longitude=lon)
        response = {}
        response['products'] = serializer.data
        for item in response['products']:
            lat = item['lat']
            lon = item['lon']
            p2 = Point(latitude=lat, longitude=lon)
            item['distance'] = distance.distance(p1, p2).km

        response['success'] = 1

        return Response(response)


class VendorDetail(APIView):

    ret = {
        'success': -1
    }

    def post(self, request, format = None):
        vendorid = request.DATA.get('vendorid', None)

        if not vendorid:
            return Response(self.ret)

        queryset = logic.getVendor(vendorid)
        if queryset == None:
            return Response(self.ret)

        serializer = VendorSerializer(queryset)

        response = serializer.data

        response['success'] = 0
        return Response(response)


class CategoryList(APIView):

    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        vendorid = request.DATA.get('vendorid', None)
        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        print '%s, %s,%s' % (vendorid,pagesize,curpage)

        if not vendorid or not pagesize or not curpage:
            return Response(self.ret)


        dataset = logic.getCategoryList(vendorid)

        if dataset == None:
            return Response(self.ret)

        paginator = Paginator(dataset, pagesize)
        try:
            queryset = paginator.page(curpage)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = serializers.CateListResponse(instance=queryset)

        response = serializer.data
        response['success'] = 0
        return Response(response)



class CategoryDetail(APIView):

    ret = {
        'ret': -1
    }


    def post(self, request, format = None):
        categoryid = request.DATA.get('categoryid', None)
        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        print '%s, %s,%s' % (categoryid,pagesize,curpage)

        if not categoryid or not pagesize or not curpage:
            return Response(self.ret)


        dataset = logic.getProductsByCate(categoryid)

        if dataset == None:
            return Response(self.ret)

        paginator = Paginator(dataset, pagesize)
        try:
            queryset = paginator.page(curpage)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = serializers.SimpleProductSerializer(instance=queryset)

        products = serializer.data
        response = {}
        response['products'] = products
        response['ret'] = 0
        return Response(response)


class ProfileView(APIView):

    ret = {
        'ret': -1
    }


    def post(self, request, format = None):
        userid = request.DATA.get('userid', None)

        if not userid:
            return Response(self.ret)


        dataset = logic.getUserProfile(userid)

        if dataset == None:
            return Response(self.ret)

        serializer = serializers.ProfileSerializer(dataset)

        response = serializer.data
        response['ret'] = 0
        return Response(response)

class NewFeedbackView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        userid = request.DATA.get('userid', None)
        content = request.DATA.get('content', None)

        if not userid or not content:
            return Response(self.ret)

        user = logic.getUser(userid)

        if not user:
            return Response(self.ret)

        created = logic.addFeedback(user, content)

        if created:
            self.ret['success'] = 0

            return Response(self.ret)

        else:
            return Response(self.ret)


class OrderDetailView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        orderid = request.DATA.get('orderid', None)

        if not orderid:
            return Response(self.ret)

        order = logic.getOrderById(orderid)

        if not order:
            return Response(self.ret)


        serializer = serializers.Order2Serializer(order)

        response = serializer.data

        return Response(response)


class CompanyProfileView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        queryset = logic.getCompanyProfile()

        if not queryset:
            return Response(self.ret)


        serializer = serializers.CompanySerializer(queryset)

        response = serializer.data

        return Response(response)

class BookingListView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        userid = request.DATA.get('userid', None)

        if not userid:
            return Response(self.ret)

        queryset = logic.getBookings(userid)

        if not queryset:
            return Response(self.ret)

        serializer = serializers.BookingSerializer(queryset)

        response = serializer.data

        return Response(response)

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

import utils

class RegisterView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        print 'aaa'

        firstname = request.DATA.get('firstname', None)
        lastname = request.DATA.get('lastname', None)
        email = request.DATA.get('email', None)
        password = request.DATA.get('password', None)

        if not utils.is_email_available(email):
            return Response(self.ret)

        user = utils.create_inactive_user(username=email, email=email, password=password, firstname = firstname, lastname = lastname)
        #if user:
        #    user.first_name = firstname
        #    user.last_name = lastname
        #    user.save()

        ret = {
            'success':0
        }

        return Response(ret)
from django.shortcuts import render_to_response
def activate(request, activation_key=None):
    """
    Given an an activation key, look up and activate the user
    account corresponding to that key (if possible).

    """

    print 'activate'
    utils.activate_user(activation_key)
    # if not activated
    success_url = utils.get_settings('REGISTRATION_API_ACTIVATION_SUCCESS_URL')
    if success_url is not None:
        return render_to_response('registration/activation_complete.html')

from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from serializers import TokenSerializer
from serializers import LoginSerializer
from serializers import UserProfileUpdateSerializer
from serializers import UserDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView

class LoggedInRESTAPIView(APIView):
    authentication_classes = ((SessionAuthentication, TokenAuthentication))
    permission_classes = ((IsAuthenticated,))


class LoggedOutRESTAPIView(APIView):
    permission_classes = ((AllowAny,))


class Login(LoggedOutRESTAPIView, GenericAPIView):

    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        # Create a serializer with request.DATA
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            # Authenticate the credentials by grabbing Django User object
            user = authenticate(username=serializer.data['username'],
                                password=serializer.data['password'])

            if user and user.is_authenticated():
                if user.is_active:
                    # TODO: be able to configure this to either be
                    # session or token or both
                    # right now it's both.
                    login(request, user)

                    # Return REST Token object with OK HTTP status
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(TokenSerializer(token).data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'This account is disabled.'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid Username/Password.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login, logout, get_user_model
class Logout(LoggedInRESTAPIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class UserDetails(LoggedInRESTAPIView, GenericAPIView):

    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """

    serializer_class = UserProfileUpdateSerializer

    def get(self, request):
        # Create serializers with request.user and profile
        user_details = UserDetailsSerializer(request.user)
        serializer = self.serializer_class(request.user.get_profile())

        # Send the Return the User and its profile model with OK HTTP status
        return Response({
            'user': user_details.data,
            'profile': serializer.data},
            status=status.HTTP_200_OK)

    def post(self, request):
        # Get the User object updater via this Serializer
        serializer = self.serializer_class(
            request.user.get_profile(), data=request.DATA, partial=True)

        if serializer.is_valid():
            # Save UserProfileUpdateSerializer
            serializer.save()

            # Return the User object with OK HTTP status
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Return the UserProfileUpdateSerializer errors with Bad Request
            # HTTP status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from models import Booking
class BookingEditView(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        op = request.DATA.get('op')

        if op not in ['add', 'del']:
            return Response(self.ret)

        userid = request.user.pk

        if op == 'del':
            bookingid = request.DATA.get('id')
            if not bookingid:
                return Response(self.ret)

            obj = logic.getBookingByid(bookingid)
            if obj:
                obj.delete()
                response = {'success': 0}
                return Response(response)
            else:
                return Response(self.ret)

        elif op == 'add':
            date = request.DATA.get('date')
            persons = request.DATA.get('persons')
            vendor_id = request.DATA.get('vendorid')

            obj, created = Booking.objects.get_or_create(vendor_id = vendor_id, user_id = userid, persons = persons, date = date)
            if created:
                obj.save()

            response = {'success': 0}
            response["id"] = obj.pk
            return Response(response)
        else:
            return Response(self.ret)


class FavoriteView(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        op = request.DATA.get('op')

        if op not in ['add', 'del']:
            return Response(self.ret)

        userid = request.user.pk

        if op == 'del':
            id = request.DATA.get('id')
            if not id:
                return Response(self.ret)

            obj = logic.getProductByid(id)
            if obj:
                obj.userlikes -= 1
                logic.removelike(id, userid)
                obj.save()
                response = {'success': 0, 'like':obj.userlikes}
                return Response(response)
            else:
                return Response(self.ret)

        elif op == 'add':
            pid = request.DATA.get('id')
            obj = logic.getProductByid(pid)
            if obj:
                logic.addlike(pid, userid)
                obj.userlikes += 1
                obj.save()
                response = {'success': 0, 'like': obj.userlikes}
                return Response(response)
            else:
                return Response(self.ret)


        else:
            return Response(self.ret)


class FavouriteListViwe(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        try:
            userid = request.DATA.get('userid')
            curpage = request.DATA.get('curpage')
            pagesize = request.DATA.get('pagesize')

            if not userid:
                return Response(self.ret)

            likes = logic.getFavouriteByUser(userid)

            products = []
            for item in likes:
                products.append(item.product)

            paginator = Paginator(products, pagesize)
            try:
                queryset = paginator.page(curpage)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)

            serializer = serializers.SimpleProductSerializer(queryset.object_list, many=True)

            response = {}
            response['products'] = serializer.data
            response['success'] = 0

            return Response(response)

        except Exception as ex:
            return Response(self.ret)


from serializers import SimpleOrderSerializer

class PendingOrderListView(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        pagesize = request.DATA.get('pagesize', None)
        curpage = request.DATA.get('curpage', None)

        queryset = logic.getPendingOrder()

        if queryset == None:
            return Response(self.ret)

        paginator = Paginator(queryset, pagesize)
        try:
            vendors = paginator.page(curpage)
        except PageNotAnInteger:
            vendors = paginator.page(1)
        except EmptyPage:
            vendors = paginator.page(paginator.num_pages)

        serializer = SimpleOrderSerializer(vendors.object_list, many=True)

        response = serializer.data

        return Response(response)

from models import Order
class ChooseDeliverOrderView(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        orderid = request.DATA.get('orderid', None)

        obj = logic.getOrderById(orderid)

        if not obj:
            return Response(self.ret)

        userid = request.user.pk


        if obj.status == Order.PENDING:
            obj.deliverUser = request.user
            obj.status = Order.PROCESSING
            obj.save()

            response = {'success' : 0}
            return Response(response)

        else:
            return Response(self.ret)


class DeliverReportView(LoggedInRESTAPIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        orderid = request.DATA.get('orderid', None)

        obj = logic.getOrderById(orderid)

        if not obj:
            return Response(self.ret)

        userid = request.user.pk

        location = 'dummy location'

        from models import DeliverReport

        obj, created = DeliverReport.objects.get_or_create(user = request.user, order = obj, location = location)

        obj.save()

        response = {'success': 0}

        return Response(response)

from django.db import transaction

class OrderCreateView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:
            with transaction.atomic():
                print type(request.DATA)
                serializer = serializers.Order2Serializer(data=request.DATA)
                print request.DATA



                if serializer.is_valid():
                    obj = serializer.object
                    obj.save()
                    items = request.DATA.get('products')
                    print items
                    if not items:
                        return Response(self.ret)
                    print type(items)
                    serializer = serializers.OrderItemSerializer(data = items, many=True)

                    if serializer.is_valid():
                        orderitems = serializer.object

                        for i in range(len(orderitems)):
                            orderitem = orderitems[i]
                            orderitem.order_id = obj.id
                            orderitem.save()

                            options = items[i]['option_values']

                            if options:
                                serializer = serializers.OrderItemDetailSerializer(data = options, many=True)
                                if serializer.is_valid():
                                    options = serializer.object
                                    for option in options:
                                        option.orderitem_id = orderitem.id
                                        option.save()


                            print dir(orderitem)

                            #print orderitem.objects
                            print orderitem.option_values.all()





                    print serializer.is_valid()

                    products = serializer.object
                    print products

                    obj.save()
                    #products.save()

                    response = {'success':0}
                    return Response(response)
                else:
                    return Response(self.ret)
        except Exception as ex:
            print ex
            import traceback
            traceback.print_exc()
            return Response(self.ret)

class OrderListView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:
            userid = request.DATA.get('userid', None)
            curpage = request.DATA.get('curpage', None)
            pagesize = request.DATA.get('pagesize',None)

            if not userid:
                return Response(self.ret)

            user = logic.getUser(userid)
            if not user:
                return Response(self.ret)



            dataset = logic.getOrdersByUser(user)

            if not dataset:
                return Response(self.ret)

            paginator = Paginator(dataset, pagesize)
            try:
                queryset = paginator.page(curpage)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)

            serializer = serializers.Order2Serializer(queryset.object_list, many=True)

            response = {}
            response['orders'] = serializer.data

            return Response(response)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print ex
            return Response(self.ret)


class FinishOrderView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:

            orderid = request.DATA.get('orderid', None)
            userid = request.DATA.get('userid', None)
            statustype = request.DATA.get('type', None)

            if not orderid or not userid or not statustype:
                return Response(self.ret)

            obj = logic.getOrderById(orderid)

            if not obj:
                return Response(self.ret)

            if obj.deliverUser_id != userid:
                return Response(self.ret)

            if statustype == 'paid':
                obj.status = obj.PAID
            elif statustype == 'unpaid':
                obj.status = obj.UNPAID
            else:
                return Response(self.ret)

            obj.save()

            response = {'success': 0}

            return Response(response)
        except Exception as ex:
            return Response(self.ret)


from shop.models import DeliverReport
import urllib2
import json
from geopy.geocoders import GoogleV3
from movebees.settings import GOOGLE_SECRET_KEY
class ReportLocationView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:
            print request.DATA
            orderid = request.DATA.get('orderid', None)
            userid = request.DATA.get('userid', None)
            lon = request.DATA.get('lon', None)
            lat = request.DATA.get('lat', None)

            if not orderid or not userid or not lon or not lat:
                return Response(self.ret)

            latlon = '%s,%s' % (lat,lon)

            curUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s&key=%s' % (latlon, 'AIzaSyAe50PasAkJ_JS4hJZfFnrIKqqmprjp1Lc')
            print curUrl
            j = urllib2.urlopen(curUrl)
            js = json.load(j)

            print js
            ourResult = js['results'][0]['formatted_address']

            locatin = ourResult

            print locatin

            order = logic.getOrderById(orderid)
            if not order:
                return Response(self.ret)

            user = logic.getUser(userid)

            if not user:
                return Response(self.ret)

            obj, created = DeliverReport.objects.get_or_create(order = order, user = user, location = locatin, lon = float(lon), lat = float(lat))


            obj.save()

            response = {'success': 0}

            return Response(response)
        except Exception as ex:
            print ex
            return Response(self.ret)

class OrderServeView(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:

            orderid = request.DATA.get('orderid', None)
            userid = request.DATA.get('userid', None)

            if not orderid or not userid:
                return Response(self.ret)


            order = logic.getOrderById(orderid)
            if not order:
                return Response(self.ret)

            user = logic.getUser(userid)


            if order.deliverUser:
                return Response(self.ret)
            else:
                order.deliverUser = user
            order.save()
            response = {}
            response['success'] = 0

            return Response(response)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print ex
            return Response(self.ret)


class OrderGetLocation(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):

        try:

            orderid = request.DATA.get('orderid', None)
            userid = request.DATA.get('userid', None)

            if not orderid or not userid:
                return Response(self.ret)


            orders = logic.getOrderLocation(orderid)
            if not orders:
                return Response(self.ret)


            serializer = serializers.LocationSerializer(orders, many=True)

            response = {}
            response['locations'] = serializer.data
            print response
            response['success'] = 0

            return Response(response)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print ex
            return Response(self.ret)


class CommentList(APIView):
    ret = {
        'success': -1
    }


    def post(self, request, format = None):
        try:
            vendorid = request.DATA.get('vendorid', None)
            pagesize = request.DATA.get('pagesize', None)
            curpage = request.DATA.get('curpage', None)

            print '%s,%s' % (pagesize,curpage)

            if not vendorid or not pagesize or not curpage:
                return Response(self.ret)


            dataset = logic.getCommentsByVendor(vendorid)

            if dataset == None:
                return Response(self.ret)

            paginator = Paginator(dataset, pagesize)
            try:
                queryset = paginator.page(curpage)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)

            serializer = serializers.CommentSerializer(queryset.object_list, many=True)

            response = {}
            response['comments'] = serializer.data

            return Response(response)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print ex
            return Response(self.ret)