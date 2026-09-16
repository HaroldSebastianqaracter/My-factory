# Herramientas
herramiestas sevas

## Agentes de Claude Code

Definiciones en `.claude/agents/`. Para usarlas en otro proyecto, copiar el archivo a la carpeta `.claude/agents/` de ese proyecto; Claude Code lo carga al abrir la sesión ahí.

| Agente | Qué hace | Cómo invocarlo |
|---|---|---|
| `revisor-de-agentes` | Revisa definiciones de subagentes (`.claude/agents/*.md`) y las skills que precargan contra una lista de buenas prácticas documentadas. Devuelve veredicto (LISTO / LISTO CON CAMBIOS / NO LISTO) y hallazgos por severidad con la corrección lista para pegar. Solo lee; no modifica nada. | "Revisá `.claude/agents/mi-agente.md` con el revisor-de-agentes", o sin ruta para revisar todos los agentes del proyecto. |

Referencias en las que se basa la lista de revisión: documentación de subagentes y skills de Claude Code, y los artículos de Anthropic *Building effective agents* y *Effective context engineering for AI agents*. Los enlaces están al final del propio agente.

## Skills de Claude Code

Definiciones en `.claude/skills/`. Para usarlas en otro proyecto, copiar la carpeta completa de la skill a `.claude/skills/` de ese proyecto. Para tenerlas en todos, copiarla a `~/.claude/skills/`.

| Skill | Qué hace | Cuándo se activa |
|---|---|---|
| `ver-la-pantalla` | Renderiza una web local en Chrome sin ventana, saca captura y **mide el DOM**: avisa de elementos que se salen del viewport, solapes, elementos vacíos y errores de consola. Convierte el diseño a ciegas en un bucle de cambiar, mirar y corregir. | Cualquier trabajo sobre HTML, CSS o maquetación, y cuando alguien dice que algo "se ve mal", "se corta" o "se solapa". |

`ver-la-pantalla` necesita Playwright en un entorno virtual aparte (las instrucciones están en la propia skill). No descarga ningún navegador: usa el Chrome o el Edge ya instalados.

La skill mide además de fotografiar por un motivo concreto: hay defectos que la captura no enseña. El caso que la originó fue una celda de 47 px que en realidad medía 109 porque otra regla CSS con el mismo nombre de clase la deformaba. En la imagen parecía simplemente un poco ancha.
