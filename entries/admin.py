from django.contrib import admin
from .models import Entry, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_private')
    list_filter = ('is_private', 'tags', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author')
        }),
        ('Содержание', {
            'fields': ('content', 'image', 'is_private')
        }),
        ('Теги', {
            'fields': ('tags',)
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )