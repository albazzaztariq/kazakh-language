"""Build ъ (044a) as 'uh-oh': clip а (0430) + 110 ms silence + clip о (043e), both already trimmed/normalised."""
import av, numpy as np, glob, os, base64, json
print("[DEBUG] uh-oh start", flush=True)
D = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Alphabet/Letters Audio"
def load(n):
    c = av.open(f"{D}/{n}.mp3"); r = c.streams.audio[0].rate
    x = np.concatenate([fr.to_ndarray() for fr in c.decode(audio=0)], axis=1)[0].astype(np.float32); c.close(); return x, r
a, r = load("0430"); o, _ = load("043e")
y = np.concatenate([a, np.zeros(int(0.11 * r), np.float32), o]); y *= 0.4 / abs(y).max()
print(f"[DEBUG] uh-oh {len(y)/r:.2f}s", flush=True)
f = f"{D}/044a.mp3"
out = av.open(f, "w", format="mp3"); s = out.add_stream("mp3", rate=r); s.layout = "mono"
fr = av.AudioFrame.from_ndarray(y.reshape(1, -1), format="flt", layout="mono"); fr.sample_rate = r
for p in s.encode(fr): out.mux(p)
for p in s.encode(None): out.mux(p)
out.close()
d = {chr(int(os.path.basename(g)[:4], 16)): base64.b64encode(open(g, "rb").read()).decode() for g in glob.glob(f"{D}/*.mp3")}
open(f"{D}/audio.js", "w", encoding="utf-8").write("const AUDIO = " + json.dumps(d, ensure_ascii=False) + ";")
