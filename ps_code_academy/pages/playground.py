import streamlit as st

from components import ui
from core import sandbox

ui.hero("Playground", "Try any Python code safely. Nothing here is graded.")
st.session_state.setdefault("pg_code", 'name = "RP Code Academy"\nprint("Hello from", name)\n')
st.text_area("Code", key="pg_code", height=300, label_visibility="collapsed")
st.text_area("Program input (optional)", key="pg_stdin", height=80)
if st.button("▶ Run", type="primary"):
    r = sandbox.run_code(st.session_state["pg_code"], stdin=st.session_state.get("pg_stdin", ""))
    if r.error:
        st.error(r.error)
    if r.stdout:
        st.code(r.stdout, language="text")
    if r.stderr:
        st.code(r.stderr, language="text")
    st.caption(f"Finished in {r.duration:.2f}s")
