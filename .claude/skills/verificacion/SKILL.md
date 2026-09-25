---
name: verificacion
description: Construye o actualiza el plan de verificación (<spec>-verification.md) de una spec, un componente o la salida de un agente — qué propiedades importan, con qué método se comprueba cada una, su etiqueta Trust Spec (T/A/I/D/U) y su punto ciego. Úsala al escribir o revisar una spec, antes de dar por terminado un componente, al decidir qué tests o evals hacen falta, y cuando haya que dejar por escrito un riesgo aceptado.
---

# Plan de verificación

El catálogo de métodos vive en el documento de validadores del proyecto (por ejemplo `docs/validators.md`). Si existe, es la única fuente: léelo antes de asignar nada y no inventes métodos fuera de él. Si el proyecto no tiene uno, usa el catálogo mínimo del final de esta skill. Si falta un método que el proyecto necesita, añadirlo es un cambio en ese documento y se consulta con el usuario antes de tocarlo.

Esta skill produce un artefacto: `specs/<nombre-de-la-spec>-verification.md`, hermano de la spec que verifica. Un componente sin spec no se verifica: primero se escribe su spec.

## Pasos

### 1. Delimitar el alcance

Nombra exactamente qué se verifica y de qué tipo es cada parte:

- **Determinista**: código (API, esquemas, transformaciones, persistencia, UI).
- **No determinista**: lo que un agente decide o escribe (trayectoria de herramientas, texto generado, coherencia con las reglas de dominio del proyecto).

La mezcla es lo normal. Separarla es lo que decide qué mitad del catálogo aplica.

### 2. Enumerar las propiedades que importan

Una propiedad es una afirmación que puede ser falsa. «Autenticación» no lo es; «un usuario sin sesión nunca recibe el cuerpo de un documento» sí.

Barre estas fuentes hasta agotarlas:

- Lo que la spec promete, cláusula a cláusula.
- Los límites: entradas vacías, máximos, concurrencia, fallo de dependencias.
- Los invariantes que deben cumplirse siempre, incluido el orden («nunca publicar antes de validar»).
- El modelo de amenaza: prompt injection, mal uso de herramientas, goal drift, exfiltración.
- Las propiedades de la salida de los agentes: formato, coherencia entre salidas y cumplimiento de las reglas de dominio del proyecto, si las tiene escritas.

Criterio de fin: toda promesa de la spec aparece como al menos una propiedad, y cada propiedad se puede afirmar o negar sin discutir qué significa.

### 3. Asignar método y etiqueta

Para cada propiedad, elige del catálogo el método más barato que dé evidencia real, y arrastra su etiqueta.

Reglas de asignación:

- Una propiedad que un tipo ya garantiza no necesita un test (`A` antes que `T`).
- Una propiedad sobre texto generado no se cubre con un test de ejemplo: va a evals, y la etiqueta es `I` si el scorer es un modelo juez.
- Un invariante de orden en un flujo multi-agente es `model checking` (`A`), no un test de integración.
- Contención (sandbox, guardrails, rollout progresivo) es `D`: la evidencia es observar que bloquea, no que el código exista.
- Una propiedad puede llevar dos métodos cuando cada uno cubre una mitad distinta; escribe los dos.
- **Escribe el punto ciego del método elegido**, no solo lo que detecta. Si no sabes qué se le escapa, no has entendido el método.
- **Si el dato lo declara el mismo agente al que juzgas, un método no basta.** Una consulta sobre un campo autodeclarado mide obediencia al formato, no verdad: añade un segundo método que mire el texto.
- Una propiedad que queda con un solo método se marca **validador solitario**. No es un error, es una deuda que hay que ver.

Lo que no puedas verificar se etiqueta `U` con motivo y con qué lo hace tolerable (impacto bajo, reversible, detectable en producción). `U` es una decisión escrita, no un hueco.

Criterio de fin: cero propiedades sin etiqueta y cero métodos sin punto ciego escrito.

### 4. Escribir el archivo

```markdown
# Verificación — <nombre de la spec>

Plan de verificación de [`<spec>.md`](<spec>.md). Métodos y etiquetas según <el documento de validadores del proyecto>.

## Propiedades verificadas

| # | Propiedad | Método | Tag | Punto ciego | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Un usuario sin sesión nunca recibe el cuerpo de un documento | Integration testing | `T` | Solo cubre las rutas que la prueba enumera; una ruta nueva nace sin cubrir | `tests/api/test_documentos.py` | pendiente |

## Riesgos aceptados

| # | Propiedad | Por qué no se verifica | Qué lo hace tolerable |
| --- | --- | --- | --- |
| 7 | El texto generado mantiene el tono entre sesiones largas | No hay scorer fiable todavía | Revisión humana antes de publicar |
```

**Punto ciego** es lo que ese método no ve aunque pase. **Evidencia** apunta a dónde vive la comprobación (archivo de test, suite de evals, dashboard, paso del pipeline) o `—` si aún no existe. **Estado** es `pendiente`, `implementado` o `fallando`.

### 5. Cerrar

Revisa contra estas cinco condiciones antes de darlo por hecho:

1. Cada promesa de la spec está en la tabla.
2. Cada fila lleva un método del catálogo, escrito con su nombre del catálogo.
3. Cada `U` tiene motivo y atenuante.
4. Cada fila tiene punto ciego escrito, y las filas con un solo método están señaladas como validador solitario.
5. El plan entra en el mismo commit que la spec y el código, si las reglas del proyecto (`AGENTS.md`, `CLAUDE.md`) lo piden.

## Al revisar un plan existente

No lo reescribas: dilo en cuatro frentes.

- **Verde ciego**: una fila en verde cuyo único método no puede ver el fallo que importa, casi siempre porque el dato que consulta lo produce el agente evaluado. Es el frente que se revisa **primero**: una fila roja se ve, una fila verde y ciega no.
- **Optimismo de etiqueta**: una fila marcada `T` cuya evidencia no existe, o marcada `A` cuando el tipo no garantiza esa propiedad.
- **Propiedades que faltan**: la spec cambió y la tabla no.
- **`U` disfrazado**: una propiedad que nadie comprueba pero aparece como verificada. Bájala a la tabla de riesgos aceptados.

## Catálogo mínimo (si el proyecto no tiene uno)

Cada método se etiqueta según de dónde saca su evidencia:

| Código | Tipo | Cómo se verifica |
| --- | --- | --- |
| **T** | Test | Ejecutando el sistema contra entradas concretas |
| **A** | Analysis | Razonamiento estático: tipos, SAST, ejecución simbólica o prueba formal |
| **I** | Inspection | Una persona o un modelo crítico lo lee y lo juzga |
| **D** | Demonstration | Observando el funcionamiento correcto en un escenario realista (staging, sandbox) |
| **U** | Unverifiable / Accepted Risk | Ningún método aplica o no compensa el coste; se nombra en vez de dejarlo como supuesto silencioso |

| Método | Tag |
| --- | --- |
| Type checking, static analysis / SAST, symbolic execution, formal verification / theorem proving, model checking | `A` |
| Unit / integration testing, property-based testing, mutation testing, contract testing, CI/CD integration, red-teaming / adversarial testing | `T` |
| Evals | `T` (`I` si el scorer es un modelo juez) |
| Human-in-the-loop review, multi-agent verification | `I` |
| Runtime observability / tracing, sandboxed execution, guardrails, progressive rollout | `D` |
