"""Renderiza una página local sin ventana, saca captura y devuelve medidas del DOM.

La captura enseña cómo queda; las medidas enseñan lo que la captura esconde. Un elemento
deformado por una regla CSS ajena se ve idéntico a uno correcto hasta que lo medís.

Uso:
    python mirar.py URL SALIDA.png [ANCHOxALTO] [--espera SEG] [--medir "#a,#b,.c"]
    python mirar.py http://127.0.0.1:8765/ shot.png 1600x780 --espera 3 --medir "#mando,#cinta"

Sin --medir usa una lista de selectores habituales. Devuelve código 1 si algo se sale del
viewport o si la consola registró errores, para poder encadenarlo en un script.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

POR_DEFECTO = "header,nav,main,footer,#app,#root,.container,button"

MEDIR = """(sels) => {
  const caja = e => { const b = e.getBoundingClientRect();
    return {t: Math.round(b.top), b: Math.round(b.bottom),
            l: Math.round(b.left), r: Math.round(b.right),
            w: Math.round(b.width), h: Math.round(b.height)}; };
  const vis = e => { const s = getComputedStyle(e);
    return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.01; };

  const elems = [];
  for (const sel of sels) {
    document.querySelectorAll(sel).forEach((e, i) => {
      if (elems.length > 60) return;
      elems.push({sel: sel + (i ? `[${i}]` : ''), caja: caja(e), visible: vis(e),
                  hijos: e.children.length, texto: (e.textContent || '').trim().length});
    });
  }

  const fuera = elems.filter(e => e.visible && (e.caja.b > innerHeight + 1 || e.caja.t < -1 ||
                                                e.caja.r > innerWidth + 1 || e.caja.l < -1));
  const solapes = [];
  for (let i = 0; i < elems.length; i++) for (let j = i + 1; j < elems.length; j++) {
    const a = elems[i], b = elems[j];
    if (!a.visible || !b.visible) continue;
    if (a.sel.split('[')[0] === b.sel.split('[')[0]) continue;
    const x = Math.min(a.caja.r, b.caja.r) - Math.max(a.caja.l, b.caja.l);
    const y = Math.min(a.caja.b, b.caja.b) - Math.max(a.caja.t, b.caja.t);
    if (x > 4 && y > 4) solapes.push(`${a.sel} x ${b.sel}`);
  }
  return {viewport: [innerWidth, innerHeight], elems, fuera, solapes: solapes.slice(0, 8),
          scrollAlto: document.documentElement.scrollHeight};
}"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("salida", type=Path)
    p.add_argument("tamano", nargs="?", default="1920x1040")
    p.add_argument("--espera", type=float, default=3.0, help="segundos tras la carga")
    p.add_argument("--medir", default=POR_DEFECTO, help="selectores separados por coma")
    p.add_argument("--navegador", default="chrome", help="chrome o msedge")
    a = p.parse_args()

    ancho, alto = (int(x) for x in a.tamano.lower().split("x"))
    sels = [s.strip() for s in a.medir.split(",") if s.strip()]

    with sync_playwright() as pw:
        nav = pw.chromium.launch(channel=a.navegador, args=["--no-sandbox", "--disable-gpu"])
        pag = nav.new_page(viewport={"width": ancho, "height": alto})
        fallos: list[str] = []
        pag.on("console", lambda m: fallos.append(f"consola: {m.text}") if m.type == "error" else None)
        pag.on("pageerror", lambda e: fallos.append(f"pageerror: {e}"))
        pag.on("response", lambda r: fallos.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 else None)

        pag.goto(a.url, wait_until="load")
        pag.wait_for_timeout(int(a.espera * 1000))
        a.salida.parent.mkdir(parents=True, exist_ok=True)
        pag.screenshot(path=str(a.salida))
        m = pag.evaluate(MEDIR, sels)
        nav.close()

    print(f"viewport   {m['viewport'][0]}x{m['viewport'][1]}   captura: {a.salida}")
    print(f"{'selector':<28} {'x':>12} {'y':>12} {'tam':>11}  estado")
    for e in m["elems"][:24]:
        c = e["caja"]
        estado = "visible" if e["visible"] else "OCULTO"
        if e["visible"] and e["hijos"] == 0 and e["texto"] == 0:
            estado = "VACIO"
        print(f"{e['sel']:<28} {c['l']:>5}..{c['r']:<5} {c['t']:>5}..{c['b']:<5} "
              f"{c['w']:>4}x{c['h']:<5}  {estado}")

    problema = False
    if m["fuera"]:
        problema = True
        print("\nSE SALEN DEL VIEWPORT:")
        for e in m["fuera"]:
            print(f"  {e['sel']}  ->  {e['caja']}")
    if m["solapes"]:
        print("\nposibles solapes: " + "; ".join(m["solapes"]))
    if fallos:
        problema = True
        print("\nERRORES:")
        for f in dict.fromkeys(fallos[:8]):
            print(f"  {f}")
    if not problema:
        print("\nsin recortes ni errores de consola")
    return 1 if problema else 0


if __name__ == "__main__":
    sys.exit(main())
