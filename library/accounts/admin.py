from django.contrib import admin

from .models import Profile, BookReceipt, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'place_of_study', 'form_of_study']
    raw_id_fields = ['user']
    list_filter = ['form_of_study']
    search_fields = ['user__username', 'place_of_study']

@admin.register(BookReceipt)
class BookReceiptAdmin(admin.ModelAdmin):
    list_display = ['profile', 'book__title', 'date_received', 'date_due']
    list_filter = ['profile', 'book', 'date_received']
    search_fields = ['profile__user__username', 'book__title']
    date_hierarchy = 'date_received'
    raw_id_fields = ['profile', 'book']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)
    list_filter = ('created_at',)

