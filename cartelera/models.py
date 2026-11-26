import uuid
from django.db import models

# Create your models here.
def formato_clp(valor):
    return f"${valor:,}".replace(",", ".")


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Espectaculo(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='espectaculos',
    )
    titulo = models.CharField(max_length=120)
    afiche = models.ImageField(upload_to='afiches/')
    precio = models.PositiveIntegerField()
    en_cartelera = models.BooleanField(default=True)
    duracion_min = models.PositiveSmallIntegerField()
    sala = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    @property
    def precio_clp(self):
        return formato_clp(self.precio)


class Ticket(models.Model):
    espectaculo = models.ForeignKey(
        Espectaculo,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    cantidad = models.PositiveSmallIntegerField()
    creado = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=12, unique=True, editable=False)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"{self.codigo} - {self.espectaculo}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self._generar_codigo()
        super().save(*args, **kwargs)

    @staticmethod
    def _generar_codigo():
        while True:
            codigo = uuid.uuid4().hex[:8].upper()
            if not Ticket.objects.filter(codigo=codigo).exists():
                return codigo

    @property
    def total(self):
        return self.espectaculo.precio * self.cantidad

    @property
    def total_clp(self):
        return formato_clp(self.total)