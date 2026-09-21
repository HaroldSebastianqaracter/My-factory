---
name: estructura-proyecto
description: Crea el esqueleto de un proyecto — solo carpetas y ficheros marcador, sin contenido ni lógica — a partir de un árbol descrito en un doc de arquitectura, en una spec o por el usuario. Úsala cuando pidan "crea la estructura", "monta las carpetas", "scaffold", "esqueleto del proyecto" o cuando una arquitectura ya escrita no tenga todavía su árbol de ficheros en disco.
---

# Esqueleto de proyecto

Produce el **esqueleto**: el árbol de carpetas y ficheros de un proyecto, vacío. La idea del proyecto, la lógica, los esquemas y los prompts no entran aquí; eso lo escribe quien tenga la spec delante. El esqueleto existe para que ese trabajo tenga sitio donde caer.

## Pasos

### 1. Localizar la fuente del árbol

El árbol no se inventa: se copia de donde ya esté decidido. Busca en este orden y quédate con la primera fuente que lo tenga:

1. Un bloque de código con un árbol (`src/`, `├──`, `└──`) en `docs/`, `specs/`, `README.md` o `ARCHITECTURE.md`.
2. La descripción del usuario en el prompt.
3. Ninguna de las dos: propón un árbol mínimo para el stack que el usuario nombre, muéstralo y espera su conformidad antes de crear nada.

Criterio de fin: tienes un árbol escrito, línea a línea, y sabes de qué fichero salió.

### 2. Leer las reglas del repo

Abre `AGENTS.md` y `CLAUDE.md` si existen. Dos cosas condicionan el esqueleto:

- **Reglas sobre qué precede a qué.** Un repo que exige spec antes de código convierte cada fichero en `src/` en un cambio que necesita su spec. Cumple la regla: crea primero lo que la regla permite (carpetas, `README.md`, ficheros de configuración) y di en el resumen qué ficheros de código quedaron fuera y por qué.
- **Convenciones de nombre** (idioma de las carpetas, singular o plural, kebab o snake). El esqueleto las hereda; el árbol de la fuente manda sobre cualquier convención tuya.

Criterio de fin: puedes nombrar la regla que afecta al esqueleto, o afirmar que no hay ninguna.

### 3. Presentar el plan

Muestra el árbol completo que vas a crear, marcando qué ficheros van vacíos y cuáles llevan una línea de marcador. Si el árbol viene de un doc (fuente 1) y el repo no impone confirmación, crea directamente; en los otros dos casos, espera el sí.

### 4. Crear

Crea con `mkdir -p` y con escritura de fichero. Los generadores del ecosistema (`npm create`, `cookiecutter`, `django-admin startproject`) producen contenido, no esqueleto: si el usuario los quiere, es una decisión suya y se ejecutan aparte.

Contenido de cada fichero según su tipo, y nada más:

| Fichero | Contenido |
| --- | --- |
| `README.md` de una carpeta | Una línea: qué va ahí, con enlace al doc que lo define si existe |
| `__init__.py`, `index.ts`, `mod.rs` y equivalentes | Vacío |
| Módulo de código (`servicio.py`, `router.py`, `App.tsx`) | Vacío |
| Carpeta que debe existir sin ficheros | `.gitkeep` |
| Configuración (`pyproject.toml`, `package.json`, `.gitignore`) | Solo si el árbol la nombra; con el mínimo que la herramienta exige para ser válida y nada de dependencias |

Criterio de fin: cada línea del árbol del paso 1 existe en disco, y ningún fichero contiene más que lo que dice la tabla.

### 5. Verificar

Ejecuta un listado recursivo y compáralo con el árbol del paso 1, línea a línea. Después, `git status` debe mostrar solo ficheros nuevos: el esqueleto no modifica nada que ya existiera.

Criterio de fin: cero líneas del árbol sin fichero, cero ficheros fuera del árbol, cero ficheros modificados.

### 6. Resumir

Tres cosas, y ninguna más: de dónde salió el árbol, qué se creó, y qué quedó fuera por una regla del repo (paso 2). El commit lo decide el usuario.

## Cuando ya hay parte del esqueleto

Un proyecto a medias es el caso normal. El árbol de la fuente sigue mandando: crea lo que falte y deja intacto lo que exista, aunque tenga contenido. Si un fichero existente está en un sitio distinto al que dice el árbol, no lo muevas: nómbralo en el resumen como discrepancia entre doc y disco, para que el usuario decida cuál de los dos se corrige.
