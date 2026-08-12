"""
=========================================================
OmniMind AI Assistant
Footer Component
=========================================================

Reusable application footer.
"""

from __future__ import annotations

from datetime import datetime

import platform
import streamlit as st

from config.constants import APP_NAME, VERSION


class Footer:
    """
    Reusable footer component.
    """

    def __init__(self):

        pass

    # =====================================================
    # VERSION
    # =====================================================

    def version(self):

        st.caption(f"Version: {VERSION}")

    # =====================================================
    # SYSTEM
    # =====================================================

    def system_information(self):

        with st.expander(
            "System Information",
            expanded=False,
        ):

            st.write(f"Platform : {platform.system()}")

            st.write(f"Python : {platform.python_version()}")

            st.write(f"Streamlit : {st.__version__}")

    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        col1, col2, col3 = st.columns(3)

        col1.success("🟢 Online")

        col2.info(datetime.now().strftime("%d %b %Y"))

        col3.info(datetime.now().strftime("%H:%M:%S"))

    # =====================================================
    # LINKS
    # =====================================================

    def links(self):

        st.markdown("""
            **Resources**

            - Documentation
            - API Reference
            - GitHub Repository
            - Report Issues
            """)

    # =====================================================
    # COPYRIGHT
    # =====================================================

    def copyright(self):

        year = datetime.now().year

        st.markdown(f"""
            ---
            © {year} **{APP_NAME}**

            All Rights Reserved.
            """)

    # =====================================================
    # COMPLETE FOOTER
    # =====================================================

    def render(self):

        st.divider()

        self.status()

        self.version()

        self.system_information()

        self.links()

        self.copyright()


footer = Footer()
