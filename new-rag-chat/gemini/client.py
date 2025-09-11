from __future__ import annotations

import os
import google.generativeai as genai


_configured = False


def _ensure_configured():
    global _configured
    if _configured:
        return
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    _configured = True


def get_answer(prompt: str) -> str | None:
    _ensure_configured()
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:  # noqa: BLE001
        print(f"Gemini error: {e}")
        return None
