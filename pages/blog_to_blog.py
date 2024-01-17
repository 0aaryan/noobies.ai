import streamlit as st
import tempfile
import os
from clarifai.modules.css import ClarifaiStreamlitCSS
from noobies_ai.core.blog_generator import BlogGenerator
import re
import pandas as pd

# allow unsafe html

# page icon should be website icon
st.set_page_config(page_title="Blog to Blog", page_icon=" 📝 ", layout="centered")


# ClarifaiStreamlitCSS.insert_default_css(st)

# initalize session state
if "blog_generated" not in st.session_state:
    st.session_state.blog_generated = False


def get_clarifai_pat():
    """
    Get the Clarifai PAT from the user.
    """
    with st.sidebar:
        st.subheader("Add your Clarifai PAT")

        # Get the USER_ID, APP_ID, Clarifai API Key
        CLARIFAI_PAT = st.text_input("Clarifai PAT", type="password")
        return CLARIFAI_PAT


import base64
import shutil


def create_download_zip(temp_dir, blog_dir):
    """
    Create a zip file in the temp directory.
    """

    # i want to zip the blog_dir
    # zip should be called bolg_dir.split("/")[-1] + ".zip"
    # zip should be in temp_dir

    try:
        shutil.make_archive(
            os.path.join(temp_dir, blog_dir.split("/")[-1]), "zip", blog_dir
        )
        with open(os.path.join(temp_dir, blog_dir.split("/")[-1] + ".zip"), "rb") as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download="{blog_dir.split("/")[-1]}.zip">Download zip file</a>'
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error creating zip file: {e}")
        return None


def convert_to_dict(blog_metadata):
    """
    Convert blog metadata to a dictionary.
    """
    try:
        blog_metadata_dict = {}
        blog_metadata = blog_metadata.split("\n")
        for line in blog_metadata[1:]:
            if line.strip() == "":
                continue
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            blog_metadata_dict[key] = value
        return blog_metadata_dict
    except Exception as e:
        st.error(f"Error converting blog metadata to dictionary: {e}")


def generate_blog(blog_url, generate_ai_images, is_topic=False):
    """
    Generate a new blog based on the given URL.
    """
    try:
        temp_dir = tempfile.TemporaryDirectory()
        blog_generator = BlogGenerator()
        temp_dir_abs = os.path.abspath(temp_dir.name)
        st.session_state.temp_dir = temp_dir_abs
        blog_dir = blog_generator.generate_blog(
            url=blog_url,
            base_dir=temp_dir_abs,
            debug=True,
            generate_images=generate_ai_images,
            is_topic=is_topic,
        )

        st.markdown("## Generated Blog")
        with st.spinner("Loading your blog..."):
            # zip
            create_download_zip(temp_dir_abs, blog_dir)
        md_file_name = blog_dir.split("/")[-1] + ".md"
        blog_md = open(os.path.join(blog_dir, md_file_name), "r").read()
        st.success("Blog loaded!")
        blog_metadata = blog_md.split("---")[1]
        blog = "---".join(blog_md.split("---")[2:])
        st.markdown("## Blog Metadata")
        # convert to dict
        metadata_dict = convert_to_dict(blog_metadata)
        metadata_df = pd.DataFrame(
            list(metadata_dict.items()), columns=["Key", "Value"]
        )
        st.table(metadata_df)
        if generate_ai_images:
            st.markdown("## Generated Images")
            for i in range(0, 6, 2):
                col1, col2 = st.columns(2)

                try:
                    image_path1 = os.path.join(
                        blog_dir, "img", "posts", blog_dir.split("/")[-1], f"{i}.png"
                    )
                    col1.image(image_path1)
                except FileNotFoundError:
                    continue
                try:
                    image_path2 = os.path.join(
                        blog_dir, "img", "posts", blog_dir.split("/")[-1], f"{i+1}.png"
                    )
                    col2.image(image_path2)
                except FileNotFoundError:
                    continue
        st.markdown("## Blog Content")
        st.markdown(blog)

        st.session_state.blog_generated = True
    except Exception as e:
        st.error(f"Error generating blog: {e}")


def main():
    """
    Main function to run the application.
    """
    try:
        _, img_col, _ = st.columns([1, 3, 1])
        img_col.image("./static/images/neon_logo.png")
        st.title("📝 Blog to Blog")
        st.markdown("Enter a blog URL and we'll generate a new blog for you! 🚀")
        st.markdown("- Generating a blog with images takes 2-5 minutes. ⏳")
        st.markdown("- Generating a blog without images takes 30 seconds. ⏳")

        with st.form(key="blog_to_blog"):
            blog_url = st.text_input(
                "🔗 Blog URL",
            )
            generate_ai_images = st.checkbox("🖼️ Generate AI Images", value=True)
            submit_button = st.form_submit_button(label="GENERATE 🚀")
        if submit_button:
            with st.spinner("Generating your blog..."):
                # image = st.image("./static/images/loading.gif")
                generate_blog(blog_url, generate_ai_images)
                st.success("✅ Blog generated!")
                # remove the loading gif
                # image.empty()
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
