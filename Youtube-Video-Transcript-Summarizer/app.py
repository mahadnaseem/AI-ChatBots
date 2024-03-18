import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube Video summarizer, you will be taking a transcript text and summarizing the entire video 
            and providing the summary in points within 200 or 250 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    
    except Exception as e:
        raise e


def generate_gemini_content(transcript_text, prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube Video Content's Summarizer 📝")
youtube_url = st.text_input("Enter Youtube Video Link:")

if youtube_url:
    video_id = youtube_url.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Summarize"):
        transcript_text=extract_transcript_details(youtube_url)  
  
        with st.spinner("Processing"):
            if transcript_text:
                summary=generate_gemini_content(transcript_text,prompt)
                st.markdown("## Detailed Notes: ")
                st.write(summary)