import streamlit as st

from components import ui
from core import achievements

ui.hero("Achievements", "Earn badges as you learn.")
have = achievements.unlocked()
st.write(f"**{len(have)} / {len(achievements.ACHIEVEMENTS)}** unlocked")
cols = st.columns(3)
for i, a in enumerate(achievements.ACHIEVEMENTS):
    with cols[i % 3]:
        ui.card(a[1], a[2], a[3], locked=a[0] not in have, extra=("Unlocked " + have[a[0]][:10]) if a[0] in have else "Locked")
        st.write("")
