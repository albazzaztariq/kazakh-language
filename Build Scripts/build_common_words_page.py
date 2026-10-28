"""Rebuild common-words.html with more food and adjectives and jump links at the top (numbers now live on numbers.html).
Inputs : the WORDS table inside kazakh_build_pages.py (loaded with exec, so the older sections stay the single source of truth);
         the existing common-words.html (its <head>/SEO block is kept as is); clips cached in Common Words/Words Audio/.
Method : replaces Adjectives with four opposite-pair groups; extends Food (chicken, beef, mutton, fish, egg ...) and Animals (chicken). Any new word gets a clip from the male
         voice kk-KZ-DauletNeural (rate -10%, trimmed, peak 0.4, same recipe as before) and the clips are embedded as base64.
         Every section gets an id, and a row of small pill links at the top jumps to each topic.
Output : common-words.html (overwritten). Other pages are not touched.
"""
import re, os, base64, json, asyncio
print("[DEBUG] common words rebuild start", flush=True)
import av, numpy as np, edge_tts
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
AD = W + "Common Words/Words Audio/"
src = open(W + "Build Scripts/kazakh_build_pages.py", encoding="utf-8").read()
ns = {}
exec(src[src.index("WORDS = ["):src.index("WORDS_INTRO")], ns)
WORDS = dict(ns["WORDS"])

# ---- adjectives (opposite pairs together) -----------------------------------------------------------------------------
ADJ_SIZE = [("үлкен", "ül-ken", "big"), ("кіші", "ki-shi", "small"), ("кішкентай", "kish-ken-tai", "little / tiny"),
            ("ұзын", "u-zyn", "long"), ("қысқа", "qys-qa", "short (length)"), ("биік", "bi-ik", "tall / high"),
            ("аласа", "a-la-sa", "short / low (height)"), ("қалың", "qa-lyñ", "thick"), ("жұқа", "zhu-qa", "thin (flat things)"),
            ("жіңішке", "zhi-ñish-ke", "thin / slender"), ("арық", "a-ryq", "thin / skinny (a person)"), ("кең", "keñ", "wide"),
            ("тар", "tar", "narrow"), ("терең", "te-reñ", "deep")]
ADJ_FEEL = [("жылдам", "zhyl-dam", "fast"), ("баяу", "ba-yau", "slow"), ("ауыр", "a-uyr", "heavy"), ("жеңіл", "zheñ-il", "light (weight)"),
            ("қатты", "qat-ty", "hard"), ("жұмсақ", "zhum-saq", "soft"), ("тегіс", "te-gis", "smooth / flat"),
            ("кедір-бұдыр", "ke-dir-bu-dyr", "rough"), ("оңай", "o-ñai", "easy"), ("қиын", "qi-yn", "difficult")]
ADJ_STATE = [("ыстық", "ys-tyq", "hot"), ("жылы", "zhy-ly", "warm"), ("салқын", "sal-qyn", "cool"), ("суық", "su-yq", "cold"),
             ("дымқыл", "dym-qyl", "wet / damp"), ("құрғақ", "qur-ghaq", "dry"), ("жарық", "zha-ryq", "bright / light"),
             ("қараңғы", "qa-rañ-ghy", "dark"), ("таза", "ta-za", "clean"), ("лас", "las", "dirty"),
             ("толы", "to-ly", "full"), ("бос", "bos", "empty"), ("ашық", "a-shyq", "open"), ("жабық", "zha-byq", "closed")]
ADJ_MORE = [("жаңа", "zha-ña", "new"), ("ескі", "es-ki", "old (things)"), ("жас", "zhas", "young"), ("кәрі", "kä-ri", "old (people)"),
            ("жаман", "zha-man", "bad"), ("әдемі", "ä-de-mi", "beautiful"), ("қымбат", "qym-bat", "expensive"), ("арзан", "ar-zan", "cheap"),
            ("жақын", "zha-qyn", "near"), ("алыс", "a-lys", "far"), ("бай", "bai", "rich"), ("кедей", "ke-dei", "poor"),
            ("күшті", "küsh-ti", "strong"), ("әлсіз", "äl-siz", "weak"), ("дұрыс", "du-rys", "correct"), ("қате", "qa-te", "wrong"),
            ("көп", "köp", "many / much"), ("аз", "az", "few / little"), ("тәтті", "tät-ti", "sweet"), ("тұзды", "tuz-dy", "salty"),
            ("қышқыл", "qysh-qyl", "sour"), ("ащы", "a-shy", "bitter / spicy")]
FOOD_MORE = [("сиыр еті", "si-yr e-ti", "beef"), ("қой еті", "qoi e-ti", "mutton / lamb"), ("тауық еті", "ta-uyq e-ti", "chicken (meat)"),
             ("балық", "ba-lyq", "fish"), ("жұмыртқа", "zhu-myrt-qa", "egg"), ("ірімшік", "i-rim-shik", "cheese"), ("май", "mai", "butter / oil"),
             ("тұз", "tuz", "salt"), ("қант", "qant", "sugar"), ("сорпа", "sor-pa", "soup")]

# ---- assemble sections in page order: (anchor id, title, rows, pill label or None) --------------------------------------
# Every word is looked up by its Kazakh spelling in POOL, so a section is just an ordered list of words and related words can sit together.
NEW_ROWS = [("бұрын", "bu-ryn", "before / ago (after a time: екі жыл бұрын = two years ago)"), ("кейін", "kei-in", "after / later"),
            ("болашақ", "bo-la-shaq", "future"), ("болашақта", "bo-la-shaq-ta", "in the future"),
            ("ерте", "er-te", "early"), ("картоп", "kar-top", "potato / potatoes"),
            ("жарты", "zhar-ty", "half (half a portion)"), ("бүтін", "bü-tin", "whole"), ("кеш", "kesh", "late / evening")]   # кеш is one word for both late and evening
POOL = {}
for _rows in list(WORDS.values()) + [ADJ_SIZE, ADJ_FEEL, ADJ_STATE, ADJ_MORE, FOOD_MORE, NEW_ROWS, [("тауық", "ta-uyq", "chicken (the bird)")]]:
    for _r in _rows: POOL[_r[0]] = _r
USED = []
def pick(words):
    """Rows for the given Kazakh words, in that order; each word may be used only once on the whole page."""
    out = []
    for w in words.split(" | "):
        assert w in POOL, w
        assert w not in USED, "used twice: " + w
        USED.append(w); out.append(POOL[w])
    return out
def keep(rows, drop):
    """The rows of an existing list minus the Kazakh words in drop (those are placed elsewhere)."""
    return [r for r in rows if r[0] not in drop]
SEC = []
def add(i, title, rows, pill=None): SEC.append((i, title, rows, pill))
add("basics", "Greetings & basics", pick("сәлем | сау болыңыз | рахмет | өтінемін | кешіріңіз | қалыңыз қалай | қайырлы таң | қайырлы кеш | қош келдіңіз | түсінбедім | қанша тұрады | иә | жоқ | бар | керек"), "Basics")
add("pronouns", "Pronouns", pick(" | ".join(r[0] for r in WORDS["Pronouns"])), "Pronouns")
add("questions", "Question words", pick(" | ".join(r[0] for r in WORDS["Question words"])), "Questions")
add("people", "People", pick("адам | бала | дос | мұғалім"), "People")
add("verbs", "Verbs (dictionary form ends in -у)", pick(" | ".join(r[0] for r in WORDS["Verbs (dictionary form ends in -у)"])), "Verbs")
add("adjectives", "Adjectives: size, shape and amount", pick(" | ".join(r[0] for r in ADJ_SIZE) + " | көп | аз | жарты | бүтін"), "Adjectives")
add("adjectives-feel", "Adjectives: speed, weight and feel", pick(" | ".join(r[0] for r in ADJ_FEEL)))
add("adjectives-state", "Adjectives: temperature, light and condition", pick(" | ".join(r[0] for r in ADJ_STATE)))
add("adjectives-taste", "Adjectives: taste", pick("тәтті | тұзды | қышқыл | ащы"))
add("adjectives-more", "Adjectives: more opposites", pick("жақсы | жаман | " + " | ".join(r[0] for r in keep(ADJ_MORE, {"жаман", "көп", "аз", "тәтті", "тұзды", "қышқыл", "ащы"}))))
add("nouns", "Everyday nouns", pick("ақша | кітап | есік"), "Nouns")
add("colors", "Colors", pick(" | ".join(r[0] for r in WORDS["Colors"])), "Colors")
add("family", "Family", pick("ана | әке | ата | әже | аға | апа | ұл | қыз"), "Family")
add("time", "Time", pick("күн | түн | апта | ай | жыл | бұрын | кейін | болашақ | болашақта | уақыт | сағат | қазір | кеше | бүгін | ертең | таңертең | ерте | кеш"), "Time")
add("days", "Days of the week", pick(" | ".join(r[0] for r in WORDS["Days of the week"])), "Days")
add("food", "Food & drink", pick("тамақ | нан | ет | сиыр еті | қой еті | тауық еті | балық | жұмыртқа | ірімшік | май | тұз | қант | сорпа | алма | картоп | күріш | су | шай | сүт | қымыз"), "Food")
add("animals", "Animals", pick(" | ".join(r[0] for r in WORDS["Animals"]) + " | тауық"), "Animals")
add("body", "Body", pick(" | ".join(r[0] for r in WORDS["Body"])), "Body")
add("nature", "Nature", pick(" | ".join(r[0] for r in WORDS["Nature"])), "Nature")
add("places", "Places", pick("үй | қала | ауыл | жол | мектеп | дүкен | базар"), "Places")
NUMBER_WORDS = {r[0] for r in WORDS.get("Numbers", [])} | set("бір екі үш төрт бес алты жеті сегіз тоғыз он".split())   # these live on numbers.html
assert set(USED) == set(POOL) - NUMBER_WORDS, ("left out:", set(POOL) - NUMBER_WORDS - set(USED))
print(f"[DEBUG] {len(USED)} words placed, none lost, none doubled", flush=True)

# ---- audio ---------------------------------------------------------------------------------------------------------------
os.makedirs(AD, exist_ok=True)
def clip(word):
    """Male Kazakh voice says the word; trimmed MP3 at peak 0.4, cached by codepoints in AD. Returns the file path."""
    f = AD + "-".join(f"{ord(c):x}" for c in word) + ".mp3"
    if os.path.exists(f): return f
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
audio = {}
for _, _, rows, _ in SEC:
    for kk, _, _ in rows:
        if kk not in audio: audio[kk] = base64.b64encode(open(clip(kk), "rb").read()).decode()
print(f"[DEBUG] {len(audio)} clips", flush=True)

# ---- html ----------------------------------------------------------------------------------------------------------------
ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
def table(rows):
    t = "<table class=\"lesson-table\"><thead><tr><th>Kazakh</th><th>Say it</th><th>English</th></tr></thead><tbody>"
    for kk, say, en in rows:
        t += f"<tr><td class=\"c0\"><button class=\"speak\" data-word=\"{kk}\" aria-label=\"Play {kk}\">{ICON}</button>{kk}</td><td class=\"c1\">{say}</td><td class=\"c2\">{en}</td></tr>"
    return t + "</tbody></table>"
pills = "".join(f"<a href=\"#{i}\">{p}</a>" for i, _, _, p in SEC if p)
body = "".join(f"        <section class=\"lesson-section\" id=\"{i}\"><h2>{t}</h2>{table(r)}</section>\n" for i, t, r, _ in SEC)
old = open(W + "common-words.html", encoding="utf-8").read()
head = old[:old.index("<body>")]
intro = "A small core vocabulary goes a long way: the most frequent words appear in most everyday sentences. Learn these, then use the Suffixes and Sentences pages to combine them."
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
        const topBtn = document.getElementById('toTop');
        const syncTop = () => topBtn.classList.toggle('show', window.scrollY > 380);
        window.addEventListener('scroll', syncTop, { passive: true });
        topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
        syncTop();
    </script>
""" % json.dumps(audio, ensure_ascii=False)
html = head + f"""<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Common Words</h1>
            <p class="section-subtitle">{intro}</p>
        </header>

        <div class="divider"></div>

        <nav class="jump-links" aria-label="Jump to a topic">{pills}</nav>

{body}
        <div class="page-nav">
            <a href="index.html" class="btn">Home</a>
            <a href="suffixes.html" class="btn">&rarr;</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
    <button type="button" class="float-top" id="toTop" aria-label="Back to the top of the page"><span aria-hidden="true">&uarr;</span> Top</button>
{player}</body>
</html>
"""
open(W + "common-words.html", "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote common-words.html, {len(html)} bytes, {sum(len(r) for _, _, r, _ in SEC)} rows", flush=True)
