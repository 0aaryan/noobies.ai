GENERATE_VIDEO_FROM_TOPIC = {
    "template": """- you are a professional content creator and you need to write a video script on the following notes: {topic} , script should be {duration} long dont go beyond limit and it should be engaging
    - script should be in {language} language
    - strictly follow the this syntax:
    - SYNTAX:{syntax}
    - use double quotes for the keys and values for json so that we can parse it easily
    - number of parts should be based on number of images which is {num_of_images}.
    - you can add details from your own knowledge
    - be creative
    - keep the tone of the script {tone}
    - return only the script nothing else just the script
    - this video should go viral on youtube shorts and tiktok
    - give just the script that i can directly pass to text to speech no voice effect no background just the voiceover
    - dont add any sound effects or background music just plain text
    - image prompts should be very very descriptive more than 15 words
    - also keep in mind following instructions:
    INSTUCTIONS:{instructions}""",
    "input_variables": [
        "topic",
        "duration",
        "tone",
        "instructions",
        "language",
        "num_of_images",
        "syntax",
    ],
}
