"""Build sentence-game.html (the "Sentence Constructor Game"): a sentence is shown in Kazakh or English and the player puts the words of the other language in order.
Inputs : common-words.html (every word and its group, read at build time so group names always match the Common Words Test) and the sentence tables below.
Method : 1) Sentences are generated here from small templates that need NO suffix rules (adjective before noun, "бұл" = this, possessive and "have" forms taken from
            the hand-written tables P1 / P2 / PRON_LOC, so every Kazakh form is spelled out by hand and nothing is computed from vowel harmony).
         2) Every sentence is tagged with the Common Words groups its content words belong to (helper words such as бұл, ал, және, еді, бар, жоқ and names are free).
            A sentence is offered when all of its groups are among the groups the player ticked.
         3) Difficulty = number of Kazakh words: Easy 2-3, Medium 4-5, Hard 6 or more. A round is 10 sentences (fewer if fewer match).
         4) The page shows the sentence, a line to build the answer on, and the shuffled words (tiles). Tiles are dragged (pointer events, works with a finger) or tapped
            to move between the bank and the line. Submit colours each tile green (right position) or red (wrong position); the player fixes and submits again.
            Score = 100 x (1 - wrong submits / (sentences x 3)).
Output : sentence-game.html (styles live in styles.css under "Sentence game").
"""
import re, json, html, random, itertools, hashlib, os
print("[DEBUG] sentence game build start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
rng = random.Random(2610)

# ---- group of every common word -----------------------------------------------------------------------------------------
src = open(W + "common-words.html", encoding="utf-8").read()
GROUP = {}
for sid, title, body in re.findall(r'<section class="lesson-section" id="([^"]+)"[^>]*><h2>(.*?)</h2>(.*?)</section>', src, re.S):
    g = "Adjectives" if sid.startswith("adjectives") else html.unescape(title)
    g = {"Greetings & basics": "Greetings & Basics", "Question words": "Question Words", "Everyday nouns": "Everyday Nouns",
         "Days of the week": "Days of the Week", "Verbs (dictionary form ends in -у)": "Verbs"}.get(g, g)
    for kk in re.findall(r'</button>(.*?)</td><td class="c1">', body): GROUP[html.unescape(kk)] = g
print(f"[DEBUG] {len(GROUP)} common words in {len(set(GROUP.values()))} groups", flush=True)

# ---- hand-written vocabulary --------------------------------------------------------------------------------------------
FREE = {"бұл", "ал", "және", "еді", "бар", "жоқ"}   # helper words that never need a group
ART = lambda adj: "an" if adj[0] in "aeiou" else "a"
OBJ_ADJ = {  # object noun -> (English, allowed adjectives)
    "үй": ("house", "үлкен кіші жаңа ескі әдемі қымбат арзан"), "кітап": ("book", "үлкен кіші жаңа ескі әдемі қымбат арзан"),
    "есік": ("door", "үлкен кіші жаңа ескі әдемі қымбат арзан"), "қала": ("city", "үлкен кіші жаңа ескі әдемі"),
    "ауыл": ("village", "үлкен кіші жаңа ескі әдемі"), "жол": ("road", "үлкен кіші жаңа ескі"), "мектеп": ("school", "үлкен кіші жаңа ескі әдемі"),
    "дүкен": ("shop", "үлкен кіші жаңа ескі қымбат арзан"), "базар": ("market", "үлкен кіші жаңа ескі қымбат арзан")}
ADJ_EN = {"үлкен": "big", "кіші": "small", "жаңа": "new", "ескі": "old", "әдемі": "beautiful", "қымбат": "expensive", "арзан": "cheap", "жас": "young",
          "жақсы": "good", "күшті": "strong", "бай": "rich", "кәрі": "old", "көп": "a lot of", "аз": "little", "биік": "tall", "терең": "deep", "ұзын": "long",
          "көк": "blue", "жарық": "bright", "ыстық": "hot", "суық": "cold", "жылы": "warm", "тәтті": "sweet", "тұзды": "salty", "қышқыл": "sour", "таза": "clean",
          "қызыл": "red", "жасыл": "green", "сары": "yellow", "ақ": "white", "қара": "black", "қоңыр": "brown"}
OADJ2 = [("үлкен", "жаңа"), ("кіші", "жаңа"), ("үлкен", "әдемі"), ("ескі", "кіші"), ("жаңа", "әдемі"), ("ескі", "қымбат"), ("жаңа", "арзан")]
ANTI = [("үлкен", "кіші"), ("жаңа", "ескі"), ("қымбат", "арзан"), ("кіші", "үлкен"), ("ескі", "жаңа"), ("арзан", "қымбат")]
COLORS = "қызыл көк жасыл сары ақ қара қоңыр".split()
COL_THING = {"үй": "house", "кітап": "book", "есік": "door", "ит": "dog", "мысық": "cat", "ат": "horse"}
ANIMAL = {"ит": "dog", "мысық": "cat", "ат": "horse", "қой": "sheep", "түйе": "camel", "құс": "bird"}
ANIMAL_ADJ = "үлкен кіші жас әдемі жақсы".split()
# my / your forms written out by hand (first and second person singular possessive)
P1 = {"үй": "үйім", "кітап": "кітабым", "есік": "есігім", "ит": "итім", "мысық": "мысығым", "ақша": "ақшам", "дос": "досым", "әке": "әкем", "ана": "анам",
      "ата": "атам", "әже": "әжем", "аға": "ағам", "апа": "апам", "мұғалім": "мұғалімім", "бала": "балам"}
P2 = {"үй": "үйің", "кітап": "кітабың", "есік": "есігің", "ит": "итің", "мысық": "мысығың", "ақша": "ақшаң", "дос": "досың", "әке": "әкең", "ана": "анаң",
      "ата": "атаң", "әже": "әжең", "аға": "ағаң", "апа": "апаң", "мұғалім": "мұғалімің", "бала": "балаң"}
THING_EN = {"үй": "house", "кітап": "book", "есік": "door", "ит": "dog", "мысық": "cat", "ақша": "money"}
THING_ADJ = {"үй": "үлкен кіші жаңа ескі әдемі қымбат арзан", "кітап": "үлкен кіші жаңа ескі әдемі қымбат арзан", "есік": "үлкен кіші жаңа ескі әдемі",
             "ит": "үлкен кіші жас жақсы", "мысық": "үлкен кіші жас жақсы", "ақша": "көп аз"}
PERS_EN = {"дос": "friend", "әке": "father", "ана": "mother", "ата": "grandfather", "әже": "grandmother", "аға": "older brother", "апа": "older sister",
           "мұғалім": "teacher", "бала": "child"}
def pers_adj(p):
    a = ["жақсы", "күшті", "бай"] + (["жас"] if p not in ("ата", "әже") else ["кәрі"]) + (["әдемі"] if p in ("ана", "әже", "апа") else [])
    return a
PADJ2 = [("жақсы", "жас"), ("жақсы", "күшті"), ("жас", "күшті"), ("бай", "жақсы")]
PRON_LOC = {"менде": ("мен", "I have"), "сенде": ("сен", "You have"), "бізде": ("біз", "We have"), "оларда": ("олар", "They have")}
PRON_LOC_NEG = {"менде": "I don't have", "сенде": "You don't have", "бізде": "We don't have", "оларда": "They don't have"}
HAVE = {"кітап": "a book", "үй": "a house", "ит": "a dog", "мысық": "a cat", "ат": "a horse", "дос": "a friend", "бала": "a child", "ақша": "money", "түйе": "a camel",
        "қой": "a sheep", "нан": "bread", "күріш": "rice", "картоп": "potatoes", "су": "water", "шай": "tea", "сүт": "milk", "алма": "an apple"}
FOOD = {"нан": "bread", "күріш": "rice", "картоп": "a potato", "алма": "an apple", "балық": "fish", "жұмыртқа": "an egg", "ет": "meat", "сүт": "milk", "шай": "tea",
        "су": "water", "сорпа": "soup", "қант": "sugar", "тұз": "salt", "май": "butter"}
FOOD_ADJ = [("шай", "tea", "ыстық", False), ("сорпа", "soup", "ыстық", False), ("су", "water", "суық", False), ("сүт", "milk", "жылы", False),
            ("алма", "apple", "тәтті", True), ("шай", "tea", "тәтті", False), ("балық", "fish", "тұзды", False), ("алма", "apple", "қышқыл", True)]
FOOD2 = [("шай", "tea", "ыстық", "hot", "тәтті", "sweet"), ("сорпа", "soup", "ыстық", "hot", "тұзды", "salty")]
NAT = [("тау", "mountain", "биік", "tall"), ("тау", "mountain", "әдемі", "beautiful"), ("көл", "lake", "терең", "deep"), ("көл", "lake", "үлкен", "big"),
       ("өзен", "river", "ұзын", "long"), ("өзен", "river", "терең", "deep"), ("аспан", "sky", "көк", "blue"), ("жұлдыз", "star", "жарық", "bright"),
       ("жұлдыз", "star", "әдемі", "beautiful"), ("жер", "earth", "үлкен", "big")]
BODY = [("қол", "hand", "қолым", "таза", "clean"), ("қол", "hand", "қолым", "жылы", "warm"), ("қол", "hand", "қолым", "суық", "cold"),
        ("жүрек", "heart", "жүрегім", "үлкен", "big"), ("жүрек", "heart", "жүрегім", "жақсы", "good")]
DAYS = [("дүйсенбі", "Monday"), ("сейсенбі", "Tuesday"), ("сәрсенбі", "Wednesday"), ("бейсенбі", "Thursday"), ("жұма", "Friday"), ("сенбі", "Saturday"), ("жексенбі", "Sunday")]
NAMES = [("Алекс", "Alex"), ("Айгүл", "Aigul"), ("Ержан", "Yerzhan"), ("Дана", "Dana"), ("Нұрлан", "Nurlan"), ("Аружан", "Aruzhan")]
PLACE_Q = {"үй": "house", "қала": "city", "ауыл": "village", "мектеп": "school", "дүкен": "shop", "базар": "market", "кітап": "book", "есік": "door", "жол": "road",
           "мұғалім": "teacher", "дос": "friend", "бала": "child", "әке": "father", "ана": "mother"}
PRICE_Q = {"кітап": "book", "есік": "door", "ит": "dog", "ат": "horse", "нан": "bread", "су": "water", "шай": "tea", "сүт": "milk", "ет": "meat", "балық": "fish",
           "алма": "apple", "картоп": "potato", "күріш": "rice"}
PROPER = {"I", "I'm"} | {d for _, d in DAYS} | {n for _, n in NAMES}

# ---- build the sentence list ------------------------------------------------------------------------------------------------
SENT, SEEN, BASES = [], set(), {}
def add(kk, en, bases):
    """kk / en: the full sentence with punctuation. bases: the common words its content words come from (groups are looked up from them)."""
    assert kk not in SEEN, kk
    for b in bases: assert b in GROUP, "not a common word: " + b
    SEEN.add(kk); BASES[kk] = bases
    ktoks = [w.strip(",.?!") for w in kk.split()]
    if ktoks[0] not in {n for n, _ in NAMES}: ktoks[0] = ktoks[0].lower()
    etoks = [w.strip(",.?!") for w in en.split()]
    if etoks[0] not in PROPER and etoks[0] != "I": etoks[0] = etoks[0].lower()
    groups = sorted({GROUP[b] for b in bases})
    n = len(ktoks)
    kt = kk[0].upper() + kk[1:]
    SENT.append({"k": ktoks, "e": etoks, "kt": kt, "et": en, "g": groups, "d": 0 if n <= 3 else 1 if n <= 5 else 2,
                 "a": hashlib.sha1(kt.encode("utf-8")).hexdigest()[:12]})   # "a" = name of the Kazakh audio clip in Sentence Audio/
def sample(items, n):
    items = list(items); rng.shuffle(items); return items[:n]

# objects with adjectives
for o, (oe, adjs) in OBJ_ADJ.items():
    for a in adjs.split():
        ae = ADJ_EN[a]
        add(f"Бұл {a} {o}.", f"This is {ART(ae)} {ae} {oe}.", [o, a])
        add(f"{o[0].upper() + o[1:]} {a}.", f"The {oe} is {ae}.", [o, a])
        add(f"Бұл {o} {a}.", f"This {oe} is {ae}.", [o, a])
for o in ("үй", "кітап", "есік"):
    for a1, a2 in OADJ2:
        add(f"Бұл {o} {a1} және {a2}.", f"This {OBJ_ADJ[o][0]} is {ADJ_EN[a1]} and {ADJ_EN[a2]}.", [o, a1, a2])
# colours
for t, te in COL_THING.items():
    for c in COLORS:
        ce = ADJ_EN[c]
        add(f"Бұл {c} {t}.", f"This is a {ce} {te}.", [t, c])
        add(f"{t[0].upper() + t[1:]} {c}.", f"The {te} is {ce}.", [t, c])
pairs = [(a, b) for a in ("ит", "мысық", "ат") for b in ("ит", "мысық", "ат") if a != b]
for (t1, t2), (c1, c2) in sample(itertools.product(pairs, itertools.permutations(COLORS, 2)), 70):
    add(f"Бұл {c1} {t1}, ал бұл {c2} {t2}.", f"This is a {ADJ_EN[c1]} {ANIMAL[t1]}, and this is a {ADJ_EN[c2]} {ANIMAL[t2]}.", [t1, t2, c1, c2])
# animals
for t, te in ANIMAL.items():
    for a in ANIMAL_ADJ:
        add(f"Бұл {a} {t}.", f"This is a {ADJ_EN[a]} {te}.", [t, a])
# my / your things and people
for t, te in THING_EN.items():
    for a in THING_ADJ[t].split():
        ae = ADJ_EN[a]
        add(f"Менің {P1[t]} {a}.", f"My {te} is {ae}." if t != "ақша" else f"I have {ae} money.", [t, a, "мен"])
        if t != "ақша": add(f"Сенің {P2[t]} {a}.", f"Your {te} is {ae}.", [t, a, "сен"])
    add(f"Бұл менің {P1[t]}.", f"This is my {te}." if t != "ақша" else "This is my money.", [t, "мен"])
    add(f"Бұл сенің {P2[t]}.", f"This is your {te}." if t != "ақша" else "This is your money.", [t, "сен"])
for p, pe in PERS_EN.items():
    for a in pers_adj(p):
        add(f"Менің {P1[p]} {a}.", f"My {pe} is {ADJ_EN[a]}.", [p, a, "мен"])
        add(f"Сенің {P2[p]} {a}.", f"Your {pe} is {ADJ_EN[a]}.", [p, a, "сен"])
    add(f"Бұл менің {P1[p]}.", f"This is my {pe}.", [p, "мен"])
    add(f"Бұл сенің {P2[p]}.", f"This is your {pe}.", [p, "сен"])
for t in ("үй", "кітап", "есік"):
    for a1, a2 in OADJ2:
        add(f"Менің {P1[t]} {a1} және {a2}.", f"My {THING_EN[t]} is {ADJ_EN[a1]} and {ADJ_EN[a2]}.", [t, a1, a2, "мен"])
    for a1, a2 in ANTI:
        add(f"Менің {P1[t]} {a1}, ал сенің {P2[t]} {a2}.", f"My {THING_EN[t]} is {ADJ_EN[a1]}, and your {THING_EN[t]} is {ADJ_EN[a2]}.", [t, a1, a2, "мен", "сен"])
for p in ("дос", "әке", "ана", "аға", "апа", "мұғалім"):
    for a1, a2 in PADJ2:
        add(f"Менің {P1[p]} {a1} және {a2}.", f"My {PERS_EN[p]} is {ADJ_EN[a1]} and {ADJ_EN[a2]}.", [p, a1, a2, "мен"])
for p1, p2 in sample(itertools.permutations(("дос", "әке", "ана", "аға", "апа", "мұғалім"), 2), 25):
    for a1, a2 in sample([(x, y) for x in ("жақсы", "жас", "күшті") for y in ("жақсы", "жас", "күшті") if x != y], 1):
        add(f"Менің {P1[p1]} {a1}, ал сенің {P2[p2]} {a2}.", f"My {PERS_EN[p1]} is {ADJ_EN[a1]}, and your {PERS_EN[p2]} is {ADJ_EN[a2]}.", [p1, p2, a1, a2, "мен", "сен"])
# having things
for pl, (pb, pen) in PRON_LOC.items():
    for n, ne in HAVE.items():
        add(f"{pl[0].upper() + pl[1:]} {n} бар.", f"{pen} {ne}.", [n, pb])
        if pl in ("менде", "сенде"): add(f"{pl[0].upper() + pl[1:]} {n} жоқ.", f"{PRON_LOC_NEG[pl]} {ne}." if ne != "money" else f"{pen.replace(' have', '')} have no money.", [n, pb])
for pl in ("менде", "бізде"):
    for n1, n2 in sample(itertools.permutations(("кітап", "ит", "мысық", "үй", "дос", "ат", "бала", "түйе"), 2), 20):
        en1, en2 = HAVE[n1], HAVE[n2]
        add(f"{pl[0].upper() + pl[1:]} {n1} және {n2} бар.", f"{PRON_LOC[pl][1]} {en1} and {en2}.", [n1, n2, PRON_LOC[pl][0]])
# questions
add("Бұл не?", "What is this?", ["не"]); add("Бұл кім?", "Who is this?", ["кім"]); add("Бұл қанша?", "How much is this?", ["қанша"])
add("Сенің атың кім?", "What is your name?", ["сен", "кім"])
add("Қалыңыз қалай?", "How are you?", ["қалыңыз қалай"]); add("Қанша тұрады?", "How much does it cost?", ["қанша тұрады"])
add("Бұл қанша тұрады?", "How much does this cost?", ["қанша тұрады"])
add("Қайырлы таң.", "Good morning.", ["қайырлы таң"]); add("Қайырлы кеш.", "Good evening.", ["қайырлы кеш"])
for t, te in PLACE_Q.items(): add(f"{t[0].upper() + t[1:]} қайда?", f"Where is the {te}?", [t, "қайда"])
for t, te in PRICE_Q.items(): add(f"{t[0].upper() + t[1:]} қанша?", f"How much is the {te}?", [t, "қанша"])
for n, ne in NAMES:
    add(f"Менің атым {n}.", f"My name is {ne}.", ["мен"])
    add(f"Менің атым {n}, ал сенің атың кім?", f"My name is {ne}, and what is your name?", ["мен", "сен", "кім"])
# days
for i, (d, de) in enumerate(DAYS):
    nd, ne_ = DAYS[(i + 1) % 7], None
    pd = DAYS[(i - 1) % 7]
    add(f"Бүгін {d}.", f"Today is {de}.", [d, "бүгін"]); add(f"Ертең {d}.", f"Tomorrow is {de}.", [d, "ертең"]); add(f"Кеше {d} еді.", f"Yesterday was {de}.", [d, "кеше"])
    add(f"Бүгін {d}, ертең {nd[0]}.", f"Today is {de}, tomorrow is {nd[1]}.", [d, nd[0], "бүгін", "ертең"])
    add(f"Кеше {pd[0]} еді, бүгін {d}.", f"Yesterday was {pd[1]}, today is {de}.", [pd[0], d, "кеше", "бүгін"])
    add(f"Кеше {pd[0]} еді, бүгін {d}, ертең {nd[0]}.", f"Yesterday was {pd[1]}, today is {de}, tomorrow is {nd[1]}.", [pd[0], d, nd[0], "кеше", "бүгін", "ертең"])
# food
for f, fe in FOOD.items(): add(f"Бұл {f}.", f"This is {fe}.", [f])
for f, fe, a, count in FOOD_ADJ:
    ae = ADJ_EN[a]
    add(f"Бұл {a} {f}.", f"This is {'a ' if count else ''}{ae} {fe}.", [f, a]); add(f"{f[0].upper() + f[1:]} {a}.", f"The {fe} is {ae}.", [f, a])
for f, fe, a1, e1, a2, e2 in FOOD2: add(f"Бұл {f} {a1} және {a2}.", f"This {fe} is {e1} and {e2}.", [f, a1, a2])
for f, fe in (("алма", "an apple"), ("жұмыртқа", "an egg")):
    add(f"Бұл жарты {f}.", f"This is half {fe}.", [f, "жарты"]); add(f"Бұл бүтін {f}.", f"This is a whole {fe[3:]}.", [f, "бүтін"])
# nature and body
for n, ne, a, ae in NAT:
    add(f"{n[0].upper() + n[1:]} {a}.", f"The {ne} is {ae}.", [n, a]); add(f"Бұл {a} {n}.", f"This is {ART(ae)} {ae} {ne}.", [n, a])
for (n1, e1, a1, ae1), (n2, e2, a2, ae2) in sample([(x, y) for x in NAT for y in NAT if x[0] != y[0]], 30):
    add(f"{n1[0].upper() + n1[1:]} {a1}, ал {n2} {a2}.", f"The {e1} is {ae1}, and the {e2} is {ae2}.", [n1, a1, n2, a2])
for n, ne, poss, a, ae in BODY: add(f"Менің {poss} {a}.", f"My {ne} is {ae}.", [n, a, "мен"])
print(f"[DEBUG] {len(SENT)} sentences; Easy {sum(s['d'] == 0 for s in SENT)}, Medium {sum(s['d'] == 1 for s in SENT)}, Hard {sum(s['d'] == 2 for s in SENT)}", flush=True)
# "Бұл {adj} {noun}" (This is a red house) and "Бұл {noun} {adj}" (This house is red) are both accepted for either English sentence: both orders are good Kazakh.
# Every "Бұл {adj} {noun}" sentence gets its "Бұл {noun} {adj}" twin if it does not exist yet, then the two are linked.
for x in list(SENT):
    if len(x["k"]) == 3 and x["k"][0] == "бұл" and x["k"][1] in ADJ_EN and x["k"][2] not in ADJ_EN:
        m = re.match(r"^This is (?:an? )?(\S+) (.+)\.$", x["et"]); assert m, x["et"]
        twin = f"Бұл {x['k'][2]} {x['k'][1]}."
        if twin not in SEEN: add(twin, f"This {m.group(2)} is {m.group(1)}.", BASES[x["kt"]])
BYKK = {x["kt"]: x for x in SENT}
for x in list(SENT):
    if len(x["k"]) == 3 and x["k"][0] == "бұл" and x["k"][1] in ADJ_EN and x["k"][2] not in ADJ_EN:
        y = BYKK[f"Бұл {x['k'][2]} {x['k'][1]}."]
        x["alt"] = [{"k": y["k"], "a": y["a"]}]; y["alt"] = [{"k": x["k"], "a": x["a"]}]
print(f"[DEBUG] {len(SENT)} sentences now; {sum('alt' in x for x in SENT)} accept a second Kazakh word order", flush=True)
rng.shuffle(SENT)
no_clip = [x["kt"] for x in SENT if not os.path.exists(W + "Sentence Audio/" + x["a"] + ".mp3")]
print(f"[DEBUG] {len(no_clip)} sentences have no audio clip yet", flush=True); assert not os.environ.get("NEED_AUDIO") or not no_clip, "run build_sentence_audio.py first"
GROUPS = [g for g in dict.fromkeys(GROUP.values())]
STARTER = ["Pronouns", "Adjectives", "Places", "Everyday Nouns", "Colors"]
assert all(g in GROUPS for g in STARTER)
USED = sorted({g for s in SENT for g in s["g"]})
print("[DEBUG] groups that produce sentences: " + ", ".join(USED), "| none for: " + ", ".join(g for g in GROUPS if g not in USED), flush=True)
print("[DEBUG] starter set gives " + ", ".join(f"{n}: {sum(1 for s in SENT if s['d'] == d and all(g in STARTER for g in s['g']))}" for d, n in enumerate(("Easy", "Medium", "Hard"))), flush=True)

# ---- page -----------------------------------------------------------------------------------------------------------------
JS = r"""
        const MAX_WRONG_PER_SENTENCE = 3, ROUND_SIZE = 10;
        const DIFFS = [['easy', 'Easy', 0], ['medium', 'Medium', 1], ['hard', 'Hard', 2], ['mixed', 'Mixed', -1]];
        const $ = id => document.getElementById(id);
        const shuffle = a => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        const setupEl = $('setup'), roundEl = $('round'), groupsEl = $('groups'), goBtn = $('go'), noteEl = $('note'), diffEl = $('diffs');
        const langKk = $('langKk'), langEn = $('langEn'), lineEl = $('line'), bankEl = $('bank'), submitEl = $('submit'), msgEl = $('msg'), promptEl = $('prompt');
        const speakEl = $('speak'), tallyEl = $('tally'), resultEl = $('result'), playEl = $('play'), scoreEl = $('score'), missedBox = $('missedBox'), missedEl = $('missed');
        let lang = 'en', diff = 'easy', anySelected = false;                 // lang = language the sentence is SHOWN in ('en' means the player builds Kazakh)
        const selected = new Set(STARTER);

        // ---- setup ----
        function setLang(l) { lang = l; langKk.setAttribute('aria-pressed', l === 'kk' ? 'true' : 'false'); langEn.setAttribute('aria-pressed', l === 'en' ? 'true' : 'false'); }
        langKk.addEventListener('click', () => setLang('kk')); langEn.addEventListener('click', () => setLang('en'));
        DIFFS.forEach(([id, label]) => {
            const b = document.createElement('button'); b.type = 'button'; b.className = 'group-btn'; b.textContent = label; b.dataset.id = id;
            b.addEventListener('click', () => { diff = id; refresh(); }); diffEl.appendChild(b);
        });
        GROUPS.forEach(name => {
            const b = document.createElement('button'); b.type = 'button'; b.className = 'group-btn'; b.textContent = name;
            b.addEventListener('click', () => { if (anySelected) return; selected.has(name) ? selected.delete(name) : selected.add(name); refresh(); }); groupsEl.appendChild(b);
        });
        $('anyBtn').addEventListener('click', () => { anySelected = !anySelected; refresh(); });
        const diffIdx = () => DIFFS.find(d => d[0] === diff)[2];
        function pool() { const d = diffIdx(); return SENTS.filter(s => (d < 0 || s.d === d) && (anySelected || s.g.every(g => selected.has(g)))); }
        function refresh() {
            [...groupsEl.children].forEach(b => { b.setAttribute('aria-pressed', selected.has(b.textContent) ? 'true' : 'false'); b.disabled = anySelected; });
            [...diffEl.children].forEach(b => b.setAttribute('aria-pressed', b.dataset.id === diff ? 'true' : 'false'));
            $('anyBtn').setAttribute('aria-pressed', anySelected ? 'true' : 'false');
            const n = pool().length;
            noteEl.textContent = n ? n + (n === 1 ? ' sentence matches' : ' sentences match') + (n < ROUND_SIZE ? ', so a round will have ' + n + '.' : '.')
                                   : 'No sentences match. Tick more groups or change the difficulty.';
            goBtn.disabled = n === 0;
        }

        // ---- round state ----
        let sents = [], idx = 0, state = null, locked = false, solved = false, wrongSubmits = 0, wrongSet = new Set(), nextTimer = null, nextId = 1;
        const usedSet = new Set();
        const SAME = { kk: new Map(SENTS.map(s => [s.k.join(' '), s])), en: new Map(SENTS.map(s => [s.e.join(' '), s])) };   // finds another real sentence with the same words in the same order
        const built = s => lang === 'kk' ? s.e : s.k;                       // the words the player puts in order
        function startRound() {
            const p = shuffle(pool());
            let fresh = p.filter(s => !usedSet.has(s));
            if (fresh.length < Math.min(ROUND_SIZE, p.length)) { p.forEach(s => usedSet.delete(s)); fresh = p; }
            sents = fresh.slice(0, ROUND_SIZE); sents.forEach(s => usedSet.add(s));
            beginRound();
        }
        function beginRound() {                                            // starts (or restarts) the sentences in `sents`; the words are shuffled afresh each time
            idx = 0; wrongSubmits = 0; wrongSet = new Set();
            resultEl.hidden = true; playEl.hidden = false; setupEl.hidden = true; roundEl.hidden = false;
            showSentence();
        }
        function showSentence() {
            clearTimeout(nextTimer); stopAudio(); locked = false; solved = false; msgEl.textContent = '';
            speakEl.hidden = true; submitEl.textContent = 'Submit'; $('clear').hidden = false;
            const s = sents[idx], words = built(s);
            tallyEl.textContent = 'Sentence ' + (idx + 1) + ' of ' + sents.length;
            promptEl.textContent = lang === 'kk' ? s.kt : s.et; promptEl.lang = lang === 'kk' ? 'kk' : 'en';
            let order = shuffle(words.map(text => ({ id: nextId++, text })));
            for (let i = 0; i < 10 && order.length > 1 && order.every((t, j) => t.text === words[j]); i++) order = shuffle(order);
            state = { bank: order, line: [] };
            render();
        }
        function tileEl(t, where) {
            const b = document.createElement('button'); b.type = 'button'; b.className = 'sc-tile' + (t.status ? ' ' + t.status : '') + (t.dragging ? ' dragging' : '');
            b.textContent = t.text; b.dataset.id = t.id; b.lang = lang === 'kk' ? 'en' : 'kk';
            b.addEventListener('pointerdown', e => dragStart(e, t, b));
            b.addEventListener('click', () => { if (justDragged || locked) return; move(t, where === 'bank' ? 'line' : 'bank'); });
            return b;
        }
        function render() {
            lineEl.innerHTML = ''; bankEl.innerHTML = '';
            state.line.forEach(t => lineEl.appendChild(tileEl(t, 'line'))); state.bank.forEach(t => bankEl.appendChild(tileEl(t, 'bank')));
            lineEl.classList.toggle('empty', !state.line.length);
            submitEl.disabled = solved ? false : (locked || state.bank.length > 0);
        }
        function clearStatus() { state.line.concat(state.bank).forEach(t => { delete t.status; }); }
        function remove(t) { state.bank = state.bank.filter(x => x !== t); state.line = state.line.filter(x => x !== t); }
        function move(t, to, at) {
            clearStatus(); remove(t); msgEl.textContent = '';
            if (to === 'bank') state.bank.push(t); else state.line.splice(at === undefined ? state.line.length : at, 0, t);
            render();
        }

        // ---- drag and drop (pointer events: mouse, pen and finger) ----
        let drag = null, justDragged = false;
        function dragStart(e, t, el) {
            if (locked || (e.button !== undefined && e.button > 0)) return;
            drag = { t, el, id: e.pointerId, sx: e.clientX, sy: e.clientY, moving: false, ghost: null };
            try { el.setPointerCapture(e.pointerId); } catch (x) {}
            el.addEventListener('pointermove', dragMove); el.addEventListener('pointerup', dragEnd); el.addEventListener('pointercancel', dragEnd);
        }
        function overLine(x, y) { const r = lineEl.getBoundingClientRect(); return x >= r.left - 10 && x <= r.right + 10 && y >= r.top - 14 && y <= r.bottom + 14; }
        function dragMove(e) {
            if (!drag || e.pointerId !== drag.id) return;
            if (!drag.moving) {
                if (Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) < 8) return;
                drag.moving = true; const r = drag.el.getBoundingClientRect();
                drag.dx = e.clientX - r.left; drag.dy = e.clientY - r.top;
                drag.ghost = drag.el.cloneNode(true); drag.ghost.classList.add('ghost'); drag.ghost.style.width = r.width + 'px'; document.body.appendChild(drag.ghost);
                drag.el.classList.add('dragging');
            }
            drag.ghost.style.left = (e.clientX - drag.dx) + 'px'; drag.ghost.style.top = (e.clientY - drag.dy) + 'px';
            lineEl.classList.toggle('over', overLine(e.clientX, e.clientY));
        }
        function dragEnd(e) {
            if (!drag || e.pointerId !== drag.id) return;
            const d = drag; drag = null;
            d.el.removeEventListener('pointermove', dragMove); d.el.removeEventListener('pointerup', dragEnd); d.el.removeEventListener('pointercancel', dragEnd);
            try { d.el.releasePointerCapture(e.pointerId); } catch (x) {}
            lineEl.classList.remove('over');
            if (!d.moving) return;                                         // a tap: the click handler does the work
            d.ghost.remove(); justDragged = true; setTimeout(() => { justDragged = false; }, 0);
            if (e.type === 'pointercancel') { render(); return; }
            if (overLine(e.clientX, e.clientY)) {
                const others = state.line.filter(x => x !== d.t), els = others.map(x => lineEl.querySelector('[data-id="' + x.id + '"]'));
                let at = others.length;
                for (let i = 0; i < els.length; i++) {
                    const r = els[i].getBoundingClientRect();
                    if (e.clientY < r.top || (e.clientY <= r.bottom && e.clientX < r.left + r.width / 2)) { at = i; break; }
                }
                move(d.t, 'line', at);
            } else move(d.t, 'bank');
        }

        // ---- submit ----
        // Audio of the sentence in the language the player just built: the Kazakh clip (Sentence Audio/), or the browser's English voice.
        let audio = null, clipName = null;
        const clipUrl = s => 'Sentence%20Audio/' + (clipName || s.a) + '.mp3';
        const canSpeakEnglish = 'speechSynthesis' in window;
        function stopAudio() { if (audio) { audio.pause(); audio = null; } if (canSpeakEnglish) speechSynthesis.cancel(); speakEl.classList.remove('playing'); }
        function playSentence() {
            stopAudio(); const s = sents[idx], done = () => speakEl.classList.remove('playing');
            speakEl.classList.add('playing');
            if (lang === 'en') { audio = new Audio(clipUrl(s)); audio.onended = done; audio.onerror = done; audio.play().catch(done); }
            else if (canSpeakEnglish) { const u = new SpeechSynthesisUtterance(s.et); u.lang = 'en-US'; u.rate = 0.95; u.onend = done; u.onerror = done; speechSynthesis.speak(u); }
            else done();
        }
        speakEl.addEventListener('click', playSentence);
        submitEl.addEventListener('click', () => {
            if (solved) { nextSentence(); return; }                         // after a correct answer this button reads Next / Finish
            if (locked || state.bank.length) return;
            const s = sents[idx], line = state.line.map(t => t.text);
            const accepted = [{ k: built(s), a: s.a }].concat(lang === 'en' && s.alt ? s.alt : []);   // alternative Kazakh word orders that are just as good
            const hits = c => c.k.filter((w, i) => w === line[i]).length;
            const match = accepted.find(c => hits(c) === c.k.length && c.k.length === line.length);
            const best = match || accepted.reduce((b, c) => hits(c) > hits(b) ? c : b), sol = best.k;
            clipName = best.a;                                              // the clip of the order the player actually built
            let ok = true;
            state.line.forEach((t, i) => { t.status = t.text === sol[i] ? 'ok' : 'bad'; if (t.status === 'bad') ok = false; });
            if (ok) {
                locked = true; solved = true; msgEl.textContent = 'Correct!'; $('clear').hidden = true;
                submitEl.textContent = idx === sents.length - 1 ? 'Finish' : 'Next';
                speakEl.hidden = lang === 'kk' && !canSpeakEnglish; if (!speakEl.hidden) playSentence();
            }
            else {
                wrongSubmits++; wrongSet.add(sents[idx]);
                const other = SAME[lang === 'en' ? 'kk' : 'en'].get(state.line.map(t => t.text).join(' '));
                msgEl.textContent = other && other !== sents[idx]
                    ? 'That order is a real sentence: “' + (lang === 'en' ? other.et : other.kt) + '” It is not the one shown, so the red words are in the wrong place.'
                    : 'The red words are in the wrong place.';
            }
            render();
        });
        $('clear').addEventListener('click', () => { if (locked) return; clearStatus(); state.bank = state.bank.concat(state.line); state.line = []; msgEl.textContent = ''; render(); });
        function nextSentence() { idx++; if (idx >= sents.length) finish(); else showSentence(); }
        function finish() {
            clearTimeout(nextTimer); stopAudio();
            scoreEl.textContent = Math.max(0, Math.round(100 * (1 - wrongSubmits / (sents.length * MAX_WRONG_PER_SENTENCE))));
            missedEl.innerHTML = ''; const wrong = sents.filter(s => wrongSet.has(s)); missedBox.hidden = !wrong.length;
            wrong.forEach(s => {
                const row = document.createElement('div'); row.className = 'missed-row';
                const q = document.createElement('span'); q.className = 'missed-q'; q.lang = lang === 'kk' ? 'kk' : 'en'; q.textContent = lang === 'kk' ? s.kt : s.et;
                const a = document.createElement('span'); a.className = 'missed-a'; a.lang = lang === 'kk' ? 'en' : 'kk'; a.textContent = lang === 'kk' ? s.et : s.kt;
                row.append(q, a); missedEl.appendChild(row);
            });
            playEl.hidden = true; resultEl.hidden = false;
        }
        goBtn.addEventListener('click', () => { if (!goBtn.disabled) startRound(); });
        $('fresh').addEventListener('click', startRound);                  // New Deck: other sentences from the same setup
        $('repeat').addEventListener('click', beginRound);                 // Repeat This Deck: the same sentences again
        function backToSetup() { clearTimeout(nextTimer); stopAudio(); roundEl.hidden = true; setupEl.hidden = false; }
        $('back').addEventListener('click', backToSetup); $('change').addEventListener('click', backToSetup);
        setLang('en'); refresh();
"""

title = "Kazakh Sentence Constructor: Put the Words in Order"
desc = "Practise Kazakh word order: a sentence is shown in English or Kazakh and you drag the words of the other language into the right order."
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <link rel="stylesheet" href="styles.css?v=26">
    <meta name="description" content="%(desc)s">
    <link rel="canonical" href="https://albazzaztariq.github.io/kazakh-language/sentence-game.html">
    <meta name="theme-color" content="#00AFCA">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Sentence Constructor</h1>
            <p class="section-subtitle">Put the words in the right order</p>
        </header>

        <div class="divider"></div>

        <div class="game">
            <div id="setup">
                <div class="setup-title">Sentence Displayed in:</div>
                <div class="lang-row">
                    <button type="button" class="group-btn lang-btn" id="langKk" aria-pressed="false">Kazakh</button>
                    <button type="button" class="group-btn lang-btn" id="langEn" aria-pressed="true">English</button>
                </div>
                <div class="setup-title setup-title-groups">Difficulty</div>
                <div class="group-grid sc-diffs" id="diffs"></div>
                <div class="setup-title setup-title-groups">Select the Groups of Vocabulary the Sentences May Use</div>
                <div class="group-grid" id="groups"></div>
                <button type="button" class="any-btn" id="anyBtn" aria-pressed="false">Any</button>
                <div class="deck-size-note sc-note" id="note"></div>
                <div class="deck-size-note">Little helper words (this, and, was, there is) and names are always allowed. Verbs are not used yet because they need endings.</div>
                <button type="button" class="go-btn" id="go" disabled>Go</button>
            </div>

            <div id="round" hidden>
                <button type="button" class="link-btn" id="back">&larr; Change setup</button>
                <div id="play">
                    <div class="sc-tally" id="tally" aria-live="polite"></div>
                    <div class="game-word sc-prompt" id="prompt"></div>
                    <div class="sc-line empty" id="line" aria-label="Your answer"></div>
                    <div class="sc-bank" id="bank" aria-label="Words to place"></div>
                    <div class="sc-msg-row">
                        <div class="sc-msg" id="msg" role="status" aria-live="polite"></div>
                        <button type="button" class="speak sc-speak" id="speak" aria-label="Play this sentence" hidden>
                            <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>
                        </button>
                    </div>
                    <div class="sc-buttons">
                        <button type="button" class="link-btn" id="clear">Clear</button>
                        <button type="button" class="go-btn sc-submit" id="submit" disabled>Submit</button>
                    </div>
                </div>
                <div class="game-result" id="result" hidden>
                    <div class="result-label">Score</div>
                    <div class="result-score"><span id="score">0</span><span class="result-max"> / 100</span></div>
                    <div class="missed-box" id="missedBox" hidden>
                        <div class="missed-title">Missed</div>
                        <div class="missed-list" id="missed"></div>
                    </div>
                    <div class="game-actions">
                        <button type="button" class="btn" id="repeat">Repeat This Deck</button>
                        <button type="button" class="btn" id="fresh">New Deck</button>
                        <button type="button" class="btn" id="change">Change Setup</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="page-nav">
            <a href="index.html" class="btn">Home</a>
        </div>

        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>

    <script>
        const SENTS = %(sents)s;
        const GROUPS = %(groups)s, STARTER = %(starter)s;
%(js)s    </script>
</body>
</html>
""" % {"title": title, "desc": desc, "sents": json.dumps(SENT, ensure_ascii=False, separators=(",", ":")), "groups": json.dumps(GROUPS, ensure_ascii=False),
       "starter": json.dumps(STARTER, ensure_ascii=False), "js": JS}
open(W + "sentence-game.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote sentence-game.html, {len(page)} bytes", flush=True)
