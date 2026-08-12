"""
=========================================================
OmniMind AI Assistant
Vision Page
=========================================================

Image analysis workspace powered by VisionAgent.
"""

from __future__ import annotations

import streamlit as st

from components.sidebar import sidebar
from components.navbar import navbar
from components.uploader import uploader
from components.notifications import notifications
from components.footer import footer

from agents.vision_agent import VisionAgent


class VisionPage:
    """
    Computer Vision workspace.
    """

    def __init__(self):

        self.agent = VisionAgent()

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Vision",
            page_icon="🖼",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self):

        return sidebar.render()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(
        self,
        model: str,
    ):

        navbar.render(
            page_title="🖼 Vision Workspace",
            model_name=model,
        )

    # =====================================================
    # ACTIONS
    # =====================================================

    def render_actions(self):

        col1, col2, col3 = st.columns(3)

        with col1:

            analyze = st.button(
                "🔍 Analyze",
                use_container_width=True,
            )

        with col2:

            caption = st.button(
                "📝 Generate Caption",
                use_container_width=True,
            )

        with col3:

            ocr = st.button(
                "📄 OCR",
                use_container_width=True,
            )

        return {
            "analyze": analyze,
            "caption": caption,
            "ocr": ocr,
        }

    # =====================================================
    # IMAGE UPLOAD
    # =====================================================

    def upload_image(self):

        return uploader.render(
            title="Upload an Image",
            allowed_types=uploader.IMAGE_TYPES,
            destination="uploads/images",
        )

    # =====================================================
    # WORKSPACE
    # =====================================================

    def workspace(
        self,
        image_path,
        actions,
    ):

        if image_path is None:

            st.info("Upload an image to begin.")

            return

        st.image(
            str(image_path),
            use_container_width=True,
        )

        if actions["analyze"]:

            with st.spinner("Analyzing image..."):

                result = self.agent.analyze_image(image_path)

            st.subheader("Analysis")

            st.write(result)

            notifications.success("Vision", "Image analyzed successfully.")

        if actions["caption"]:

            with st.spinner("Generating caption..."):

                caption = self.agent.generate_caption(image_path)

            st.subheader("Caption")

            st.write(caption)

        if actions["ocr"]:

            with st.spinner("Extracting text..."):

                text = self.agent.extract_text(image_path)

            st.subheader("OCR Output")

            st.text_area(
                "Detected Text",
                text,
                height=250,
            )

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        actions = self.render_actions()

        st.divider()

        image = self.upload_image()

        self.workspace(
            image,
            actions,
        )

        st.divider()

        self.render_footer()


vision_page = VisionPage()


def main():

    vision_page.render()


if __name__ == "__main__":

    main()
