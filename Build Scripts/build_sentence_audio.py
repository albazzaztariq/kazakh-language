"""Make the Kazakh audio clip of every sentence in the Sentence Constructor (sentence-game.html).
Inputs : the SENTS list inside sentence-game.html (each sentence has its Kazakh text "kt" and a clip name "a").
Method : the same recipe as the word clips: male voice kk-KZ-DauletNeural, rate -10%, silence trimmed from both ends, peak normalised to 0.4, mono MP3.
         Eight requests run at once; a clip that already exists is skipped, so the script can be stopped and run again. A failed request is retried 3 times.
Output : Sentence Audio/<a>.mp3 (one file per sentence). Prints progress every 25 clips and a final count of missing files.
"""
import os, re, json, asyncio, sys, time
print("[DEBUG] sentence audio start", flush=True)
import av, numpy as np, edge_tts
W = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/"
OUT = W + "Sentence Audio/"
os.makedirs(OUT, exist_ok=True)
page = open(W + "sentence-game.html", encoding="utf-8").read()
SENTS = json.loads(page.split("const SENTS = ")[1].split(";\n")[0])
todo = [(s["a"], s["kt"]) for s in SENTS if not os.path.exists(OUT + s["a"] + ".mp3")]
print(f"[DEBUG] {len(SENTS)} sentences, {len(todo)} clips to make", flush=True)

def trim(path):
    """Cut leading/trailing silence and normalise the peak to 0.4 (same as the word clips)."""
    c = av.open(path); r = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close()
    idx = np.where(abs(x) > 0.02 * abs(x).max())[0]; pad = int(0.05 * r)
    y = x[max(0, idx[0] - pad):min(len(x), idx[-1] + pad)]; y = y * (0.4 / abs(y).max())
    out = av.open(path, "w", format="mp3"); st = out.add_stream("mp3", rate=r); st.layout = "mono"
    fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = r
    for p in st.encode(fr): out.mux(p)
    for p in st.encode(None): out.mux(p)
    out.close()

done = 0
async def one(sem, name, text):
    global done
    async with sem:
        for attempt in range(3):
            try:
                tmp = OUT + name + ".part.mp3"
                await asyncio.wait_for(edge_tts.Communicate(text, "kk-KZ-DauletNeural", rate="-10%").save(tmp), timeout=60)
                trim(tmp); os.replace(tmp, OUT + name + ".mp3"); break
            except Exception as e:
                print(f"[DEBUG] retry {attempt + 1} for {text!r}: {e}", flush=True); await asyncio.sleep(2)
        done += 1
        if done % 25 == 0: print(f"[DEBUG] {done}/{len(todo)} done, {time.strftime('%H:%M:%S')}", flush=True)

async def main():
    sem = asyncio.Semaphore(8)
    await asyncio.gather(*(one(sem, n, t) for n, t in todo))
t0 = time.time(); asyncio.run(main())
missing = [s["kt"] for s in SENTS if not os.path.exists(OUT + s["a"] + ".mp3")]
print(f"[DEBUG] finished in {time.time() - t0:.0f}s; missing {len(missing)}", flush=True)
