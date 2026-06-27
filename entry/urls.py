from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',login,name='login'),
    path('profile/', profile, name='profile'),
    

    path('meetings/create/', create_meeting),
    path('all_meetings/', all_meetings),
    path('my_meetings/', my_meetings),
    
    path('products/', products, name='products'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:id>/',remove_from_cart,name='remove_from_cart'),
    
    

    path('title/', get_title),
    path('title/update/',update_title),

    path('portfolio/',get_portfolios),

    path('portfolio/<int:pk>/update/',update_portfolio),

    path('services/', SView),
    path('testimonials/', TView),
    path('testimonials/update/', update_testimonials),
    
    path('settings/', get_settings),
    path('settings/update/', update_settings),
    path('settings/upload_video/', upload_video),
   
    path('videos/', VView),

]

