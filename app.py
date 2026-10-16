import os
import json
import random
import requests
import streamlit as st

st.set_page_config(page_title="Shorts Subscriber Studio", page_icon="🔥", layout="wide")
st.title("🔥 Shorts Subscriber Studio")
st.caption("ANIMASI 3D SINEMATIK (ALL AGES) | HOOK DISRUPTIF → PUNCHLINE → CTA DINAMIS")

LANGUAGES = [
    "Bahasa Indonesia", "English", "Español (Spanish)", "Português (Portuguese)",
    "Français (French)", "Deutsch (German)", "Italiano (Italian)", "日本語 (Japanese)",
    "한국어 (Korean)", "中文简体 (Chinese Simplified)", "中文繁體 (Chinese Traditional)",
    "العربية (Arabic)", "हिन्दी (Hindi)", "বাংলা (Bengali)", "اردو (Urdu)",
    "Русский (Russian)", "Türkçe (Turkish)", "ไทย (Thai)", "Tiếng Việt (Vietnamese)",
    "Filipino", "Bahasa Melayu (Malay)", "Nederlands (Dutch)", "Polski (Polish)",
    "Українська (Ukrainian)", "فارسی (Persian)", "עבריत (Hebrew)", "Kiswahili (Swahili)",
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
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
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
    if not r.ok:
        try:
            msg = r.json().get("error", {}).get("message", r.text)
        except Exception:
            msg = r.text
        raise RuntimeError(f"Gemini API {r.status_code}: {msg}")
    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(txt)

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
ENDING: {x.get('ending','')}

DIRECTING RULES:
- Start INSTANTLY in media res with extreme facial expression or fast physical comedic action in 0–2s. No establishing shots.
- Spoken dialogue strictly in {language} with matching clean lip-sync.
- Final subscribe CTA must feel like a witty extension of the joke, delivered organically by the character.
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
            "hook": "Robot bulat imut meledak mengeluarkan kue gosong tepat ke arah kamera!",
            "story": "Sebuah robot canggih mencoba membuktikan ia lebih pintar dari manusia, tapi selalu salah menjawab hal sepele.",
            "dialogue": [
                {"time": "0–2 detik", "speaker": "ROBOT", "line": "Aku tahu segalanya di alam semesta!"},
                {"time": "2–5 detik", "speaker": "ANAK", "line": "Berapa satu tambah satu?"},
                {"time": "5–8 detik", "speaker": "ROBOT", "line": "Sistem eror! Jawabannya adalah semangka!"},
                {"time": "8–10 detik", "speaker": "ROBOT", "line": "Biar memoriku gak korslet lagi, pencet subscribe sekarang!"}
            ],
            "punchline": "Layar di perut robot berubah jadi emotikon menangis lalu mengeluarkan kertas kuitansi.",
            "ending": "Robot berkedip bingung sambil memegang baterai cadangan.",
            "hashtags": "#Shorts #AnimasiLucu #Robot #Animation",
            "cta_note": "CTA dihubungkan dengan eror sistem robot."
        },
        {
            "title": "KUCING OYEN JADI DETEKTIF 🐱🔍",
            "hook": "Kucing oyen berbaju jas detektif tergelincir kulit pisang dan menabrak lensa kamera!",
            "story": "Detektif kucing menyelidiki misteri hilangnya ikan asin, pelakunya ternyata pantulannya di cermin.",
            "dialogue": [
                {"time": "0–2 detik", "speaker": "KUCING", "line": "Pelakunya ada di ruangan ini!"},
                {"time": "2–5 detik", "speaker": "KUCING", "line": "Lihat tampang mencurigakan di cermin itu!"},
                {"time": "5–8 detik", "speaker": "BURUNG", "line": "Bos, itu pantulan kumis bos sendiri!"},
                {"time": "8–10 detik", "speaker": "KUCING", "line": "Tutup kasusnya dengan subscribe, sebelum aku makin malu!"}
            ],
            "punchline": "Kucing memakai kacamata hitam tapi kacanya copot sebelah.",
            "ending": "Kucing pura-pura santai sambil mengejar ekornya sendiri.",
            "hashtags": "#Shorts #KucingOyen #Animasi3D #Komedi",
            "cta_note": "CTA dibuat dari rasa malu sang detektif kucing."
        }
    ]
    return random.choice(pool)

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    key = api_key()
    st.write("Gemini API:", "✅ Terhubung" if key else "⚠️ Belum diatur")
    model = st.text_input("Model Gemini", "gemini-2.5-flash")
    st.caption("Rekomendasi: `gemini-2.5-flash` untuk cepat, atau `gemini-2.5-pro`.")
    
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
    character_idea = st.text_input("Karakter utama (opsional)", placeholder="Contoh: Kucing koki, Robot pemalas, Dinosaurus cilik")
    avoid = st.text_input("Hindari topik (opsional)", placeholder="Contoh: jumpscare kaget, topik dewasa")

if "idea" not in st.session_state:
    st.session_state.idea = None

# Action
if st.button("🔥 GENERATE IDE BARU", type="primary", use_container_width=True):
    prompt = f"""You are an elite YouTube Shorts animation director specializing in viral 3D animated shorts (family-friendly, all ages, Pixar/Illumination aesthetic).

GOAL: Maximise retention (0–2s hook) and subscriber conversions with a dynamic, context-specific CTA.

REQUIREMENTS:
1. TARGET LANGUAGE: Write all content in {target_language}. Keep slang/phrasing natural for native speakers.
2. VISUAL CHARACTERS: 3D animated characters (cute animals, expressive humans, funny robots, or mini monsters). Clean and entertaining for all ages.
   Character hint: {character_idea or 'Invent an endearing funny 3D character pair'}.
3. 0–2s DISRUPTIVE HOOK: Start directly in chaotic or curious motion aimed at the camera. NO slow intro, NO "Halo guys".
4. PUNCHLINE: Deliver a sharp comedic twist within {duration}. Humor style: {humor}.
5. DYNAMIC CONTEXTUAL CTA: The FINAL spoken dialogue line MUST be a subscribe call-to-action strictly integrated into the story's punchline.
   CRITICAL RULE: DO NOT use repetitive generic templates like "Jangan lupa subscribe" or "Subscribe sekarang gratis". Invent a completely unique CTA tied to the character's misfortune or reward.
6. AVOID: {avoid or 'none'}.

Return ONLY a valid JSON object with these keys:
{{
  "title": "Punchy title with emojis",
  "hook": "Visual + audio description of the 0-2s hook",
  "story": "Short premise summary",
  "dialogue": [
    {{"time": "0–2s", "speaker": "NAME", "line": "Line..."}},
    {{"time": "2–{duration}", "speaker": "NAME", "line": "..."}},
    {{"time": "Ending", "speaker": "NAME", "line": "Contextual subscribe line"}}
  ],
  "punchline": "The funny visual payoff",
  "ending": "Final frame/expression",
  "hashtags": "#Shorts #Animation ...",
  "cta_note": "Why this specific CTA fits this story"
}}"""

    with st.spinner("Membuat ide animasi 3D & dialog..."):
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

# Render
x = st.session_state.idea
if x:
    st.divider()
    st.subheader(x.get("title", "Ide Shorts"))
    st.code(x.get("hashtags", "#Shorts #Animation"))
    
    t1, t2, t3, t4 = st.tabs(["🎬 Cerita & Dialog", "🎥 Prompt Generator Video", "🖼️ Prompt Thumbnail", "📊 Evaluasi Konversi"])
    
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
        
        st.markdown("**🏁 ENDING & TRANSISI**")
        st.write(x.get("ending", ""))
        
        st.success(f"**💡 Alasan CTA:** {x.get('cta_note', 'CTA menyatu dengan cerita.')}")

    with t2:
        st.caption("Gunakan prompt ini untuk tool video AI (seperti Google Veo, Runway, Luma, atau Sora):")
        st.text_area("Prompt Video Animasi 3D", x.get("flow_prompt", ""), height=350)

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

    data = {k: x.get(k) for k in ["title", "hashtags", "hook", "story", "dialogue", "punchline", "ending", "flow_prompt", "thumbnail_prompt"]}
    st.download_button(
        "⬇️ Download Format JSON",
        json.dumps(data, ensure_ascii=False, indent=2),
        "shorts_animation_idea.json",
        "application/json"
    )
