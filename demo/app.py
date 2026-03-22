import json
from datetime import datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import streamlit as st


def _post_json(
    url: str, payload: dict[str, Any], timeout_s: int = 60
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)


def main() -> None:
    st.set_page_config(page_title="RAG Chat Demo", layout="centered")
    st.title("RAG Chat Demo")

    with st.sidebar:
        st.header("Settings")
        api_base = st.text_input("API base URL", value="http://localhost:8000")
        st.text_input(
            "Gemini API key",
            type="password",
            key="gemini_api_key",
            help="Stored in this Streamlit session and sent with each request.",
        )

    gemini_api_key = (st.session_state.get("gemini_api_key") or "").strip()
    chat_url = api_base.rstrip("/") + "/chat"

    if "history" not in st.session_state:
        st.session_state.history = []

    for turn in st.session_state.history:
        role = turn.get("role", "user")
        content = turn.get("message", "")
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

    query = st.chat_input("Ask something")
    if not query:
        return

    if not gemini_api_key:
        st.warning("Enter Gemini API key in the sidebar before sending messages.")
        return

    st.session_state.history.append({"role": "user", "message": query})
    with st.chat_message("user"):
        st.markdown(query)

    payload = {
        "query": query,
        "gemini_api_key": gemini_api_key,
        "history": st.session_state.history[-12:],
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = _post_json(chat_url, payload)
                answer = (resp.get("response") or "").strip()
                if not answer:
                    answer = "(empty response)"

                ts = resp.get("timestamp")
                if ts:
                    try:
                        _ = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        st.caption(ts)
                    except Exception:
                        pass

                st.markdown(answer)
                st.session_state.history.append(
                    {"role": "assistant", "message": answer}
                )

            except HTTPError as e:
                st.error(f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}")
            except URLError as e:
                st.error(f"Connection error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
