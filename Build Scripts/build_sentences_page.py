"""Rebuild sentences.html with a literal "Word for word" column and a step-by-step rule for choosing the question particle.

Inputs : the existing sentences.html (its <head>/SEO block is kept as is); tables below are written by hand.
Method : every pattern and example shows Kazakh | (Say it) | Word for word | English, where Word for word keeps Kazakh order and joins
         endings with hyphens ([question] marks the question particle). The question-word section teaches two steps:
         1) last sound decides б / м / п, 2) last vowel decides hard (а) or soft (е).
Output : sentences.html (overwritten); the home/next buttons point to Home and the Verbs page.
"""
import re
print("[DEBUG] sentences page start", flush=True)
B = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
old = open(B + "sentences.html", encoding="utf-8").read()
head = old[:old.index("<body>")]
C4 = ["c0", "c1", "c2", "c3"]
RULE = ("<p class=\"lesson-text\">English says \"I drink water\"; Kazakh says \"I water drink\" (subject, object, verb). "
        "Describing words come before the noun they describe, and endings carry the grammar. "
        "Below, the <strong>Word for word</strong> column shows the exact Kazakh order, with endings joined by hyphens.</p>")
PATTERNS = [
    ("Subject + Object + Verb", "Мен су ішемін.", "I water drink-I", "I drink water."),
    ("Question: put a question particle [ма / ме / ба / бе / па / пе] after the word you are asking about; see how to pick it below", "Сен студентсің бе?", "You student-you-are [question]?", "Are you a student?"),
    ("Negative of \"to be\": емес + ending", "Мен студент емеспін.", "I student not-I-am", "I am not a student."),
    ("Place: add the locative ending (picked on the Suffixes page)", "Мен үйдемін.", "I home-at-I-am", "I am at home."),
]
Q1 = [("a vowel, р, й or у", "м", "бала → ма, бар → ма"),
      ("қ, к, п, с, т, ш", "п", "кітап → па, студент → пе"),
      ("б, в, г, ғ, д, ж, з, л, м, н, ң", "б", "қыз → ба, студентсің → бе")]
Q2 = [("а, о, ы, ұ", "hard", "а", "ма / ба / па"), ("ә, е, і, ү, ө", "soft", "е", "ме / бе / пе")]
Q3 = [
    ("Сен студентсің бе?", "ң → б; last vowel і is soft → бе", "You student-you-are [question]?", "Are you a student?"),
    ("Бұл кітап па?", "п → п; last vowel а is hard → па", "This book [question]?", "Is this a book?"),
    ("Ол келді ме?", "vowel → м; last vowel і is soft → ме", "He came [question]?", "Did he come?"),
    ("Мұнда су бар ма?", "р → м; last vowel а is hard → ма", "Here water exists [question]?", "Is there water here?"),
    ("Бұл қыз ба?", "з → б; last vowel ы is hard → ба", "This girl [question]?", "Is this a girl?"),
    ("Ол студент пе?", "т → п; last vowel е is soft → пе", "He student [question]?", "Is he a student?"),
]
S = [
    ("Менің атым Алма.", "Me-niñ a-tym Al-ma", "My name-my Alma", "My name is Alma."),
    ("Сіздің атыңыз кім?", "Siz-diñ a-tyñ-yz kim", "Your name-your who?", "What is your name?"),
    ("Мен студентпін.", "Men stu-dent-pin", "I student-am", "I am a student."),
    ("Мен студент емеспін.", "Men stu-dent e-mes-pin", "I student not-I-am", "I am not a student."),
    ("Бұл не?", "Bul ne", "This what?", "What is this?"),
    ("Бұл менің кітабым.", "Bul me-niñ ki-ta-bym", "This my book-my", "This is my book."),
    ("Мен су ішемін.", "Men su i-she-min", "I water drink-I", "I drink water."),
    ("Мен кітап оқимын.", "Men ki-tap o-qi-myn", "I book read-I", "I read a book."),
    ("Мен қазақша сөйлеймін.", "Men qa-zaq-sha söi-lei-min", "I Kazakh-in speak-I", "I speak Kazakh."),
    ("Мен Қазақстанда тұрамын.", "Men Qa-zaq-stan-da tu-ra-myn", "I Kazakhstan-in live-I", "I live in Kazakhstan."),
]

def table(h, rows, classes):
    t = "<table class=\"lesson-table\"><thead><tr>" + "".join(f"<th>{x}</th>" for x in h) + "</tr></thead><tbody>"
    for r in rows: t += "<tr>" + "".join(f"<td class=\"{classes[i]}\">{c}</td>" for i, c in enumerate(r)) + "</tr>"
    return t + "</tbody></table>"
sec = lambda title, inner, note="": f"        <section class=\"lesson-section\"><h2>{title}</h2>{('<p class=\"lesson-note\">' + note + '</p>') if note else ''}{inner}</section>\n"

body = sec("The big rule: the verb goes last", RULE)
body += sec("Patterns", table(["Pattern", "Example", "Word for word", "English"], PATTERNS, C4))
body += sec("Questions, step 1: look at the last sound of the word you ask about", table(["The word ends in", "Question particle starts with", "Example"], Q1, ["c0", "c1", "c2"]),
            "Write the question particle separately, after the word.")
body += sec("Questions, step 2: look at the last vowel of that word", table(["Last vowel", "Type", "Question particle ends in", "So you get"], Q2, C4))
body += sec("Questions, worked through", table(["Kazakh", "How it was picked", "Word for word", "English"], Q3, C4))
body += sec("Example sentences", table(["Kazakh", "Say it", "Word for word", "English"], S, C4), "Combine these with the Common Words and Suffixes pages.")
html = head + f"""<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Sentences</h1>
            <p class="section-subtitle">Putting words and endings together</p>
        </header>

        <div class="divider"></div>

{body}
        <div class="page-nav">
            <a href="index.html" class="btn">Home</a>
            <a href="verbs.html" class="btn">&rarr;</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
</body>
</html>
"""
open(B + "sentences.html", "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote sentences.html, {len(html)} bytes", flush=True)
