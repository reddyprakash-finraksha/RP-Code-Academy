"""Shared UI helpers."""
from __future__ import annotations

import streamlit as st

from core import config


def inject_css() -> None:
    css = (config.assets_dir() / "style.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def hero(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="psca-hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def pill(kind: str, text: str) -> str:
    return f'<span class="psca-pill {kind}">{text}</span>'


def card(icon: str, title: str, desc: str, locked: bool = False, extra: str = "") -> None:
    cls = "psca-card locked" if locked else "psca-card"
    st.markdown(f'<div class="{cls}"><div class="icon">{icon}</div><div class="title">{title}</div>'
                f'<div class="desc">{desc}</div><div class="desc">{extra}</div></div>', unsafe_allow_html=True)


def safe_run(label: str):
    """Decorator-free error boundary: use as `with safe_run('x'):`."""
    import contextlib
    import logging

    @contextlib.contextmanager
    def cm():
        try:
            yield
        except Exception as exc:  # noqa: BLE001
            logging.getLogger("psca").exception("Error in %s", label)
            st.error(f"Something went wrong ({label}). Your progress is safe. Details were saved to the log. "
                     f"Error: {type(exc).__name__}")
    return cm()
