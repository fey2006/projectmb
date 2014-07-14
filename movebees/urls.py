from django.conf.urls import patterns, include, url

#from django.contrib import admin


from shop import views
#from shop import admins
from shop.admins import user_admin_site
from django.contrib.gis import admin
from movebees import settings
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'movebees.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^images/(?P<path>.*)','django.views.static.serve',{'document_root': settings.STATIC_ROOT +  "images" }),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^acct/', include('registration.backends.default.urls')),
    url(r'^api/vendor/list/', views.VendorList.as_view()),
    url(r'^api/vendor/profile/', views.VendorDetail.as_view()),
    url(r'^api/vendor/near', views.NearVendorList.as_view()),
    url(r'^api/product/list/', views.ProductList.as_view()),
    url(r'^api/vendor/detail/', views.VendorDetail.as_view()),
    url(r'^api/category/list/', views.CategoryList.as_view()),
    url(r'^api/comment/list',views.CommentList.as_view()),
    url(r'^api/product/option',views.ProductOption.as_view()),
    url(r'^api/category/detail/',views.ProductByCategory.as_view()),

    url(r'^api/profile/show/',views.ProfileView.as_view()),
    url(r'^api/feedback/new/', views.NewFeedbackView.as_view()),
    url(r'^api/order/detail/', views.OrderDetailView.as_view()),
    url(r'^api/order/create/', views.OrderCreateView.as_view()),
    url(r'^api/order/finish/', views.FinishOrderView.as_view()),
    url(r'^api/report/location/', views.ReportLocationView.as_view()),
    url(r'^api/order/location/',views.OrderGetLocation.as_view()),
    url(r'^api/order/serve/',views.OrderServeView.as_view()),
    url(r'^api/order/list/',views.OrderListView.as_view()),

    #url(r'^useradmin/', include(admins.user_admin_siste.urls)),
    url(r'^api/self/about/', views.CompanyProfileView.as_view()),
    url(r'^api/register/', views.RegisterView.as_view()),
    url(r'^api/test/', views.PurchaseList.as_view()),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'shop.views.activate',name='registration_activate'),
    url(r'^login/$', views.Login.as_view(), name='rest_login'),
    url(r'^logout/$', views.Logout.as_view(), name='rest_logout'),
    url(r'^user/$', views.UserDetails.as_view(),name='rest_user_details'),
    #url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api/booking/list/', views.BookingListView.as_view()),
    url(r'^api/booking/op/', views.BookingEditView.as_view()),
    url(r'^api/like/op', views.FavoriteView.as_view()),
    url(r'^api/like/list',views.FavouriteListViwe.as_view()),
    url(r'^api/order/pending/', views.PendingOrderListView.as_view()),
    url(r'^useradmin/',include(user_admin_site.urls)),
    #url(r'^api/deliver/report/', views.DeliverReportView.as_view()),


)
