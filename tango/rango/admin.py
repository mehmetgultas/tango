#-*-coding:utf-8-*-
from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
