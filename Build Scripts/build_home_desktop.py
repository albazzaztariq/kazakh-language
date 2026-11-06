"""Add the desktop-only home page to index.html (the layout of the two Qazaq mock-ups, built from the modules this site really has).
Inputs : index.html (the original phone/tablet home page is kept as it is) and home-desktop.css (all desktop rules, inside @media (min-width: 1024px)).
Method : 1) the original page content is wrapped in <div class="mobile-home"> (hidden on desktop only, by home-desktop.css);
         2) a <div class="desktop-home"> block is inserted after it; an inline rule hides it everywhere except where home-desktop.css shows it (1024px and wider);
         3) the head gets the Playfair Display font and the desktop stylesheet, both with media="(min-width: 1024px)" so phones do not download them;
         4) the script gets the clickable flag (Echo.mp3) for both versions and speaker buttons that play the first-word clips in Common Words/Words Audio/.
         Running the script again replaces the block between the markers, so it can be re-run after edits.
Output : index.html (overwritten).
"""
import re
print("[DEBUG] home desktop build start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
page = open(W + "index.html", encoding="utf-8").read()

ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SPEAKER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/></svg>'
BOOK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2V5z"/><path d="M8 7h6M8 11h6"/></svg>'
GAME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 8h10a4 4 0 0 1 4 4v1a3 3 0 0 1-5.2 2L14 13h-4l-1.8 2A3 3 0 0 1 3 13v-1a4 4 0 0 1 4-4z"/><path d="M8 10.5v3M6.5 12h3"/><circle cx="16" cy="11" r=".6"/><circle cx="18" cy="13" r=".6"/></svg>'
CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 9h8M8 12h5"/></svg>'
HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>'
MARK = lambda cls="": f'<svg class="{cls}" viewBox="-32 -32 64 64" aria-hidden="true"><use href="#qz-mark" x="-32" y="-32" width="64" height="64"/></svg>'
HORN = "M0 -3 C 9 -3 12 -12 6 -18 C 1 -22 -6 -19 -5 -13 C -4 -9 1 -9 2 -12"

DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
        <defs>
            <symbol id="qz-mark" viewBox="-32 -32 64 64"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
                <path id="qz-horn" d="{HORN}"/><use href="#qz-horn" transform="rotate(90)"/><use href="#qz-horn" transform="rotate(180)"/><use href="#qz-horn" transform="rotate(270)"/></g></symbol>
            <linearGradient id="qz-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d2d31"/><stop offset=".45" stop-color="#2f6068"/><stop offset=".78" stop-color="#e7b36f"/><stop offset="1" stop-color="#f3d49a"/></linearGradient>
            <radialGradient id="qz-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff3d1" stop-opacity=".95"/><stop offset=".4" stop-color="#ffd48a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd48a" stop-opacity="0"/></radialGradient>
            <linearGradient id="qz-grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9a15d"/><stop offset=".55" stop-color="#8d6a36"/><stop offset="1" stop-color="#4f3a1f"/></linearGradient>
            <linearGradient id="qz-lakeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2aa3a6"/><stop offset="1" stop-color="#0f5c63"/></linearGradient>
            <symbol id="qz-steppe" viewBox="0 0 1400 640" preserveAspectRatio="xMaxYMid slice">
                <rect width="1400" height="640" fill="url(#qz-sky)"/>
                <circle cx="1010" cy="300" r="260" fill="url(#qz-sun)"/>
                <path d="M0 330 L120 270 L200 300 L330 205 L420 270 L520 230 L640 300 L760 195 L860 260 L980 165 L1090 250 L1180 212 L1290 282 L1400 238 L1400 440 L0 440 Z" fill="#7790a0"/>
                <path d="M300 232 L330 205 L360 234 L343 227 L330 240 L317 227 Z M737 220 L760 195 L784 222 L770 217 L760 230 L749 217 Z M950 193 L980 165 L1012 196 L994 189 L980 204 L965 189 Z" fill="#f4f7fa"/>
                <path d="M0 385 L150 332 L280 372 L430 312 L580 374 L720 332 L860 392 L1000 322 L1150 388 L1300 342 L1400 374 L1400 480 L0 480 Z" fill="#41717a"/>
                <path d="M0 455 C200 418 380 446 560 436 S900 408 1100 436 S1300 446 1400 430 L1400 640 L0 640 Z" fill="url(#qz-grass)"/>
                <path d="M0 540 C260 505 520 560 760 530 S1180 505 1400 535 L1400 640 L0 640 Z" fill="#4a3a20" opacity=".55"/>
                <g transform="translate(1040 438)">
                    <ellipse cx="55" cy="68" rx="105" ry="9" fill="#2b1f10" opacity=".35"/>
                    <rect x="-18" y="22" width="146" height="48" rx="3" fill="#efe3c8"/>
                    <path d="M-30 24 Q55 -64 140 24 Z" fill="#f7eedb"/>
                    <path d="M55 -24 L55 24 M20 -14 L24 24 M90 -14 L86 24 M-2 -2 L5 24 M108 -2 L101 24" stroke="#cdb98f" stroke-width="2" fill="none"/>
                    <rect x="-18" y="36" width="146" height="9" fill="#a47a3f"/>
                    <path d="M-18 40.5 h146" stroke="#e2bd7a" stroke-width="2" stroke-dasharray="7 5"/>
                    <path d="M42 70 V46 a13 13 0 0 1 26 0 V70 Z" fill="#6b4a2b"/>
                    <circle cx="55" cy="-26" r="9" fill="none" stroke="#c19a5b" stroke-width="3"/>
                </g>
            </symbol>
            <symbol id="qz-lake" viewBox="0 0 800 300" preserveAspectRatio="xMaxYMid slice">
                <rect width="800" height="300" fill="url(#qz-sky)"/>
                <circle cx="600" cy="120" r="150" fill="url(#qz-sun)"/>
                <path d="M0 175 L90 120 L170 150 L290 80 L370 140 L470 100 L570 160 L680 90 L760 140 L800 120 L800 215 L0 215 Z" fill="#6c8b97"/>
                <path d="M270 96 L290 80 L312 100 L300 96 L290 108 L280 96 Z M660 108 L680 90 L702 112 L690 108 L680 120 L670 108 Z" fill="#f4f7fa"/>
                <path d="M0 200 L110 165 L230 195 L350 160 L480 200 L610 168 L720 198 L800 178 L800 240 L0 240 Z" fill="#2f6068"/>
                <rect y="205" width="800" height="95" fill="url(#qz-lakeg)"/>
                <path d="M0 230 h800 M0 252 h800 M0 276 h800" stroke="#ffffff" stroke-opacity=".12" stroke-width="2" stroke-dasharray="40 26"/>
            </symbol>
        </defs>
    </svg>"""

def drop(label, href, items):
    menu = "".join(f'<a href="{h}">{t}</a>' for h, t in items)
    return f'<div class="dh-drop"><button type="button" aria-haspopup="true">{label}</button><div class="dh-menu">{menu}</div></div>'
VOCAB = [("common-words.html", "Common Words"), ("core-words.html", "Core Words"), ("numbers.html", "Numbers")]
GRAM = [("suffixes.html", "Suffixes"), ("sentences.html", "Sentences"), ("verbs.html", "Verbs")]
GAMES = [("game.html", "Common Words Test"), ("verb-game.html", "Verb Conjugation"), ("sentence-game.html", "Sentence Constructor")]
NAV = ('<a href="index.html">Home</a><a href="alphabet.html">Alphabet</a>' + drop("Vocabulary", "", VOCAB) + drop("Grammar", "", GRAM) + drop("Games", "", GAMES)
       + '<a href="culture.html">Culture</a>')

def card(cls, num, title, text, href, icon, links=()):
    ls = "".join(f'<span>{t}</span>' for t in links)
    sub = f'<div class="dh-links">{ls}</div>' if links else ""
    return (f'<a class="dh-card {cls}" href="{href}"><div class="dh-num">{num}</div><h3>{title}</h3><p>{text}</p>{sub}'
            f'<div class="dh-icon">{icon}</div><div class="dh-go">{ARROW}</div>{MARK("dh-corner")}</a>')
ALPHA_ICON = '<span class="dh-serif" style="font-size:2.1rem;line-height:1">Ә</span>'
CARDS = (card("dh-c1", "01", "Alphabet", "Learn the Kazakh alphabet and its sounds, with audio for every letter.", "alphabet.html", ALPHA_ICON)
         + card("dh-c2", "02", "Vocabulary", "Build your first words and everyday phrases.", "common-words.html", CHAT, ("Common Words", "Core Words", "Numbers"))
         + card("dh-c3", "03", "Grammar", "Suffixes, sentences and verbs, step by step.", "suffixes.html", BOOK, ("Suffixes", "Sentences", "Verbs"))
         + card("dh-c4", "04", "Games", "Test yourself and build real Kazakh sentences.", "game.html", GAME, ("Common Words Test", "Verb Conjugation", "Sentence Constructor")))

WORDS = [("рахмет", "Thank you"), ("иә", "Yes"), ("жоқ", "No"), ("қош келдіңіз", "Welcome")]
WORD_BTNS = "".join(f'<button type="button" class="dh-word" data-word="{k}" aria-label="Play {k}">{SPEAKER}<span><b>{k.capitalize()}</b> &mdash; {e}</span></button>' for k, e in WORDS)
CHIPS = "".join(f'<a href="culture.html#{h}">{t}</a>' for h, t in (("uyat", "Uyat"), ("namys", "Namys"), ("zheti-ata", "Zheti Ata"), ("nauryz", "Nauryz"), ("dombra", "Dombra &amp; Aitys"), ("nomads", "Nomad Heritage")))
FOOT_NAV = '<a href="index.html">Home</a><a href="alphabet.html">Alphabet</a><a href="common-words.html">Vocabulary</a><a href="suffixes.html">Grammar</a><a href="game.html">Games</a><a href="culture.html">Culture</a>'

BLOCK = f"""<!-- desktop-home:start -->
    <div class="desktop-home">
    {DEFS}
        <section class="dh-hero">
            <svg class="dh-hero-art" aria-hidden="true" focusable="false"><use href="#qz-steppe" width="100%" height="100%"/></svg>
            <div class="dh-wrap">
                <div class="dh-bar">
                    <a class="dh-brand" href="index.html">{MARK()}<span><span class="dh-brand-name">QAZAQ</span><span class="dh-brand-sub">Learn Kazakh</span></span></a>
                    <nav class="dh-nav" aria-label="Main">{NAV}</nav>
                    <div class="dh-right"><img class="dh-flag" src="kazakhstan-flag.png" alt="Flag of Kazakhstan" title="Click me" width="60" height="30"><a class="dh-btn small" href="alphabet.html">Get Started {ARROW}</a></div>
                </div>
                <div class="dh-hero-copy">
                    <div class="dh-eyebrow">Learn Kazakh online</div>
                    <h1>A new language.<br>A whole <em>new world.</em></h1>
                    <p class="dh-kk" lang="kk">Қазақ тілін үйреніңіз</p>
                    <p class="dh-kk-sub">Qazaq tilin &uuml;yren&iuml;ңіз &middot; Learn the Kazakh language</p>
                    <p class="dh-lead">Free lessons in the Kazakh language, with audio on every word, games to make it stick, and the culture behind the words.</p>
                    <div class="dh-hero-buttons"><a class="dh-btn" href="alphabet.html">Start Learning {ARROW}</a>
                        <a class="dh-play" href="game.html"><span><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>Try a Game</a></div>
                </div>
            </div>
        </section>
        <div class="dh-strip-wrap"><div class="dh-wrap"><div class="dh-strip">
            <div>{SPEAKER}<p><strong>Hear every word</strong><span>Audio you can replay</span></p></div>
            <div>{GAME}<p><strong>Games that stick</strong><span>Test and build sentences</span></p></div>
            <div>{MARK()}<p><strong>Real culture</strong><span>Uyat, Nauryz, the dombra</span></p></div>
            <div>{HEART}<p><strong>Always free</strong><span>No sign-up needed</span></p></div>
        </div></div></div>
        <section class="dh-journey"><div class="dh-wrap"><div class="dh-journey-grid">
            <div><div class="dh-eyebrow">Start your journey</div><h2>Learn Kazakh<br>step by step</h2><p>From the alphabet to real sentences, follow the path or jump to whatever you need.</p>
                <a class="dh-btn dark" href="alphabet.html">Start with the Alphabet {ARROW}</a></div>
            <div class="dh-cards">{CARDS}</div>
        </div></div></section>
        <section class="dh-words"><div class="dh-wrap"><div class="dh-words-grid">
            <div class="dh-words-panel">{MARK("dh-ornament")}
                <div><div class="dh-eyebrow">Your first words</div><div class="dh-hello" lang="kk">Сәлем</div><div class="dh-hello-sub">S&auml;lem &mdash; Hello</div>
                    <button type="button" class="dh-word" data-word="сәлем" aria-label="Play сәлем">{SPEAKER}<span>Hear it</span></button>
                    <a class="dh-btn ghost small" style="color:#fff !important;border-color:#e2bd7a" href="common-words.html">View all vocabulary {ARROW}</a></div>
                <div class="dh-word-list">{WORD_BTNS}</div>
            </div>
            <a class="dh-culture-tile" href="culture.html"><svg class="dh-art" aria-hidden="true" focusable="false"><use href="#qz-lake" width="100%" height="100%"/></svg>
                <div><h3>More than just a language.</h3><p>Explore the customs, values and traditions behind the words.</p></div><span class="dh-go">{ARROW}</span></a>
        </div></div></section>
        <div class="dh-wrap"><section class="dh-banner"><svg class="dh-art" aria-hidden="true" focusable="false"><use href="#qz-lake" width="100%" height="100%"/></svg>
            <div><div class="dh-eyebrow">Explore Kazakhstan</div><h2>Culture, from uyat to the dombra</h2>
                <p>Why Kazakhs speak the way they do: honour, hospitality, the seven ancestors, Nauryz and the steppe.</p>
                <div class="dh-chips">{CHIPS}</div><a class="dh-btn" href="culture.html">Explore culture {ARROW}</a></div></section></div>
        <div class="dh-wrap"><div class="dh-reasons">
            <div>{BOOK}<p><strong>Made for learners</strong><span>Plain English explanations</span></p></div>
            <div>{SPEAKER}<p><strong>Audio included</strong><span>A Kazakh voice for every word</span></p></div>
            <div>{GAME}<p><strong>Practice built in</strong><span>Games and sentence building</span></p></div>
            <div>{CHAT}<p><strong>Your goal</strong><span>Understand and be understood</span></p></div>
        </div></div>
        <footer class="dh-footer">{MARK("dh-ornament l")}{MARK("dh-ornament r")}
            <div class="dh-brand">{MARK()}<span><span class="dh-brand-name">QAZAQ</span></span></div>
            <p>Learn the language. Discover the culture.</p><nav aria-label="Footer">{FOOT_NAV}</nav>
        </footer>
    </div>
    <!-- desktop-home:end -->
"""

HEAD_ADD = """    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" media="(min-width: 1024px)">
    <link rel="stylesheet" href="home-desktop.css?v=5" media="(min-width: 1024px)">
    <style>.desktop-home { display: none; }</style>
"""
SCRIPT = """    <script>
        const flagClip = new Audio('Echo.mp3');
        document.querySelectorAll('#flag-clip, .dh-flag').forEach(f => f.addEventListener('click', () => {
            flagClip.currentTime = 0;
            flagClip.play().catch(() => {});
        }));
        // desktop home: speaker buttons play the word clips (file name = the word's code points in hex)
        let wordAudio = null;
        document.querySelectorAll('.dh-word').forEach(b => b.addEventListener('click', () => {
            if (wordAudio) wordAudio.pause();
            document.querySelectorAll('.dh-word.playing').forEach(x => x.classList.remove('playing'));
            const url = 'Common%20Words/Words%20Audio/' + [...b.dataset.word].map(c => c.codePointAt(0).toString(16)).join('-') + '.mp3';
            wordAudio = new Audio(url); b.classList.add('playing');
            const done = () => b.classList.remove('playing');
            wordAudio.onended = done; wordAudio.onerror = done; wordAudio.play().catch(done);
        }));
    </script>
"""

if "<!-- desktop-home:start -->" in page:
    page = re.sub(r"<!-- desktop-home:start -->.*?<!-- desktop-home:end -->\n", lambda m: BLOCK, page, flags=re.S)
else:
    assert page.count("<body>\n    <div class=\"container\">") == 1
    page = page.replace("<body>\n    <div class=\"container\">", "<body>\n    <div class=\"mobile-home\">\n    <div class=\"container\">")
    i = page.index("    <script>")
    page = page[:i] + "    </div>\n    " + BLOCK + page[i:]
    page = page.replace("</head>", HEAD_ADD + "</head>")
j = page.index("    <script>\n        const flagClip"); k = page.index("</script>", j) + len("</script>\n")
page = page[:j] + SCRIPT + page[k:]
open(W + "index.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote index.html, {len(page)} bytes", flush=True)
