import streamlit as st
from openai import OpenAI
import re

# Set page config for a premium look & feel
st.set_page_config(
    page_title="AI Poet & Artist - Generate Poems with Art",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics, glassmorphism, glowing accents, and typography
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,700;1,400;1,600&family=Outfit:wght@400;600;700;800&display=swap');
    
    /* General app-wide styling */
    .stApp {
        background-color: #0b0c10;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(197, 160, 89, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.95) 0%, #06070a 100%);
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
    }
    
    /* Typography override */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Main container title styling */
    .main-title {
        background: linear-gradient(135deg, #FFDF00 0%, #D4AF37 50%, #8A2BE2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 5px;
        filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.3));
    }
    
    .main-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 300;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* Glassmorphism output card container */
    .poetic-card {
        background: rgba(20, 24, 39, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 
            0 10px 40px -10px rgba(0, 0, 0, 0.7),
            0 0 30px rgba(138, 43, 226, 0.1),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin: 30px auto;
        max-width: 1100px;
    }
    
    .poetic-card:hover {
        border-color: rgba(212, 175, 55, 0.45);
        box-shadow: 
            0 15px 50px -5px rgba(0, 0, 0, 0.8),
            0 0 40px rgba(212, 175, 55, 0.15),
            inset 0 1px 2px rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    /* Poetic Image styling inside card */
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
        transition: all 0.4s ease;
    }
    
    .poetic-image {
        width: 100%;
        max-width: 450px;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
        border-radius: 16px;
    }
    
    .image-container:hover .poetic-image {
        transform: scale(1.04);
    }
    
    /* Poetry layout and text stylings */
    .poem-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 10px 20px;
    }
    
    .poem-title {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 2.1rem;
        color: #D4AF37;
        margin-bottom: 25px;
        line-height: 1.3;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
        position: relative;
        display: inline-block;
    }
    
    .poem-title::after {
        content: '';
        display: block;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #D4AF37, transparent);
        margin: 12px auto 0 auto;
    }
    
    .poem-content {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.25rem;
        line-height: 1.9;
        color: #F1F5F9;
        white-space: pre-wrap;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Streamlit widget modifications */
    div[data-testid="stSidebar"] {
        background-color: #0e111a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Stylized key info alert */
    .api-alert {
        background: rgba(220, 38, 38, 0.15);
        border: 1px solid rgba(220, 38, 38, 0.3);
        color: #FECACA;
        padding: 15px 20px;
        border-radius: 12px;
        font-size: 0.95rem;
        text-align: center;
        margin: 20px auto;
        max-width: 600px;
    }
    
    /* Glowing quill animation styles */
    .quill-animation {
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(3deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    /* Footer details */
    .footer-container {
        text-align: center;
        padding: 30px 0;
        font-size: 0.9rem;
        color: #64748B;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 60px;
        font-family: 'Inter', sans-serif;
    }
    
    .footer-container a {
        color: #D4AF37;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .footer-container a:hover {
        color: #F1C40F;
        text-shadow: 0 0 8px rgba(241, 196, 15, 0.4);
    }

    /* Style the main summon button */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #0b0c10 !important;
        border: none !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        padding: 0.6rem 2rem !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: auto !important;
        display: block !important;
        margin: 0 auto !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.45) !important;
        color: #000000 !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Styles for auxiliary/regeneration buttons */
    .stButton > button[key*="regen"] {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #E2E8F0 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1.2rem !important;
    }

    .stButton > button[key*="regen"]:hover {
        background: rgba(51, 65, 85, 0.9) !important;
        border-color: rgba(212, 175, 55, 0.4) !important;
        color: #FFFFFF !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 1. API Configuration & Secrets Fetching
api_key = None
try:
    api_key = st.secrets.get("api_secret")
except Exception:
    pass

# 2. Sidebar Configuration (Clean & Modern Layout)
with st.sidebar:
    # Custom Sidebar Header
    st.markdown(
        """
        <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
            <h2 style="font-family: 'Outfit', sans-serif; color: #D4AF37; margin: 0; font-size: 1.8rem;">⚙️ Settings</h2>
            <p style="color: #64748B; font-size: 0.85rem; margin: 5px 0 0 0;">Customize your creative journey</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # API Key Handlers
    if not api_key:
        st.markdown(
            """
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 12px; margin-bottom: 20px;">
                <span style="color: #FBBF24; font-size: 0.85rem; font-weight: 500;">⚠️ API Key Required</span><br>
                <span style="color: #94A3B8; font-size: 0.8rem;">Please provide an OpenAI API key to start creating.</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        api_key_input = st.text_input("OpenAI API Key", type="password", help="Your API key is only stored in your browser session.")
        if api_key_input:
            api_key = api_key_input
    else:
        st.markdown(
            """
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 12px; margin-bottom: 20px; text-align: center;">
                <span style="color: #34D399; font-size: 0.85rem; font-weight: 600;">🔑 API Key Configured</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Poem Settings
    st.markdown("<h3 style='color: #E2E8F0; font-size: 1.1rem; margin-bottom: 15px;'>📝 Poem Parameters</h3>", unsafe_allow_html=True)
    poem_tone = st.selectbox("Tone / Mood", ["Mystical & Ethereal", "Melancholic & Reflective", "Romantic & Warm", "Epic & Heroic", "Playful & Whimsical", "Dark & Gothic", "Futuristic & Sci-Fi"])
    poem_structure = st.selectbox("Structure", ["Free Verse", "Sonnet", "Haiku", "Limerick", "Rhyming Quatrains"])
    poem_length = st.select_slider("Length", options=["Short (1-2 stanzas)", "Medium (3-4 stanzas)", "Long (5+ stanzas)"], value="Medium (3-4 stanzas)")
    
    st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # Image Settings
    st.markdown("<h3 style='color: #E2E8F0; font-size: 1.1rem; margin-bottom: 15px;'>🎨 Visual Parameters</h3>", unsafe_allow_html=True)
    image_style = st.selectbox("Visual Style", ["Surrealist Fantasy", "Classic Oil Painting", "Ethereal Watercolor", "Vibrant Digital Art", "Cyberpunk / Synthwave", "Dark Fantasy Sketch", "Surreal Dali-esque", "Minimalist Ink Drawing"])
    
    st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #475569; font-size: 0.8rem;">
            AI Poet Engine v2.0<br>
            Designed with Premium Aesthetics
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. Custom SVG Quill Logo/Icon instead of broken gfycat gif
svg_logo = """
<div class="quill-animation" style="margin-bottom: 20px;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100" style="display: block; margin: 0 auto; filter: drop-shadow(0px 8px 16px rgba(212, 175, 55, 0.25));">
        <defs>
            <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FFF3A7" />
                <stop offset="50%" stop-color="#D4AF37" />
                <stop offset="100%" stop-color="#8A7322" />
            </linearGradient>
            <linearGradient id="purple-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#A855F7" />
                <stop offset="100%" stop-color="#6366F1" />
            </linearGradient>
        </defs>
        <!-- Feather base -->
        <path d="M70,25 C58,35 48,50 35,75 C34,77 31,79 28,80 C26,80 25,79 25,77 C26,74 28,71 30,70 C55,47 65,37 70,25 Z" fill="url(#gold-grad)" />
        <!-- Feather cuts -->
        <path d="M52,43 L45,41 M45,51 L37,48 M38,61 L31,58" stroke="#0b0c10" stroke-width="1.5" stroke-linecap="round" />
        <!-- Feather shaft -->
        <path d="M26,79 Q50,45 72,23" fill="none" stroke="url(#purple-grad)" stroke-width="2" stroke-linecap="round" />
        <!-- Ink jar -->
        <path d="M18,80 C18,76 22,74 27,74 C32,74 36,76 36,80 L38,84 C38,87 34,89 27,89 C20,89 16,87 16,84 Z" fill="none" stroke="url(#gold-grad)" stroke-width="1.5" />
        <ellipse cx="27" cy="80" rx="6" ry="1.5" fill="#8A2BE2" opacity="0.6" />
    </svg>
</div>
"""

# App Title & Welcome Description
st.markdown(svg_logo, unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Welcome to the AI Poet</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='main-subtitle'>Weave exquisite, customized poetry and paint matching, high-definition visual imagery with OpenAI's most advanced mini language and art models.</p>",
    unsafe_allow_html=True
)

# Core logic functions using modern OpenAI SDK
def get_client(key):
    return OpenAI(api_key=key)

def generate_poem_text(client, topic, tone, structure, length):
    length_desc = {
        "Short (1-2 stanzas)": "short (approximately 1 to 2 stanzas or 4-8 lines)",
        "Medium (3-4 stanzas)": "medium length (approximately 3 to 4 stanzas or 12-16 lines)",
        "Long (5+ stanzas)": "long (5 stanzas or more, detailed prose)"
    }
    
    prompt = (
        f"Write an original poem about '{topic}' with a '{tone}' mood, styled as a {structure}. "
        f"The poem should be {length_desc[length]}. "
        f"Format your response with the first line being the title of the poem. Do NOT prefix it with 'Title:' or quotes. "
        f"Follow the title by two line breaks, and then output the full poem body."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a world-class, award-winning poet who writes deeply evocative, layered, and beautiful verses."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.75
    )
    return response.choices[0].message.content.strip()

def generate_artwork(client, topic, visual_style):
    prompt = f"A breathtaking, high-quality representation of '{topic}' rendered in a {visual_style} aesthetic. Award-winning composition, evocative atmosphere, highly detailed, perfect color harmony."
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response.data[0].url

# Split title and poem content for modern card representation
def parse_poem(raw_poem):
    lines = [l.strip() for l in raw_poem.split('\n') if l.strip()]
    if not lines:
        return "Verses of the Muse", "The page remains blank..."
    
    title = lines[0].replace('"', '').replace("Title:", "").strip()
    # Reassemble remaining lines preserving line breaks but removing excess spacing
    body_lines = raw_poem.split('\n')[1:]
    # Join and trim starting/ending newlines
    body = '\n'.join(body_lines).strip()
    return title, body

# Initialization of Session State
if "poem_raw" not in st.session_state:
    st.session_state.poem_raw = None
if "image_url" not in st.session_state:
    st.session_state.image_url = None
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None

# API Key Validation Banner
if not api_key:
    st.markdown(
        """
        <div class="api-alert">
            🔑 <strong>OpenAI API Key Required</strong><br>
            Please provide your OpenAI API key in the left sidebar to unlock the creative engine.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Centered Input Box and Button
    _, col_input, _ = st.columns([1, 2, 1])
    with col_input:
        input_string = st.text_input(
            "What theme or concept inspires you today?",
            placeholder="Type your topic (e.g., 'a lonely lighthouse', 'rusting memories', 'crimson sunset') and press Enter...",
            label_visibility="collapsed"
        )
        # Main generation trigger button
        generate_clicked = st.button("✨ Summon the Muse")
    
    # Trigger conditions
    should_generate = (generate_clicked or (input_string and input_string != st.session_state.active_topic))
    
    if should_generate and input_string:
        st.session_state.active_topic = input_string
        with st.spinner("💫 Weaving the tapestry of verses and painting the visual landscape..."):
            try:
                client = get_client(api_key)
                st.session_state.poem_raw = generate_poem_text(client, input_string, poem_tone, poem_structure, poem_length)
                st.session_state.image_url = generate_artwork(client, input_string, image_style)
            except Exception as e:
                st.error(f"Error communicating with OpenAI: {str(e)}")
                st.session_state.poem_raw = None
                st.session_state.image_url = None

    # Render results card if contents exist
    if st.session_state.poem_raw and st.session_state.image_url:
        poem_title, poem_body = parse_poem(st.session_state.poem_raw)
        
        # Replace line breaks with HTML line breaks for rendering inside custom card
        poem_body_html = poem_body.replace('\n', '<br>')
        
        st.markdown(
            f"""
            <div class="poetic-card">
                <div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center; justify-content: center;">
                    <div style="flex: 1; min-width: 320px; max-width: 450px;">
                        <div class="image-container">
                            <img src="{st.session_state.image_url}" class="poetic-image" alt="Generated Artwork">
                        </div>
                    </div>
                    <div style="flex: 1.3; min-width: 320px;" class="poem-container">
                        <div class="poem-title">{poem_title}</div>
                        <div class="poem-content">{poem_body_html}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Individual regeneration controls
        st.markdown("<div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'><span style='color: #64748B; font-size: 0.9rem;'>Refining details of this masterpiece?</span></div>", unsafe_allow_html=True)
        
        col_buttons = st.columns(2)
        with col_buttons[0]:
            if st.button("🔄 Regenerate Poem Only", key="regen_poem"):
                with st.spinner("Rewriting verses..."):
                    try:
                        client = get_client(api_key)
                        st.session_state.poem_raw = generate_poem_text(client, st.session_state.active_topic, poem_tone, poem_structure, poem_length)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        
        with col_buttons[1]:
            if st.button("🎨 Regenerate Image Only", key="regen_image"):
                with st.spinner("Repainting artwork..."):
                    try:
                        client = get_client(api_key)
                        st.session_state.image_url = generate_artwork(client, st.session_state.active_topic, image_style)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Modern Footer
footer_html = """
<div class="footer-container">
    Built with ❤ by <a href="https://github.com/Deyb12" target="_blank">Dave Fagarita</a> • Powered by Streamlit & OpenAI
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
