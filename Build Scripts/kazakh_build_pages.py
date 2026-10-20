"""Build the lesson pages after the alphabet: common-words.html, suffixes.html, sentences.html.
Method: data tables below are rendered into HTML that reuses styles.css; appends lesson CSS once;
links index.html buttons and the alphabet page's right-arrow to the next page in the chain.
Inputs: data in this file. Outputs: 3 new pages + edits to index.html, alphabet.html, styles.css in Web Version/."""
import re
print("[DEBUG] build pages start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css?v=10">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">{title}</h1>
            <p class="section-subtitle">{sub}</p>
        </header>

        <div class="divider"></div>
"""
FOOT = """
        <div class="page-nav">
            <a href="index.html" class="btn">Home</a>
            {arrow}
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
</body>
</html>
"""

ICON_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
SPK = '<button class="speak" data-word="{w}" aria-label="Play {w}">' + ICON_SVG + '</button>'

def table(cols, rows, speak=False):
    h = "<table class=\"lesson-table\"><thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody>"
    for r in rows:
        h += "<tr>" + "".join(f"<td class=\"c{i}\">{(SPK.format(w=c) if (speak and i == 0) else '')}{c}</td>" for i, c in enumerate(r)) + "</tr>"
    return h + "</tbody></table>\n"

def section(name, body, note=""):
    return f"        <section class=\"lesson-section\"><h2>{name}</h2>{('<p class=\"lesson-note\">' + note + '</p>') if note else ''}{body}</section>\n"

# ---------------------------------------------------------------- common words
WORDS = [
 ("Greetings & basics", [
  ("сәлем","sä-lem","hello"),("сау болыңыз","sau bo-lyn-yz","goodbye"),("рахмет","rah-met","thank you"),
  ("өтінемін","ö-ti-ne-min","please"),("кешіріңіз","ke-shi-riñ-iz","excuse me / sorry"),("иә","i-ä","yes"),
  ("жоқ","zhoq","no / there is not"),("бар","bar","there is"),("керек","ke-rek","needed / must"),("жақсы","zhaq-sy","good")]),
 ("Pronouns", [
  ("мен","men","I"),("сен","sen","you (informal)"),("сіз","siz","you (formal)"),("ол","ol","he / she / it"),
  ("біз","biz","we"),("сендер","sen-der","you (plural)"),("олар","o-lar","they")]),
 ("Question words", [
  ("кім","kim","who"),("не","ne","what"),("қайда","qai-da","where"),("қашан","qa-shan","when"),
  ("неге","ne-ge","why"),("қалай","qa-lai","how"),("қанша","qan-sha","how much / many"),("қай","qai","which")]),
 ("Numbers", [
  ("бір","bir","1"),("екі","e-ki","2"),("үш","üsh","3"),("төрт","tört","4"),("бес","bes","5"),
  ("алты","al-ty","6"),("жеті","zhe-ti","7"),("сегіз","se-giz","8"),("тоғыз","to-ghyz","9"),("он","on","10")]),
 ("People", [
  ("адам","a-dam","person"),("бала","ba-la","child"),("әке","ä-ke","father"),("ана","a-na","mother"),
  ("аға","a-gha","older brother"),("апа","a-pa","older sister"),("дос","dos","friend"),("мұғалім","mu-gha-lim","teacher")]),
 ("Verbs (dictionary form ends in -у)", [
  ("болу","bo-lu","to be / become"),("бару","ba-ru","to go"),("келу","ke-lu","to come"),("көру","kö-ru","to see"),
  ("білу","bi-lu","to know"),("алу","a-lu","to take"),("беру","be-ru","to give"),("айту","ai-tu","to say"),
  ("жеу","zheu","to eat"),("ішу","i-shu","to drink"),("оқу","o-qu","to read / study"),("жазу","zha-zu","to write"),
  ("тұру","tu-ru","to stand / live"),("сөйлеу","söi-leu","to speak"),("түсіну","tü-si-nu","to understand")]),
 ("Adjectives", [
  ("үлкен","ül-ken","big"),("кіші","ki-shi","small"),("жаман","zha-man","bad"),("жаңа","zha-ña","new"),
  ("ескі","es-ki","old (things)"),("жылы","zhy-ly","warm"),("суық","su-yq","cold"),("әдемі","ä-de-mi","beautiful"),
  ("көп","köp","many / much"),("аз","az","few / little")]),
 ("Everyday nouns", [
  ("су","su","water"),("нан","nan","bread"),("ет","et","meat"),("шай","shai","tea"),("сүт","süt","milk"),
  ("үй","üi","house / home"),("қала","qa-la","city"),("ауыл","a-uyl","village"),("жол","zhol","road"),
  ("күн","kün","day / sun"),("түн","tün","night"),("жыл","zhyl","year"),("уақыт","ua-qyt","time"),
  ("ақша","aq-sha","money"),("кітап","ki-tap","book"),("есік","e-sik","door")]),
 ("Colors", [
  ("қызыл","qy-zyl","red"),("көк","kök","blue / sky-blue"),("жасыл","zha-syl","green"),("сары","sa-ry","yellow"),
  ("ақ","aq","white"),("қара","qa-ra","black"),("қоңыр","qo-ñyr","brown")]),
 ("Family", [
  ("ата","a-ta","grandfather"),("әже","ä-zhe","grandmother"),("ұл","ul","son / boy"),("қыз","qyz","daughter / girl")]),
 ("Time", [
  ("қазір","qa-zir","now"),("бүгін","bü-gin","today"),("ертең","er-teñ","tomorrow"),("кеше","ke-she","yesterday"),
  ("таңертең","tañ-er-teñ","in the morning"),("кеш","kesh","evening"),("сағат","sa-ghat","hour / clock"),
  ("апта","ap-ta","week"),("ай","ai","month / moon")]),
 ("Days of the week", [
  ("дүйсенбі","düi-sen-bi","Monday"),("сейсенбі","sei-sen-bi","Tuesday"),("сәрсенбі","sär-sen-bi","Wednesday"),
  ("бейсенбі","bei-sen-bi","Thursday"),("жұма","zhu-ma","Friday"),("сенбі","sen-bi","Saturday"),("жексенбі","zhek-sen-bi","Sunday")]),
 ("Food", [
  ("тамақ","ta-maq","food"),("алма","al-ma","apple"),("картоп","kar-top","potato"),("күріш","kü-rish","rice"),
  ("қымыз","qy-myz","kymyz (fermented mare's milk)")]),
 ("Animals", [
  ("ит","it","dog"),("мысық","my-syq","cat"),("ат","at","horse"),("қой","qoi","sheep"),("сиыр","si-yr","cow"),
  ("түйе","tü-ie","camel"),("құс","qus","bird")]),
 ("Body", [
  ("бас","bas","head"),("көз","köz","eye"),("құлақ","qu-laq","ear"),("мұрын","mu-ryn","nose"),
  ("ауыз","a-uyz","mouth"),("қол","qol","hand / arm"),("аяқ","a-yaq","foot / leg"),("жүрек","zhü-rek","heart")]),
 ("Nature", [
  ("тау","tau","mountain"),("өзен","ö-zen","river"),("көл","köl","lake"),("аспан","as-pan","sky"),
  ("жер","zher","earth / land"),("жұлдыз","zhul-dyz","star")]),
 ("Places", [
  ("мектеп","mek-tep","school"),("дүкен","dü-ken","shop"),("базар","ba-zar","market")]),
 ("Useful phrases", [
  ("қалыңыз қалай","qa-lyñ-yz qa-lai","how are you"),("қайырлы таң","qai-yr-ly tañ","good morning"),
  ("қайырлы кеш","qai-yr-ly kesh","good evening"),("қош келдіңіз","qosh kel-diñ-iz","welcome"),
  ("түсінбедім","tü-sin-be-dim","I didn't understand"),("қанша тұрады","qan-sha tu-ra-dy","how much does it cost")]),
]
WORDS_INTRO = "A small core vocabulary goes a long way: the most frequent words appear in most everyday sentences. Learn these, then use the Suffixes and Sentences pages to combine them."
import asyncio, av, numpy as np, edge_tts, base64, json, os
AD = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Common Words/Words Audio"
os.makedirs(AD, exist_ok=True)

def build_clip(word):
    """Male Kazakh voice says the word; trimmed MP3 at peak 0.4, cached in AD by codepoints."""
    f = f"{AD}/{'-'.join(f'{ord(c):x}' for c in word)}.mp3"
    if os.path.exists(f): return f
    print(f"[DEBUG] generating word {word}", flush=True)
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
for _, rows in WORDS:
    for kk, _, _ in rows:
        audio[kk] = base64.b64encode(open(build_clip(kk), "rb").read()).decode()
print(f"[DEBUG] {len(audio)} word clips", flush=True)
PLAYER = """
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
body = "".join(section(n, table(["Kazakh", "Say it", "English"], r, speak=True)) for n, r in WORDS)
open(W + "common-words.html", "w", encoding="utf-8").write(
    HEAD.format(title="Common Words", sub=WORDS_INTRO) + "\n" + body +
    FOOT.format(arrow='<a href="suffixes.html" class="btn">&rarr;</a>').replace("</body>", PLAYER + "</body>"))

# ---------------------------------------------------------------- suffixes
PLURAL = [("after a vowel, л, р, й, у", "-лар / -лер", "бала → балалар, үй → үйлер"),
          ("after м, н, ң, or a voiced consonant (б в г ғ д ж з)", "-дар / -дер", "адам → адамдар, күн → күндер"),
          ("after a voiceless consonant (қ к п с т ш ч ф х ц һ)", "-тар / -тер", "кітап → кітаптар, дос → достар")]
CASES = [("Nominative", "(none)", "үй", "house"),("Genitive (of)", "-дың/-дің, -тың/-тің, -ның/-нің", "үйдің", "of the house"),
         ("Dative (to)", "-ға/-ге, -қа/-ке", "үйге", "to the house"),("Accusative (the, object)", "-ды/-ді, -ты/-ті, -ны/-ні", "үйді", "the house"),
         ("Locative (in / at)", "-да/-де, -та/-те", "үйде", "in the house"),("Ablative (from)", "-дан/-ден, -тан/-тен, -нан/-нен", "үйден", "from the house"),
         ("Instrumental (with / by)", "-мен/-бен/-пен", "үймен", "with the house")]
CASES2 = [("бала","ba-la","child"),("баланың","ba-la-nyñ","of the child"),("балаға","ba-la-gha","to the child"),("баланы","ba-la-ny","the child (object)"),
          ("балада","ba-la-da","at the child"),("баладан","ba-la-dan","from the child"),("баламен","ba-la-men","with the child")]
POSS = [("my","-ым/-ім · after a vowel: -м","менің үйім","my house"),("your","-ың/-ің · after a vowel: -ң","сенің үйің","your house"),
        ("his / her","-ы/-і · after a vowel: -сы/-сі","оның үйі","his/her house"),("our","-ымыз/-іміз · after a vowel: -мыз/-міз","біздің үйіміз","our house")]
BE = [("мен","-мын/-мін/-бын/-бін/-пын/-пін","мұғаліммін","I am a teacher"),("сен","-сың/-сің","мұғалімсің","you are a teacher"),
      ("сіз","-сыз/-сіз","мұғалімсіз","you (formal) are a teacher"),("ол","(none)","мұғалім","he/she is a teacher"),
      ("біз","-быз/-біз/-пыз/-піз/-мыз/-міз","мұғаліммыз","we are teachers")]
VOWEL = ("Kazakh uses <strong>vowel harmony</strong>: a suffix has a back-vowel form (а, ы, о, ұ) and a front-vowel form (е, і, ө, ү, ә), "
         "and you pick the one that matches the last vowel of the word. Consonants also change the suffix's first letter, as the tables show. "
         "Forms in the tables are the standard ones; a few words have irregular changes, so check new words in a dictionary.")
body = section("How suffixes work", "<p class=\"lesson-text\">" + VOWEL + "</p>")
body += section("Plural", table(["The word ends…", "Add", "Examples"], PLURAL))
body += section("Seven cases", table(["Case", "Suffix", "Example", "Meaning"], CASES), "Example word: үй (house). The right form depends on the final sound of the word.")
body += section("Cases on a vowel-ending word", table(["Kazakh", "Say it", "English"], CASES2))
body += section("My, your, his, our", table(["Owner", "Suffix", "Example", "English"], POSS))
body += section("\"I am…\" endings", table(["Pronoun", "Ending", "Example", "English"], BE), "Kazakh has no word for \"am / are / is\" in the present: an ending on the noun does the job.")
open(W + "suffixes.html", "w", encoding="utf-8").write(
    HEAD.format(title="Suffixes", sub="Kazakh builds meaning by adding endings to the end of a word") + "\n" + body +
    FOOT.format(arrow='<a href="sentences.html" class="btn">&rarr;</a>'))

# ---------------------------------------------------------------- sentences
S = [("Менің атым Алма.","Me-niñ a-tym Al-ma","My name is Alma."),
     ("Сіздің атыңыз кім?","Siz-diñ a-tyñ-yz kim","What is your name?"),
     ("Мен студентпін.","Men stu-dent-pin","I am a student."),
     ("Мен студент емеспін.","Men stu-dent e-mes-pin","I am not a student."),
     ("Сен студентсің бе?","Sen stu-dent-siñ be","Are you a student?"),
     ("Бұл не?","Bul ne","What is this?"),
     ("Бұл менің кітабым.","Bul me-niñ ki-ta-bym","This is my book."),
     ("Мен су ішемін.","Men su i-she-min","I drink water."),
     ("Мен кітап оқимын.","Men ki-tap o-qi-myn","I read a book."),
     ("Мен қазақша сөйлеймін.","Men qa-zaq-sha söi-lei-min","I speak Kazakh."),
     ("Мен Қазақстанда тұрамын.","Men Qa-zaq-stan-da tu-ra-myn","I live in Kazakhstan.")]
PATTERNS = [("Subject + Object + Verb","Мен су ішемін.","I water drink (= I drink water)"),
            ("Question: add бе/ба/пе/па/ме/ма at the end","Сен студентсің бе?","Are you a student?"),
            ("Negative of \"to be\": емес + ending","Мен студент емеспін.","I am not a student."),
            ("Place: add the locative suffix","Мен үйдемін.","I am at home.")]
body = section("The big rule: the verb goes last", "<p class=\"lesson-text\">English says \"I drink water\"; Kazakh says \"I water drink\" (subject, object, verb). "
               "Describing words come before the noun they describe, and endings carry the grammar.</p>")
body += section("Patterns", table(["Pattern", "Example", "English"], PATTERNS))
body += section("Example sentences", table(["Kazakh", "Say it", "English"], S), "Combine these with the Common Words and Suffixes pages.")
open(W + "sentences.html", "w", encoding="utf-8").write(
    HEAD.format(title="Sentences", sub="Putting words and endings together") + "\n" + body +
    FOOT.format(arrow='<a href="#" class="btn btn-disabled" aria-disabled="true">&rarr;</a>'))

# ---------------------------------------------------------------- css, index, alphabet arrow
css = open(W + "styles.css", encoding="utf-8").read()
if "lesson-table" not in css:
    css += """
/* ---- Lesson pages ---- */
.lesson-section {
    margin-top: 36px;
}

.lesson-section h2 {
    font-family: 'Cinzel', serif;
    font-size: 1.3rem;
    color: #FFD700;
    margin-bottom: 12px;
}

.lesson-note,
.lesson-text {
    color: rgba(255, 255, 255, 0.85);
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 12px;
}

.lesson-table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    overflow: hidden;
}

.lesson-table th {
    text-align: left;
    padding: 10px 14px;
    font-size: 0.8rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #1a1a2e;
    background: #FFD700;
}

.lesson-table td {
    padding: 10px 14px;
    color: rgba(255, 255, 255, 0.9);
    border-top: 1px solid rgba(255, 215, 0, 0.25);
}

.lesson-table td.c0 {
    color: #FFD700;
    font-weight: 600;
}
"""
    open(W + "styles.css", "w", encoding="utf-8").write(css)

css = open(W + "styles.css", encoding="utf-8").read()
if ".speak" not in css:
    css += """
/* ---- Speaker button in lesson tables ---- */
.speak {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    margin-right: 10px;
    vertical-align: middle;
    color: #FFD700;
    background: rgba(255, 215, 0, 0.12);
    border: 1px solid rgba(255, 215, 0, 0.5);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
}

.speak:hover {
    background: rgba(255, 215, 0, 0.28);
}

.speak.playing {
    background: rgba(255, 215, 0, 0.45);
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
}
"""
    open(W + "styles.css", "w", encoding="utf-8").write(css)

idx = open(W + "index.html", encoding="utf-8").read()
if "common-words.html" not in idx: idx = idx.replace('<a href="alphabet.html" class="btn">Alphabet</a>',
    '<a href="alphabet.html" class="btn">Alphabet</a>\n            <a href="common-words.html" class="btn">Common Words</a>\n'
    '            <a href="suffixes.html" class="btn">Suffixes</a>\n            <a href="sentences.html" class="btn">Sentences</a>')
open(W + "index.html", "w", encoding="utf-8").write(idx)

alpha = open(W + "alphabet.html", encoding="utf-8").read()
alpha = alpha.replace('<a href="#" class="btn btn-disabled" aria-disabled="true">&rarr;</a>', '<a href="common-words.html" class="btn">&rarr;</a>')
open(W + "alphabet.html", "w", encoding="utf-8").write(alpha)
print("[DEBUG] done", flush=True)

# ---------------------------------------------------------------- SEO + mobile
BASE = "https://albazzaztariq.github.io/kazakh-language/"
PAGES = {
 "index.html": ("Free Kazakh Language Course - Learn Kazakh Online",
                "Learn Kazakh free online: the Kazakh Cyrillic alphabet with audio, 140+ common words with pronunciation, suffixes and cases, and basic sentences."),
 "alphabet.html": ("Kazakh Alphabet - 42 Cyrillic Letters with Audio and Pronunciation",
                   "The full Kazakh Cyrillic alphabet: all 42 letters with English pronunciation and a clickable audio clip for each letter."),
 "common-words.html": ("Common Kazakh Words with Audio and Pronunciation",
                       "140+ of the most common Kazakh words and phrases with English meaning, pronunciation guide and audio: greetings, numbers, days, family, food and more."),
 "suffixes.html": ("Kazakh Suffixes and Cases Explained - Plural, Possessive, Grammar Endings",
                   "How Kazakh grammar works: vowel harmony, plural endings, the seven cases, possessive suffixes and 'I am' endings, with examples."),
 "sentences.html": ("Basic Kazakh Sentences and Word Order for Beginners",
                    "Learn how to build simple Kazakh sentences: subject-object-verb word order, questions, negation and example sentences with translations."),
}
MARK = "<!-- seo -->"
for fn, (title, desc) in PAGES.items():
    h = open(W + fn, encoding="utf-8").read()
    if MARK in h: continue
    url = BASE + ("" if fn == "index.html" else fn)
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1)
    tags = (f'{MARK}\n    <meta name="description" content="{desc}">\n    <link rel="canonical" href="{url}">\n'
            f'    <meta name="theme-color" content="#00AFCA">\n    <meta property="og:type" content="website">\n'
            f'    <meta property="og:title" content="{title}">\n    <meta property="og:description" content="{desc}">\n'
            f'    <meta property="og:url" content="{url}">\n    <meta name="twitter:card" content="summary">\n'
            f'    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{title}","description":"{desc}","url":"{url}","inLanguage":"en","about":"Kazakh language"}}</script>\n')
    h = h.replace("</head>", tags + "</head>", 1)
    open(W + fn, "w", encoding="utf-8").write(h)
open(W + "sitemap.xml", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}{'' if fn == 'index.html' else fn}</loc></url>\n" for fn in PAGES) + "</urlset>\n")
open(W + "robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

css = open(W + "styles.css", encoding="utf-8").read()
if "max-width: 480px" not in css:
    css += """
/* ---- Phones ---- */
@media (max-width: 480px) {
    header h1 { font-size: 2rem; }
    .section-title { font-size: 1.5rem; }
    .container { padding: 28px 16px; }
    .alphabet-grid { grid-template-columns: repeat(3, 1fr); gap: 10px; }
    .nav-buttons .btn { width: 100%; text-align: center; }
    .page-nav { gap: 12px; }
    .page-nav .btn { width: 46%; padding: 14px 0; font-size: 1rem; }
    .lesson-table th, .lesson-table td { padding: 9px 8px; font-size: 0.9rem; }
    .speak { width: 36px; height: 36px; margin-right: 8px; }
}
"""
    open(W + "styles.css", "w", encoding="utf-8").write(css)
print("[DEBUG] seo+mobile done", flush=True)
