"""Build create-deck.html: pick your own words for a custom deck, name it, and save it to your Google-linked account.

Inputs : common-words.html (topic sections and every word row, plus its jump-link pills), read at build time so this page always matches the vocabulary.
Flow   : 1) Selection screen: looks like the Common Words page (group pills at the top jump to each topic). Tapping anywhere on a word's row toggles its checkbox
            (the speaker button only plays the clip). A floating "Top" button with an up arrow slides in after you scroll and jumps back to the pills.
            A floating button on the right reads "Add 5 Cards", "Add 4 Cards" ... greyed out, and becomes "Create Deck (N)" once 5 or more words are ticked.
         2) Name screen (same page): name the deck (up to 40 characters), sign in with Google if needed, press Save Deck; the deck is stored under the signed-in user
            (deck-store.js, Firebase Auth + Firestore) and the browser returns to the Word Game page.
         The selection survives a reload of the page (sessionStorage). If account sign-in is not configured yet, the name screen says so and Save stays off.
Output : create-deck.html (styles live in styles.css under "Create Deck")."""
import re, json, html
print("[DEBUG] create-deck page start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
src = open(W + "common-words.html", encoding="utf-8").read()
pills = re.findall(r'<a href="#([^"]+)">([^<]+)</a>', src)
ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
sections, n_words = "", 0
for sid, title, body in re.findall(r'<section class="lesson-section" id="([^"]+)"><h2>(.*?)</h2>(.*?)</section>', src, re.S):
    rows = ""
    for kk, say, en in re.findall(r'</button>(.*?)</td><td class="c1">(.*?)</td><td class="c2">(.*?)</td>', body):
        k = html.unescape(kk); n_words += 1
        rows += (f'<tr class="pick-row" data-word="{html.escape(k, quote=True)}"><td class="c0"><input type="checkbox" class="pick-cb" aria-label="Add {html.escape(k, quote=True)} to the deck">'
                 f'<button type="button" class="speak" data-word="{html.escape(k, quote=True)}" aria-label="Play {html.escape(k, quote=True)}">{ICON}</button>{kk}</td><td class="c1">{say}</td><td class="c2">{en}</td></tr>')
    sections += (f'        <section class="lesson-section" id="{sid}"><h2>{title}</h2><table class="lesson-table"><thead><tr><th>Kazakh</th><th>Say it</th><th>English</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table></section>\n')
pill_html = "".join(f'<a href="#{i}">{l}</a>' for i, l in pills)
print(f"[DEBUG] {n_words} words in {len(pills)} pills", flush=True)

JS = r"""
        const $ = id => document.getElementById(id);
        const MIN = 5, STORE_KEY = 'kw-create-deck';
        const rows = [...document.querySelectorAll('tr.pick-row')];
        const selected = new Set();
        try { JSON.parse(sessionStorage.getItem(STORE_KEY) || '[]').forEach(w => selected.add(w)); } catch (e) {}
        const createBtn = $('createDeck'), topBtn = $('toTop');

        function sync() {
            rows.forEach(r => { const on = selected.has(r.dataset.word); r.classList.toggle('picked', on); r.querySelector('.pick-cb').checked = on; });
            const n = selected.size, left = MIN - n;
            createBtn.disabled = n < MIN;
            createBtn.textContent = n < MIN ? 'Add ' + left + (left === 1 ? ' Card' : ' Cards') : 'Create Deck (' + n + ')';
            try { sessionStorage.setItem(STORE_KEY, JSON.stringify([...selected])); } catch (e) {}
        }
        rows.forEach(tr => tr.addEventListener('click', e => {
            if (e.target.closest('.speak')) return;                      // the speaker only plays the word
            const cb = tr.querySelector('.pick-cb');
            if (e.target !== cb) cb.checked = !cb.checked;               // a click on the checkbox itself has already toggled it
            cb.checked ? selected.add(tr.dataset.word) : selected.delete(tr.dataset.word);
            sync();
        }));

        // speaker: plays the word's clip from Common Words/Words Audio/ (never automatically)
        let audio = null;
        const clipUrl = w => 'Common%20Words/Words%20Audio/' + [...w].map(c => c.codePointAt(0).toString(16)).join('-') + '.mp3';
        document.querySelectorAll('button.speak').forEach(b => b.addEventListener('click', () => {
            if (audio) audio.pause();
            document.querySelectorAll('button.speak.playing').forEach(x => x.classList.remove('playing'));
            audio = new Audio(clipUrl(b.dataset.word)); b.classList.add('playing');
            const done = () => b.classList.remove('playing'); audio.onended = done; audio.onerror = done; audio.play().catch(done);
        }));

        // floating "Top" button: slides in once you scroll away from the group pills
        const onScroll = () => topBtn.classList.toggle('show', window.scrollY > 380);
        window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
        topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

        // ---- name screen ----
        const pickEl = $('pickScreen'), nameEl = $('nameScreen'), nameIn = $('deckName'), saveBtn = $('saveDeck'), msg = $('saveMsg'), acct = $('acct');
        let user = null, store = null, saving = false;
        const chosen = () => rows.filter(r => selected.has(r.dataset.word)).map(r => r.dataset.word);   // in page order
        function updateSave() { saveBtn.disabled = saving || !user || !nameIn.value.trim(); }
        function renderAcct() {
            acct.innerHTML = '';
            if (!store) { acct.textContent = 'Checking sign-in...'; return; }
            if (!store.isConfigured()) { acct.textContent = "Account sign-in isn't set up yet, so decks can't be saved. (Setup steps are in Account Setup.md.)"; return; }
            if (user) {
                const who = document.createElement('span'); who.textContent = 'Signed in as ' + (user.name ? user.name + ' \u00b7 ' : '') + user.email + ' ';
                const out = document.createElement('button'); out.type = 'button'; out.className = 'link-btn inline'; out.textContent = 'Sign out';
                out.addEventListener('click', () => store.signOutUser()); acct.append(who, out);
            } else {
                const b = document.createElement('button'); b.type = 'button'; b.className = 'btn google-btn'; b.textContent = 'Sign in with Google';
                b.addEventListener('click', async () => { msg.textContent = ''; try { await store.signIn(); } catch (e) { msg.textContent = 'Sign-in did not finish. Allow pop-ups for this site and try again.'; } });
                const note = document.createElement('div'); note.className = 'name-note'; note.textContent = 'Your saved decks are kept in your account, so they follow you to any device.';
                acct.append(b, note);
            }
        }
        async function openName() {
            const words = chosen(); if (words.length < MIN) return;
            $('deckCount').textContent = words.length + ' words in this deck';
            const list = $('deckWords'); list.innerHTML = '';
            rows.filter(r => selected.has(r.dataset.word)).forEach(r => { const li = document.createElement('li'); li.textContent = r.dataset.word + ' \u2013 ' + r.querySelector('.c2').textContent; list.appendChild(li); });
            pickEl.hidden = true; nameEl.hidden = false; createBtn.hidden = true; topBtn.hidden = true; window.scrollTo(0, 0); renderAcct(); updateSave(); nameIn.focus();
            if (!store) {
                try { store = await import('./deck-store.js'); } catch (e) { acct.textContent = 'Could not load the account code. Check your connection.'; return; }
                renderAcct();
                if (store.isConfigured()) store.onUser(u => { user = u; renderAcct(); updateSave(); });
            }
        }
        createBtn.addEventListener('click', () => { if (!createBtn.disabled) openName(); });
        $('backToPick').addEventListener('click', () => { nameEl.hidden = true; pickEl.hidden = false; createBtn.hidden = false; topBtn.hidden = false; msg.textContent = ''; onScroll(); });
        nameIn.addEventListener('input', () => { msg.textContent = ''; updateSave(); });
        saveBtn.addEventListener('click', async () => {
            if (saveBtn.disabled) return;
            saving = true; saveBtn.textContent = 'Saving...'; updateSave(); msg.textContent = '';
            try {
                await store.saveDeck(nameIn.value, chosen());
                try { sessionStorage.removeItem(STORE_KEY); } catch (e) {}
                window.location.href = 'game.html';
            } catch (e) {
                msg.textContent = e.message === 'duplicate' ? 'You already have a deck with that name. Pick another name.' : e.message === 'name' ? 'Give the deck a name of up to 40 characters.'
                    : e.message === 'words' ? 'A deck needs between 5 and 200 words.' : 'Could not save the deck. Check your connection and try again.';
                saving = false; saveBtn.textContent = 'Save Deck'; updateSave();
            }
        });
        sync();
"""

page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create Your Own Deck - Kazakh Word Game</title>
    <link rel="stylesheet" href="styles.css?v=14">
    <meta name="robots" content="noindex">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="game.html" class="back-link">&larr; Back to Word Game</a>

        <div id="pickScreen">
            <header>
                <h1 class="section-title">Create Deck</h1>
                <p class="section-subtitle">Tap a word to add it to your deck. Pick at least 5, from any groups, then press Create Deck.</p>
            </header>

            <div class="divider"></div>

            <nav class="jump-links" aria-label="Jump to a topic">%(pills)s</nav>

%(sections)s
        </div>

        <div id="nameScreen" hidden>
            <header>
                <h1 class="section-title">Name Your Deck</h1>
                <p class="section-subtitle" id="deckCount"></p>
            </header>
            <div class="divider"></div>
            <div class="name-card">
                <label class="deck-size-label" for="deckName">Deck name</label>
                <input type="text" id="deckName" maxlength="40" autocomplete="off" placeholder="For example: Market words">
                <div class="acct" id="acct"></div>
                <div class="deck-size-msg" id="saveMsg" role="alert"></div>
                <button type="button" class="go-btn" id="saveDeck" disabled>Save Deck</button>
                <button type="button" class="link-btn" id="backToPick">&larr; Back to word selection</button>
                <details class="deck-words"><summary>Show the words in this deck</summary><ul id="deckWords"></ul></details>
            </div>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>

    <button type="button" class="float-top" id="toTop" aria-label="Back to the group buttons at the top"><span aria-hidden="true">&uarr;</span> Top</button>
    <button type="button" class="float-create" id="createDeck" disabled>Add 5 Cards</button>

    <script>
%(js)s    </script>
</body>
</html>
""" % {"pills": pill_html, "sections": sections, "js": JS}
open(W + "create-deck.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote create-deck.html, {len(page)} bytes", flush=True)
