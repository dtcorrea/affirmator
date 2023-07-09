# Import libraries
import streamlit as st

from google.oauth2 import service_account
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from streamlit_extras.let_it_rain import rain

# Load credentials
# Google uses a JSON format for their credentials but Streamlit secrets are in
# TOML only, that's why we need to load the credentials as below
credentials = service_account.Credentials.from_service_account_info(dict(st.secrets['google_service_account']))

# Prompt template to be used to generate the messages
template = """You are in a relationship with someone whose love language is words of affirmation. You are not naturally inclined to express your love through words but you want to express your love in a way that your partner will truly appreciate.

If provided, please consider some of the information below about the partner:
- Name: {name}
- Affectionate name: {love_name}
- Gender: {gender}
- Relationship status: {relationship}

If provided, please also consider the context below:
- Time of the day for the message: {time}
- Tone of the message: {tone}
- Anything else to mention: {add}

Requirements:
- The message gas to br brief with no more than 25 words that can be sent via text.
- Make sure the message only mentions the partner and no other people. Do not assume the partners have children.
"""

# Loading template with the input variables and setting up the Vertex AI model with LangChain
prompt = PromptTemplate(template=template, input_variables=['gender', 'relationship', 'name', 'love_name', 'time', 'tone', 'add'])

llm = VertexAI(temperature=0.5,
                max_output_tokens=128,
                top_p=0.8,
                top_k=40,
                project=st.secrets['google_service_account']['project_id'],
                credentials=credentials)

llm_chain = LLMChain(prompt=prompt, llm=llm)

### Beginning of Streamlit page
st.set_page_config(page_title="AIffirmation")

st.image(image='aiffirmation.png', use_column_width='always')

st.markdown("Are you in a relationship with someone whose love language is *words of affirmation* but you are not good at expressing your love through words? **AIffirmation** is here for you!")
st.markdown("**AIffirmation** will help you write personalized text messages to your partner that will make them feel loved and appreciated, even if words of affirmation do not come naturally to you.")
st.markdown("We hope this app will get you going on your own very soon!")

st.caption('Disclaimer: This app is a prototype and is not intended to be used for any purpose other than testing and evaluation.')

# Forms to get input variables
with st.form(key='my_form_to_submit'):

    col1, col2 = st.columns(2)
    with col1:
        st.header('Tell us more about your partner:')
        option_gender = st.selectbox(
            ':smiley: What is their gender?',
            ('female', 'male', 'non-binary'))
        option_relationship = st.selectbox(
            ':gem: What is your relationship status?',
            ('dating', 'engaged', 'married'))
        option_name = st.text_area(label=":heart_eyes: What is their name (optional)", placeholder="Your partner's name...", key="name")
        option_love_name = st.text_area(label=":kissing_closed_eyes: What do you call them? (optional)", placeholder="Your partner's love name...", key="love_name")


    with col2:
        st.header('Tell us more about the message:')
        option_time = st.selectbox(
            ':sunrise: What time of the day will you send this?',
            ('morning', 'afternoon', 'night'))
        option_tone = st.selectbox(
            ':see_no_evil: What tone do you want?',
            ('romantic', 'professional', 'pirate', 'old-english'))
        option_add = st.text_area(label=":boom: Is there anything else you want to add?", placeholder="Additional info...", key="add")

    submit_button = st.form_submit_button(label=':love_letter: **Generate message**', use_container_width=True)

st.markdown("### Your message:")

# Adding a submit button so the app doesn't run everything every time a new input is changed
if submit_button:
    with st.spinner("AIffirming.."):
        message = llm_chain.run(gender=option_gender, relationship=option_relationship, name=option_name, love_name=option_love_name, time=option_time, tone=option_tone, add=option_add)

        st.write(message)

        rain(emoji="❤️",
        font_size=54,
        falling_speed=5,
        animation_length=1)