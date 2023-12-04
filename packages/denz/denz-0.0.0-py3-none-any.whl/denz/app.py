"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"denz v{version('denz')}")  # type: ignore[no-untyped-call]
