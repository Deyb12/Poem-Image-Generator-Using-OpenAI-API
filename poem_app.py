import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["api_secret"]

# Function to generate an image using OpenAI
def generate_image(input_string): 
    response = openai.Image.create(
        prompt=input_string,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url

# Function to generate a poem using OpenAI's GPT-3 language model
def generate_poem(input_string):
    prompt = f"Write a title about {input_string} and poem about {input_string}\n\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    poem = response.choices[0].text.strip()
    return poem

gif_url = "https://thumbs.gfycat.com/TenseIncomparableAfricanfisheagle-size_restricted.gif"
with st.columns(3)[1]:
    st.image(gif_url, width=250)
st.markdown("<h1 style='font-size: 42px; font-family: Courier New;'>Welcome to the <span style='color: #D4AF37;'>AI Poet</span>!</h1><p style = 'font-size: 18px;'>Please enter a few words that best describe how you envision your poem to look and sound. Once you have provided the information, you can press enter button in your keyboard to generate your poem instantly.</p><br>", unsafe_allow_html=True)
input_string = st.text_input("Enter a topic for your poem and image:")

if input_string:
    st.subheader("Generated Poem with Image:")
    
    if "input_string" not in st.session_state or st.session_state.input_string != input_string:
        st.session_state.input_string = input_string
        st.session_state.image = generate_image(input_string)
        st.session_state.poem = generate_poem(input_string)
    
    if st.button("Regenerate Image"):
        image = generate_image(input_string)
        st.session_state.image = image
    else:
        image = st.session_state.image
    
    if st.button("Regenerate Poem"):
        poem = generate_poem(input_string)
        st.session_state.poem = poem
    else:
        poem = st.session_state.poem
    poem_with_linebreaks = poem.replace('\n', '<br>')
    st.markdown(f"""
        <div style='border: 1px solid black; padding: 20px; background-color: lightblue;'>
            <div style='display: flex; justify-content: center;'>
                <img src='{image}' width=300>
            </div>
            <p style='text-align: center; font-size: 18px; font-family: Monotype Baskerville; margin-top: 20px;'>{poem_with_linebreaks}</p>
        </div>
    """, unsafe_allow_html=True)
    
    

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Built with ❤ by <a style='display: block; text-align: center;' href="https://github.com/Deyb12" target="_blank">DAVE FAGARITA</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
