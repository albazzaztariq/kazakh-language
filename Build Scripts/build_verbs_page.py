"""Build verbs.html: Kazakh verb endings taught as numbered steps, then example sentences (same table style as sentences.html).

Inputs : none; every table below is written by hand (forms were checked against the suffix rules shown on the page itself).
Method : Step 1 stem, Step 2 hard or soft vowel, Step 3 tense ending, spelling exceptions, Step 4 who (person endings),
         a worked "build it" table that applies all four steps, then short example-sentence tables (Kazakh | Say it | English).
         No explanatory paragraphs.
Output : verbs.html in the Web Version folder.
"""
print("[DEBUG] verbs page start", flush=True)
B = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
C3 = ["c0", "c1", "c2"]
STEPS = [
    ("Step 1: Get the stem (drop -у)", ["Dictionary form", "Stem", "English"], C3, [
        ("бару", "бар", "to go"), ("келу", "кел", "to come"), ("алу", "ал", "to take"),
        ("көру", "көр", "to see"), ("ішу", "іш", "to drink")]),
    ("Step 2: Hard or soft? Look at the last vowel of the stem", ["Last vowel", "Type", "Example"], C3, [
        ("а, о, ы, ұ", "hard", "бар, ал, тұр"), ("ә, е, і, ү, ө", "soft", "кел, көр, іш")]),
    ("Step 3: Pick the tense ending (hard or soft, from step 2)", ["Tense", "Hard stem (бар)", "Soft stem (кел)"], C3, [
        ("Past (went)", "бар + ды = барды", "кел + ді = келді"),
        ("Right now (is going)", "бар + ып жатыр", "кел + іп жатыр"),
        ("Usually / future (goes, will go)", "бар + а", "кел + е"),
        ("Have done (has gone)", "бар + ған", "кел + ген"),
        ("Not + past (did not go)", "бар + ма + ды", "кел + ме + ді"),
        ("Not + now / future (does not go)", "бар + ма + й", "кел + ме + й")]),
    ("Spelling exceptions", ["Rule", "Example", "English"], C3, [
        ("Stem ends in қ к п с т ш: ды / ді becomes ты / ті", "кет + ті = кетті", "he left"),
        ("Stem ends in қ к п с т ш: ма / ме becomes па / пе", "іш + пе + й + мін = ішпеймін", "I do not drink"),
        ("Stem ends in қ к п с т ш: ған / ген becomes қан / кен", "кет + кен + мін = кеткенмін", "I have left"),
        ("Stem ends in a vowel: а / е becomes й", "сөйле + й + мін = сөйлеймін", "I speak"),
        ("Stem ends in a vowel: ып / іп becomes п", "істе + п жатыр + мын = істеп жатырмын", "I am working")]),
    ("Step 4: Add who (hard / soft again, same rule as step 2)", ["Who", "Past", "Usually / future", "Right now (after жатыр)"], ["c0", "c1", "c1", "c1"], [
        ("мен (I)", "-м", "-мын / -мін", "-мын"), ("сен (you)", "-ң", "-сың / -сің", "-сың"),
        ("сіз (you, polite)", "-ңыз / -ңіз", "-сыз / -сіз", "-сыз"), ("ол (he / she)", "nothing", "-ды / -ді", "nothing"),
        ("біз (we)", "-қ / -к", "-мыз / -міз", "-мыз"), ("сендер (you all)", "-ңдар / -ңдер", "-сыңдар / -сіңдер", "-сыңдар"),
        ("сіздер (you all, polite)", "-ңыздар / -ңіздер", "-сыздар / -сіздер", "-сыздар"), ("олар (they)", "nothing", "-ды / -ді", "nothing")]),
    ("Put it together, one step at a time", ["English", "Build it", "Kazakh"], ["c2", "c1", "c0"], [
        ("I went", "бару → бар (а = hard) + ды + м", "бардым"),
        ("We came", "келу → кел (е = soft) + ді + к", "келдік"),
        ("He left", "кету → кет (е = soft, ends in т) + ті", "кетті"),
        ("You (polite) will come", "келу → кел (soft) + е + сіз", "келесіз"),
        ("They are going", "бару → бар (hard) + ып жатыр", "барып жатыр"),
        ("He does not go", "бару → бар (hard) + ма + й + ды", "бармайды"),
        ("I do not drink", "ішу → іш (soft, ends in ш) + пе + й + мін", "ішпеймін"),
        ("I have been (gone)", "бару → бар (hard) + ған + мын", "барғанмын")]),
]
GROUPS = [
    ("Examples: past", [
        ("Мен үйге бардым.", "Men üi-ge bar-dym", "I went home."),
        ("Сен мектепке бардың.", "Sen mek-tep-ke bar-dyñ", "You went to school."),
        ("Ол кеше келді.", "Ol ke-she kel-di", "He / she came yesterday."),
        ("Біз кеше келдік.", "Biz ke-she kel-dik", "We came yesterday."),
    ]),
    ("Examples: right now", [
        ("Мен жұмыс істеп жатырмын.", "Men zhu-mys is-tep zha-tyr-myn", "I am working."),
        ("Сен не істеп жатырсың?", "Sen ne is-tep zha-tyr-syñ", "What are you doing?"),
        ("Олар сөйлесіп жатыр.", "O-lar söi-le-sip zha-tyr", "They are talking."),
    ]),
    ("Examples: usually / future", [
        ("Мен су ішемін.", "Men su i-she-min", "I drink water."),
        ("Сен ертең келесің.", "Sen er-teñ ke-le-siñ", "You will come tomorrow."),
        ("Ол күнде жұмысқа барады.", "Ol kün-de zhu-mys-qa ba-ra-dy", "He / she goes to work every day."),
        ("Біз ертең келеміз.", "Biz er-teñ ke-le-miz", "We will come tomorrow."),
    ]),
    ("Examples: have done", [
        ("Мен Қазақстанға барғанмын.", "Men Qa-zaq-stan-gha bar-ghan-myn", "I have been to Kazakhstan."),
        ("Сен мұны көргенсің.", "Sen mu-ny kör-gen-siñ", "You have seen this."),
        ("Ол келген.", "Ol kel-gen", "He / she has come."),
    ]),
    ("Examples: not", [
        ("Мен бармадым.", "Men bar-ma-dym", "I did not go."),
        ("Сен келмедің.", "Sen kel-me-diñ", "You did not come."),
        ("Мен су ішпеймін.", "Men su ish-pei-min", "I do not drink water."),
        ("Олар келмейді.", "O-lar kel-mei-di", "They are not coming."),
    ]),
    ("Commands", [
        ("Үйге бар!", "Üi-ge bar", "Go home! (informal)"),
        ("Қазір келіңіз!", "Qa-zir ke-liñ-iz", "Come now! (polite)"),
        ("Бірге барайық!", "Bir-ge ba-rai-yq", "Let's go together!"),
    ]),
]

def table(head, rows, classes):
    t = "<table class=\"lesson-table\"><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
    for r in rows: t += "<tr>" + "".join(f"<td class=\"{classes[i]}\">{c}</td>" for i, c in enumerate(r)) + "</tr>"
    return t + "</tbody></table>"

body = ""
for name, head, classes, rows in STEPS:
    body += f"        <section class=\"lesson-section\"><h2>{name}</h2>{table(head, rows, classes)}</section>\n"
for name, rows in GROUPS:
    body += f"        <section class=\"lesson-section\"><h2>{name}</h2>{table(['Kazakh', 'Say it', 'English'], rows, C3)}</section>\n"

title = "Kazakh Verb Conjugation Step by Step with Examples"
desc = "Learn Kazakh verb endings step by step: the stem, hard or soft vowels, tense endings and who is doing it, with worked examples for I, you, he, we and they."
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css?v=12">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/verbs.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Verbs</h1>
            <p class="section-subtitle">Four steps to any verb form, then examples</p>
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
