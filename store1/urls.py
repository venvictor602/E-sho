from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('contact/', views.contact, name="contact"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_Item/', views.update_item, name="update_Item"),
    path('processOrder/', views.processOrder, name="processOrder"),
    path('login/', views.Login, name="login"),
    path('Signup/', views.Signup, name="Signup"),
    path('logout/', views.logoutUser, name="logout")
]