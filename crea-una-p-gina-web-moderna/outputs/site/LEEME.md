# Basurero Inteligente · Proyecto Arduino 2026

Una página de presentación en español, hecha con HTML, CSS y JavaScript.

## Abrir la página

Abre `index.html` con Chrome, Edge, Firefox o cualquier navegador moderno. No necesitas instalar herramientas ni compilar el proyecto. Conserva los archivos y la carpeta `assets` juntos.

La página funciona sin conexión. Las tipografías de Google se cargan cuando hay acceso a Internet; sin conexión se usan las fuentes alternativas del sistema.

## Cambiar nombres y fotografías

En la parte superior de `script.js`, edita el objeto `PROJECT`:

- `team`: reemplaza los nombres de los integrantes. Puedes agregar o quitar integrantes.
- `photos`: coloca la ruta de cada fotografía en `src` y su descripción en `alt`. Por ejemplo, `src: 'assets/prototipo.jpg'`.

Copia las fotos a la carpeta `assets`. Los tres espacios de galería se mantienen como reservas hasta que agregues fotografías. Si una foto no se encuentra, se conserva el espacio reservado.

Ejemplo de integrante:

```js
{ name: 'Nombre Apellido' }
```

Ejemplo de foto:

```js
{ src: 'assets/prototipo.jpg', alt: 'Nuestro prototipo terminado' }
```

## Organización

- `index.html`: estructura, contenido e iconos.
- `styles.css`: colores globales, tipografías, portada, navegación y presentación del proyecto.
- `sections.css`: secciones restantes, demostración, tarjetas y adaptación para celular.
- `script.js`: personalización, menú móvil, animaciones de aparición y demostración interactiva.
- `assets/smart-bin.png`: ilustración conceptual original de la portada. No representa una fotografía del prototipo real.

## Ajustes visuales

Modifica las variables de `:root` en `styles.css` para cambiar los colores.

La demostración usa tiempos ilustrativos y no se comunica con hardware. No fija una distancia de detección ni un tiempo de cierre para el prototipo real.

## Imagen ecológica de portada

Archivo: `assets/smart-bin.png`. Editado con la herramienta integrada ImageGen.

Prompt final aplicado:

> Use case: precise-object-edit.
> Asset type: square website hero product illustration.
> Input image 1 is the edit target: the existing smart trash bin image.
> Primary request: make this bin visibly ecological and approachable as a school ecological invention. Change the bin body and lid exterior to matte forest/leaf green with a practical slightly textured recycled-plastic appearance. Put one simple prominent white three-arrow recycling symbol centered on the front panel. Reduce the futuristic metallic gadget look and simplify the decorative circuit lines, using only subtle turquoise/lime light accents.
> Preserve invariants: retain the square composition, current three-quarter camera view, bin proportions and position, dark navy background #07131b, hovering hand on the upper right, cyan sensing waves between hand and bin, open lid, and exactly two ultrasonic circular sensors on the upper front. Keep the polished product-render lighting and clear silhouette, with subdued ecological green material.
> Constraints: no words, numbers, brands, UI, watermark, plants, or extra objects. Recycling symbol is a pictogram only. Produce exactly one edited image.

Las animaciones respetan la preferencia de movimiento reducido del dispositivo. La página tiene navegación por teclado, enlace para saltar al contenido y un menú adaptable.

## Publicar

Puedes subir todo el contenido de esta carpeta a cualquier alojamiento de páginas estáticas. No requiere servidor de aplicaciones, base de datos ni claves privadas.
