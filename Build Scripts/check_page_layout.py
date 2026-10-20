"""Layout check for every page in the Web Version folder: finds words broken in the middle and sideways overflow.

Inputs : all *.html files in the Web Version folder, rendered in headless Chromium (file:// URLs) at phone, tablet and desktop widths.
Method : for every word in every text node (split at spaces, slashes, hyphens, which are legal break points) a DOM Range is measured;
         a word whose client rects sit on more than one line was broken mid-word (like "TYP / E"). Also reports pages whose document is wider
         than the viewport and lesson sections that need a horizontal scrollbar.
Output : one line per page/width problem, then PASS or FAIL (exit code 1 on FAIL). Run it after every page rebuild or CSS change.
"""
import glob, os, sys
print("[DEBUG] layout check start", flush=True)
from playwright.sync_api import sync_playwright
ROOT = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
WIDTHS = [320, 360, 375, 384, 390, 412, 480, 768, 1000]
JS = """() => {
  const broken = new Set(), skip = new Set(['SCRIPT', 'STYLE']);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = walker.nextNode())) {
    const el = n.parentElement; if (!el || skip.has(el.tagName)) continue;
    const re = /[^\\s\\/\\-]{3,}/g; let m;
    while ((m = re.exec(n.textContent))) {
      const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
      const rects = [...r.getClientRects()].filter(x => x.width > 0);
      if (rects.length > 1 && new Set(rects.map(x => Math.round(x.top))).size > 1) broken.add(m[0] + ' <' + el.tagName.toLowerCase() + '>');
    }
  }
  const wide = [...document.querySelectorAll('.lesson-section')].filter(s => s.scrollWidth > s.clientWidth + 1).map(s => s.id || s.querySelector('h2').textContent);
  return {broken: [...broken], pageOverflow: document.documentElement.scrollWidth > innerWidth, wide};
}"""
problems = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob(ROOT + "*.html")):
        name = os.path.basename(f)
        for w in WIDTHS:
            pg = b.new_page(viewport={"width": w, "height": 900}); pg.goto("file:///" + f.replace(" ", "%20")); pg.wait_for_timeout(250)
            r = pg.evaluate(JS); pg.close()
            if r["broken"] or r["pageOverflow"] or r["wide"]:
                problems += 1
                print(f"[FAIL] {name} @ {w}px: broken words={r['broken'][:6]}{'...' if len(r['broken']) > 6 else ''} ({len(r['broken'])}); page overflow={r['pageOverflow']}; scrolling sections={r['wide'][:4]}", flush=True)
    b.close()
print("PASS: no broken words or sideways overflow on any page at any width" if not problems else f"FAIL: {problems} page/width combinations", flush=True)
sys.exit(1 if problems else 0)
