"""Build game.html (the "Common Words Test"): flash cards for the Common Words vocabulary, in either direction, with group selection, scored out of 100.

Inputs : common-words.html (every table row: Kazakh word, English meaning, topic section), read at build time so the game always matches the page.
Flow   : 1) Setup screen. "Question Word Displayed in:" with Kazakh / English buttons (one is always selected), then "Select One or More Groups of
            Vocabulary to Review" over toggle buttons (one per topic group; the four adjective sections form one "Adjectives" group). Below them a
            distinct "Any" button: when on, groups are locked off and a card-count slider + text field appears (5 to 50; typing 4 or less shows
            "5 Card Minimum" and snaps to 5 on leaving the field, typing over 50 shows "50 Card Maximum" and clamps to 50). A green "Go" starts.
         2) Play. A group deck is every word in the selected groups; an Any deck is N random words, avoiding words used in earlier Any decks until the
            vocabulary runs out. Kazakh mode shows the Kazakh word (speaker button plays its clip, nothing autoplays) and four English choices; English
            mode shows the English meaning and four Kazakh choices (no speaker, it would give the answer away).
            The wrong choices always come from the question's own group (an adjective question only gets adjective choices); only when a group is too
            small (Places has 3 words) they may also come from the other noun groups, and only as a last resort from anywhere. Choices never share a
            meaningful English word with the right answer. A wrong pick turns red and stays red; the right pick turns green, everything locks for
            1.5 seconds, then the next card appears. A rolling click-counter shows "Cards Completed" = unique cards ever completed this visit; it
            only animates when the number actually changes.
         3) Results (score only here). Score = 100 x (1 - wrong picks / (cards x 3)). Buttons: Repeat This Deck, Generate New Deck (Any mode only),
            Change Groups.
Keys 1-4 also pick a choice. Output: game.html (styles live in styles.css under "Word game").
"""
import re, json, html, os
print("[DEBUG] game page start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
src = open(W + "common-words.html", encoding="utf-8").read()
cards = []
for sid, title, body in re.findall(r'<section class="lesson-section" id="([^"]+)"><h2>(.*?)</h2>(.*?)</section>', src, re.S):
    group = "Adjectives" if sid.startswith("adjectives") else html.unescape(title)
    group = {"Greetings & basics": "Greetings & Basics", "Question words": "Question Words", "Everyday nouns": "Everyday Nouns",
             "Days of the week": "Days of the Week", "Verbs (dictionary form ends in -у)": "Verbs"}.get(group, group)
    for kk, en in re.findall(r'</button>(.*?)</td><td class="c1">.*?</td><td class="c2">(.*?)</td>', body):
        cards.append({"k": html.unescape(kk), "e": html.unescape(en), "g": group})
groups = list(dict.fromkeys(c["g"] for c in cards))
print(f"[DEBUG] {len(cards)} cards in {len(groups)} groups: " + ", ".join(f"{g} {sum(1 for c in cards if c['g'] == g)}" for g in groups), flush=True)
missing = [c["k"] for c in cards if not os.path.exists(W + "Common Words/Words Audio/" + "-".join(f"{ord(ch):x}" for ch in c["k"]) + ".mp3")]
assert not missing, f"no audio clip for {missing}"   # the speaker button loads these files, so every card needs one

JS = r"""
        const STOP = new Set(['to', 'a', 'the', 'of', 'or', 'and', 'in']);
        const NEXT_DELAY_MS = 1500, MIN_SIZE = 5, MAX_SIZE = 50, MAX_WRONG_PER_CARD = 3;
        // Groups whose words are all nouns: a tiny noun group (Places has 3 words) may borrow wrong choices from the other noun groups.
        const NOUN_GROUPS = new Set(['People', 'Everyday Nouns', 'Family', 'Food', 'Animals', 'Body', 'Nature', 'Places', 'Days of the Week', 'Time']);
        const $ = id => document.getElementById(id);
        const setupEl = $('setup'), roundEl = $('round'), groupsEl = $('groups'), anyBtn = $('anyBtn'), goBtn = $('go'), sizeBox = $('sizeBox');
        const wordEl = $('word'), choicesEl = $('choices'), countEl = $('count'), playEl = $('play'), resultEl = $('result'), scoreEl = $('score');
        const rangeEl = $('sizeRange'), numEl = $('sizeNum'), msgEl = $('sizeMsg'), freshBtn = $('fresh'), speakEl = $('speak');
        const langKk = $('langKk'), langEn = $('langEn');
        let deckCards = [], deck = [], current = null, locked = false, wrongPicks = 0, deckSize = 20, anyMode = false, anySelected = false, nextTimer = null;
        let lang = 'kk';                   // language of the question: 'kk' = Kazakh word shown, English choices; 'en' = English shown, Kazakh choices
        const selected = new Set();        // chosen group names
        const used = new Set();            // cards already dealt in an Any deck (new Any decks avoid them until the vocabulary runs out)
        const completedCards = new Set();  // every unique card answered correctly this visit; the counter shows its size

        const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        const tokens = s => new Set(s.toLowerCase().replace(/\(.*?\)/g, ' ').split(/[^a-z']+/).filter(w => w && !STOP.has(w)));
        const clash = (a, b) => a.e.toLowerCase() === b.e.toLowerCase() || [...tokens(a.e)].some(t => tokens(b.e).has(t));

        // ---- setup screen ----
        function setLang(l) {
            lang = l;
            langKk.setAttribute('aria-pressed', l === 'kk' ? 'true' : 'false');
            langEn.setAttribute('aria-pressed', l === 'en' ? 'true' : 'false');
        }
        langKk.addEventListener('click', () => setLang('kk'));
        langEn.addEventListener('click', () => setLang('en'));

        const GROUP_NAMES = [...new Set(CARDS.map(c => c.g))];
        GROUP_NAMES.forEach(name => {
            const b = document.createElement('button');
            b.type = 'button'; b.className = 'group-btn'; b.textContent = name; b.setAttribute('aria-pressed', 'false');
            b.addEventListener('click', () => { if (anySelected) return; selected.has(name) ? selected.delete(name) : selected.add(name); refreshSetup(); });
            groupsEl.appendChild(b);
        });
        function refreshSetup() {
            [...groupsEl.children].forEach(b => {
                b.setAttribute('aria-pressed', selected.has(b.textContent) ? 'true' : 'false');
                b.disabled = anySelected;
            });
            anyBtn.setAttribute('aria-pressed', anySelected ? 'true' : 'false');
            sizeBox.hidden = !anySelected;                       // the card-count slider only exists in Any mode
            goBtn.disabled = !(anySelected || selected.size > 0);
        }
        anyBtn.addEventListener('click', () => { anySelected = !anySelected; if (anySelected) selected.clear(); refreshSetup(); });

        // ---- card-count slider + text field (Any mode), limits 5 to 50 ----
        const showMsg = text => { msgEl.textContent = text; };
        function setSize(n) { deckSize = n; rangeEl.value = n; numEl.value = n; }
        rangeEl.addEventListener('input', () => { setSize(Number(rangeEl.value)); showMsg(''); });
        numEl.addEventListener('input', () => {
            numEl.value = numEl.value.replace(/[^0-9]/g, '').slice(0, 3);
            if (numEl.value === '') { showMsg(''); return; }
            const n = Number(numEl.value);
            if (n > MAX_SIZE) { setSize(MAX_SIZE); showMsg(MAX_SIZE + ' Card Maximum'); }
            else if (n < MIN_SIZE) { showMsg(MIN_SIZE + ' Card Minimum'); }      // not applied; the field snaps back when you leave it
            else { deckSize = n; rangeEl.value = n; showMsg(''); }
        });
        function settleSize() {                                  // called when leaving the field and on Go
            if (numEl.value === '') { numEl.value = deckSize; showMsg(''); return; }
            const n = Number(numEl.value);
            if (n < MIN_SIZE) { setSize(MIN_SIZE); showMsg(MIN_SIZE + ' Card Minimum'); }
        }
        numEl.addEventListener('blur', settleSize);
        numEl.addEventListener('keydown', e => { if (e.key === 'Enter') numEl.blur(); });

        // ---- play ----
        // Wrong choices: same group first, then (noun groups only) the other noun groups, then anywhere as a last resort; never a clash with the answer.
        function pickChoices(card) {
            const ok = c => c !== card && !clash(card, c);
            const chosen = [];
            const take = list => { for (const c of shuffle(list)) { if (chosen.length >= 3) break; if (!chosen.some(x => clash(x, c))) chosen.push(c); } };
            take(CARDS.filter(c => ok(c) && c.g === card.g));
            if (chosen.length < 3 && NOUN_GROUPS.has(card.g)) take(CARDS.filter(c => ok(c) && c.g !== card.g && NOUN_GROUPS.has(c.g)));
            if (chosen.length < 3) take(CARDS.filter(c => ok(c)));
            return shuffle([card, ...chosen]);
        }

        // Click-counter style tally: one strip of digits 0-9 per place; changing a digit rolls its strip. It only animates when the number changes.
        let shownText = null;
        function showCount() {
            const text = String(completedCards.size).padStart(3, '0');
            if (text === shownText) return;
            while (countEl.children.length < text.length) {
                const cell = document.createElement('span'); cell.className = 'digit';
                const strip = document.createElement('span'); strip.className = 'digit-strip';
                for (let d = 0; d < 10; d++) { const n = document.createElement('span'); n.textContent = d; strip.appendChild(n); }
                cell.appendChild(strip); countEl.insertBefore(cell, countEl.firstChild);
            }
            [...countEl.children].forEach((cell, i) => { cell.firstChild.style.transform = 'translateY(' + (-Number(text[i]) * 1.2) + 'em)'; });
            countEl.setAttribute('aria-label', 'Cards completed: ' + completedCards.size);
            if (shownText !== null) { countEl.classList.remove('tick'); void countEl.offsetWidth; countEl.classList.add('tick'); }
            shownText = text;
        }

        // Repeating a deck keeps the counter where it is: it only counts cards never completed before.
        function startDeck() {
            deck = shuffle(deckCards); wrongPicks = 0;
            resultEl.hidden = true; playEl.hidden = false; freshBtn.hidden = !anyMode;
            speakEl.hidden = lang !== 'kk';                      // an English question has no audio (it would give the answer away)
            nextCard();
        }

        function newAnyDeck() {
            let fresh = shuffle(CARDS.filter(c => !used.has(c)));
            if (fresh.length < deckSize) { used.clear(); fresh = shuffle(CARDS); }
            deckCards = fresh.slice(0, deckSize);
            deckCards.forEach(c => used.add(c));
            startDeck();
        }

        // Every card is worth 100 / deck size points; each wrong pick costs a third of a card (a card can have at most 3 wrong picks).
        function finishDeck() {
            scoreEl.textContent = Math.round(100 * (1 - wrongPicks / (deckCards.length * MAX_WRONG_PER_CARD)));
            playEl.hidden = true; resultEl.hidden = false;
        }

        // Speaker button: plays the word's clip from Common Words/Words Audio/ (file name = the word's code points in hex). Never plays by itself.
        let audio = null;
        const clipUrl = w => 'Common%20Words/Words%20Audio/' + [...w].map(c => c.codePointAt(0).toString(16)).join('-') + '.mp3';
        function stopAudio() { if (audio) { audio.pause(); audio = null; } speakEl.classList.remove('playing'); }
        speakEl.addEventListener('click', () => {
            stopAudio();
            audio = new Audio(clipUrl(current.k));
            const done = () => speakEl.classList.remove('playing');
            audio.onended = done; audio.onerror = done;
            speakEl.classList.add('playing');
            audio.play().catch(done);
        });

        function nextCard() {
            stopAudio();
            if (!deck.length) { finishDeck(); return; }
            current = deck.pop(); locked = false;
            const question = lang === 'kk' ? current.k : current.e;
            wordEl.textContent = question; wordEl.lang = lang === 'kk' ? 'kk' : 'en';
            wordEl.parentElement.classList.toggle('long', question.length > 16);
            choicesEl.innerHTML = '';
            pickChoices(current).forEach((c, i) => {
                const b = document.createElement('button');
                b.type = 'button'; b.className = 'choice'; b.textContent = lang === 'kk' ? c.e : c.k; b.dataset.key = i + 1;
                b.addEventListener('click', () => answer(b, c));
                choicesEl.appendChild(b);
            });
        }

        function answer(btn, card) {
            if (locked || btn.classList.contains('wrong')) return;
            if (card === current) {
                locked = true; btn.classList.add('correct');
                completedCards.add(current); showCount();          // showCount ignores a card that was already counted
                nextTimer = setTimeout(nextCard, NEXT_DELAY_MS);
            } else {
                wrongPicks++; btn.classList.add('wrong'); btn.disabled = true;
            }
        }

        function backToSetup() {
            clearTimeout(nextTimer); stopAudio();
            roundEl.hidden = true; setupEl.hidden = false;
        }

        goBtn.addEventListener('click', () => {
            if (goBtn.disabled) return;
            if (anySelected) { settleSize(); anyMode = true; newAnyDeck(); }
            else { anyMode = false; deckCards = CARDS.filter(c => selected.has(c.g)); startDeck(); }
            setupEl.hidden = true; roundEl.hidden = false;
        });
        $('back').addEventListener('click', backToSetup);
        $('change').addEventListener('click', backToSetup);
        $('repeat').addEventListener('click', startDeck);
        freshBtn.addEventListener('click', newAnyDeck);

        document.addEventListener('keydown', e => {
            if (e.target.tagName === 'INPUT' || roundEl.hidden || playEl.hidden) return;   // typing a deck size must not answer cards
            const b = choicesEl.querySelector('.choice[data-key="' + e.key + '"]');
            if (b && !b.disabled) b.click();
        });
        showCount(); refreshSetup();
"""

title = "Kazakh Common Words Test: Flash Cards"
desc = "Test yourself on common Kazakh words: choose vocabulary groups, see the word in Kazakh or English, and pick the right meaning from four choices."
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <link rel="stylesheet" href="styles.css?v=11">
    <meta name="description" content="%(desc)s">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/game.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Common Words Test</h1>
            <p class="section-subtitle">Flash cards for the Common Words vocabulary</p>
        </header>

        <div class="divider"></div>

        <div class="game">
            <div id="setup">
                <div class="setup-title">Question Word Displayed in:</div>
                <div class="lang-row">
                    <button type="button" class="group-btn lang-btn" id="langKk" aria-pressed="true">Kazakh</button>
                    <button type="button" class="group-btn lang-btn" id="langEn" aria-pressed="false">English</button>
                </div>
                <div class="setup-title setup-title-groups">Select One or More Groups of Vocabulary to Review</div>
                <div class="group-grid" id="groups"></div>
                <button type="button" class="any-btn" id="anyBtn" aria-pressed="false">Any</button>
                <div class="deck-size" id="sizeBox" hidden>
                    <label class="deck-size-label" for="sizeNum">Cards per deck</label>
                    <div class="deck-size-row">
                        <input type="range" id="sizeRange" min="5" max="50" step="1" value="20" aria-label="Cards per deck, slider">
                        <input type="text" id="sizeNum" inputmode="numeric" autocomplete="off" maxlength="3" value="20" aria-describedby="sizeMsg">
                    </div>
                    <div class="deck-size-msg" id="sizeMsg" role="alert"></div>
                </div>
                <button type="button" class="go-btn" id="go" disabled>Go</button>
            </div>

            <div id="round" hidden>
                <button type="button" class="link-btn" id="back">&larr; Change groups</button>
                <div class="tally" aria-live="polite">
                    <span class="tally-label">Cards Completed</span>
                    <div class="tally-digits" id="count" aria-label="Cards completed: 0"></div>
                </div>
                <div id="play">
                    <div class="game-word">
                        <span id="word" lang="kk"></span>
                        <button type="button" class="speak game-speak" id="speak" aria-label="Play this word">
                            <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>
                        </button>
                    </div>
                    <div class="game-choices" id="choices"></div>
                </div>
                <div class="game-result" id="result" hidden>
                    <div class="result-label">Score</div>
                    <div class="result-score"><span id="score">0</span><span class="result-max"> / 100</span></div>
                    <div class="game-actions">
                        <button type="button" class="btn" id="repeat">Repeat This Deck</button>
                        <button type="button" class="btn" id="fresh">Generate New Deck</button>
                        <button type="button" class="btn" id="change">Change Groups</button>
                    </div>
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
