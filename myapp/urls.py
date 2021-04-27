
from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('contact/',views.contact,name='contact'),
	path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
 	path('enter_otp/',views.enter_otp,name='enter_otp'),
 	path('enter_email/',views.enter_email,name='enter_email'),
 	path('varify_forgot_otp/',views.varify_forgot_otp,name='varify_forgot_otp'),
 	path('update_password/',views.update_password,name='update_password'),
 	path('logout/',views.logout,name='logout'),
 	path('change_password/',views.change_password,name='change_password'),
 	path('edit_profile/',views.edit_profile,name='edit_profile'),
 	path('sellar_edit_profile/',views.sellar_edit_profile,name='sellar_edit_profile'),
 	path('sellar_change_password/',views.sellar_change_password,name='sellar_change_password'),
 	path('sellar_add_product/',views.sellar_add_product,name='sellar_add_product'),
 	path('sellar_index/',views.sellar_index,name='sellar_index'),
 	path('sellar_view_product/',views.sellar_view_product,name='sellar_view_product'),
 	path('sellar_product_detail/<int:pk>/',views.sellar_product_detail,name='sellar_product_detail'),
 	path('sellar_edit_product/<int:pk>/',views.sellar_edit_product,name='sellar_edit_product'),
 	path('sellar_delete_product/<int:pk>/',views.sellar_delete_product,name='sellar_delete_product'),
 	path('user_view_product/<str:pb>/',views.user_view_product,name='user_view_product'),
 	path('user_product_detail/<int:pid>/',views.user_product_detail,name='user_product_detail'),
 	path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
 	path('mywishlist/',views.mywishlist,name='mywishlist'),
 	path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
 	path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
 	path('mycart',views.mycart,name='mycart'),
 	path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
 	path('change_qty/',views.change_qty,name='change_qty'),
 	path('pay/',views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),


]



