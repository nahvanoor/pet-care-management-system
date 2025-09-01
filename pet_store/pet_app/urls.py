from django.urls import path,include
from . import views


urlpatterns = [
    path("",views.home),
    path('login',views.login),
    path('register',views.register),
    path('admin_home',views.admin_home),
    path('user_home',views.user_home),
    path('trainer_home',views.trainer_home),
    path('petstore_home',views.petstore_home),
    path('profile',views.profile),
    path('edit_profile/<id>/',views.edit_profile),
    path('add_pets',views.add_pets),
    path('add_pet_foods',views.add_pet_foods),
    path('add_pet_accessories',views.add_pet_accessories),
    path('edit_pets/<id>',views.edit_pets),
    path('delete_pets/<id>',views.delete_pets),
    path('edit_foods/<id>',views.edit_foods),
    path('delete_foods/<id>',views.delete_foods),
    path('edit_accessories/<id>',views.edit_accessories),
    path('delete_accessories/<id>',views.delete_accessories),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<str:type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity')
]