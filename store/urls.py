from django.urls import path, include

from . import views
from . api import DeliveryListAPIView, DeliveryListCreateAPIView, DeliveryRetrieveUpdateDestroyAPIView


urlpatterns = [
     path('', views.index, name="index"),
     # PRODUCTS
     path('products/', views.product_list, name="product-list"),
     path('products/<int:pk>', views.product_detail, name="product-detail"),
     path('products/create', views.product_create, name="product-create"),
     path('products/<int:pk>/delete', views.product_delete, name="product-delete"),
     path('products/<int:pk>/add-to-cart',views.product_add_to_cart, name="add-to-cart"),
		 

	# USER
     path('profile/', views.profile, name="profile"),
     path('profile/signup', views.signup, name="signup"),
     path('profile/login', views.login, name="login"),
     path('profile/logout', views.logout, name="logout"),
     path('profile/password-reset-request', views.password_reset_request, name="password-reset-request"),
     path('profile/password-reset', views.password_reset, name="password-reset"),
     path('profile/add-address', views.add_address, name="add-address"),
     path('profile/delete-address/<int:pk>', views.delete_address, name="delete-address"),
  	
	
	# CART
     path('cart/', views.cart, name="cart"),
     path('cart/products/<int:pk>/remove-from-cart',views.remove_from_cart, name="remove-from-cart"),
     path('cart/products/<int:pk>/edit-quantity', views.edit_quantity, name="edit-quantity"),
     path('cart/<int:pk>/checkout',views.checkout, name="checkout"),
     path('cart/<int:pk>/make-order-ready-for-delivery',views.make_order_ready_for_delivery, name="make-order-ready-for-delivery"),


    # API
    path('api/v1/', DeliveryListAPIView.as_view()),
    path('api/v1/<int:pk>', DeliveryRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/create', DeliveryListCreateAPIView.as_view()),
    path('api/v1/modify/<int:pk>', DeliveryRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
]
