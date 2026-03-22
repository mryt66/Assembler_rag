from typing import Any
from google import genai
from langfuse import get_client
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from config.config import settings

_configured = False
_langfuse: Any | None = None


def _supports_legacy_tracing_api(langfuse_client: Any) -> bool:
    return hasattr(langfuse_client, "start_as_current_span")


def _ensure_configured() -> None:
    global _configured, _langfuse
    if _configured:
        return

    GoogleGenAIInstrumentor().instrument()

    try:
        # Avoid initializing a disabled Langfuse client when keys are missing.
        if settings.langfuse_public_key and settings.langfuse_secret_key:
            _langfuse = get_client()
            if _langfuse is not None:
                _langfuse.auth_check()
        else:
            _langfuse = None
    except Exception:
        _langfuse = None
    _configured = True


def get_answer(prompt: str, gemini_api_key: str) -> str | None:
    _ensure_configured()
    client = genai.Client(api_key=gemini_api_key)
    try:
        if _langfuse is not None and _supports_legacy_tracing_api(_langfuse):
            with _langfuse.start_as_current_span(name="outer-process") as outer_span:
                with outer_span.start_as_current_generation(
                    name="gemini-generate",
                    model=settings.gemini_model,
                    input={"user_input": prompt},
                ) as gen:
                    resp = client.models.generate_content(
                        model=settings.gemini_model,
                        contents=prompt,
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
                model=settings.gemini_model,
                contents=prompt,
            )

        return getattr(resp, "text", None)

    except Exception as e:
        print(f"[Gemini error] {e}")
        return None
