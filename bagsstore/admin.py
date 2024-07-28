from django.contrib import admin

# Register your models here.

from bagsstore.models import Category,Type,Size,Brand,Tag,Colour,Bag

admin.site.register(Category)

admin.site.register(Type)

admin.site.register(Size)

admin.site.register(Brand)

admin.site.register(Tag)

admin.site.register(Colour)

admin.site.register(Bag)


