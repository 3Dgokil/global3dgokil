import os
import json
import time
import random
import requests
import streamlit as st

st.set_page_config(page_title="Shorts Subscriber Studio", page_icon="🔥", layout="wide")
st.title("🔥 Shorts Subscriber Studio")
st.caption("ANIMASI 3D SINEMATIK (ALL AGES) | HOOK DISRUPTIF → PUNCHLINE → CTA DINAMIS → SEAMLESS LOOP")

LANGUAGES = [
    "Bahasa Indonesia", "English", "Español (Spanish)", "Português (Portuguese)",
    "Français (French)", "Deutsch (German)", "Italiano (Italian)", "日本語 (Japanese)",
    "한국어 (Korean)", "中文简体 (Chinese Simplified)", "中文繁體 (Chinese Traditional)",
    "العربية (Arabic)", "हिन्दी (Hindi)", "বাংলা (Bengali)", "اردو (Urdu)",
    "Русский (Russian)", "Türkçe (Turkish)", "ไทย (Thai)", "Tiếng Việt (Vietnamese)",
    "Filipino", "Bahasa Melayu (Malay)", "Nederlands (Dutch)", "Polski (Polish)",
    "Українська (Ukrainian)", "فارسی (Persian)", "עברית (Hebrew)", "Kiswahili (Swahili)",
    "Bahasa lain (isi sendiri)"
]

def api_key():
    try:
        if st.secrets.get("GEMINI_API_KEY"):
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")

def call_gemini(key, model, prompt):
    # Urutan model fallback otomatis jika server sedang sibuk (503/429)
    candidate_models = [model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    fallback_models = list(dict.fromkeys(candidate_models))
    
    last_error = ""
    for target_model in fallback_models:
        for attempt in range(2):
            try:
                r = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent",
                    headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 1.0,
                            "responseMimeType": "application/json"
                        }
                    },
                    timeout=90
                )
                
                if r.ok:
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(txt)
                
                # Tangani server kelebihan beban (503) atau batas kuota sesaat (429)
                if r.status_code in [503, 429]:
                    time.sleep(2)
                    continue
                else:
                    msg = r.json().get("error", {}).get("message", r.text)
                    last_error = f"{r.status_code}: {msg}"
                    break
            except Exception as e:
                last_error = str(e)
                time.sleep(1)
                
    raise RuntimeError(f"Server Gemini sedang sibuk. Detail: {last_error}")

def prompts(x, duration, language):
    dialogue_text = "\n".join(
        f'{d.get("time","")} {d.get("speaker","")}: "{d.get("line","")}"' 
        for d in x.get("dialogue", [])
    )
    
    x["flow_prompt"] = f"""Create a {duration} vertical 9:16 high-end 3D cinematic animation (Pixar/Illumination style), suitable for all ages.
VISUAL TONE: Vibrant studio lighting, expressive facial physics, warm cinematic colors, energetic pacing, sharp 4K render quality.

HOOK (0–2s): {x.get('hook','')}
STORY: {x.get('story','')}
DIALOGUE & ACTIONS:
{dialogue_text}
PUNCHLINE: {x.get('punchline','')}
ENDING & SEAMLESS LOOP: {x.get('loop_transition', x.get('ending',''))}

SEAMLESS INFINITY LOOP DIRECTING RULES:
- Start INSTANTLY in media res with extreme facial expression or fast physical comedic action in 0–2s. No establishing shots.
- Spoken dialogue strictly in {language} with matching clean lip-sync.
- Final subscribe CTA must feel like a witty extension of the joke, delivered organically by the character.
- PERFECT SEAMLESS LOOP: The very final 1-2 seconds MUST physically reset or launch the character back to the EXACT opening pose/frame ({x.get('hook','')}), creating an endless, flawless loop with zero abrupt cuts.
- Aspect ratio 9:16 vertical framed. No text overlays, no subtitles, no watermarks, no gore."""

    x["thumbnail_prompt"] = f"""3D cinematic animation YouTube Shorts thumbnail, 9:16 vertical, Pixar/DreamWorks render quality, all ages comedy. 
Main Scene: {x.get('hook','')}. 
Characters: Over-the-top funny shocked expressions, extreme perspective towards camera, vibrant rim lighting, high-contrast colorful background. 
Focus: Strong comedic tension and curiosity gap. Clean negative space at top and bottom. No watermark, no text artifacts."""
    
    x.setdefault("hashtags", "#Shorts #AnimasiLucu #Animation #ComedyShorts")
    return x

def local_idea(language):
    pool = [
        {
            "title": "ROBOT KOK GAGAL UJIAN?! 🤖💥",
            "hook": "Robot bulat imut tersengat listrik kecil dan mendarat tegak di depan lensa kamera!",
            "story": "Sebuah robot canggih mencoba membuktikan ia lebih pintar dari manusia, tapi selalu salah menjawab hal sepele.",
            "dialogue": [
                {"time": "0–2 detik", "speaker": "ROBOT", "line": "Aku tahu segalanya di alam semesta!"},
                {"time": "2–5 detik", "speaker": "ANAK", "line": "Berapa satu tambah satu?"},
                {"time": "5–7 detik", "speaker": "ROBOT", "line": "Sistem eror! Jawabannya adalah semangka!"},
                {"time": "7–9 detik", "speaker": "ROBOT", "line": "Biar memoriku gak korslet lagi, pencet subscribe sekarang!"},
                {"time": "9–10 detik", "speaker": "ROBOT", "line": "Waduh, korslet lagi, awas!"}
            ],
            "punchline": "Layar di perut robot meledak confetti lalu tubuhnya memantul ke belakang.",
            "ending": "Robot memantul dan kembali mendarat tepat ke posisi awal di depan kamera.",
            "loop_transition": "Ledakan confetti kecil mendorong robot memantul dan mendarat tegak kembali ke posisi detik 0, menyambung langsung ke dialog pembuka tanpa jeda.",
            "hashtags": "#Shorts #AnimasiLucu #Robot #Animation",
            "cta_note": "CTA dihubungkan dengan eror sistem robot dan ditutup transisi memantul ke posisi awal."
        },
        {
            "title": "KUCING OYEN JADI DETEKTIF 🐱🔍",
            "hook": "Kucing oyen berdasi tergelincir karpet lalu mendarat dengan gaya sok keren tepat menghadap kamera!",
            "story": "Detektif kucing menyelidiki misteri hilangnya ikan asin, pelakunya ternyata pantulannya di cermin.",
            "dialogue": [
                {"time": "0–2 detik", "speaker": "KUCING", "line": "Pelakunya pasti ada di ruangan ini!"},
                {"time": "2–5 detik", "speaker": "KUCING", "line": "Lihat tampang mencurigakan di cermin itu!"},
                {"time": "5–7 detik", "speaker": "BURUNG", "line": "Bos, itu pantulan kumis bos sendiri!"},
                {"time": "7–9 detik", "speaker": "KUCING", "line": "Tutup kasusnya dengan subscribe, sebelum aku makin malu!"},
                {"time": "9–10 detik", "speaker": "KUCING", "line": "Ups, licin lagi!"}
            ],
            "punchline": "Kucing kaget saat sadar dan melompat panik ke atas.",
            "ending": "Kucing jatuh meluncur kembali ke posisi awal di depan kamera.",
            "loop_transition": "Kucing terpeleset karpet yang sama dan meluncur tepat kembali ke pose gaya detektif di detik 0 secara seamless.",
            "hashtags": "#Shorts #KucingOyen #Animasi3D #Komedi",
            "cta_note": "CTA dibuat dari rasa malu sang detektif dan diakhiri loop terpeleset kembali ke awal."
        }
    ]
    return random.choice(pool)

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    key = api_key()
    st.write("Gemini API:", "✅ Terhubung" if key else "⚠️ Belum diatur")
    model = st.text_input("Model Gemini", "gemini-2.5-flash")
    st.caption("Rekomendasi: `gemini-2.5-flash` atau `gemini-2.0-flash`.")
    
    language_choice = st.selectbox("🌎 Bahasa cerita & dialog", LANGUAGES, index=0)
    if language_choice == "Bahasa lain (isi sendiri)":
        custom_language = st.text_input("Nama bahasa", placeholder="Contoh: Sunda, Javanese, Italian")
        target_language = custom_language.strip() or "Bahasa Indonesia"
    else:
        target_language = language_choice
        
    duration = st.selectbox("Durasi", ["8 detik", "10 detik", "12 detik", "15 detik"], index=1)
    humor = st.selectbox("Formula Komedi", [
        "Slapstick fisik + salah paham polos",
        "Ekspektasi tinggi vs kenyataan hancur",
        "Karakter sok jenius yang blunder",
        "Plot twist instan tak terduga"
    ])
    character_idea = st.text_input("Karakter utama (opsional)", placeholder="Contoh: Tupai ilmuwan, Robot pemalas, Kucing koki")
    avoid = st.text_input("Hindari topik (opsional)", placeholder="Contoh: jumpscare kaget, topik dewasa")

if "idea" not in st.session_state:
    st.session_state.idea = None

# Tombol Eksekusi
if st.button("🔥 GENERATE IDE BARU", type="primary", use_container_width=True):
    prompt = f"""You are an elite YouTube Shorts animation director specializing in viral 3D animated shorts (family-friendly, all ages, Pixar/Illumination aesthetic).

GOAL: Maximise retention (0–2s hook), subscriber conversions (dynamic CTA), and flawless SEAMLESS INFINITY LOOP.

REQUIREMENTS:
1. TARGET LANGUAGE: Write all content in {target_language}. Keep phrasing natural for native speakers.
2. VISUAL CHARACTERS: 3D animated characters (cute animals, expressive humans, funny robots). Clean and entertaining for all ages.
   Character hint: {character_idea or 'Invent an endearing funny 3D character pair'}.
3. 0–2s DISRUPTIVE HOOK: Start directly in curious or energetic motion facing camera. NO slow intro, NO greetings.
4. PUNCHLINE: Deliver a sharp comedic twist within {duration}. Humor style: {humor}.
5. DYNAMIC CONTEXTUAL CTA: The dialogue line right before the end MUST be a subscribe call-to-action strictly integrated into the story's punchline.
   CRITICAL RULE: DO NOT use repetitive generic templates like "Jangan lupa subscribe". Invent a fresh CTA tied to the character's unique situation.
6. SEAMLESS INFINITY LOOP REQUIREMENT:
   The video MUST NOT cut abruptly at the end. Design the very final action/dialogue line (last 1-2 seconds) so that the character falls, resets, teleports, or lands EXACTLY back into the opening position/camera angle of the 0–2s hook, making the video replay endlessly without a seam.
7. AVOID: {avoid or 'none'}.

Return ONLY a valid JSON object with these keys:
{{
  "title": "Punchy title with emojis",
  "hook": "Visual + audio description of the 0-2s hook",
  "story": "Short premise summary",
  "dialogue": [
    {{"time": "0–2s", "speaker": "NAME", "line": "Opening hook line"}},
    {{"time": "Mid", "speaker": "NAME", "line": "Middle build-up"}},
    {{"time": "CTA", "speaker": "NAME", "line": "Contextual subscribe line"}},
    {{"time": "Ending/Loop", "speaker": "NAME", "line": "Final loop transition reaction line"}}
  ],
  "punchline": "The funny visual payoff",
  "ending": "Final comedic moment",
  "loop_transition": "Exact visual action explaining how the final frame connects flawlessly back to the 0-2s hook frame",
  "hashtags": "#Shorts #Animation ...",
  "cta_note": "Why this specific CTA fits this story"
}}"""

    with st.spinner("Membuat ide animasi 3D, CTA dinamis, & Seamless Loop..."):
        try:
            if key:
                result = call_gemini(key, model, prompt)
            else:
                result = local_idea(target_language)
            st.session_state.idea = prompts(result, duration, target_language)
        except Exception as e:
            st.error(f"Gagal mengambil dari Gemini: {e}")
            st.info("Menggunakan ide cadangan lokal...")
            st.session_state.idea = prompts(local_idea(target_language), duration, target_language)

# Tampilan Hasil
x = st.session_state.idea
if x:
    st.divider()
    st.subheader(x.get("title", "Ide Shorts"))
    st.code(x.get("hashtags", "#Shorts #Animation"))
    
    t1, t2, t3, t4 = st.tabs(["🎬 Cerita, Dialog & Loop", "🎥 Prompt Generator Video", "🖼️ Prompt Thumbnail", "📊 Evaluasi Konversi"])
    
    with t1:
        st.markdown("**⚡ HOOK INSTAN (0–2 Detik)**")
        st.write(x.get("hook", ""))
        
        st.markdown("**📖 SINOPSIS SINGKAT**")
        st.write(x.get("story", ""))
        
        st.markdown("**🗣️ STRUKTUR DIALOG**")
        for d in x.get("dialogue", []):
            st.write(f"**{d.get('time','')} | {d.get('speaker','')}** — {d.get('line','')}")
            
        st.markdown("**💥 PUNCHLINE**")
        st.write(x.get("punchline", ""))
        
        st.markdown("**🔄 MEKANISME SEAMLESS LOOP (Sambungan Tak Terasa)**")
        st.info(x.get("loop_transition", x.get("ending", "")))
        
        st.success(f"**💡 Alasan CTA:** {x.get('cta_note', 'CTA menyatu dengan cerita.')}")

    with t2:
        st.caption("Prompt ini sudah dilengkapi aturan **Seamless Loop** otomatis. Cukup salin ke generator video AI Anda:")
        st.text_area("Prompt Video Animasi 3D (Siap Pakai)", x.get("flow_prompt", ""), height=380)

    with t3:
        st.caption("Gunakan prompt ini di Midjourney / Imagen / DALL-E:")
        st.text_area("Prompt Thumbnail 9:16", x.get("thumbnail_prompt", ""), height=220)

    with t4:
        st.write("Ukur efektivitas CTA dinamis terhadap retensi dan langganan:")
        c1, c2, c3 = st.columns(3)
        views = c1.number_input("Views Shorts", min_value=0, value=0, step=100)
        subs = c2.number_input("Subscriber Masuk", min_value=0, value=0, step=1)
        apvd = c3.number_input("Rata-rata % Ditonton (APVD)", min_value=0.0, max_value=200.0, value=90.0, step=1.0)
        
        if views > 0:
            rate = (subs / views) * 100
            st.metric("Tingkat Konversi Subscriber", f"{rate:.2f}%", f"{subs} subs")
            if rate >= 1.0:
                st.success("Konversi luar biasa! Hook dan CTA bekerja maksimal.")
            elif rate >= 0.3:
                st.info("Performa stabil standar Shorts.")
            else:
                st.warning("Perlu evaluasi: apakah punchline dan CTA cukup memicu tawa penonton?")

    data = {k: x.get(k) for k in ["title", "hashtags", "hook", "story", "dialogue", "punchline", "ending", "loop_transition", "flow_prompt", "thumbnail_prompt"]}
    st.download_button(
        "⬇️ Download Format JSON",
        json.dumps(data, ensure_ascii=False, indent=2),
        "shorts_animation_idea.json",
        "application/json"
    )
