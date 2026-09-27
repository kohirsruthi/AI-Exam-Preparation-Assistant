import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Exam Preparation Assistant",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 AI Exam Preparation Assistant")

st.write(
    "Enter an exam topic and get a simple, clear, "
    "exam-oriented explanation using AI."
)

st.divider()


# --------------------------------------------------
# CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    st.error(
        "Groq API key not found. "
        "Please add GROQ_API_KEY to your .env file."
    )
    st.stop()


# --------------------------------------------------
# CREATE GROQ CLIENT
# --------------------------------------------------

client = Groq(api_key=API_KEY)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

topic = st.text_area(
    "📚 Enter your exam topic",
    placeholder="Example: Operating System Deadlock",
    height=120
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button("🤖 Explain Topic", use_container_width=True):

    # Basic validation
    if not topic.strip():

        st.warning(
            "⚠️ Please enter a topic before clicking the button."
        )

    else:

        # --------------------------------------------------
        # STRUCTURED PROMPT
        # --------------------------------------------------

        prompt = f"""
You are an AI Exam Preparation Assistant.

The student is preparing for an exam.

Explain the following topic:

Topic:
{topic}

Follow these instructions:

1. Give a simple definition.
2. Explain the concept in easy language.
3. Give the important points.
4. Give a simple example if applicable.
5. Mention important points students can remember for exams.
6. Keep the explanation clear and organized.
7. Do not make the answer unnecessarily complicated.

Format the response using headings and bullet points.
"""

        # --------------------------------------------------
        # API CALL
        # --------------------------------------------------

        try:

            with st.spinner("🤖 Preparing your exam explanation..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful AI exam preparation "
                                "assistant for college students."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_completion_tokens=1000
                )

            # --------------------------------------------------
            # GET AI RESPONSE
            # --------------------------------------------------

            answer = response.choices[0].message.content

            # --------------------------------------------------
            # DISPLAY RESULT
            # --------------------------------------------------

            st.success("✅ Explanation generated successfully!")

            st.subheader("📖 Exam Preparation Notes")

            st.markdown(answer)

        # --------------------------------------------------
        # ERROR HANDLING
        # --------------------------------------------------

        except Exception as error:

            st.error(
                "❌ Something went wrong while contacting the AI."
            )

            st.info(
                "Please check your API key and internet connection, "
                "then try again."
            )

            st.write("Error details:", error)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Exam Preparation Assistant | Beginner AI Project"
)