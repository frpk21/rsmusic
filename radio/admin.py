from django.contrib import admin

from .models import Generos

from django.contrib.admin.widgets import AutocompleteSelect

class GenerosAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre', )
    list_filter = ('nombre',)

    class Meta:
        model = Generos

admin.site.register(Generos, GenerosAdmin)