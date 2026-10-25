"""Build culture.html: short explanations of Kazakh cultural ideas (definition in 3 sentences or fewer, then examples), with jump buttons and a floating Top button.
Inputs : the TOPICS list below (id, button label, title, Kazakh term line, definition, examples). Nothing is read from other pages.
Method : same page layout as common-words.html (back link, header, jump-link pills, one lesson-section per topic, page-nav), plus a floating "Top" button
         that appears after scrolling (same behaviour as common-words.html and create-deck.html).
Output : culture.html (overwritten). The homepage link to it lives in index.html (Culture section, Explore button).
"""
import html
print("[DEBUG] culture page build start", flush=True)
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"

TOPICS = [
    ("uyat", "Uyat", "Uyat (ұят)", "ұят &middot; u-yat &middot; shame, modesty, conscience",
     "Uyat is the Kazakh sense of shame and social conscience: the inner feeling that an action would be improper in front of family, elders or neighbours. "
     "It works less as a written rule than as a shared standard of modesty, respect and restraint. "
     "Adults say <em>Ұят!</em> (&ldquo;Shame!&rdquo;) to stop a child, or anyone, from behaving badly, and a person who has no uyat is considered shameless.",
     ["Staying seated while an older person stands, or not offering them your seat.",
      "Raising your voice, swearing or arguing with elders, or interrupting them.",
      "Wasting bread, stepping over it or putting it upside down on the table. Bread is treated with respect, and a piece that falls is picked up and kissed.",
      "Not greeting relatives and neighbours, or visiting someone and leaving without thanking the host.",
      "Boasting about your own success. Modesty is the expected behaviour.",
      "Useful phrases: <em>Бұл ұят</em> (bul u-yat), &ldquo;that is shameful&rdquo;; <em>ұялу</em> (u-ya-lu), &ldquo;to feel shy or ashamed&rdquo;."]),
    ("zheti-ata", "Zheti Ata", "Zheti ata (жеті ата)", "жеті ата &middot; zhe-ti a-ta &middot; the seven fathers",
     "Zheti ata, &ldquo;the seven fathers&rdquo;, is the tradition of knowing your male ancestors back seven generations. "
     "It ties each person to a clan (<em>ру</em>, ru), and it traditionally forbids marriage between people who share an ancestor within those seven generations. "
     "Knowing your lineage is a sign of a good upbringing and gives every Kazakh a place in the wider family of the tribe.",
     ["Children are taught to recite the names of their father, grandfather and further ancestors, one generation at a time.",
      "When two Kazakhs meet, it is common to ask which clan (<em>ру</em>) each belongs to; people often find that they are related.",
      "Families keep a <em>шежіре</em> (she-zhi-re), a genealogy tree of the clan, and pass it down.",
      "Clans belong to one of three historical groupings, the <em>жүз</em> (zhuz): the Senior, Middle and Junior Zhuz.",
      "Because of the seven-generation rule, people marry outside their own paternal line.",
      "A well-known saying: <em>Жеті атасын білмеген &mdash; жетесіз</em>, roughly &ldquo;a person who does not know their seven ancestors lacks proper upbringing&rdquo;."]),
    ("hospitality", "Hospitality", "Hospitality (қонақжайлылық)", "қонақжайлылық &middot; qo-naq-zhai-ly-lyq &middot; hospitality &nbsp;|&nbsp; дастархан &middot; das-tar-khan &middot; the cloth spread with food for guests, and by extension the meal itself",
     "A guest (<em>қонақ</em>, qo-naq) is treated with great honour in Kazakh culture, and welcoming one is a duty and a pleasure. "
     "The host sets out the <em>дастархан</em> (das-tar-khan), the cloth spread on the floor or table and covered with tea, bread, sweets and as much food as the home can offer; the word also means the meal itself. "
     "A common saying is <em>Қонақ келсе &mdash; құт келеді</em>, &ldquo;when a guest comes, good fortune comes&rdquo;.",
     ["Tea (<em>шай</em>) comes first and is poured only half-way into the small bowl (<em>кесе</em>, ke-se) so that it stays hot; the host keeps refilling it as a sign of care.",
      "The most honoured guest is seated at the <em>төр</em> (tör), the place of honour farthest from the door.",
      "At a feast the host serves <em>бешбармақ</em> (besh-bar-maq), meat with boiled noodles, and the honoured guest is offered the sheep&rsquo;s head and shares out the portions.",
      "Shoes are taken off at the door of a home.",
      "Visitors usually bring a small gift, often sweets or something for the children, and are expected to taste what is offered.",
      "Leaving without eating anything is considered impolite; the host is likely to insist that you stay a little longer."]),
    ("nauryz", "Nauryz", "Nauryz (Наурыз)", "Наурыз &middot; nau-ryz &middot; the spring new year",
     "Nauryz is the traditional new year, celebrated on the spring equinox, 21 to 23 March, and it is a public holiday in Kazakhstan. "
     "It marks the end of winter and the renewal of nature, and people use it to forgive, settle disputes and begin again. "
     "It is one of the largest celebrations of the year, with food, music, games and visits to relatives and neighbours.",
     ["Families tidy the house, pay back debts and make peace with anyone they have quarrelled with before the new year begins.",
      "<em>Наурыз көже</em> (nau-ryz kö-zhe), a soup traditionally made with seven ingredients, is shared with everyone who visits.",
      "Towns set up yurts in public squares where visitors are given tea, food and sweets.",
      "Traditional games and sports are played, such as <em>көкпар</em> (kök-par), horseback riding with a goat carcass, and <em>қыз қуу</em> (qyz quu), a mounted chase between a young man and a young woman.",
      "The greeting is <em>Наурыз құтты болсын!</em> (nau-ryz qut-ty bol-syn), &ldquo;may Nauryz be blessed!&rdquo;"]),
    ("dombra", "Dombra &amp; Aitys", "The dombra (домбыра) and aitys (айтыс)", "домбыра &middot; dom-by-ra &middot; two-string lute &nbsp;|&nbsp; айтыс &middot; ai-tys &middot; poetic duel",
     "The dombra is the two-stringed lute at the centre of Kazakh music, and it accompanies songs, epics and storytelling. "
     "Aitys is a contest in which two <em>ақын</em> (a-qyn), improvising poets, sing verses against each other with wit and sharp humour, often on the spot. "
     "Both are central to the Kazakh oral tradition, which kept history and poetry alive long before they were written down.",
     ["At festivals and on television, an aitys pits two akyns against each other; the audience cheers the best answers.",
      "<em>Күй</em> (küi) are instrumental pieces for the dombra that tell a story or describe an event, a feeling or an animal; Kurmangazy, a 19th-century composer, is one of the most famous writers of küi.",
      "<em>Жырау</em> (zhy-rau) were singers of epic poems who performed history and advice for khans and the people.",
      "Many Kazakh families keep a dombra at home, and children often learn to play it.",
      "National Dombra Day is celebrated on the first Sunday of July.",
      "UNESCO has recognised the aitys tradition as part of humanity&rsquo;s intangible cultural heritage."]),
]

TOPICS += [
    ("namys", "Namys", "Namys (намыс)", "намыс &middot; na-mys &middot; honour, self-respect, pride",
     "Namys is a person&rsquo;s sense of honour and pride, including the good name of their family and their people. "
     "Uyat is about avoiding shameful acts, while namys is about not letting your dignity be trampled, keeping your word and standing up when you are wronged. "
     "The two ideas are often named together as <em>ар-намыс</em> (ar-na-mys), &ldquo;honour and conscience&rdquo;.",
     ["The <em>батыр</em> (ba-tyr), a heroic warrior in the epics and in history, is the model of namys; Kabanbai, Bogenbai and Raiymbek are batyrs from the fight against the Dzungars in the 1700s.",
      "A family&rsquo;s namys depends on how it treats guests, so a host who sends a visitor away hungry is thought to have lost honour.",
      "Parents tell children to behave so that they do not bring shame on the family name.",
      "<em>Намыстану</em> (na-mys-ta-nu) means to feel your honour hurt, or to be stung by a challenge into doing better.",
      "Namys appears at sport too: <em>қазақша күрес</em> (qa-zaq-sha kü-res), Kazakh wrestling, is a traditional contest at celebrations that is won on skill and pride."]),
    ("elders", "Elders &amp; Titles", "Elders and how to address people", "аға &middot; a-gha &middot; older brother &nbsp;|&nbsp; апа &middot; a-pa &middot; older sister",
     "Age decides the order of respect in Kazakh society: elders speak first, are served first and are addressed with kinship words, not just names. "
     "Even strangers are called <em>аға</em> (older brother) or <em>апа</em> (older sister) when they are a little older, and much older people are called <em>ата</em> (grandfather) or <em>әже</em> (grandmother). "
     "A saying sums it up: <em>Үлкенге &mdash; құрмет, кішіге &mdash; ізет</em>, &ldquo;respect for the elder, courtesy for the younger&rdquo;.",
     ["The <em>ақсақал</em> (aq-saq-al), literally &ldquo;white beard&rdquo;, is a respected elder whose word counts in a family or village.",
      "Younger people greet older people first, and wait for them to sit or begin eating.",
      "Use the formal <em>сіз</em> (siz), &ldquo;you&rdquo;, with elders, strangers and people you want to show respect to, and the informal <em>сен</em> (sen) with friends and children.",
      "<em>Ағай</em> (a-ghai) and <em>апай</em> (a-pai) are polite ways to address a man or woman such as a teacher, a shopkeeper or a neighbour.",
      "On public transport and in a home, younger people give up the best seat to an older person."]),
    ("family", "Family &amp; Weddings", "Family ties and weddings", "құда &middot; qu-da &middot; in-laws &nbsp;|&nbsp; нағашы &middot; na-gha-shy &middot; mother&rsquo;s relatives",
     "Kazakh families are wide webs of relatives with names for each role, and a marriage joins two whole families, not just two people. "
     "The two sets of parents become <em>құда</em> (qu-da), in-laws, and a person&rsquo;s mother&rsquo;s relatives, the <em>нағашы</em> (na-gha-shy), hold a warm and special place. "
     "Weddings are large celebrations, and they keep several old customs alongside modern ones.",
     ["<em>Құда түсу</em> (qu-da tü-su): the groom&rsquo;s family visits the bride&rsquo;s family to ask formally for the marriage, usually with gifts.",
      "<em>Қыз ұзату</em> (qyz u-za-tu): a farewell party at the bride&rsquo;s parents&rsquo; home before she moves to her husband&rsquo;s family.",
      "<em>Беташар</em> (be-ta-shar): a ritual at traditional weddings in which the new bride, the <em>келін</em> (ke-lin), is introduced to the groom&rsquo;s relatives while a singer gives her advice in verse.",
      "<em>Жиен</em> (zhi-yen), a person&rsquo;s sister&rsquo;s child, is treated with special affection by the mother&rsquo;s brothers, and the two sides tease each other in a friendly way.",
      "Because of the zheti ata rule, the couple must not be related through the male line for seven generations."]),
    ("milestones", "Life Milestones", "Life milestones: birth to remembrance", "бесік той &middot; be-sik toi &middot; cradle celebration",
     "Kazakh families mark each stage of life with a gathering of relatives and neighbours, from the birth of a baby to the memory of someone who has died. "
     "These events are shared by the whole extended family, and being present at them matters more than a gift. "
     "Many follow Islamic custom combined with older traditions.",
     ["<em>Бесік той</em> (be-sik toi): a celebration when the baby is first laid in the cradle, the <em>бесік</em> (be-sik).",
      "<em>Ат қою</em> (at qo-yu): the naming, when an elder or imam says the baby&rsquo;s name softly in its ear.",
      "<em>Тұсау кесу</em> (tu-sau ke-su), &ldquo;cutting the fetters&rdquo;: when a child starts to walk, a rope is loosely tied around their feet and cut by a respected person to wish them a firm path.",
      "<em>Көңіл айту</em> (kö-ñil ai-tu), giving condolences: relatives and neighbours visit a bereaved family at once to offer comfort.",
      "Burial follows Islamic custom, soon after death, and the family holds memorial prayers and a meal, an <em>ас</em> (as), on the 7th day (<em>жетісі</em>, zhe-ti-si), the 40th day (<em>қырқы</em>, qyr-qy) and after a year."]),
    ("gifts", "Gifts", "Gifts and sharing", "сыбаға &middot; sy-ba-gha &middot; a share of food &nbsp;|&nbsp; шапан &middot; sha-pan &middot; long robe",
     "Gifts and shared food show respect and belonging in Kazakh culture, and who gives what to whom follows long-standing habits. "
     "A guest of honour may be given a <em>шапан</em> (sha-pan), a long traditional robe worn over the shoulders, and a family member who could not come to a feast is sent their <em>сыбаға</em> (sy-ba-gha), their share. "
     "The idea is that no one is left out of what the family has.",
     ["<em>Шапан жабу</em> (sha-pan zha-bu): to drape a chapan over the shoulders of an honoured guest or the newly married couple.",
      "<em>Сыбаға</em>: the best portion of the meat at a feast is set aside for the most honoured person, and relatives who are absent are sent theirs.",
      "<em>Шашу</em> (sha-shu): sweets and coins showered over the bride, the groom or the guests at a celebration to wish them good fortune and sweetness.",
      "<em>Тарту</em> (tar-tu): a formal present given to an honoured person, offered and received politely, usually with the right hand or both hands.",
      "Visitors bring something for the table or for the children, and the host will not let them leave empty-handed."]),
    ("nomads", "Nomad Heritage", "Nomad heritage: yurt, pasture and horse", "киіз үй &middot; ki-iz üi &middot; yurt (felt house) &nbsp;|&nbsp; жайлау &middot; zhai-lau &middot; summer pasture",
     "For centuries Kazakhs were nomadic herders who moved with their horses, sheep and camels between seasonal pastures, and that way of life still shapes many of their customs. "
     "The yurt, the horse and the seasons are at the centre of the old culture. "
     "Hospitality, respect for elders and the oral poetry on this page all grew out of it.",
     ["The <em>киіз үй</em> (ki-iz üi), the yurt, is a round tent of felt over a wooden frame that can be taken down and carried to the next pasture.",
      "The <em>шаңырақ</em> (sha-ñy-raq) is the round wooden crown at the top of the yurt, a symbol of the family and home; it is shown on the national emblem, and a common blessing is <em>Шаңырағың биік болсын</em>, &ldquo;may your shanyrak be high&rdquo;.",
      "<em>Жайлау</em> (zhai-lau) is the high summer pasture, and <em>қыстау</em> (qys-tau) the sheltered winter quarters; many families still go to the zhailau in summer.",
      "The horse is the most respected animal; horse races, <em>бәйге</em> (bäi-ge), are held at festivals, and mare&rsquo;s milk is made into kymyz.",
      "Hunting with trained golden eagles by <em>бүркітші</em> (bür-kit-shi), eagle hunters, is a living tradition."]),
    ("proverbs", "Proverbs &amp; Tales", "Proverbs and folktales", "мақал-мәтел &middot; ma-qal ma-tel &middot; proverbs and sayings",
     "Kazakhs use proverbs, <em>мақал-мәтел</em> (ma-qal ma-tel), all the time, and a well-chosen saying is a polite way to give advice or correct someone without criticising them directly. "
     "Folktales and legends are the other half of the oral tradition, and they teach the same values with humour. "
     "Learning a few of each helps you follow conversations and understand jokes.",
     ["<em>Жеті рет өлшеп, бір рет кес</em> (zhe-ti ret öl-shep, bir ret kes): &ldquo;measure seven times, cut once&rdquo;, which means to think before you act.",
      "<em>Сабыр түбі &mdash; сары алтын</em> (sa-byr tü-bi sa-ry al-tyn): &ldquo;patience in the end is yellow gold&rdquo;.",
      "<em>Бірлік бар жерде &mdash; тірлік бар</em> (bir-lik bar zher-de tir-lik bar): &ldquo;where there is unity, there is life&rdquo;.",
      "<em>Алдар Көсе</em> (al-dar kö-se) is the clever trickster of Kazakh tales who outwits greedy rich men and rulers.",
      "<em>Қожанасыр</em> (qo-zha-na-syr), or Khoja Nasreddin, is a wise fool in jokes told across Central Asia and the Middle East.",
      "<em>Қорқыт ата</em> (qor-qyt a-ta) is a legendary sage and musician, said to have invented the <em>қобыз</em> (qo-byz), a bowed string instrument."]),
]
ORDER = ["uyat", "namys", "elders", "zheti-ata", "family", "milestones", "hospitality", "gifts", "nauryz", "nomads", "dombra", "proverbs"]
TOPICS.sort(key=lambda t: ORDER.index(t[0]))

pills = "".join(f"<button type=\"button\" data-topic=\"{i}\" aria-pressed=\"false\">{p}</button>" for i, p, *_ in TOPICS)
def section(i, pill, title, terms, definition, examples):
    li = "".join(f"<li>{e}</li>" for e in examples)
    return (f"        <section class=\"lesson-section culture-topic\" id=\"{i}\" hidden><h2>{title}</h2>"
            f"<p class=\"culture-terms\">{terms}</p><p class=\"culture-def\">{definition}</p>"
            f"<h3 class=\"culture-eg-title\">Examples</h3><ul class=\"culture-eg\">{li}</ul></section>\n")
body = "".join(section(*t) for t in TOPICS)
for _, _, _, _, definition, _ in TOPICS:   # the definition is meant to stay short
    assert definition.count(". ") <= 2 and definition.endswith("."), definition[:40]   # at most three sentences

DESC = "Kazakh culture explained simply: uyat, namys, respect for elders, zheti ata, weddings, hospitality, gifts, Nauryz, nomad heritage, the dombra and aitys, and proverbs."
TITLE = "Kazakh Culture Explained: Uyat, Namys, Hospitality, Nauryz and More"
URL = "https://albazzaztariq.github.io/kazakh-language/culture.html"
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <link rel="stylesheet" href="styles.css?v=20">
<!-- seo -->
    <meta name="description" content="{DESC}">
    <link rel="canonical" href="{URL}">
    <meta name="theme-color" content="#00AFCA">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{TITLE}">
    <meta property="og:description" content="{DESC}">
    <meta property="og:url" content="{URL}">
    <meta name="twitter:card" content="summary">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>

        <header>
            <h1 class="section-title">Culture</h1>
            <p class="section-subtitle">Ideas that shape everyday life in Kazakhstan. Knowing them helps you understand what Kazakhs say and why.</p>
        </header>

        <div class="divider"></div>

        <nav class="jump-links culture-nav" id="cultureNav" aria-label="Choose a topic">{pills}</nav>

{body}
        <footer>
            <p>Qazaq tilin &uuml;yren&iuml;ңіз &mdash; Learn the Kazakh language</p>
        </footer>
    </div>
    <a href="index.html" class="float-top float-home show" aria-label="Back to the home page">Home</a>
    <script>
        const nav = document.getElementById('cultureNav');
        const buttons = [...nav.querySelectorAll('button')], sections = [...document.querySelectorAll('.culture-topic')];
        // Show only the chosen topic; the buttons stay frozen at the top while its text scrolls.
        function showTopic(id, scroll) {{
            sections.forEach(s => {{ s.hidden = s.id !== id; }});
            buttons.forEach(b => b.setAttribute('aria-pressed', b.dataset.topic === id ? 'true' : 'false'));
            if (scroll) {{
                const sec = document.getElementById(id);
                window.scrollTo(0, Math.max(0, sec.getBoundingClientRect().top + window.scrollY - nav.offsetHeight - 12));
            }}
            try {{ history.replaceState(null, '', '#' + id); }} catch (e) {{}}
        }}
        buttons.forEach(b => b.addEventListener('click', () => showTopic(b.dataset.topic, true)));
        const fromLink = location.hash.slice(1);
        if (sections.some(s => s.id === fromLink)) showTopic(fromLink, false);
    </script>
</body>
</html>
"""
open(W + "culture.html", "w", encoding="utf-8").write(page)
print(f"[DEBUG] wrote culture.html, {len(page)} bytes, {len(TOPICS)} topics", flush=True)
