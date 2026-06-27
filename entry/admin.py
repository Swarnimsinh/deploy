# user swarnimsinha
# email sinha@gmail.com
# 12345

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(CartItem)



admin.site.register(Title)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(Portfolio)
admin.site.register(Video)
admin.site.register(WebsiteSettings)