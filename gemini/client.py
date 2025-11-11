import os
from langfuse import get_client

# import google.generativeai as genai
from google import genai
import json

from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from dotenv import load_dotenv
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, Field
import yaml


_configured = False
_langfuse = None
_judge_template: str | None = None


class BinaryAnswer(BaseModel):
    value: Annotated[int, Field(ge=0, le=1)] = Field(
        description="0 jeśli nie dotyczy, 1 jeśli dotyczy"
    )


def _ensure_configured():
    global _configured, _langfuse, _judge_template, client
    if _configured:
        return

    # Load environment variables from .env if present
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    client = genai.Client(api_key=api_key)
    GoogleGenAIInstrumentor().instrument()

    # Model will be instantiated at each call site explicitly

    try:
        _langfuse = get_client()
        if _langfuse is not None:
            _langfuse.auth_check()
            print("[langfuse] initialized successfully ✅")
    except Exception as e:
        print(f"[langfuse] optional init failed: {e}")
        _langfuse = None
    _configured = True

    # Load judge YAML template if present
    try:
        # Judge prompt expected in data/judge_prompt.yaml (repo data directory)
        project_root = Path(__file__).resolve().parent.parent
        judge_path = project_root / "data" / "judge_prompt.yaml"
        if judge_path.exists():
            with judge_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                _judge_template = str(data.get("prompt") or "").strip() or None
        else:
            print(f"[judge] template not found at {judge_path}")
    except Exception as e:  # noqa: BLE001
        print(f"[judge] failed to load YAML template: {e}")


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
                    output_text = getattr(resp, "text", "")
                    gen.update(output={"llm_output": output_text})
                try:
                    outer_span.update(output=output_text)
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


def evaluate_answer(output_text: str) -> str | None:
    _ensure_configured()
    if not _judge_template:
        print("[judge] template missing: gemini/judge_prompt.yaml not found or invalid")
        return None
    eval_prompt = _judge_template.replace("{output}", output_text or "")
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=eval_prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": BinaryAnswer.model_json_schema(),
            },
        )
        return resp.text
    except Exception as e:
        print(f"[Judge error] {e}")
        return None


def get_answer_and_judgment(prompt: str) -> tuple[str | None, str | None]:
    """Return (possibly filtered answer, judgment).

    If judgment == "0" we return a standardized rejection message instead
    of the original LLM answer.
    """
    answer = get_answer(prompt)
    if not answer:
        return None, None
    judgment = json.loads(evaluate_answer(answer))
    if judgment["value"] == 0:
        filtered = f"Twoje zapytanie {prompt} nie jest związane z Językiem Maszyny W. Proszę o zadanie pytania dotyczącego tego języka."
        return filtered, judgment
    return answer, judgment
