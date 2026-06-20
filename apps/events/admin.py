from django.contrib import admin
from apps.events.models import Event
from apps.events.models import Category


@admin.register(Category)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'organizer', 'date', 'category','location', 'seats', 'created_at', 'updated_at')
    def formfield_for_foreignkey(self,db_field, request, **kwargs):
        if db_field.name == 'organizer':
            kwargs['queryset'] = db_field.related_model.objects.filter(is_organizer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    autocomplete_fields = ['location']
    search_fields = ('title', 'date', 'location__city', 'location__state', 'location__region', 'location__zip_code', 'location__street_address', 'created_at', 'updated_at')
