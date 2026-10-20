"""Add an 'example words' section to alphabet.html, below the letter buttons.

Method: for each (letter, Kazakh word, English meaning) row, edge-tts (male voice kk-KZ-DauletNeural, rate -10%)
renders the word, silence is trimmed and the peak normalised to 0.4 (same recipe as the common-words page).
The MP3s are base64-embedded as WORD_AUDIO in a second <script> block, so the page still works offline.
Inputs : the ROWS table below; Alphabet/Words Audio/ is the clip cache.
Outputs: alphabet.html with a <!-- letter-words --> section before the page-nav and a <!-- letter-words-script -->
         block before </body>. Re-running replaces both blocks (idempotent).
"""
import asyncio, av, numpy as np, edge_tts, base64, json, os, re
print("[DEBUG] letter-words start", flush=True)

HTML = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/alphabet.html"
AD = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Alphabet/Words Audio"
os.makedirs(AD, exist_ok=True)

# (letter, word, English). Letters follow the order of the buttons above; a letter may have several rows.
ROWS = [
    ("А", "ана", "mother"), ("Ә", "әпке", "older sister"), ("Б", "бала", "child"), ("В", "вагон", "train car"),
    ("Г", "гүл", "flower"), ("Ғ", "аға", "older brother"), ("Д", "адам", "person"), ("Е", "ене", "mother-in-law"),
    ("Ё", "ёлка", "fir tree / Christmas tree"), ("Ж", "жаз", "summer"), ("З", "зат", "thing, object"),
    ("И", "ит", "dog"), ("И", "иә", "yes"), ("Й", "ай", "moon, month"), ("К", "көлік", "vehicle"),
    ("Қ", "қала", "city"), ("Л", "ел", "country, people"), ("М", "мақсат", "goal, aim"), ("Н", "нан", "bread"),
    ("Ң", "таң", "dawn"), ("О", "ол", "he, she, it"), ("Ө", "өте", "very"), ("П", "апа", "older sister, mother"),
    ("Р", "рақмет", "thank you"), ("С", "су", "water"), ("Т", "тау", "mountain"),
    ("У", "тау", "mountain"), ("У", "су", "water"), ("Ұ", "бұл", "this"), ("Ү", "үй", "house"),
    ("Ф", "фильм", "film"), ("Х", "хат", "letter"), ("Һ", "жиһаз", "furniture"), ("Ц", "цирк", "circus"),
    ("Ч", "чек", "receipt, check"), ("Ш", "шаш", "hair"), ("Щ", "щётка", "brush"), ("Ы", "ыдыс", "dish, vessel"),
    ("І", "ірімшік", "cheese"), ("Э", "элеватор", "grain elevator"), ("Ю", "аю", "bear"), ("Я", "аяқ", "foot, leg"),
]

def build_clip(word):
    """Male Kazakh voice says the word; trimmed MP3 at peak 0.4, cached in AD by codepoints. Returns the file path."""
    f = f"{AD}/{'-'.join(f'{ord(c):x}' for c in word)}.mp3"
    if os.path.exists(f):
        print(f"[DEBUG] cached {word}", flush=True); return f
    print(f"[DEBUG] generating {word}", flush=True)
    asyncio.run(edge_tts.Communicate(word, "kk-KZ-DauletNeural", rate="-10%").save(f))
    c = av.open(f); r = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.05 * r)
    y = x[max(0, idx[0]-pad):min(len(x), idx[-1]+pad)]; y = y * (0.4 / abs(y).max())
    out = av.open(f, "w", format="mp3"); st = out.add_stream("mp3", rate=r); st.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = r
    for p in st.encode(fr): out.mux(p)
    for p in st.encode(None): out.mux(p)
    out.close(); return f

audio = {}
for _, w, _ in ROWS:
    if w not in audio:
        audio[w] = base64.b64encode(open(build_clip(w), "rb").read()).decode()
print(f"[DEBUG] {len(audio)} unique clips, {sum(len(v) for v in audio.values())} base64 bytes", flush=True)

ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
body = ""
for i, (L, w, en) in enumerate(ROWS):
    span = sum(1 for r in ROWS if r[0] == L)
    first = i == 0 or ROWS[i-1][0] != L
    cell = f'<td class="c0" rowspan="{span}">{L}</td>' if first else ""
    body += (f'<tr>{cell}<td><button class="speak" data-wordclip="{w}" aria-label="Play {w}">{ICON}</button>{w}</td>'
             f'<td>{en}</td></tr>\n')
section = f"""<!-- letter-words -->
        <section class="lesson-section">
            <h2>Each letter in a word</h2>
            <table class="lesson-table"><thead><tr><th>Letter</th><th>Word</th><th>English</th></tr></thead><tbody>
{body}</tbody></table>
        </section>
        <!-- /letter-words -->
"""
script = ("<!-- letter-words-script -->\n    <script>\n        const WORD_AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";\n" + """        let currentWord = null;
        document.querySelectorAll('button.speak[data-wordclip]').forEach(btn => {
            btn.addEventListener('click', function () {
                const data = WORD_AUDIO[this.getAttribute('data-wordclip')];
                if (!data) return;
                if (currentWord) { currentWord.pause(); }
                document.querySelectorAll('button.speak.playing').forEach(b => b.classList.remove('playing'));
                const a = new Audio('data:audio/mpeg;base64,' + data);
                currentWord = a;
                this.classList.add('playing');
                const done = () => this.classList.remove('playing');
                a.onended = done; a.onerror = done;
                a.play().catch(done);
            });
        });
    </script>
    <!-- /letter-words-script -->
""")

html = open(HTML, encoding="utf-8").read()
html = re.sub(r"[ \t]*<!-- letter-words -->.*?<!-- /letter-words -->\n\n?", "", html, flags=re.S)
html = re.sub(r"[ \t]*<!-- letter-words-script -->.*?<!-- /letter-words-script -->\n", "", html, flags=re.S)
assert html.count('<div class="page-nav">') == 1 and html.count("</body>") == 1
html = html.replace('<div class="page-nav">', "        " + section + "\n        " + '<div class="page-nav">', 1)
html = html.replace("</body>", "    " + script + "</body>", 1)
open(HTML, "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote {len(html)} bytes", flush=True)
