# Gokil Global Shorts Studio

Photorealistic live-action comedy Shorts generator. Designed for strong opening hooks, story-specific subscribe CTA, and strict character-mode instructions.

## Deploy
1. Upload `app.py`, `requirements.txt`, and `README.md` to the root of your GitHub repository.
2. In Streamlit Cloud, connect the repository and deploy `app.py`.
3. In Streamlit app Settings → Secrets, add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

4. Set language to English for global content. Choose the character mode carefully.
5. Generate a story and copy the Google Flow prompt.

## Character mode rules
- **Skeleton realistis:** skeleton must be the lead from the opening; no human-only replacement.
- **Manusia realistis:** human actors only.
- **Manusia + Skeleton realistis:** both must appear in the main action.
- **Semar live-action:** Semar-inspired practical costume performer is the lead.
- **Semar live-action + Manusia:** both must appear.

Note: prompts can strongly guide Google Flow but cannot guarantee every generated frame. Review the output before publishing.
