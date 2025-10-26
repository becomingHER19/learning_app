import streamlit as st
import random

# ------------------- Page config -------------------
st.set_page_config(page_title="LexiAI Dashboard", layout="wide")

# ------------------- Initialize session state -------------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'dashboard'

if 'feedback_count' not in st.session_state:
    st.session_state['feedback_count'] = 0

# ------------------- CSS Styling -------------------
st.markdown("""
<style>
body {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f9f9;
    color: #333;
}
.header {
    background: linear-gradient(120deg, #b0f2b6, #fdd9a8);
    padding: 50px 20px;
    border-radius: 0 0 50% 50% / 10%;
    text-align: center;
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
    padding: 40px 20px;
    text-align: center;
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
    cursor: pointer;
}
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}
.card h3 {
    margin-top: 10px;
}
.sidebar .sidebar-content {
    background-color: #fdf5e6;
    padding: 20px;
    border-radius: 15px;
}
button {
    background: linear-gradient(120deg, #b0f2b6, #fdd9a8);
    border: none;
    padding: 10px 25px;
    margin: 10px 0;
    border-radius: 20px;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}
button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ------------------- Sidebar -------------------
st.sidebar.title("Settings ⚙️")
username = st.sidebar.text_input("Username")
st.sidebar.button("Update Profile")

# ------------------- Page Routing -------------------
page = st.session_state['page']

# ------------------- Dashboard -------------------
if page == 'dashboard':
    quotes = [
        "Every child is a star in their own way ✨",
        "Learning is a journey, not a race 🚀",
        "Empower. Educate. Excel 💡",
        "Small steps lead to big achievements 🏆"
    ]

    st.markdown(f"""
    <div class="header">
        <h1>Welcome, {username if username else 'LexiAI User'}!</h1>
        <p>{random.choice(quotes)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section"><h2>Explore</h2></div>', unsafe_allow_html=True)

    # Cards as columns with buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 Read and Learn"):
            st.session_state['page'] = 'read_and_learn'
            st.rerun()
        st.markdown("""
        <div class="card">
            <h3>📚 Read and Learn</h3>
            <p>Explore interactive lessons and reading materials</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🧮 Math Buddy"):
            st.session_state['page'] = 'math_buddy'
            st.rerun()
        st.markdown("""
        <div class="card">
            <h3>🧮 Math Buddy</h3>
            <p>AI-assisted problem solving and hints for children</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🎨 Activities</h3>
            <p>Fun learning activities and games</p>
        </div>
        """, unsafe_allow_html=True)

    # Quick Links
    st.markdown('<div class="section"><h2>Quick Links</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Support / Feedback"):
            st.session_state['page'] = 'feedback'
            st.experimental_rerun()
    with col2:
        st.markdown('[Email us](mailto:lexiai@gmail.com)', unsafe_allow_html=True)

# ------------------- Read and Learn Page -------------------
elif page == 'read_and_learn':
    st.title("📚 Read and Learn")
    st.write("Welcome to the Read and Learn section!")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()

# ------------------- Math Buddy Page -------------------
elif page == 'math_buddy':
    st.title("🧮 Math Buddy")
    st.write("Solve problems and get AI hints here!")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()

# ------------------- Feedback Page -------------------
elif page == 'feedback':
    st.title("💬 Feedback & Support")
    rating = st.slider("Rate LexiAI:", 1, 5, 3)
    feedback_text = st.text_area("Write your feedback:")

    if st.button("Submit Feedback"):
        st.session_state['feedback_count'] += 1
        st.success(f"Thanks for your feedback! Total feedback received: {st.session_state['feedback_count']}")
        st.write("Your rating:", rating)
        st.write("Your message:", feedback_text)

    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()
