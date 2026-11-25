"""Reusable exercise/project panel: editor, run, check, hints, solution."""
from __future__ import annotations

import streamlit as st

from core import checker, config, progress, sandbox
from core import achievements


def _reset(iid: str, starter: str) -> None:
    st.session_state[f"code_{iid}"] = starter
    st.session_state.pop(f"res_{iid}", None)


def _toast_new() -> None:
    for a in achievements.evaluate():
        st.toast(f"{a[1]} Achievement unlocked: {a[2]}!", icon="🏅")


def _show_result(res) -> None:
    kind, data = res
    if kind == "run":
        if data.error:
            st.error(data.error)
        if data.stdout:
            st.markdown("**Output**")
            st.code(data.stdout, language="text")
        elif not data.stderr and not data.error:
            st.info("Your program ran but printed nothing.")
        if data.stderr:
            st.markdown("**Messages**")
            st.code(data.stderr, language="text")
        st.caption(f"Finished in {data.duration:.2f}s")
        return
    n = len(data.outcomes)
    if data.passed:
        st.success(f"🎉 All {n} test{'s' if n != 1 else ''} passed!")
        return
    f = data.first_failure
    st.error(f"Not yet: {data.passed_count} of {n} tests passed. Test {f.index} failed.")
    if f.stdin.strip():
        st.markdown("**Input given**")
        st.code(f.stdin, language="text")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Expected output**")
        st.code(f.expected or "(nothing)", language="text")
    with c2:
        st.markdown("**Your output**")
        st.code(f.actual or "(nothing)", language="text")
    if f.error:
        st.markdown("**Error message**")
        st.code(f.error, language="text")


def render(item: dict, kind: str = "exercise") -> None:
    iid = item["id"]
    prog = progress.get_item(iid)
    code_key, stdin_key, res_key = f"code_{iid}", f"stdin_{iid}", f"res_{iid}"
    if code_key not in st.session_state:
        st.session_state[code_key] = prog["last_code"] or item["starter"]

    st.markdown(item["prompt"])
    st.text_area("Your code", key=code_key, height=max(180, 24 * (st.session_state[code_key].count("\n") + 3)),
                 label_visibility="collapsed", max_chars=config.MAX_CODE_CHARS)
    with st.expander("Program input (optional, for programs that use input())"):
        st.text_area("stdin", key=stdin_key, height=80, label_visibility="collapsed",
                     placeholder="Type input lines here, one per line")

    b1, b2, b3, b4, b5 = st.columns(5)
    code = st.session_state[code_key]
    if b1.button("▶ Run", key=f"run_{iid}", width="stretch"):
        with st.spinner("Running..."):
            st.session_state[res_key] = ("run", sandbox.run_code(code, stdin=st.session_state.get(stdin_key, "")))
        progress.save_code(iid, code, kind)
    if b2.button("✅ Check", key=f"chk_{iid}", type="primary", width="stretch"):
        with st.spinner("Checking against test cases..."):
            res = checker.check(item, code)
        progress.record_attempt(iid, code, res.passed, kind)
        st.session_state[res_key] = ("check", res)
        _toast_new()
    n_hints = len(item["hints"])
    if b3.button("💡 Hint", key=f"hint_{iid}", width="stretch", disabled=n_hints == 0):
        progress.use_hint(iid, n_hints, kind)
    prog = progress.get_item(iid)
    unlocked = progress.solution_unlocked(iid, n_hints)
    if b4.button("👀 Solution", key=f"sol_{iid}", width="stretch", disabled=not unlocked,
                 help=f"Unlocks after {config.SOLUTION_UNLOCK_ATTEMPTS} unsuccessful checks, or after passing."):
        progress.view_solution(iid, kind)
    b5.button("↺ Reset", key=f"rst_{iid}", width="stretch", on_click=_reset, args=(iid, item["starter"]))

    prog = progress.get_item(iid)
    if res_key in st.session_state:
        _show_result(st.session_state[res_key])
    for i in range(prog["hints_used"]):
        st.info(f"💡 Hint {i + 1}: {item['hints'][i]}")
    if prog["solution_viewed"]:
        with st.expander("Reference solution", expanded=True):
            st.code(item["solution"], language="python")
