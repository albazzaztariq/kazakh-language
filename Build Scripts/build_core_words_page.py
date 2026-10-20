"""Build core-words.html: the 300 most frequent Kazakh lemmas with English meaning, type, common forms and audio.

Inputs : Temp/core_vocabulary.tsv (ranked lemmas, from Temp/build_core_list.py); Temp/counts_*.pkl (surface-form counts, used to pick
         the common forms); GLOSSES below (English meanings, written by hand - review before relying on them).
Method : verbs are shown in the dictionary form ending in -u (stem + у, with п/қ/к -> б/ғ/г); a few nouns get their dictionary vowel back
         (алд -> алды). Each displayed word is spoken by the male Kazakh voice kk-KZ-DauletNeural (rate -10%, silence trimmed, peak 0.4,
         same recipe as the common-words page); clips are cached in Core Words/Words Audio/ and embedded in the page as base64.
Output : core-words.html (columns: Word with speaker button | English with the word type underneath | Common forms).
"""
import csv, pickle, os, re, asyncio, base64, json, shutil, collections
print("[DEBUG] core words page start", flush=True)
import av, numpy as np, edge_tts
B = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
AD = B + "Core Words/Words Audio/"; CW = B + "Common Words/Words Audio/"
os.makedirs(AD, exist_ok=True)

GLOSSES = """
бол = to be, to become
ол = he, she, it; that
мен = I; also "with" (мен/пен/бен)
ал = to take, to get
бұл = this
да = also, too (да/де/та/те)
е = to be (linking word: еді = was, екен = apparently)
де = to say, to call
ма = question particle (ма/ме/ба/бе/па/пе)
бар = there is, existing; also the verb бару, to go
кел = to come
бір = one; a
тұр = to stand; shows an ongoing state
не = what
айт = to say, to tell
өз = own; oneself
бер = to give
олар = they
және = and
сол = that (the one already mentioned)
сен = you (informal)
жоқ = no; there is not
бірақ = but
біз = we
жат = to lie down; shows an ongoing state
осы = this
үшін = for; because of
жер = land, earth; place
керек = needed, necessary
кет = to leave, to go away
адам = person
көр = to see
шық = to go out, to come out
қал = to stay, to remain
біл = to know
қала = city, town
жақсы = good; well
тап = to find
жүр = to walk, to move about
қой = to put, to place
жаса = to make, to do
істе = to do, to work
жыл = year
күн = day; sun
бала = child
отыр = to sit
жол = road, way
бас = head; main
ғана = only, just
кез = time, moment (кезінде = at the time of)
бәрі = everything, all, everyone
екі = two
қара = to look at; black
қазір = now
баста = to begin
ет = to do, to make
көп = many, much
енді = now, from now on
уақыт = time
тек = only, just
ойла = to think
сал = to put in; to build
тағы = also, again, more
қалай = how
соң = after, end (соңында = at the end)
мүмкін = possible; maybe
жақ = side, direction
басқа = other, else
үй = house, home
иә = yes
түс = to get off, to go down; also: dream, colour
барлық = all, whole
өт = to pass, to go by
сөз = word; speech
жаңа = new; just now
сияқты = like, similar to
жет = to reach; to be enough
өте = very
қажет = necessary
рет = time (as in "one time")
жұмыс = work, job
жас = young; age
шығар = to take out, to produce
ат = horse; name (аты = his/her name)
орын = place; seat
қайт = to return, to go back
бұрын = before, earlier
кейін = after, later
ғой = emphatic particle ("you know", "after all")
іш = inside; stomach
көз = eye
егер = if
жай = simple; matter, situation
ұста = to hold, to catch
қол = hand; arm
су = water
ең = most (the superlative word)
көрсет = to show
әлем = world
сіз = you (polite)
қыз = girl; daughter
жағдай = situation, condition
айнал = to turn; to become
үш = three
аш = to open; hungry
күш = strength, power
нәрсе = thing
тоқта = to stop (yourself)
кім = who
дейін = until, up to
түр = kind, type; form
қайда = where
қандай = what kind of; what a
дұрыс = correct, right
қарсы = against; opposite
туралы = about, concerning
жара = to suit, to be fit (жарайды = okay)
әке = father
жан = soul; person; life
жібер = to send; to let go
әлі = still, yet
мына = this (here, close to me)
іс = deed, affair, matter
жаз = to write; also: summer
қос = to add, to join; a pair
сондықтан = therefore, so
мектеп = school
кір = to enter
ара = gap, interval (арасында = between, among)
түсін = to understand
ай = moon; month
тарт = to pull, to draw
дәл = exactly, precisely
сұра = to ask
қайта = again; back
ой = thought, idea
біреу = someone, somebody
жоғары = high; up, upper
бірге = together
үлкен = big, large; adult
кешір = to forgive (кешіріңіз = excuse me, sorry)
аудар = to translate; to turn over
тіпті = even; at all
қарай = toward
қабылда = to accept, to receive
қорға = to defend, to protect
өмір = life
алға = forward, ahead
әрі = and also; further
жөн = proper way (жөнінде = concerning)
таста = to throw; to abandon
алд = front (алдында = in front of)
күт = to wait
әрине = of course
мәселе = problem, issue
ана = mother
немесе = or
шабуыл = attack
сөйле = to speak
бүгін = today
сақта = to keep, to save; to protect
ойна = to play
қатты = hard; loud; strongly
ойын = game; play
міне = here it is; look!
жүз = hundred; face
оқы = to read; to study
ел = country; people, nation
төрт = four
арт = back, rear (артында = behind)
сана = to count; to consider
бері = since; this way
көмек = help
бет = face; page; side
өлтір = to kill
соқ = to hit, to strike
от = fire
мүмкіндік = opportunity, possibility
халық = people, nation
ата = to name; also: grandfather
қолда = to support; to use
сын = to break (by itself); also: criticism
қалдыр = to leave behind
ұш = to fly
тез = fast, quick
шақыр = to call, to invite
онда = there; then
ешкім = nobody, no one
шын = true, real; truth
жалғыз = alone, only
көтер = to lift, to raise
дайын = ready
керемет = wonderful, great
әйел = woman; wife
себеп = reason, cause
батыр = hero, brave warrior
тіл = language; tongue
зат = thing, object
жігіт = young man
бес = five
тас = stone
бойы = along, throughout
ақша = money
бойынша = according to; by
жайлы = about; comfortable
жең = to defeat, to win
өткіз = to spend (time); to hold (an event)
хан = khan (ruler)
тым = too, too much
өл = to die
есті = to hear
бөл = to divide, to share
сондай = such, like that
солай = that way, so
дос = friend
бірнеше = several, a few
ес = mind, memory
негіз = basis, foundation
әр = every, each
сонда = then, in that case
қаш = to run away, to flee
бөлім = section, department
орта = middle; environment
соғыс = war
қыл = to do, to make
соңғы = last, final
ештеңе = nothing
әкел = to bring
мың = thousand
аяқ = foot, leg
емес = not; is not
қиын = difficult
келесі = next
сағат = hour; clock, watch
тыңда = to listen
та = also, too (the да variant)
сат = to sell
арқылы = through, by means of
кеш = evening; late
ізде = to search, to look for
аст = bottom (астында = under)
топ = group, crowd
құр = to build, to establish
күшті = strong
ас = food, meal
жаман = bad
же = to eat
түсір = to drop, to lower; to film
өйткені = because
біт = to finish, to come to an end
маңызды = important
шеш = to solve, to decide
тоқтат = to stop (something), to halt
есім = name (a given name)
жарық = light; bright
ту = to be born; also: flag
байқа = to notice
мықты = strong, sturdy; great
көлік = vehicle, transport
жақын = near, close
біраз = some, a little; a while
бүкіл = whole, entire
ұмыт = to forget
ауыр = heavy; hard; ill
алайда = however
көңіл = mood, feelings; attention
түн = night
жап = to close, to shut
ауа = air; weather
ашық = open; clear
сендер = you (plural, informal)
таны = to recognize
көмектес = to help
рас = true; truth
мырза = mister, sir
басқар = to manage, to govern
тиіс = must, supposed to
жина = to gather, to collect
үст = top, surface (үстінде = on)
мынау = this (pointing at it)
дайында = to prepare
ауыл = village
бөлік = part, piece
секілді = like, as if
дүние = world; thing
доп = ball
анық = clear, definite
жүрек = heart
білдір = to express, to inform
қызық = interesting; fun
яғни = that is, i.e.
еш = no, not any
қатар = row; alongside
қанша = how much, how many
үйрен = to learn
бұз = to break, to destroy
кездес = to meet
өзгер = to change
жеткіз = to deliver, to convey
қызмет = service; job
"""
GL = {l.split(" = ")[0]: l.split(" = ", 1)[1] for l in GLOSSES.strip().splitlines()}
DROP = {"ти"}                                              # infinitive form not certain, skipped
SHOW = {"алд": "алды", "аст": "асты", "үст": "үсті", "е": "е", "қой": "қою"}   # dictionary form overrides
TYPE = {"мен": "pronoun", "да": "particle", "та": "particle", "ма": "particle", "ғой": "particle", "емес": "particle", "сонда": "adverb",
        "әрі": "conjunction", "бар": "adjective / verb", "де": "verb", "е": "verb"}
POS = {"NOUN": "noun", "VERB": "verb", "AUX": "verb", "ADJ": "adjective", "ADV": "adverb", "PRON": "pronoun", "DET": "determiner",
       "ADP": "postposition", "CCONJ": "conjunction", "SCONJ": "conjunction", "PART": "particle", "NUM": "numeral", "INTJ": "interjection"}

def infinitive(stem):
    s = stem[:-1] + {"п": "б", "қ": "ғ", "к": "г"}.get(stem[-1], stem[-1])
    return s + "у"

rows = [r for r in csv.DictReader(open(B + "Temp/core_vocabulary.tsv", encoding="utf-8"), delimiter="\t") if r["lemma"] not in DROP][:300]
missing = [r["lemma"] for r in rows if r["lemma"] not in GL]
assert not missing, f"no gloss for {missing}"

forms = collections.defaultdict(collections.Counter)
for n in ("subs", "news", "wiki"):
    for lem, fs in pickle.load(open(B + f"Temp/counts_{n}.pkl", "rb"))["forms"].items():
        for f, c in fs.items(): forms[lem][f] += c

def clip(word):
    """Male Kazakh voice says the word; trimmed MP3 at peak 0.4, cached in AD by codepoints. Returns the file path."""
    name = "-".join(f"{ord(c):x}" for c in word) + ".mp3"; f = AD + name
    if os.path.exists(f): return f
    if os.path.exists(CW + name): shutil.copy2(CW + name, f); return f
    print(f"[DEBUG] generating {word}", flush=True)
    asyncio.run(edge_tts.Communicate(word, "kk-KZ-DauletNeural", rate="-10%").save(f))
    c = av.open(f); r = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.05 * r)
    y = x[max(0, idx[0] - pad):min(len(x), idx[-1] + pad)]; y = y * (0.4 / abs(y).max())
    out = av.open(f, "w", format="mp3"); st = out.add_stream("mp3", rate=r); st.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = r
    for p in st.encode(fr): out.mux(p)
    for p in st.encode(None): out.mux(p)
    out.close(); return f

ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>'
audio, body = {}, ""
for r in rows:
    lem = r["lemma"]
    word = SHOW.get(lem) or (infinitive(lem) if r["upos"] in ("VERB", "AUX") else lem)
    audio[word] = base64.b64encode(open(clip(word), "rb").read()).decode()
    tot = sum(forms[lem].values()) or 1
    fs = [f for f, c in forms[lem].most_common(8) if f != word and f != lem and c >= max(4, 0.04 * tot)][:4]
    body += (f'<tr><td class="c0"><button class="speak" data-word="{word}" aria-label="Play {word}">{ICON}</button>{word}</td>'
             f'<td>{GL[lem]}<span class="type-tag">{TYPE.get(lem) or POS.get(r["upos"], r["upos"].lower())}</span></td><td>{" ".join(fs)}</td></tr>\n')
print(f"[DEBUG] {len(rows)} rows, {len(audio)} clips", flush=True)

title = "Core Kazakh Words - The 300 Most Frequent Words with Audio"
desc = "The 300 most frequent Kazakh words with English meanings, audio and common forms, ranked from spoken and written corpora."
intro = ("These are the 300 most frequent Kazakh words, ranked by how often they appear in spoken subtitles and in written news and Wikipedia text. "
         "Each word is shown in dictionary form (verbs end in -у), and the last column lists the forms you will actually see, so мен, менің and маған count as one word. "
         "A small set of words does most of the work in any language: in a test on separate Kazakh sentences, these 300 made up about 54% of all the words. "
         "Learn these first and about every second word you hear or read will already be familiar, which is the base everything else builds on.")
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css?v=4">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/core-words.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Core Words</h1>
            <p class="section-subtitle">{intro}</p>
        </header>

        <div class="divider"></div>

        <section class="lesson-section"><table class="lesson-table"><thead><tr><th>Word</th><th>English</th><th>Common forms</th></tr></thead><tbody>
{body}</tbody></table></section>

        <div class="page-nav">
            <a href="common-words.html" class="btn">&larr;</a>
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>

    <script>
        const AUDIO = {json.dumps(audio, ensure_ascii=False)};
        let current = null;
        document.querySelectorAll('button.speak').forEach(btn => {{
            btn.addEventListener('click', function () {{
                const data = AUDIO[this.getAttribute('data-word')];
                if (!data) return;
                if (current) {{ current.pause(); }}
                document.querySelectorAll('button.speak.playing').forEach(b => b.classList.remove('playing'));
                const a = new Audio('data:audio/mpeg;base64,' + data);
                current = a;
                this.classList.add('playing');
                const done = () => this.classList.remove('playing');
                a.onended = done; a.onerror = done;
                a.play().catch(done);
            }});
        }});
    </script>
</body>
</html>
"""
open(B + "core-words.html", "w", encoding="utf-8").write(html)
print(f"[DEBUG] wrote core-words.html, {len(html)} bytes", flush=True)
