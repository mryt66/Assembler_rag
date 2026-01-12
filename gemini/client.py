import os
from langfuse import get_client

# import google.generativeai as genai
from google import genai

from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from dotenv import load_dotenv


_configured = False
_langfuse = None


def _ensure_configured():
    global _configured, _langfuse, client
    if _configured:
        return

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    client = genai.Client(api_key=api_key)
    GoogleGenAIInstrumentor().instrument()

    try:
        _langfuse = get_client()
        if _langfuse is not None:
            _langfuse.auth_check()
            print("[langfuse] initialized successfully ✅")
    except Exception as e:
        print(f"[langfuse] optional init failed: {e}")
        _langfuse = None
    _configured = True


def get_answer(prompt: str) -> str | None:
    _ensure_configured()
    try:
        if _langfuse is not None:
            with _langfuse.start_as_current_span(name="outer-process") as outer_span:
                with outer_span.start_as_current_generation(
                    name="gemini-generate",
                    model="gemini-2.5-flash",
                    input={"user_input": prompt},
                ) as gen:
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash", contents=prompt
                    )
                    output_text = getattr(resp, "text", "") or ""
                    gen.update(output={"llm_output": output_text})
                try:
                    outer_span.update(output=output_text)
                except Exception:
                    pass
            try:
                _langfuse.flush()
            except Exception:
                pass
        else:
            resp = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )

        return getattr(resp, "text", None)

    except Exception as e:
        print(f"[Gemini error] {e}")
        return None
