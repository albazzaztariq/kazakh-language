"""Build game.html: a flash-card word game for the Common Words vocabulary.

Inputs : common-words.html (every table row: Kazakh word, English meaning, topic section), read at build time so the game always matches the page.
Method : the page embeds the cards as JSON. Each round shows one Kazakh word (no pronunciation line) and four English choices: the right one plus three
         distractors, preferring the same topic and never sharing a meaningful word with the right answer (so "thin" never competes with "thin / slender").
         A wrong pick turns red and stays red; picking more wrong ones turns them red too; the right pick turns green, everything locks for 3 seconds,
         then the next card appears. Cards come in a shuffled order and the deck reshuffles when it runs out. Keys 1-4 also pick a choice.
Output : game.html (styles live in styles.css under "Word game").
"""
import re, json, html
print("[DEBUG] game page start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
src = open(W + "common-words.html", encoding="utf-8").read()
cards = []
for sid, title, body in re.findall(r'<section class="lesson-section" id="([^"]+)"><h2>(.*?)</h2>(.*?)</section>', src, re.S):
    for kk, en in re.findall(r'</button>(.*?)</td><td class="c1">.*?</td><td class="c2">(.*?)</td>', body):
        cards.append({"k": html.unescape(kk), "e": html.unescape(en), "s": sid})
print(f"[DEBUG] {len(cards)} cards from {len(set(c['s'] for c in cards))} sections", flush=True)

title = "Kazakh Word Game: Flash Cards for Common Words"
desc = "Practice common Kazakh words with a flash-card game: see the word, pick the English meaning from four choices."
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <link rel="stylesheet" href="styles.css?v=5">
    <meta name="description" content="%(desc)s">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/game.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Word Game</h1>
            <p class="section-subtitle">Common Words flash cards</p>
        </header>

        <div class="divider"></div>

        <div class="game">
            <p class="game-status" id="status" aria-live="polite"></p>
            <div class="game-word" id="word" lang="kk"></div>
            <div class="game-choices" id="choices"></div>
        </div>

        <div class="page-nav">
            <a href="common-words.html" class="btn">&larr;</a>
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>

    <script>
        const CARDS = %(cards)s;
        const STOP = new Set(['to', 'a', 'the', 'of', 'or', 'and', 'in']);
        const NEXT_DELAY_MS = 3000;
        const wordEl = document.getElementById('word'), choicesEl = document.getElementById('choices'), statusEl = document.getElementById('status');
        let deck = [], current = null, locked = false, wrongThisCard = 0, seen = 0, firstTry = 0;

        const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        const tokens = s => new Set(s.toLowerCase().replace(/\\(.*?\\)/g, ' ').split(/[^a-z']+/).filter(w => w && !STOP.has(w)));
        const clash = (a, b) => a.e.toLowerCase() === b.e.toLowerCase() || [...tokens(a.e)].some(t => tokens(b.e).has(t));

        function pickChoices(card) {
            const others = shuffle(CARDS.filter(c => c !== card && !clash(card, c)));
            const chosen = [];
            const take = list => { for (const c of list) { if (chosen.length >= 3) break; if (!chosen.some(x => clash(x, c))) chosen.push(c); } };
            take(others.filter(c => c.s === card.s).slice(0, 2));
            take(others);
            return shuffle([card, ...chosen]);
        }

        function nextCard() {
            if (!deck.length) deck = shuffle(CARDS);
            current = deck.pop(); locked = false; wrongThisCard = 0; seen++;
            wordEl.textContent = current.k;
            choicesEl.innerHTML = '';
            pickChoices(current).forEach((c, i) => {
                const b = document.createElement('button');
                b.type = 'button'; b.className = 'choice'; b.textContent = c.e; b.dataset.key = i + 1;
                b.addEventListener('click', () => answer(b, c));
                choicesEl.appendChild(b);
            });
            statusEl.textContent = 'Card ' + seen + ' \\u00b7 first try: ' + firstTry + ' of ' + (seen - 1);
        }

        function answer(btn, card) {
            if (locked || btn.classList.contains('wrong')) return;
            if (card === current) {
                locked = true; btn.classList.add('correct');
                if (wrongThisCard === 0) firstTry++;
                statusEl.textContent = 'Card ' + seen + ' \\u00b7 first try: ' + firstTry + ' of ' + seen;
                setTimeout(nextCard, NEXT_DELAY_MS);
            } else {
                wrongThisCard++; btn.classList.add('wrong'); btn.disabled = true;
            }
        }

        document.addEventListener('keydown', e => {
            const b = choicesEl.querySelector('.choice[data-key="' + e.key + '"]');
            if (b && !b.disabled) b.click();
        });
        nextCard();
    </script>
</body>
</html>
""" % {"title": title, "desc": desc, "cards": json.dumps(cards, ensure_ascii=False)}
open(W + "game.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote game.html, {len(page)} bytes", flush=True)
