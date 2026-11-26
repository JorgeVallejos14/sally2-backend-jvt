from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Espectaculo, Ticket

# Register your models here.
admin.site.site_header = "Administracion de la Feria de Knothole"
admin.site.site_title = "Feria de Knothole"
admin.site.index_title = "Gestion de la cartelera"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_espectaculos')
    search_fields = ('nombre',)

    @admin.display(description='Espectaculos')
    def total_espectaculos(self, obj):
        return obj.espectaculos.count()


@admin.register(Espectaculo)
class EspectaculoAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'titulo', 'categoria', 'precio_formateado',
                    'duracion_min', 'sala', 'en_cartelera')
    list_display_links = ('titulo',)
    list_filter = ('categoria', 'en_cartelera')
    search_fields = ('titulo',)
    list_editable = ('en_cartelera',)
    list_select_related = ('categoria',)
    readonly_fields = ('miniatura',)

    @admin.display(description='Afiche')
    def miniatura(self, obj):
        if obj.afiche:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;">',
                obj.afiche.url,
            )
        return '-'

    @admin.display(description='Precio', ordering='precio')
    def precio_formateado(self, obj):
        return obj.precio_clp


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'espectaculo', 'nombre', 'cantidad',
                    'total_formateado', 'creado')
    list_filter = ('espectaculo',)
    search_fields = ('codigo', 'nombre', 'email')
    list_select_related = ('espectaculo',)
    readonly_fields = ('codigo', 'creado')

    @admin.display(description='Total')
    def total_formateado(self, obj):
        return obj.total_clp