from django.contrib import admin

from .models import Component, Recipe, Tag, Unit


class ComponentInLine(admin.TabularInline):
    model = Component
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title', 'author',)
    list_filter = ('author', 'pub_date',)
    filter_horizontal = ('components', 'tag',)
    inlines = (ComponentInLine,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    list_filter = ('dimension',)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('unit', 'value')
    search_fields = ('unit',)
    list_filter = ('unit',)
