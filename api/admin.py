from django.contrib import admin
from api.infrastructure.models import ProductModel, LogModel, ProductQuery
from api.models import User
# Register your models here.
admin.site.register(User)
admin.site.register(ProductModel)
admin.site.register(LogModel)
admin.site.register(ProductQuery)
