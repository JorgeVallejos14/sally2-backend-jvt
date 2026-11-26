from django.shortcuts import render, get_object_or_404
from .models import Categoria, Espectaculo

# Create your views here.
def inicio(request):
    espectaculos = Espectaculo.objects.select_related('categoria').filter(
        en_cartelera=True
    )

    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')

    if q:
        espectaculos = espectaculos.filter(titulo__icontains=q)
    if categoria_id.isdigit():
        espectaculos = espectaculos.filter(categoria_id=int(categoria_id))

    contexto = {
        'espectaculos': espectaculos,
        'categorias': Categoria.objects.all(),
        'q': q,
        'categoria_sel': categoria_id,
    }
    return render(request, 'cartelera/inicio.html', contexto)


def detalle(request, id):
    espectaculo = get_object_or_404(
        Espectaculo.objects.select_related('categoria'),
        id=id,
        en_cartelera=True,
    )
    return render(request, 'cartelera/detalle.html', {'espectaculo': espectaculo})