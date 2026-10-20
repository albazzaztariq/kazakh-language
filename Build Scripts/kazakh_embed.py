"""Replace the speechSynthesis script in alphabet.html with embedded-MP3 playback.
Input: Kazakh Audio/audio.js (AUDIO map letter -> base64 MP3). Output: alphabet.html rewritten."""
import re
print("[DEBUG] embed start", flush=True)
HTML = "C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/alphabet.html"
audio_js = open("C:/Users/azt12/OneDrive/Documents/Computing/All Projects/Kazakh Language/Web Version/Alphabet/Letters Audio/audio.js", encoding="utf-8").read()
html = open(HTML, encoding="utf-8").read()
player = """
        // Audio is embedded in the page (MP3, base64) so it works offline and without any browser TTS voice.
        let current = null;
        document.querySelectorAll('button.letter-card').forEach(btn => {
            btn.addEventListener('click', function () {
                const data = AUDIO[this.getAttribute('data-sound')];
                if (!data) return;
                if (current) { current.pause(); }
                document.querySelectorAll('button.letter-card.playing').forEach(b => b.classList.remove('playing'));
                const a = new Audio('data:audio/mpeg;base64,' + data);
                current = a;
                this.classList.add('playing');
                const done = () => this.classList.remove('playing');
                a.onended = done;
                a.onerror = done;
                a.play().catch(done);
            });
        });
"""
new = "<script>\n        " + audio_js + "\n" + player + "    </script>"
html2, n = re.subn(r"<script>.*?</script>", lambda m: new, html, flags=re.S)
print(f"[DEBUG] replaced {n} script block(s)", flush=True)
open(HTML, "w", encoding="utf-8").write(html2)
print(f"[DEBUG] wrote {len(html2)} bytes", flush=True)
