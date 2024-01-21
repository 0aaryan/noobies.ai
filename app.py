import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS
import base64
from streamlit_card import card
import os
import streamlit.components.v1 as components


def get_clarifai_pat():
    """
    Get the Clarifai PAT from the user.
    """
    with st.sidebar:
        st.subheader("Add your Clarifai PAT")
        CLARIFAI_PAT = st.text_input("Clarifai PAT", type="password")
        # add button and export to env
        if st.button("Add PAT"):
            os.environ["CLARIFAI_PAT"] = CLARIFAI_PAT
            st.success("✅ PAT added!")
            st.balloons()
        return CLARIFAI_PAT


def get_image_data(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data


def showcase():
    st.header("📚 Blogs created using noobies.ai")
    blog_col_1, blog_col_2, blog_col_3 = st.columns([1, 3, 1])
    components.iframe(
        "https://stuckaryan.tech/blogs/how_joining_a_lablab_ai_hackathon_can_boost_your_career/",
        scrolling=True,
        height=400,
    )
    st.markdown("--- ")
    st.header("🎥 Videos created using noobies.ai")

    vid_col_3, vid_col_2, vid_col_1 = st.columns(3)
    vid_col_1.video("./static/videos/noobies_intro.webm")
    vid_col_1.text("🤖 NOOBIES.AI : The AI Content Generator")

    vid_col_2.video("./static/videos/lab_lab_intro.webm")
    vid_col_2.text("🔬 Lab Lab AI : Community of AI Enthusiasts")

    vid_col_3.video("./static/videos/clarifai_intro.webm")
    vid_col_3.text("🧠 Clarifai : AI for Everyone")

    st.markdown("--- ")


def footer():
    # add socials also my website stuckaryan.tech mail aroraryan826@gmail.com
    st.markdown("## Connect with us")
    # use globe for website
    st.markdown(
        """
        <a href="https://www.youtube.com/@StuckAryan" target="_blank">
            <img src="https://img.shields.io/badge/YouTube-000000?style=for-the-badge&logo=youtube&logoColor=white"/>
        </a>
        <a href="https://stuckaryan.tech" target="_blank">
            <img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=google-chrome&logoColor=white"/>
        </a>
        <a href="https://www.github.com/0aaryan" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white"/>
        </a>
        <a href="https://www.linkedin.com/in/am-aryan-arora/" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=linkedin&logoColor=white"/>
        </a>
        <a href="mailto:aroraryan826@gmail.com?subject=Subject%20Here&body=Hello%20Aryan" target="_blank">
            <img src="https://img.shields.io/badge/Gmail-000000?style=for-the-badge&logo=gmail&logoColor=white"/>
        </a>

        """,
        unsafe_allow_html=True,
    )


# page icon should be image camera
st.set_page_config(page_title="noobies.ai", page_icon="📷", layout="centered")


def main():
    # show logo image in center

    _, img_col, _ = st.columns([1, 3, 1])
    img_col.image("./static/images/neon_logo.png")

    st.info(
        """
        **Welcome to noobies.ai!** 🚀

        noobies.ai is an open-source project designed to empower users in AI-driven content generation. It provides an extensive set of tools for creating diverse content, including blogs, images, videos, and audio. The project aims to simplify AI-based content creation while ensuring accessibility and user-friendliness.
        """
    )

    with st.sidebar:
        _, img_col, _ = st.columns([1, 3, 1])
        img_col.image("./static/images/neon_logo.png")
    st.markdown("--- ")
    st.header("🛠️ Tools")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    st.markdown("--- ")
    # text colour blck
    blog_image_1 = get_image_data("./static/images/blog1.png")
    video_image_2 = get_image_data("./static/images/video2.png")
    video_image_1 = get_image_data("./static/images/video1.png")
    blog_image_2 = get_image_data("./static/images/blog2.png")
    # add block border to title
    with col1:
        hasClicked = card(
            title="📝 BLOG TO BLOG",
            text="",
            image=blog_image_1,
            url="/blog_to_blog",
            key="blog_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "title": {
                    "text-shadow": "0px 0px 1px #111111",
                    "color": "white",
                    "font-weight": "bold",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col2:
        hasClicked = card(
            title="📚 TOPIC TO BLOG",
            text="",
            image=blog_image_2,
            url="/topic_to_blog",
            key="video_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col3:
        hasClicked = card(
            title="🎬 TOPIC TO VIDEO",
            text="",
            image=video_image_1,
            url="/topic_to_video",
            key="image_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col4:
        hasClicked = card(
            title="🎥 VIDEO TO VIDEO",
            text="",
            image=video_image_2,
            url="./pages/blog_to_video.py",
            key="audio_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    showcase()


if __name__ == "__main__":
    get_clarifai_pat()
    main()
    footer()
