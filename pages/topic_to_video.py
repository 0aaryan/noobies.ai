import streamlit as st
import tempfile
import os
from clarifai.modules.css import ClarifaiStreamlitCSS
from noobies_ai.core.video_generator import VideoGenerator


def get_clarifai_pat():
    """
    Get the Clarifai PAT from the user.

    Returns:
        str: The Clarifai PAT entered by the user.
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


def init():
    """
    Initialize the session variables.
    """
    session_variables = [
        "video_script",
        "audio_path",
        "voice_option",
        "image_prompts",
        "script_parts",
        "image_paths",
        "video_path",
    ]
    for variable in session_variables:
        if variable not in st.session_state:
            st.session_state[variable] = None


def generate_video():
    """
    Generates a video based on user inputs.

    Returns:
        None
    """
    try:
        video_generator = VideoGenerator()
        with st.form(key="generate_video_form"):
            col1, col2 = st.columns(2)
            with col1:
                topic = st.text_input(
                    "Enter Topic 📝",
                    placeholder="3 scary places in the world",
                )
                duration = st.number_input(
                    "Enter Duration (seconds) ⏳", min_value=1, max_value=120, value=30
                )
                duration = str(duration) + "s"
                tone = st.text_input("Enter Tone 🎵", placeholder="scary")

            with col2:
                instructions = st.text_input(
                    "Enter Instructions ✍️", placeholder="Add my name in the script"
                )
                language = st.selectbox(
                    "Select Language 🌐", video_generator.get_languages()
                )
                num_of_images = st.number_input(
                    value=5, min_value=1, max_value=20, label="Number of Images 🖼️"
                )
            _, center, _ = st.columns([2, 3, 1])
            with center:
                submit_button = st.form_submit_button(label="Generate Script 🚀")

            if submit_button:
                with st.spinner("Generating Script"):
                    generated_script = video_generator.generate_script(
                        topic,
                        duration=duration,
                        tone=tone,
                        instructions=instructions,
                        language=language,
                        num_of_images=num_of_images,
                    )
                if generated_script is None:
                    st.error("Error generating video")

                else:
                    st.success("Script generated successfully")
                    st.session_state.video_script = generated_script
        if st.session_state.video_script is not None:
            col1, col2 = st.columns(2)
            title = st.session_state.video_script["video_title"]
            description = st.session_state.video_script["video_description"]
            script_parts = st.session_state.video_script["script_parts"]
            image_prompts = st.session_state.video_script["image_prompts"]

            with col1:
                st.text_input("Title 📌", value=title)
                st.text_area("Description 📝", value=description)

            with col2:
                with st.expander("Script 📜" ,expanded=False):
                    for i, part in enumerate(script_parts):
                        st.text_input(f"Part {i+1} ✏️", value=part, key=f"part{i+1}")

                with st.expander("Image Prompts 🖼️"):
                    for i, prompt in enumerate(image_prompts):
                        st.text_input(
                            f"Prompt {i+1} ✏️", value=prompt, key=f"prompt{i+1}"
                        )

            with col2:
                with st.expander("Audio Options 🎵" ,expanded=False):
                    voice_option = st.selectbox(
                        options=video_generator.get_voice_ids().keys(),
                        label="Voice 🔊",
                    )
                    st.session_state.voice_option = video_generator.get_voice_ids()[
                        voice_option
                    ]
                st.info("subtitle options are not available yet")
                # font_color = st.color_picker("Font Color 🎨", value="#ffff00")
                # font_list = video_generator.get_font_list()
                # font = st.selectbox("Font 📝", font_list)
                # font_size = st.slider(
                #     "Font Size 🔍", min_value=1, max_value=120, value=70, step=10
                # )
                font_color = "#ffff00"
                font = None
                font_size = 70

            _, center, _ = st.columns([3, 2, 3])
            with center:
                submit_button = st.button("Generate Video 🎥")

            if submit_button:
                # temp_dir = tempfile.TemporaryDirectory()
                temp_dir = tempfile.TemporaryDirectory()

                with st.spinner("Generating voice for your video"):
                    st.info("Generating audio takes 30-60 seconds")
                    try:
                        audio_path = os.path.join(temp_dir.name, "voice.mp3")
                        voice_option = video_generator.get_voice_ids()[voice_option]
                        print(voice_option)
                        print(temp_dir.name, audio_path, voice_option)
                        updated_script_parts = []
                        for i in range(len(script_parts)):
                            updated_script_parts.append(st.session_state[f"part{i+1}"])
                        updated_image_prompts = []
                        for i in range(len(image_prompts)):
                            updated_image_prompts.append(
                                st.session_state[f"prompt{i+1}"]
                            )

                        print(updated_script_parts, updated_image_prompts)
                        video_generator.generate_audio(
                            output_file=audio_path,
                            voice_id=st.session_state.voice_option,
                            script_parts=updated_script_parts,
                        )
                        st.session_state.audio_path = audio_path

                    except Exception as e:
                        print(e)
                        st.error("Error generating audio")

                if st.session_state.audio_path is not None:
                    st.audio(st.session_state.audio_path, format="audio/mp3")

                with st.spinner("Generating images for your video"):
                    st.info("Generating one image takes 20-30 seconds")
                    try:
                        image_path = os.path.join(temp_dir.name, "images")
                        # mk folder if not exists
                        os.makedirs(image_path, exist_ok=True)
                        image_paths = video_generator.generate_images(
                            image_prompts=updated_image_prompts,
                            image_path=image_path,
                        )
                        st.session_state.image_paths = image_paths
                    except Exception as e:
                        print(e)
                        st.error("Error generating images")

                if st.session_state.image_paths is not None:
                    num_of_images = len(st.session_state.image_paths)
                    cols = st.columns(num_of_images)
                    for i, col in enumerate(cols):
                        col.image(st.session_state.image_paths[i])

                    with st.spinner("Generating video"):
                        try:
                            st.info("Generating video takes 60 seconds")
                            output_file = "video.mp4"
                            video_path = video_generator.generate_video(
                                video_dir=temp_dir.name,
                                output_file=output_file,
                                subtitle_options={
                                    "font_color": font_color,
                                    "font_size": font_size,
                                    "font": font,
                                },
                            )
                            st.session_state.video_path = video_path
                        except Exception as e:
                            print(e)
                            st.error("Error generating video")

                    if st.session_state.video_path is not None:
                        _, center, _ = st.columns([1, 1, 1])
                        center.video(st.session_state.video_path)

    except Exception as e:
        st.error(f"Error: {e}")
        st.error(
            "Please try again later",
        )


def main():
    """
    Main function to run the application.
    """

    try:
        _, img_col, _ = st.columns([1, 3, 1])
        img_col.image("./static/images/neon_logo.png")
        st.title(
            " 📽️ topic to video",
            help="- first generate a script and then generate a video from that script\n- you can also re generate the script if you don't like it\n- you can also change the video options",
        )
        generate_video()

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    init()
    get_clarifai_pat()
    if os.environ.get("CLARIFAI_PAT") is None:
        st.error("Please add your Clarifai PAT in the sidebar.")
    else:
        main()
