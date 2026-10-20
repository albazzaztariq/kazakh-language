"""Build numbers.html: Kazakh numbers from 0 to a million, as patterns plus the words you cannot work out yourself.

Inputs : the tables below (written by hand); clips cached in Numbers/Words Audio/ (seeded from Common Words/Words Audio/ when present).
Method : 0-10, then 11 and 19 to show "ten + digit", the tens (20-90), hundreds/thousands/a million, then four built-up examples.
         New words are spoken by the male Kazakh voice kk-KZ-DauletNeural (rate -10%, trimmed, peak 0.4, as on the other pages) and embedded as base64.
Output : numbers.html (same table markup and speaker buttons as the Common Words page).
"""
import os, base64, json, asyncio, shutil
print("[DEBUG] numbers page start", flush=True)
import av, numpy as np, edge_tts
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
AD = W + "Numbers/Words Audio/"; OLD = W + "Common Words/Words Audio/"
os.makedirs(AD, exist_ok=True)
ONES = [("нөл", "nöl", "0"), ("бір", "bir", "1"), ("екі", "e-ki", "2"), ("үш", "üsh", "3"), ("төрт", "tört", "4"), ("бес", "bes", "5"),
        ("алты", "al-ty", "6"), ("жеті", "zhe-ti", "7"), ("сегіз", "se-giz", "8"), ("тоғыз", "to-ghyz", "9"), ("он", "on", "10")]
TEENS = [("он бір", "on bir", "11"), ("он тоғыз", "on to-ghyz", "19")]
TENS = [("жиырма", "zhi-yr-ma", "20"), ("отыз", "o-tyz", "30"), ("қырық", "qy-ryq", "40"), ("елу", "e-lu", "50"),
        ("алпыс", "al-pys", "60"), ("жетпіс", "zhet-pis", "70"), ("сексен", "sek-sen", "80"), ("тоқсан", "toq-san", "90")]
BIG = [("жүз", "zhüz", "100"), ("екі жүз", "e-ki zhüz", "200"), ("мың", "myñ", "1,000"), ("он мың", "on myñ", "10,000"),
       ("жүз мың", "zhüz myñ", "100,000"), ("миллион", "mil-li-on", "1,000,000")]
BUILD = [("жиырма бір", "zhi-yr-ma bir", "21"), ("жүз жиырма үш", "zhüz zhi-yr-ma üsh", "123"),
         ("үш жүз қырық бес", "üsh zhüz qy-ryq bes", "345"), ("екі мың жиырма алты", "e-ki myñ zhi-yr-ma al-ty", "2,026")]
SEC = [("0 to 10", ONES), ("11 to 19: ten + the digit", TEENS), ("Tens: 20 to 90", TENS),
       ("Hundreds, thousands, a million", BIG), ("Putting numbers together: biggest part first", BUILD)]

def clip(word):
    """Male Kazakh voice says the word; trimmed MP3 at peak 0.4, cached by codepoints in AD. Returns the file path."""
    name = "-".join(f"{ord(c):x}" for c in word) + ".mp3"; f = AD + name
    if os.path.exists(f): return f
    if os.path.exists(OLD + name): shutil.copy2(OLD + name, f); return f
    print(f"[DEBUG] generating {word}", flush=True)
    asyncio.run(edge_tts.Communicate(word, "kk-KZ-DauletNeural", rate="-10%").save(f))
    c = av.open(f); r = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.05 * r)
    y = x[max(0, idx[0] - pad):min(len(x), idx[-1] + pad)]; y = y * (0.4 / abs(y).max())
    out = av.open(f, "w", format="mp3"); st = out.add_stream("mp3", rate=r); st.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = r
    for p in st.encode(fr): out.mux(p)
    for p in st.encode(None): out.mux(p)
    out.close(); return f
audio = {kk: base64.b64encode(open(clip(kk), "rb").read()).decode() for _, rows in SEC for kk, _, _ in rows}
print(f"[DEBUG] {len(audio)} clips", flush=True)

ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
def table(rows):
    t = "<table class=\"lesson-table\"><thead><tr><th>Kazakh</th><th>Say it</th><th>Number</th></tr></thead><tbody>"
    for kk, say, n in rows:
        t += f"<tr><td class=\"c0\"><button class=\"speak\" data-word=\"{kk}\" aria-label=\"Play {kk}\">{ICON}</button>{kk}</td><td class=\"c1\">{say}</td><td class=\"c2\">{n}</td></tr>"
    return t + "</tbody></table>"
body = "".join(f"        <section class=\"lesson-section\"><h2>{t}</h2>{table(r)}</section>\n" for t, r in SEC)
title = "Kazakh Numbers: Counting from 0 to a Million with Audio"
desc = "Learn to count in Kazakh from 0 to a million: the numbers 0 to 10, the pattern for 11 to 19, the tens, hundreds, thousands and how to put numbers together."
player = """
    <script>
        const AUDIO = %s;
        let current = null;
        document.querySelectorAll('button.speak').forEach(btn => {
            btn.addEventListener('click', function () {
                const data = AUDIO[this.getAttribute('data-word')];
                if (!data) return;
                if (current) { current.pause(); }
                document.querySelectorAll('button.speak.playing').forEach(b => b.classList.remove('playing'));
                const a = new Audio('data:audio/mpeg;base64,' + data);
                current = a;
                this.classList.add('playing');
                const done = () => this.classList.remove('playing');
                a.onended = done; a.onerror = done;
                a.play().catch(done);
            });
        });
    </script>
""" % json.dumps(audio, ensure_ascii=False)
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css?v=7">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/numbers.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Numbers</h1>
            <p class="section-subtitle">From zero to a million: the words you need, and how they combine</p>
        </header>

        <div class="divider"></div>

{body}
        <div class="page-nav">
            <a href="common-words.html" class="btn">&larr;</a>
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
{player}</body>
</html>
"""
open(W + "numbers.html", "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote numbers.html, {len(html)} bytes", flush=True)
