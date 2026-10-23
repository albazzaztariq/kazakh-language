"""Build verb-game.html: a Kazakh verb-conjugation construction game with a tutorial.

Inputs : none (the suffix tables below are the same rules taught on verbs.html: stem, hard/soft vowel, tense ending, who).
Flow   : Tutorial first. It walks through one verb at a time, revealing the steps one by one ("Next Step"), then moves on to the next verb with a different
         tense/person, looping until "Start Game" is pressed (that button is always visible).
         Game: each question names a verb, a tense and a person; you build the form in four steps, each a four-choice (step 2: two-choice) pick:
         1 the stem (drop -у), 2 hard or soft (last vowel), 3 the tense ending (with the spelling exceptions as tempting wrong choices),
         4 the person ending. A wrong pick turns red and stays red; the right pick turns green and the next step follows after 1 second, with a one-line
         reason. After step 4 the finished word and its equation are shown with a Next Verb button. A rolling click-counter ("Forms Built") counts unique
         verb + tense + person combinations built and only animates when the number changes.
Rules  : hard vowels а о ы ұ, soft vowels ә е і ү ө; voiceless endings қ к п с т ш (ды->ты, ма->па, ған->қан); vowel-ending stems (а/е->й, ып->п).
         "біз" is left out of the "have done" tense because its ending is not covered on verbs.html.
Output : verb-game.html (styles live in styles.css under "Word game" and "Verb game").
"""
print("[DEBUG] verb game page start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"

JS = r"""
        const STEP_DELAY_MS = 1000;
        const HARD = 'аоыұ', SOFT = 'әеіүө', VOICELESS = 'қкпстшчцщфхһ', VOWELS = 'аәеёиіоөуұүыэюя';
        const VERBS = [['бар', 'to go'], ['кел', 'to come'], ['ал', 'to take'], ['көр', 'to see'], ['бер', 'to give'], ['біл', 'to know'], ['кет', 'to leave'],
                       ['айт', 'to say'], ['іш', 'to drink'], ['тұр', 'to stand / live'], ['сөйле', 'to speak'], ['жаса', 'to make'], ['ойна', 'to play'],
                       ['қара', 'to look'], ['істе', 'to do / work']].map(([stem, en]) => ({ stem, en, dict: stem + 'у' }));
        const PERSONS = [['мен', 'I'], ['сен', 'you (informal)'], ['сіз', 'you (polite)'], ['ол', 'he / she'], ['біз', 'we'], ['сендер', 'you all (informal)'],
                         ['сіздер', 'you all (polite)'], ['олар', 'they']].map(([kk, en]) => ({ kk, en }));
        // person endings as [hard, soft], in the order of PERSONS
        const PAST_END = [['м', 'м'], ['ң', 'ң'], ['ңыз', 'ңіз'], ['', ''], ['қ', 'к'], ['ңдар', 'ңдер'], ['ңыздар', 'ңіздер'], ['', '']];
        const MYN_END = [['мын', 'мін'], ['сың', 'сің'], ['сыз', 'сіз'], ['', ''], ['мыз', 'міз'], ['сыңдар', 'сіңдер'], ['сыздар', 'сіздер'], ['', '']];
        const ADY_END = [['мын', 'мін'], ['сың', 'сің'], ['сыз', 'сіз'], ['ды', 'ді'], ['мыз', 'міз'], ['сыңдар', 'сіңдер'], ['сыздар', 'сіздер'], ['ды', 'ді']];
        const PERF_END = MYN_END.map((e, i) => i === 4 ? ['быз', 'біз'] : e);
        const lastVowel = w => { for (let i = w.length - 1; i >= 0; i--) if ((HARD + SOFT).includes(w[i])) return w[i]; return 'а'; };
        const isHard = stem => HARD.includes(lastVowel(stem));
        const endsVoiceless = s => VOICELESS.includes(s[s.length - 1]);
        const endsVowel = s => VOWELS.includes(s[s.length - 1]);
        const pick = (pair, hard) => pair[hard ? 0 : 1];
        const NEG = (stem, h) => endsVoiceless(stem) ? pick(['па', 'пе'], h) : pick(['ма', 'ме'], h);

        // Every tense: how its ending is built from the stem, which person-ending table it uses, every spelling it can take (for wrong choices), and why.
        const TENSES = [
            { id: 'past', label: 'Past', end: PAST_END,
              parts: (s, h) => [endsVoiceless(s) ? pick(['ты', 'ті'], h) : pick(['ды', 'ді'], h)],
              variants: [['ды'], ['ді'], ['ты'], ['ті']],
              why: (s, h) => endsVoiceless(s) ? s + ' ends in ' + s.slice(-1) + ', a voiceless sound (қ к п с т ш), so ды / ді becomes ты / ті' : 'Past = ды (hard) or ді (soft); ' + s + ' does not end in қ к п с т ш' },
            { id: 'now', label: 'Right now', end: MYN_END, fixedHard: true,
              parts: (s, h) => [endsVowel(s) ? 'п' : pick(['ып', 'іп'], h), ' жатыр'],
              variants: [['ып', ' жатыр'], ['іп', ' жатыр'], ['п', ' жатыр']],
              why: (s, h) => endsVowel(s) ? s + ' ends in a vowel, so ып / іп becomes п' : 'Right now = ып (hard) or іп (soft) + жатыр' },
            { id: 'future', label: 'Usually / future', end: ADY_END,
              parts: (s, h) => [endsVowel(s) ? 'й' : pick(['а', 'е'], h)],
              variants: [['а'], ['е'], ['й']],
              why: (s, h) => endsVowel(s) ? s + ' ends in a vowel, so а / е becomes й' : 'Usually / future = а (hard) or е (soft)' },
            { id: 'perf', label: 'Have done', end: PERF_END, noPerson: [4],
              parts: (s, h) => [endsVoiceless(s) ? pick(['қан', 'кен'], h) : pick(['ған', 'ген'], h)],
              variants: [['ған'], ['ген'], ['қан'], ['кен']],
              why: (s, h) => endsVoiceless(s) ? s + ' ends in ' + s.slice(-1) + ', a voiceless sound (қ к п с т ш), so ған / ген becomes қан / кен' : 'Have done = ған (hard) or ген (soft)' },
            { id: 'npast', label: 'Not (past)', end: PAST_END,
              parts: (s, h) => [NEG(s, h), pick(['ды', 'ді'], h)],
              variants: [['ма', 'ды'], ['ме', 'ді'], ['па', 'ды'], ['пе', 'ді']],
              why: (s, h) => endsVoiceless(s) ? s + ' ends in ' + s.slice(-1) + ', a voiceless sound, so ма / ме becomes па / пе, then ды / ді' : 'Not (past) = ма (hard) or ме (soft), then ды / ді' },
            { id: 'nnow', label: 'Not (now / future)', end: ADY_END,
              parts: (s, h) => [NEG(s, h), 'й'],
              variants: [['ма', 'й'], ['ме', 'й'], ['па', 'й'], ['пе', 'й']],
              why: (s, h) => endsVoiceless(s) ? s + ' ends in ' + s.slice(-1) + ', a voiceless sound, so ма / ме becomes па / пе, then й' : 'Not (now / future) = ма (hard) or ме (soft), then й' },
        ];
        const showParts = parts => parts.map(p => p.trim()).join(' + ');
        const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        const unique = a => [...new Set(a)];

        // Build everything about one question: the word, and the four steps with their choices and one-line reasons.
        function buildQuestion(verb, tense, p) {
            const stem = verb.stem, hard = isHard(stem), h = tense.fixedHard ? true : hard;
            const parts = tense.parts(stem, hard);
            const ending = pick(tense.end[p], tense.fixedHard ? true : hard);
            const word = stem + parts.join('') + ending;
            const endText = e => e === '' ? 'nothing' : '-' + e;
            // step 1: the stem
            const stemChoices = unique([stem, verb.dict, stem.slice(0, -1), ...shuffle(VERBS.filter(v => v !== verb)).map(v => v.stem)]).slice(0, 4);
            // step 3: the tense ending: the right spelling plus the other spellings of this tense, then spellings of other tenses
            const right = showParts(parts);
            const alts = unique([...tense.variants.map(showParts), ...shuffle(TENSES.filter(t => t !== tense)).flatMap(t => t.variants.map(showParts))]).filter(x => x !== right);
            const near = alts.slice(0, tense.variants.length - 1);
            const suffixChoices = shuffle([right, ...near, ...alts.slice(near.length).slice(0, 3 - near.length)]);
            // step 4: the person ending: the same ending in the other vowel type, then other persons' endings
            const table = tense.end, hh = tense.fixedHard ? true : hard;
            const rightE = endText(ending);
            const flip = endText(pick(table[p], !hh));
            const others = unique(shuffle(table.map((e, i) => i === p ? null : endText(pick(e, hh))).filter(x => x !== null)));
            const endChoices = shuffle(unique([rightE, flip, ...others]).filter((x, i, a) => true).slice(0, 4));
            if (!endChoices.includes(rightE)) endChoices[0] = rightE;
            const steps = [
                { title: 'Step 1: Get the stem (drop -у)', choices: stemChoices, right: stem, shown: stem,
                  why: verb.dict + ' without -у gives ' + stem },
                { title: 'Step 2: Hard or soft? Look at the last vowel of the stem', choices: ['Hard', 'Soft'], right: hard ? 'Hard' : 'Soft', shown: hard ? 'hard' : 'soft',
                  why: 'The last vowel of ' + stem + ' is ' + lastVowel(stem) + ', so it is ' + (hard ? 'hard (а о ы ұ)' : 'soft (ә е і ү ө)') },
                { title: 'Step 3: Pick the tense ending (' + tense.label + ')', choices: suffixChoices, right: right, shown: right, why: tense.why(stem, hard) },
                { title: 'Step 4: Add who (' + PERSONS[p].kk + ', ' + PERSONS[p].en + ')', choices: endChoices, right: rightE, shown: rightE,
                  why: PERSONS[p].kk + ' takes ' + (ending === '' ? 'no ending' : rightE) + (tense.fixedHard ? ' (after жатыр the endings are always hard)' : ' in this tense') },
            ];
            const equation = [stem, ...parts.map(x => x.trim()), ...(ending === '' ? [] : [ending])].join(' + ') + ' = ' + word;
            return { verb, tense, p, stem, hard, word, equation, steps, key: verb.stem + '|' + tense.id + '|' + p };
        }
        const task = q => q.verb.dict + ' (' + q.verb.en + ') \u00b7 ' + q.tense.label + ' \u00b7 ' + PERSONS[q.p].kk + ' (' + PERSONS[q.p].en + ')';
        const randomQuestion = prev => {
            for (;;) {
                const verb = VERBS[Math.floor(Math.random() * VERBS.length)], tense = TENSES[Math.floor(Math.random() * TENSES.length)];
                const people = PERSONS.map((_, i) => i).filter(i => !(tense.noPerson || []).includes(i)), p = people[Math.floor(Math.random() * people.length)];
                if (!prev || prev.key !== verb.stem + '|' + tense.id + '|' + p) return buildQuestion(verb, tense, p);
            }
        };

        // ---- tutorial: the same steps, revealed one at a time, verb after verb ----
        const $ = id => document.getElementById(id);
        const tutorialEl = $('tutorial'), roundEl = $('vround');
        const EXAMPLES = [['бар', 'past', 0], ['кел', 'future', 1], ['кет', 'past', 3], ['сөйле', 'future', 0], ['іш', 'nnow', 0], ['көр', 'perf', 2],
                          ['ойна', 'now', 4], ['кет', 'perf', 0], ['жаса', 'npast', 3]];
        let exIndex = 0, exQ = null, exStep = 0;
        function loadExample() {
            const [stem, tid, p] = EXAMPLES[exIndex % EXAMPLES.length];
            exQ = buildQuestion(VERBS.find(v => v.stem === stem), TENSES.find(t => t.id === tid), p); exStep = 0;
            $('tTask').textContent = 'Make: ' + task(exQ);
            $('tSteps').innerHTML = '';
            $('tNext').textContent = 'Next Step';
            revealStep();
        }
        function addCard(title, line, why) {
            const card = document.createElement('div'); card.className = 'vg-card';
            const t = document.createElement('div'); t.className = 'vg-card-title'; t.textContent = title;
            const a = document.createElement('div'); a.className = 'vg-card-answer'; a.textContent = line;
            const w = document.createElement('div'); w.className = 'vg-card-why'; w.textContent = why;
            card.append(t, a, w); $('tSteps').appendChild(card);
            card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
        function revealStep() {
            if (exStep < 4) {
                const s = exQ.steps[exStep];
                addCard(s.title, s.shown, s.why);
                exStep++;
                $('tNext').textContent = exStep < 4 ? 'Next Step' : 'Put It Together';
            } else if (exStep === 4) {
                addCard('Put it together', exQ.word, exQ.equation);
                exStep++;
                $('tNext').textContent = 'Next Verb';
            } else {
                exIndex++; loadExample();
            }
        }
        $('tNext').addEventListener('click', revealStep);

        // ---- game ----
        const countEl = $('count');
        const completed = new Set();
        let shownText = null;
        function showCount() {                                      // rolling tally; animates only when the number changes
            const text = String(completed.size).padStart(3, '0');
            if (text === shownText) return;
            while (countEl.children.length < text.length) {
                const cell = document.createElement('span'); cell.className = 'digit';
                const strip = document.createElement('span'); strip.className = 'digit-strip';
                for (let d = 0; d < 10; d++) { const n = document.createElement('span'); n.textContent = d; strip.appendChild(n); }
                cell.appendChild(strip); countEl.insertBefore(cell, countEl.firstChild);
            }
            [...countEl.children].forEach((cell, i) => { cell.firstChild.style.transform = 'translateY(' + (-Number(text[i]) * 1.2) + 'em)'; });
            countEl.setAttribute('aria-label', 'Forms built: ' + completed.size);
            if (shownText !== null) { countEl.classList.remove('tick'); void countEl.offsetWidth; countEl.classList.add('tick'); }
            shownText = text;
        }
        let q = null, stepIndex = 0, locked = false, timer = null;
        const builtEl = $('gBuilt'), choicesEl = $('gChoices'), whyEl = $('gWhy'), titleEl = $('gStepTitle'), nextEl = $('gNext'), finalEl = $('gFinal');
        function builtSoFar() {                                     // the word being assembled, filled in as the steps are completed
            const s = q.steps;
            return [stepIndex > 0 ? q.stem : '?', stepIndex > 2 ? showParts(q.tense.parts(q.stem, q.hard)) : '?', stepIndex > 3 ? (q.word.slice(q.stem.length + q.tense.parts(q.stem, q.hard).join('').length) || '\u2205') : '?'].join(' + ');
        }
        function newQuestion() {
            clearTimeout(timer);
            q = randomQuestion(q); stepIndex = 0;
            $('gTask').textContent = 'Make: ' + task(q);
            nextEl.hidden = true; finalEl.hidden = true; choicesEl.hidden = false; titleEl.hidden = false;
            showStep();
        }
        function showStep() {
            const s = q.steps[stepIndex]; locked = false;
            builtEl.textContent = builtSoFar();
            titleEl.textContent = s.title; whyEl.textContent = '';
            choicesEl.innerHTML = '';
            s.choices.forEach(text => {
                const b = document.createElement('button');
                b.type = 'button'; b.className = 'choice'; b.textContent = text;
                b.addEventListener('click', () => answer(b, text));
                choicesEl.appendChild(b);
            });
        }
        function answer(btn, text) {
            if (locked || btn.classList.contains('wrong')) return;
            const s = q.steps[stepIndex];
            if (text !== s.right) { btn.classList.add('wrong'); btn.disabled = true; return; }
            locked = true; btn.classList.add('correct'); whyEl.textContent = s.why;
            timer = setTimeout(() => {
                stepIndex++;
                if (stepIndex < 4) { showStep(); return; }
                builtEl.textContent = q.equation;                   // all four steps done: show the finished word
                choicesEl.hidden = true; titleEl.hidden = true; whyEl.textContent = '';
                finalEl.textContent = q.word; finalEl.hidden = false; nextEl.hidden = false;
                completed.add(q.key); showCount();                  // an already-built combination does not move the counter
            }, STEP_DELAY_MS);
        }
        nextEl.addEventListener('click', newQuestion);

        function startGame() { tutorialEl.hidden = true; roundEl.hidden = false; newQuestion(); }
        function showTutorial() { clearTimeout(timer); roundEl.hidden = true; tutorialEl.hidden = false; }
        $('startGame').addEventListener('click', startGame);
        $('toTutorial').addEventListener('click', showTutorial);
        showCount(); loadExample();
"""

title = "Kazakh Verb Conjugation Game: Build the Verb Step by Step"
desc = "Learn to conjugate Kazakh verbs by building them step by step: the stem, hard or soft vowels, the tense ending and who is doing it. Starts with a tutorial."
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <link rel="stylesheet" href="styles.css?v=14">
    <meta name="description" content="%(desc)s">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/verb-game.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Verb Conjugation</h1>
            <p class="section-subtitle">Build the verb one step at a time</p>
        </header>

        <div class="divider"></div>

        <div class="game">
            <div id="tutorial">
                <div class="setup-title">Tutorial</div>
                <div class="vg-task" id="tTask"></div>
                <div id="tSteps" class="vg-steps"></div>
                <button type="button" class="btn vg-next" id="tNext">Next Step</button>
                <button type="button" class="go-btn" id="startGame">Start Game</button>
            </div>

            <div id="vround" hidden>
                <button type="button" class="link-btn" id="toTutorial">&larr; Back to tutorial</button>
                <div class="tally" aria-live="polite">
                    <span class="tally-label">Forms Built</span>
                    <div class="tally-digits" id="count" aria-label="Forms built: 0"></div>
                </div>
                <div class="vg-task" id="gTask"></div>
                <div class="vg-built" id="gBuilt"></div>
                <div class="vg-final" id="gFinal" hidden></div>
                <div class="vg-step-title" id="gStepTitle"></div>
                <div class="game-choices" id="gChoices"></div>
                <div class="vg-why" id="gWhy" role="status"></div>
                <button type="button" class="btn vg-next" id="gNext" hidden>Next Verb</button>
            </div>
        </div>

        <div class="page-nav">
            <a href="verbs.html" class="btn">&larr;</a>
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>

    <script>
%(js)s    </script>
</body>
</html>
""" % {"title": title, "desc": desc, "js": JS}
open(W + "verb-game.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote verb-game.html, {len(page)} bytes", flush=True)
