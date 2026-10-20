"""Build verbs.html: a short, example-driven Kazakh verb conjugation page.

Inputs : none (everything is generated from the stems and suffix lists below, so every form on the page is produced by one rule).
Method : two worked verbs, hard-vowel бару (stem бар-) and soft-vowel келу (stem кел-). Each table row is stem + tense suffix + personal ending,
         built by code from the HARD/SOFT suffix pairs, so the page cannot disagree with its own rules.
Output : verbs.html (same CSS/layout as the other lesson pages; no paragraphs, only a one-line subtitle, steps, tables).
"""
print("[DEBUG] verbs page start", flush=True)
B = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
PERSONS = [("мен", "I"), ("сен", "you (informal)"), ("сіз", "you (polite)"), ("ол", "he / she"), ("біз", "we"),
           ("сендер", "you all (informal)"), ("сіздер", "you all (polite)"), ("олар", "they")]
# Each suffix is (hard, soft). Personal-ending sets are listed per person in the order of PERSONS.
PAST_END = [("м", "м"), ("ң", "ң"), ("ңыз", "ңіз"), ("", ""), ("қ", "к"), ("ңдар", "ңдер"), ("ңыздар", "ңіздер"), ("", "")]
MYN_END = [("мын", "мін"), ("сың", "сің"), ("сыз", "сіз"), ("", ""), ("мыз", "міз"), ("сыңдар", "сіңдер"), ("сыздар", "сіздер"), ("", "")]
ADY_END = [("мын", "мін"), ("сың", "сің"), ("сыз", "сіз"), ("ды", "ді"), ("мыз", "міз"), ("сыңдар", "сіңдер"), ("сыздар", "сіздер"), ("ды", "ді")]
PERF_END = [MYN_END[0], MYN_END[1], MYN_END[2], ("", ""), ("быз", "біз"), MYN_END[5], MYN_END[6], ("", "")]
VERBS = [("бар", 0, "бару", "go"), ("кел", 1, "келу", "come")]          # (stem, 0 hard / 1 soft, dictionary form, English)

def col(i, build): return [build(VERBS[i][0], VERBS[i][1], p) for p in range(8)]
def past(s, h, p): return s + ("ды", "ді")[h] + PAST_END[p][h]
def cont(s, h, p): return s + ("ып", "іп")[h] + " жатыр" + MYN_END[p][0]          # жатыр is a hard word, so its endings are always hard
def habit(s, h, p): return s + ("а", "е")[h] + ADY_END[p][h]
def perf(s, h, p): return s + ("ған", "ген")[h] + PERF_END[p][h]
def npast(s, h, p): return s + ("ма", "ме")[h] + ("ды", "ді")[h] + PAST_END[p][h]
def npres(s, h, p): return s + ("ма", "ме")[h] + "й" + ADY_END[p][h]

TENSES = [
    ("Past", "stem + ды/ді + person", past, ["I went", "you went", "you went", "he/she went", "we went", "you all went", "you all went", "they went"]),
    ("Now (happening right now)", "stem + ып/іп + жатыр + person", cont, ["I am going", "you are going", "you are going", "he/she is going", "we are going", "you all are going", "you all are going", "they are going"]),
    ("Usually / future", "stem + а/е + person (add ертең, tomorrow, to make it future)", habit, ["I go / will go", "you go / will go", "you go / will go", "he/she goes / will go", "we go / will go", "you all go / will go", "you all go / will go", "they go / will go"]),
    ("Have done", "stem + ған/ген + person", perf, ["I have gone", "you have gone", "you have gone", "he/she has gone", "we have gone", "you all have gone", "you all have gone", "they have gone"]),
    ("Not (past)", "stem + ма/ме + ды/ді + person", npast, ["I did not go", "you did not go", "you did not go", "he/she did not go", "we did not go", "you all did not go", "you all did not go", "they did not go"]),
    ("Not (now / future)", "stem + ма/ме + й + person", npres, ["I do not go", "you do not go", "you do not go", "he/she does not go", "we do not go", "you all do not go", "you all do not go", "they do not go"]),
]

def table(rows, head):
    t = "<table class=\"lesson-table\"><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
    for r in rows: t += "<tr>" + "".join(f"<td class=\"c0\">{c}</td>" if i == 0 else f"<td>{c}</td>" for i, c in enumerate(r)) + "</tr>"
    return t + "</tbody></table>"

sections = ""
for name, formula, fn, eng in TENSES:
    rows = [(PERSONS[p][0], col(0, fn)[p], col(1, fn)[p], eng[p]) for p in range(8)]
    sections += f"<section class=\"lesson-section\"><h2>{name}</h2><ul class=\"steps\"><li>{formula}</li></ul>{table(rows, ['Who', 'бару (go)', 'келу (come)', 'English'])}</section>\n"
CMD = [("сен", "бар", "кел", "go! (informal)"), ("сіз", "барыңыз", "келіңіз", "go! (polite)"), ("сендер", "барыңдар", "келіңдер", "go! (you all)"),
       ("сіздер", "барыңыздар", "келіңіздер", "go! (you all, polite)"), ("біз", "барайық", "келейік", "let's go")]
sections += f"<section class=\"lesson-section\"><h2>Commands</h2><ul class=\"steps\"><li>informal: bare stem &middot; polite: stem + ыңыз/іңіз &middot; let's: stem + айық/ейік</li></ul>{table(CMD, ['Who', 'бару (go)', 'келу (come)', 'English'])}</section>\n"

steps = f"""<section class="lesson-section"><h2>How to build any verb form</h2><ul class="steps">
<li>1. Take the dictionary form and drop -у: <strong>бару</strong> &rarr; <strong>бар</strong>, <strong>келу</strong> &rarr; <strong>кел</strong></li>
<li>2. Add the tense suffix: hard vowels (а, о, ы, ұ) use а/ды/ған, soft vowels (ә, е, і, ү, ө) use е/ді/ген</li>
<li>3. Add the person ending: -м (I), -ң (you), -ңыз (polite), nothing (he/she/they)</li>
<li>I went: бар + ды + м = <strong>бардым</strong></li>
<li>We came: кел + ді + к = <strong>келдік</strong></li>
<li>I do not go: бар + ма + й + мын = <strong>бармаймын</strong></li>
<li>Voiceless ending (қ к п с т ш ч ц щ ф х һ): ды becomes ты: кет + ті + м = <strong>кеттім</strong> (I left)</li>
<li>Stem ends in a vowel: а/е becomes й: оқы + й + мын = <strong>оқимын</strong> (I read), сөйле + й + мін = <strong>сөйлеймін</strong> (I speak)</li>
</ul></section>
"""
title = "Kazakh Verb Conjugation - Past, Present, Future, Negative"
desc = "Kazakh verb conjugation made simple: past, present, future, have done, negative and commands, with every person worked through on two example verbs."
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/verbs.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Verb Conjugation</h1>
            <p class="section-subtitle">stem + tense + person, worked through on бару (go) and келу (come)</p>
        </header>

        <div class="divider"></div>

        {steps}
        {sections}
        <div class="page-nav">
            <a href="sentences.html" class="btn">&larr;</a>
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
</body>
</html>
"""
open(B + "verbs.html", "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote verbs.html, {len(html)} bytes", flush=True)
