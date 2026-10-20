"""Build verbs.html: Kazakh verb endings taught straight from example sentences, in the same style as sentences.html.

Inputs : none; the sentences below are written by hand (Kazakh | Say it | English), grouped by tense and person.
Method : a Patterns table (formula -> one worked sentence) followed by one example-sentence table per tense, mixing "me" and "someone else".
         No explanatory paragraphs. Page uses the same lesson-table markup/CSS as sentences.html.
Output : verbs.html in the Web Version folder.
"""
print("[DEBUG] verbs page start", flush=True)
B = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
PATTERNS = [
    ("Find the stem: drop -у from the dictionary form", "бару → бар, келу → кел", "to go → bar-, to come → kel-"),
    ("Past: stem + ды/ді + person", "Мен үйге бардым.", "I went home."),
    ("Right now: stem + ып/іп + жатыр + person", "Мен үйге барып жатырмын.", "I am going home."),
    ("Usually / future: stem + а/е + person", "Мен ертең үйге барамын.", "Tomorrow I will go home."),
    ("Have done: stem + ған/ген + person", "Мен үйге барғанмын.", "I have been home."),
    ("Not (past): stem + ма/ме + ды/ді + person", "Мен үйге бармадым.", "I did not go home."),
    ("Not (now / future): stem + ма/ме + й + person", "Мен үйге бармаймын.", "I do not go / will not go home."),
    ("Command: the bare stem", "Үйге бар!", "Go home!"),
    ("After қ к п с т ш: ды becomes ты", "кет + ті + м = кеттім", "I left"),
    ("Stem ends in a vowel: а/е becomes й", "оқы + й + мын = оқимын", "I read"),
]
GROUPS = [
    ("Past: ды / ді", [
        ("Мен үйге бардым.", "Men üi-ge bar-dym", "I went home."),
        ("Сен мектепке бардың.", "Sen mek-tep-ke bar-dyñ", "You went to school."),
        ("Сіз Алматыға бардыңыз.", "Siz Al-ma-ty-gha bar-dyñ-yz", "You went to Almaty (polite)."),
        ("Ол кеше келді.", "Ol ke-she kel-di", "He / she came yesterday."),
        ("Біз кеше келдік.", "Biz ke-she kel-dik", "We came yesterday."),
        ("Сендер кеше келдіңдер ме?", "Sen-der ke-she kel-diñ-der me", "Did you all come yesterday?"),
        ("Олар кеше келді.", "O-lar ke-she kel-di", "They came yesterday."),
    ]),
    ("Right now: ып / іп + жатыр", [
        ("Мен жұмыс істеп жатырмын.", "Men zhu-mys is-tep zha-tyr-myn", "I am working."),
        ("Сен не істеп жатырсың?", "Sen ne is-tep zha-tyr-syñ", "What are you doing?"),
        ("Ол ойнап жатыр.", "Ol oi-nap zha-tyr", "He / she is playing."),
        ("Біз оқып жатырмыз.", "Biz o-qyp zha-tyr-myz", "We are studying."),
        ("Олар сөйлесіп жатыр.", "O-lar söi-le-sip zha-tyr", "They are talking."),
    ]),
    ("Usually / future: а / е", [
        ("Мен су ішемін.", "Men su i-she-min", "I drink water."),
        ("Сен ертең келесің.", "Sen er-teñ ke-le-siñ", "You will come tomorrow."),
        ("Сіз қазақша сөйлейсіз.", "Siz qa-zaq-sha söi-lei-siz", "You speak Kazakh (polite)."),
        ("Ол күнде жұмысқа барады.", "Ol kün-de zhu-mys-qa ba-ra-dy", "He / she goes to work every day."),
        ("Біз ертең келеміз.", "Biz er-teñ ke-le-miz", "We will come tomorrow."),
        ("Сендер нан жейсіңдер.", "Sen-der nan zhei-siñ-der", "You all eat bread."),
        ("Олар қалада тұрады.", "O-lar qa-la-da tu-ra-dy", "They live in the city."),
    ]),
    ("Have done: ған / ген", [
        ("Мен Қазақстанға барғанмын.", "Men Qa-zaq-stan-gha bar-ghan-myn", "I have been to Kazakhstan."),
        ("Сен мұны көргенсің.", "Sen mu-ny kör-gen-siñ", "You have seen this."),
        ("Ол келген.", "Ol kel-gen", "He / she has come."),
        ("Олар келген.", "O-lar kel-gen", "They have come."),
    ]),
    ("Not: ма / ме", [
        ("Мен бармадым.", "Men bar-ma-dym", "I did not go."),
        ("Сен келмедің.", "Sen kel-me-diñ", "You did not come."),
        ("Ол жұмысқа бармады.", "Ol zhu-mys-qa bar-ma-dy", "He / she did not go to work."),
        ("Мен су ішпеймін.", "Men su ish-pei-min", "I do not drink water."),
        ("Біз ертең бармаймыз.", "Biz er-teñ bar-mai-myz", "We will not go tomorrow."),
        ("Олар келмейді.", "O-lar kel-mei-di", "They are not coming."),
    ]),
    ("Commands", [
        ("Үйге бар!", "Üi-ge bar", "Go home! (informal)"),
        ("Мұнда кел!", "Mun-da kel", "Come here! (informal)"),
        ("Қазір келіңіз!", "Qa-zir ke-liñ-iz", "Come now! (polite)"),
        ("Су ішіңдер!", "Su i-shiñ-der", "Drink water! (you all)"),
        ("Бірге барайық!", "Bir-ge ba-rai-yq", "Let's go together!"),
    ]),
]

def table(head, rows, classes):
    t = "<table class=\"lesson-table\"><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
    for r in rows: t += "<tr>" + "".join(f"<td class=\"{classes[i]}\">{c}</td>" for i, c in enumerate(r)) + "</tr>"
    return t + "</tbody></table>"

body = f"<section class=\"lesson-section\"><h2>Patterns</h2>{table(['Pattern', 'Example', 'English'], PATTERNS, ['c0', 'c1', 'c2'])}</section>\n"
for name, rows in GROUPS:
    body += f"        <section class=\"lesson-section\"><h2>{name}</h2>{table(['Kazakh', 'Say it', 'English'], rows, ['c0', 'c1', 'c2'])}</section>\n"

title = "Kazakh Verb Conjugation with Example Sentences"
desc = "Learn Kazakh verb endings from example sentences: past, present, future, have done, negative and commands, for I, you, he, we and they."
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css?v=2">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/verbs.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Verbs</h1>
            <p class="section-subtitle">Verb endings, learned from examples</p>
        </header>

        <div class="divider"></div>

        {body}
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
