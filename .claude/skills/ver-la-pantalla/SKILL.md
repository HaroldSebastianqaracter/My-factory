---
name: ver-la-pantalla
description: Renderiza una web local en Chrome sin ventana para verla, medirla y corregirla en un bucle, en vez de escribir interfaz a ciegas. Úsala siempre que el trabajo toque HTML, CSS o maquetación, cuando alguien diga que algo "se ve mal", "se corta", "se solapa" o "no cabe", o antes de dar por buena cualquier pantalla. También cuando haya que comprobar un diseño a varios tamaños de ventana.
---

# Ver la pantalla

Un agente que escribe interfaz sin verla está adivinando. Esta skill convierte
esa adivinanza en un bucle: cambiar, renderizar, mirar, medir, corregir.

## Por qué existe

Estos tres defectos salieron en una sola sesión, en una consola que ya se había
dado por terminada dos veces:

- **El panel de botones se salía por debajo del borde** en ventanas de menos de
  900 px de alto. La causa no era obvia: al centrar con CSS Grid, un elemento más
  alto que su contenedor activa la *alineación segura* del navegador y se ancla
  arriba en vez de centrarse, así que el `transform: scale()` partía de una
  posición ya desplazada.
- **Dos clases distintas se llamaban igual.** `.hallazgo` era a la vez una fila de
  tabla (`display:grid` con una columna de 78 px) y una celda de 47 px de una barra
  de progreso. La regla de la tabla deformaba la celda: medía 109×28 en vez de
  47×15.
- **Una viñeta decorativa se comía la interfaz.** Al 78 % de negro, la columna de
  registro y los botones quedaban prácticamente invisibles.

Ninguno se ve leyendo el código. El segundo tampoco se ve mirando la captura: hace
falta **medir el DOM**. Por eso el script devuelve medidas y no solo una imagen.

## Preparación, una sola vez

```bash
python -m venv "$USERPROFILE/.pwdrv"          # fuera del proyecto: es herramienta, no dependencia
"$USERPROFILE/.pwdrv/Scripts/python.exe" -m pip install playwright
```

No hace falta `playwright install`: el script usa el Chrome o el Edge que ya están
en la máquina (`channel="chrome"`), así que se ahorra la descarga de ~150 MB.

## El bucle

1. **Levantá la app** en segundo plano y esperá a que responda de verdad. Sondeá el
   puerto, no duermas un número de segundos al azar:

   ```bash
   npm run dev &     # o python -m app ui, o lo que sea
   timeout 30 bash -c 'until curl -sf http://127.0.0.1:PUERTO >/dev/null; do sleep 1; done'
   ```

2. **Renderizá y medí:**

   ```bash
   "$USERPROFILE/.pwdrv/Scripts/python.exe" scripts/mirar.py \
       http://127.0.0.1:PUERTO/ salida.png 1920x1040 --espera 3 \
       --medir "#cabecera,#panel,.boton-principal"
   ```

3. **Mirá la imagen de verdad.** Abrila con la herramienta de lectura de archivos.
   Una captura que no se mira no sirve de nada, y una captura en negro es un fallo
   de arranque, no un diseño oscuro.

4. **Leé las medidas.** El script avisa de lo que la imagen esconde: elementos que
   se salen del viewport, solapes entre elementos, y errores de consola.

5. **Corregí y repetí.** Cada vuelta cuesta segundos.

## Comprobá siempre tres tamaños

Un diseño que solo se prueba a 1920×1080 se rompe en el portátil de al lado. Como
mínimo:

| Tamaño | Qué representa |
|---|---|
| `1920x1040` | monitor grande, ventana maximizada |
| `1600x780` | portátil con barra de marcadores |
| `1366x700` | portátil pequeño |

El defecto del panel que se salía **solo aparecía en los dos últimos**.

## Trampas que te vas a encontrar

- **`chrome --headless --screenshot` ya no funciona.** Lo quitaron del headless
  nuevo y falla sin decir nada: no genera el archivo y el código de salida no
  ayuda. Por eso esta skill usa Playwright y no la bandera.
- **Rutas largas en Windows.** `pip install playwright` revienta con
  `[Errno 2] No such file or directory` si la ruta del entorno virtual es larga.
  Instalalo en una ruta corta como `%USERPROFILE%\.pwdrv`.
- **`wait_until="networkidle"` no llega nunca** en una página que sondea cada pocos
  segundos. Usá `"load"` más una espera explícita, o esperá a un elemento concreto.
- **Animaciones de entrada.** Si la página tiene una secuencia de arranque, la espera
  tiene que superarla o vas a fotografiar el telón. Y si se salta con `sessionStorage`,
  cada pestaña nueva la repite.
- **La captura se ve reducida.** Un texto de 9 px en una imagen escalada parece
  invisible aunque esté perfectamente. Antes de declarar que algo "no se pinta",
  comprobalo con las medidas: `hijos`, `opacity`, `visibility`.
- **Mirá los errores de consola antes de cantar victoria.** Una página puede pintar
  su estructura entera mientras todas sus peticiones devuelven 500.

## Qué no hace

No sustituye a un humano mirando. Detecta recortes, solapes, elementos vacíos y
errores; no te va a decir que el color es feo ni que la jerarquía no se entiende.
Para eso, enseñá la captura y preguntá.
