from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

carpeta = Path("afiches_ejemplo")
carpeta.mkdir(exist_ok=True)

afiches = [
    ("tambores", ["Noche de", "Tambores"], "#5b2a86"),
    ("fuga", ["La Fuga de", "Robotropolis"], "#8a1c3d"),
    ("luciernagas", ["Danza de las", "Luciernagas"], "#1f6f5c"),
    ("bosque", ["Concierto", "del Bosque"], "#2f4b9a"),
    ("titeres", ["Titeres de la", "Resistencia"], "#a35a12"),
    ("gala", ["Gala del Rey", "Maximilian"], "#4a4a4a"),
]

fuente_grande = ImageFont.load_default(size=44)
fuente_chica = ImageFont.load_default(size=22)


def centrado(dibujo, texto, y, fuente, color):
    caja = dibujo.textbbox((0, 0), texto, font=fuente)
    ancho = caja[2] - caja[0]
    dibujo.text(((400 - ancho) / 2, y), texto, fill=color, font=fuente)


for nombre, lineas, color in afiches:
    imagen = Image.new("RGB", (400, 600), color)
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle((15, 15, 385, 585), outline="#ffd166", width=6)
    y = 220
    for linea in lineas:
        centrado(dibujo, linea, y, fuente_grande, "#ffffff")
        y += 70
    centrado(dibujo, "Feria de Knothole", 520, fuente_chica, "#ffd166")
    imagen.save(carpeta / f"{nombre}.png")

print("Afiches creados en la carpeta afiches_ejemplo")