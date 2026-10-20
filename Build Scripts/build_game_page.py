"""Build game.html: a flash-card word game for the Common Words vocabulary, 20 cards per deck, scored out of 100.

Inputs : common-words.html (every table row: Kazakh word, English meaning, topic section), read at build time so the game always matches the page.
Method : a deck is 20 random cards (a new deck avoids words already used in earlier decks until the vocabulary runs out). Each card shows one Kazakh
         word (no pronunciation line) and four English choices: the right one plus three distractors, preferring the same topic and never sharing a
         meaningful word with the right answer. A wrong pick turns red and stays red (more wrong picks turn red too); the right pick turns green,
         everything locks for 1.5 seconds, then the next card appears. A rolling click-counter shows "Cards Completed".
         Scoring: every card is worth 5 points and its three possible wrong picks each cost a third of that, so
         score = 100 x (1 - wrong picks / (20 x 3)). All first-try = 100; one card with one wrong pick = 98 (98.33 rounded); a card needing all
         three wrong picks first = 0 for that card. The score appears only after the 20th card, with "Repeat This Deck" and "Generate New Deck".
         Keys 1-4 also pick a choice.
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

JS = r"""
        const STOP = new Set(['to', 'a', 'the', 'of', 'or', 'and', 'in']);
        const NEXT_DELAY_MS = 1500, DECK_SIZE = 20, MAX_WRONG_PER_CARD = 3;
        const wordEl = document.getElementById('word'), choicesEl = document.getElementById('choices'), countEl = document.getElementById('count');
        const playEl = document.getElementById('play'), resultEl = document.getElementById('result'), scoreEl = document.getElementById('score');
        let deckCards = [], deck = [], current = null, locked = false, completed = 0, wrongPicks = 0;
        const used = new Set();

        const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        const tokens = s => new Set(s.toLowerCase().replace(/\(.*?\)/g, ' ').split(/[^a-z']+/).filter(w => w && !STOP.has(w)));
        const clash = (a, b) => a.e.toLowerCase() === b.e.toLowerCase() || [...tokens(a.e)].some(t => tokens(b.e).has(t));

        function pickChoices(card) {
            const others = shuffle(CARDS.filter(c => c !== card && !clash(card, c)));
            const chosen = [];
            const take = list => { for (const c of list) { if (chosen.length >= 3) break; if (!chosen.some(x => clash(x, c))) chosen.push(c); } };
            take(others.filter(c => c.s === card.s).slice(0, 2));
            take(others);
            return shuffle([card, ...chosen]);
        }

        // Click-counter style tally: one strip of digits 0-9 per place; changing a digit rolls its strip.
        function showCount() {
            const text = String(completed).padStart(2, '0');
            while (countEl.children.length < text.length) {
                const cell = document.createElement('span'); cell.className = 'digit';
                const strip = document.createElement('span'); strip.className = 'digit-strip';
                for (let d = 0; d < 10; d++) { const n = document.createElement('span'); n.textContent = d; strip.appendChild(n); }
                cell.appendChild(strip); countEl.insertBefore(cell, countEl.firstChild);
            }
            [...countEl.children].forEach((cell, i) => { cell.firstChild.style.transform = 'translateY(' + (-Number(text[i]) * 1.2) + 'em)'; });
            countEl.setAttribute('aria-label', 'Cards completed: ' + completed);
            countEl.classList.remove('tick'); void countEl.offsetWidth; countEl.classList.add('tick');
        }

        function startDeck() {
            deck = shuffle(deckCards); completed = 0; wrongPicks = 0;
            resultEl.hidden = true; playEl.hidden = false;
            showCount(); nextCard();
        }

        function newDeck() {
            let fresh = shuffle(CARDS.filter(c => !used.has(c)));
            if (fresh.length < DECK_SIZE) { used.clear(); fresh = shuffle(CARDS); }
            deckCards = fresh.slice(0, DECK_SIZE);
            deckCards.forEach(c => used.add(c));
            startDeck();
        }

        // 5 points per card; each wrong pick costs a third of a card (a card can have at most 3 wrong picks).
        function finishDeck() {
            scoreEl.textContent = Math.round(100 * (1 - wrongPicks / (deckCards.length * MAX_WRONG_PER_CARD)));
            playEl.hidden = true; resultEl.hidden = false;
        }

        function nextCard() {
            if (!deck.length) { finishDeck(); return; }
            current = deck.pop(); locked = false;
            wordEl.textContent = current.k;
            choicesEl.innerHTML = '';
            pickChoices(current).forEach((c, i) => {
                const b = document.createElement('button');
                b.type = 'button'; b.className = 'choice'; b.textContent = c.e; b.dataset.key = i + 1;
                b.addEventListener('click', () => answer(b, c));
                choicesEl.appendChild(b);
            });
        }

        function answer(btn, card) {
            if (locked || btn.classList.contains('wrong')) return;
            if (card === current) {
                locked = true; btn.classList.add('correct');
                completed++; showCount();
                setTimeout(nextCard, NEXT_DELAY_MS);
            } else {
                wrongPicks++; btn.classList.add('wrong'); btn.disabled = true;
            }
        }

        document.addEventListener('keydown', e => {
            const b = choicesEl.querySelector('.choice[data-key="' + e.key + '"]');
            if (b && !b.disabled && !playEl.hidden) b.click();
        });
        document.getElementById('repeat').addEventListener('click', startDeck);
        document.getElementById('fresh').addEventListener('click', newDeck);
        newDeck();
"""

title = "Kazakh Word Game: Flash Cards for Common Words"
desc = "Practice common Kazakh words with a flash-card game: see the word, pick the English meaning from four choices, 20 cards per deck."
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <link rel="stylesheet" href="styles.css?v=7">
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
            <div class="tally" aria-live="polite">
                <span class="tally-label">Cards Completed</span>
                <div class="tally-digits" id="count" aria-label="Cards completed: 0"></div>
            </div>
            <div id="play">
                <div class="game-word" id="word" lang="kk"></div>
                <div class="game-choices" id="choices"></div>
            </div>
            <div class="game-result" id="result" hidden>
                <div class="result-label">Score</div>
                <div class="result-score"><span id="score">0</span><span class="result-max"> / 100</span></div>
                <div class="game-actions">
                    <button type="button" class="btn" id="repeat">Repeat This Deck</button>
                    <button type="button" class="btn" id="fresh">Generate New Deck</button>
                </div>
            </div>
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
%(js)s    </script>
</body>
</html>
""" % {"title": title, "desc": desc, "cards": json.dumps(cards, ensure_ascii=False), "js": JS}
open(W + "game.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote game.html, {len(page)} bytes", flush=True)
