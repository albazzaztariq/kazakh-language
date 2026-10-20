"""ъ (044a) -> 'а-а' (vowel, break, vowel = how the hard sign is pronounced); ь (044c) -> 'й' glide as in 'ий' (soft-sign y-glide).
Male voice kk-KZ-DauletNeural, trimmed, peak 0.4. Rewrites those MP3s only, then audio.js."""
import asyncio, av, numpy as np, edge_tts, glob, os, base64, json
print("[DEBUG] signs fix start", flush=True)
D = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Alphabet/Letters Audio"
for n, text in (("044a", "а-а"), ("044c", "ий")):
    f = f"{D}/{n}.mp3"
    asyncio.run(edge_tts.Communicate(text, "kk-KZ-DauletNeural", rate="-20%").save(f))
    c = av.open(f); rate = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.04 * rate)
    y = x[max(0, idx[0]-pad):min(len(x), idx[-1]+pad)]; y = y * (0.4 / abs(y).max())
    print(f"[DEBUG] {n} {text} {len(x)/rate:.2f}s -> {len(y)/rate:.2f}s", flush=True)
    out = av.open(f, "w", format="mp3"); s = out.add_stream("mp3", rate=rate); s.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = rate
    for p in s.encode(fr): out.mux(p)
    for p in s.encode(None): out.mux(p)
    out.close()
a = {chr(int(os.path.basename(f)[:4], 16)): base64.b64encode(open(f, "rb").read()).decode() for f in glob.glob(f"{D}/*.mp3")}
open(f"{D}/audio.js", "w", encoding="utf-8").write("const AUDIO = " + json.dumps(a, ensure_ascii=False) + ";")
