import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS
import base64
from streamlit_card import card


def get_image_data(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data


# page icon should be image camera
st.set_page_config(page_title="noobies.ai", page_icon="📷", layout="centered")
ClarifaiStreamlitCSS.insert_default_css(st)


def main():
    # show logo image in center

    st.image("./static/images/logo.png")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # text colour blck
    blog_image_1 = get_image_data("./static/images/blog1.png")
    video_image_2 = get_image_data("./static/images/video2.png")
    video_image_1 = get_image_data("./static/images/video1.png")
    blog_image_2 = get_image_data("./static/images/blog2.png")
    # add block border to title
    with col1:
        hasClicked = card(
            title="BLOG TO BLOG",
            text="",
            image=blog_image_1,
            url="/blog_to_blog",
            key="blog_card",
            styles={
                "card": {},
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
            title="TOPIC TO BLOG",
            text="",
            image=blog_image_2,
            url="./pages/blog_to_video.py",
            key="video_card",
            styles={
                "card": {},
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col3:
        hasClicked = card(
            title=" TOPIC TO VIDEO",
            text="",
            image=video_image_1,
            url="./pages/blog_to_blog.py",
            key="image_card",
            styles={
                "card": {},
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col4:
        hasClicked = card(
            title="VIDEO TO VIDEO",
            text="",
            image=video_image_2,
            url="./pages/blog_to_video.py",
            key="audio_card",
            styles={
                "card": {},
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )


if __name__ == "__main__":
    main()
