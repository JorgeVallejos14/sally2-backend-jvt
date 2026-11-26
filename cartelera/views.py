from django.shortcuts import render, get_object_or_404, redirect
from .forms import TicketForm
from .models import Categoria, Espectaculo, Ticket

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

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.espectaculo = espectaculo
            ticket.save()
            return redirect('cartelera:ticket', codigo=ticket.codigo)
    else:
        form = TicketForm(initial={'cantidad': 1})

    contexto = {'espectaculo': espectaculo, 'form': form}
    return render(request, 'cartelera/detalle.html', contexto)


def ticket(request, codigo):
    ticket = get_object_or_404(
        Ticket.objects.select_related('espectaculo'),
        codigo=codigo,
    )
    return render(request, 'cartelera/ticket.html', {'ticket': ticket})