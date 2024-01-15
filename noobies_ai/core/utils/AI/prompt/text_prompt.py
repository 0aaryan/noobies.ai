GENERATE_BLOG_FROM_BLOG = {
    "template": """- you are a SEO specialist and you need to write a blog post on the following notes: {topic}
                        - you can add details from your own knowledge
                        - use your knowledge of SEO to write a blog post that will rank high on google
                        - blog should follow the following syntax: \n {syntax}
                        - strictly follow the format of the blog post, you can also add any markdown syntax you want to make the blog post look better
                        - content under each heading should also be very detailed and long and SEO optimized
                        - todays date is {date}
                        Also keep in mind following instructions:
                        INSTUCTIONS:{instructions}
                        -give full output without code block as plain text
                        -output should be in proper json format use double quotes for keys and values
                        -if you use double quotes inside content use a backslash before it
                        -output should be able to parse by json parser without any error""",
    "input_variables": ["topic", "syntax", "date", "instructions"],
}


SUMMERIZE_BLOG = {
    "template": """- you are a SEO specialist and you need to summerize the following blog post: {blog}
                dont miss any quotables and names of people, places, companies, etc.""",
    "input_variables": ["blog"],
}
