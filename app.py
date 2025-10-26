import streamlit as st

# Page config
st.set_page_config(page_title="About LexiAI", layout="wide")

# CSS Styles
st.markdown("""
<style>
body {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f9f9;
}
.header {
    background: linear-gradient(120deg, #b0f2b6, #fdd9a8);
    text-align: center;
    padding: 60px 20px;
    border-radius: 0 0 50% 50% / 10%;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.header h1 {
    font-size: 3rem;
    margin-bottom: 10px;
}
.header p {
    font-size: 1.5rem;
    font-style: italic;
    color: #555;
}
.section {
    padding: 60px 20px;
    text-align: center;
}
.section h2 {
    font-size: 2rem;
    color: #4caf50;
    margin-bottom: 20px;
}
.section p {
    max-width: 800px;
    margin: 0 auto 30px auto;
    font-size: 1.1rem;
}
.cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
}
.card {
    background: #fff;
    border-radius: 15px;
    padding: 30px;
    width: 250px;
    text-align: center;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}
.card .icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
    color: #ff9800;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.cta button, .get-started {
    background: linear-gradient(120deg, #b0f2b6, #fdd9a8);
    border: none;
    padding: 15px 30px;
    margin: 10px;
    border-radius: 30px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}
.cta button:hover, .get-started:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
input, button {
    font-family: 'Roboto', sans-serif;
}
@media(max-width:768px) {
    .cards {
        flex-direction: column;
        align-items: center;
    }
}
</style>
""", unsafe_allow_html=True)


# Define pages (About vs Sign In)
if "page" not in st.session_state:
    st.session_state.page = "about"

# HEADER PAGE
if st.session_state.page == "about":
    st.markdown("""
    <div class="header">
        <h1>LexiAI</h1>
        <p>"Giving every child a voice in their learning"</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Started 🚀", use_container_width=True):
        st.session_state.page = "signin"
        st.rerun()

    # Mission
    st.markdown("""
    <div class="section">
        <h2>Our Mission 🎯</h2>
        <p>At LexiAI, we believe that every child deserves a fair chance to learn and succeed.
        Our mission is to make personalized education accessible to children with learning differences,
        delayed literacy, or those in underserved rural communities.
        We combine cutting-edge AI with child-friendly learning tools to make every learning journey engaging and fun.</p>
    </div>
    """, unsafe_allow_html=True)

    # Who We Serve
    st.markdown("""
    <div class="section" style="background:#e8f5e9; border-radius:20px;">
        <h2>Who We Serve 👩‍🏫</h2>
        <p>LexiAI is designed for children of all abilities, especially those in government schools or supported by NGOs. We focus on:</p>
        <div class="cards">
            <div class="card">
                <div class="icon">🧠</div>
                <p>Children with learning disabilities</p>
            </div>
            <div class="card">
                <div class="icon">📖</div>
                <p>Children with delayed literacy</p>
            </div>
            <div class="card">
                <div class="icon">🏫</div>
                <p>Kids in rural areas with limited access to quality education</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # What We Offer
    st.markdown("""
    <div class="section">
        <h2>What We Offer 📚</h2>
        <div class="cards">
            <div class="card">
                <div class="icon">🎯</div>
                <p>Personalized learning paths tailored to each child</p>
            </div>
            <div class="card">
                <div class="icon">🤖</div>
                <p>Interactive reading assistance with AI feedback</p>
            </div>
            <div class="card">
                <div class="icon">🎮</div>
                <p>Fun, engaging educational games and stories</p>
            </div>
            <div class="card">
                <div class="icon">🏆</div>
                <p>Progress tracking to celebrate every achievement</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vision
    st.markdown("""
    <div class="section" style="background:#fff3e0; border-radius:20px;">
        <h2>Our Vision 🌟</h2>
        <p>We envision a world where every child can learn confidently, express themselves,
        and reach their full potential—without barriers or limitations.</p>
    </div>
    """, unsafe_allow_html=True)


# SIGN-IN PAGE
elif st.session_state.page == "signin":
    st.markdown("""
    <div style="background: linear-gradient(120deg, #b0f2b6, #fdd9a8); padding:100px 20px; border-radius:20px; text-align:center;">
        <h2>Sign In / Log In 🔑</h2>
        <p>Welcome back! Let’s continue your LexiAI journey.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In")

        if submit:
            if email and password:
                st.session_state.authenticated = True
                st.switch_page("dashboard.py")
            else:
                st.error("Please enter both email and password.")
