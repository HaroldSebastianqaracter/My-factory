# Herramientas
herramiestas sevas

## Agentes de Claude Code

Definiciones en `.claude/agents/`. Para usarlas en otro proyecto, copiar el archivo a la carpeta `.claude/agents/` de ese proyecto; Claude Code lo carga al abrir la sesión ahí.

| Agente | Qué hace | Cómo invocarlo |
|---|---|---|
| `revisor-de-agentes` | Revisa definiciones de subagentes (`.claude/agents/*.md`) y las skills que precargan contra una lista de buenas prácticas documentadas. Devuelve veredicto (LISTO / LISTO CON CAMBIOS / NO LISTO) y hallazgos por severidad con la corrección lista para pegar. Solo lee; no modifica nada. | "Revisá `.claude/agents/mi-agente.md` con el revisor-de-agentes", o sin ruta para revisar todos los agentes del proyecto. |
| `validador-de-codigo` | Valida el código que escribió otro agente (commit, rango o árbol de trabajo) contra las reglas del proyecto (`AGENTS.md`, spec, linters configurados). Ejecuta antes de opinar: tests, linters comparados con el commit padre, y comprueba que cada test nuevo **fallaba antes** del cambio. Busca la «picaresca» del implementador (tests debilitados, `xfail`, silenciadores, valores cableados, mocks de la pieza a corregir) y reproduce los fallos que sospecha. Devuelve APROBADO / APROBADO CON CAMBIOS / RECHAZADO con evidencia repetible. No modifica el repo. | "Validá el commit `abc123` con el validador-de-codigo", "validá `main..HEAD`", o sin referencia para el árbol de trabajo. Conviene decirle qué debía hacer el cambio (fase, requisito). |

Referencias en las que se basa la lista de revisión: documentación de subagentes y skills de Claude Code, y los artículos de Anthropic *Building effective agents* y *Effective context engineering for AI agents*. Los enlaces están al final del propio agente.

## Skills de Claude Code

Definiciones en `.claude/skills/<nombre>/SKILL.md`. Para usarlas en todos los proyectos, copiar la carpeta a `~/.claude/skills/`; para uno solo, a la carpeta `.claude/skills/` de ese proyecto.

| Skill | Qué hace | Cómo invocarla |
|---|---|---|
| `estructura-proyecto` | Crea el esqueleto de un proyecto: solo carpetas y ficheros vacíos o con una línea de marcador, a partir del árbol descrito en un doc de arquitectura, en una spec o por el usuario. Lee `AGENTS.md`/`CLAUDE.md` y respeta sus reglas (por ejemplo, spec antes de código). No escribe lógica ni ejecuta generadores. | `/estructura-proyecto`, o pedir "crea la estructura" / "monta las carpetas". |
