"""Regenerate all 42 letter clips with the male voice kk-KZ-DauletNeural, trim silence, peak-normalise to 0.4.
Spoken form: consonants use their Kazakh letter name (бе, ве, ...) because a bare consonant is mispronounced by TTS;
vowels and ъ/ь use the bare letter. Output: Kazakh Audio/*.mp3 (overwritten) and Kazakh Audio/audio.js."""
import asyncio, av, numpy as np, edge_tts, re, os, base64, json
print("[DEBUG] all-male start", flush=True)
D = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Alphabet/Letters Audio"
HTML = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/alphabet.html"
VOICE = "kk-KZ-DauletNeural"
SPOKEN = {"б":"бе","в":"ве","г":"ге","ғ":"ға","д":"де","ж":"же","з":"зе","й":"ий","к":"ка","қ":"қа","л":"эл","м":"эм","н":"эн","ң":"ың","п":"пе","р":"эр","с":"эс","т":"те","ф":"эф","х":"ха","һ":"һа","ц":"цэ","ч":"че","ш":"ше","щ":"ща"}
letters = re.findall(r'data-sound="(.)"', open(HTML, encoding="utf-8").read())
audio = {}
for ch in letters:
    f = f"{D}/{ord(ch):04x}.mp3"
    asyncio.run(edge_tts.Communicate(SPOKEN.get(ch, ch), VOICE, rate="-20%").save(f))
    c = av.open(f); rate = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.04 * rate)
    y = x[max(0, idx[0]-pad):min(len(x), idx[-1]+pad)]
    y = y * (0.4 / abs(y).max())
    print(f"[DEBUG] {ch} {len(x)/rate:.2f}s -> {len(y)/rate:.2f}s", flush=True)
    out = av.open(f, "w", format="mp3"); s = out.add_stream("mp3", rate=rate); s.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = rate
    for p in s.encode(fr): out.mux(p)
    for p in s.encode(None): out.mux(p)
    out.close()
    audio[ch] = base64.b64encode(open(f, "rb").read()).decode()
open(f"{D}/audio.js", "w", encoding="utf-8").write("const AUDIO = " + json.dumps(audio, ensure_ascii=False) + ";")
print("[DEBUG] wrote audio.js", flush=True)
