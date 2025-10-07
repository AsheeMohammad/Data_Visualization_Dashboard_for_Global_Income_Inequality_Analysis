import streamlit as st
from auth_module import signup, login, send_otp, update_password
from streamlit_lottie import st_lottie
import requests
import os


def centered_layout(content_func):
    """Reusable wrapper to center page content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        content_func()

st.set_page_config(page_title="Animated Login System", layout="wide")
# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "mode" not in st.session_state:
    st.session_state.mode = "Login"
if "page" not in st.session_state:
    st.session_state.page = "Home"
# OTP and reset_email are internal (not used as widget keys)
if "otp" not in st.session_state:
    st.session_state.otp = ""
if "reset_email" not in st.session_state:
    st.session_state.reset_email = ""
if "theme" not in st.session_state:
    st.session_state.theme = "System (Default)"
# ---------------- Lottie Loader ----------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            st.warning(f"Lottie URL failed: {url}")
            return {}
        return r.json()
    except Exception as e:
        st.warning(f"Error loading Lottie animation: {e}")
        return {}
# Helpers for Forgot Password
def verify_otp(entered_otp: str) -> bool:
    return entered_otp == st.session_state.otp
def reset_password(email: str, new_password: str) -> bool:
    return auth.update_password(email, new_password)
# LOGIN / SIGNUP / FORGOT UI
def auth_ui():
    # Custom CSS for titles, labels, and inputs
    st.markdown("""
        <style>
        /* App main title */
        .app-title {
            font-size: 72px;
            font-weight: 800;
            color: #ffffff;
            text-align: center;
            margin-bottom: 2rem;
        }
        /* Section titles like 🔐 Login, ✨ Signup */
        .login-title {
            font-size: 50px;
            font-weight: bold;
            color: #1abc9c;
            margin-bottom: 1rem;
            text-align: center;
        }
        /* ✅ Fix: Bigger labels for Email, Password, Username, OTP */
        div[data-testid="stTextInput"] > div > div > p,
        div[data-testid="stPasswordInput"] > div > div > p {
            font-size: 100px !important;   /* bigger font */
            font-weight: bold !important;  /* bold */
            color: #ffffff !important;    /* white */
        }
        /* Input box text */
        input {
            font-size: 18px !important;
            height: 45px !important;
        }
        /* Centered buttons with hover effect */
        div.stButton {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        /* Streamlit buttons - full width & centered */
        div.stButton > button {
            width: 100% !important;       /* FULL WIDTH inside its column */
            padding: 1rem;
            border-radius: 30px;
            font-size: 24px;
            font-weight: bold;
            background-color: #1abc9c !important;
            color: white !important;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-15px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.2);
            background-color: #16a085 !important;
        }

        </style>
    """, unsafe_allow_html=True)

    # 🔥 Add the main app title here
    st.markdown('<div class="app-title">✨Welcome to Global Income Inequality Dashboard✨</div>', unsafe_allow_html=True)
    # 🔥 Centered Login GIF
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://assets-v2.lottiefiles.com/a/fe0a9612-83f3-11ee-9945-27ca59862aef/gMMelbR6U7.gif",
            use_container_width=True
        )

    # ---------------- LOGIN ----------------
    if st.session_state.mode == "Login":
        st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)
        # Center column for inputs and button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Email & Password inputs
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

            # CSS for Login button
            st.markdown("""
                <style>
                .login-btn button {
                    width: 100% !important;
                    height: 55px !important;
                    font-size: 22px !important;
                    font-weight: bold !important;
                    color: white !important;
                    background-color: #1abc9c !important;
                    border-radius: 10px !important;
                    border: none !important;
                    transition: all 0.3s ease;
                }
                .login-btn button:hover {
                    background-color: #16a085 !important;
                    transform: translateY(-2px);
                    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
                }
             </style>
            """, unsafe_allow_html=True)

            # Login button
            login_clicked = st.button("Login", key="login_btn", use_container_width=True, args=(), kwargs={})
            if login_clicked:
                if not login_email or not login_password:
                    st.error("Please enter email and password")
                else:
                    ok, msg = login(login_email, login_password)
                    if ok:
                        st.session_state.logged_in = True
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
            # Sign Up (left) + Forgot Password (right)
            col_left, col_right = st.columns([1, 1])
            with col_left:
                if st.button("Sign Up", key="goto_signup_btn", use_container_width=True):
                    st.session_state.mode = "Signup"
                    st.rerun()
            with col_right:
                if st.button("Forgot Password", key="forgot_btn", use_container_width=True):
                    st.session_state.mode = "ForgotPassword"
                    st.rerun()

    # ---------------- SIGNUP ----------------
    elif st.session_state.mode == "Signup":
        st.markdown('<div class="login-title">📝 Sign Up</div>', unsafe_allow_html=True)
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.button("Sign Up", key="signup_btn"):
            if not signup_email or not signup_password or not signup_confirm:
                st.error("Please fill all fields")
            elif signup_password != signup_confirm:
                st.error("Passwords do not match")
            else:
                ok, msg = signup(signup_email, signup_password)
                if ok:
                    st.success(msg)
                    st.session_state.mode = "Login"
                    st.rerun()
                else:
                    st.error(msg)
        if st.button("Go to Login", key="goto_login_btn"):
            st.session_state.mode = "Login"
            st.rerun()

    # ---------------- FORGOT PASSWORD ----------------
    elif st.session_state.mode == "ForgotPassword":
        st.markdown('<div class="login-title">🔑 Forgot Password</div>', unsafe_allow_html=True)
        # NOTE: widget key is "forgot_email" but we do NOT assign its return to st.session_state directly
        forgot_email = st.text_input("Enter your registered email", key="forgot_email")
        if st.button("Send OTP", key="send_otp_btn"):
            if not forgot_email:
                st.error("Please enter your email")
            else:
                otp = send_otp(forgot_email)  # store the OTP returned by send_otp
                if otp:
                    st.session_state.otp = otp
                    st.session_state.reset_email = forgot_email
                    st.success(f"OTP sent to {forgot_email}. Check your inbox.")
                    st.session_state.mode = "OTPVerification"
                    st.rerun()
                else:
                    st.error("Failed to send OTP. Try again.")
        if st.button("Back to Login", key="back_from_forgot_btn"):
            st.session_state.mode = "Login"
            st.rerun()

    # ---------------- OTP VERIFICATION ----------------
    elif st.session_state.mode == "OTPVerification":
        st.markdown('<div class="login-title">🔒 Verify OTP</div>', unsafe_allow_html=True)
        # OTP input is a widget with its own key; we read it into a local var
        entered_otp = st.text_input("Enter OTP", key="otp_input")
        new_password = st.text_input("Enter New Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
        if st.button("Reset Password", key="reset_password_btn"):
            if not entered_otp or not new_password or not confirm_password:
                st.error("Please fill all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif not verify_otp(entered_otp):
                st.error("Invalid OTP")
            else:
                # reset_email is stored when send_otp() ran
                if reset_password(st.session_state.reset_email, new_password):
                    st.success("Password reset successfully!")
                    # clear OTP so it can't be reused
                    st.session_state.otp = ""
                    st.session_state.reset_email = ""
                    st.session_state.mode = "Login"
                    st.rerun()
                else:
                    st.error("Error resetting password. Try again.")

        if st.button("Back to Login", key="back_from_otp_btn"):
            st.session_state.mode = "Login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Theme Selector ----------------
def render_theme_selector():
    """Dropdown at top-right corner to select theme globally"""
    st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
    theme_options = {
        "🌐 System (Default)": "System (Default)",
        "🌙 Dark": "Dark",
        "☀️ White": "White"
    }
    selected_icon = st.selectbox(
        "",  # no label
        options=list(theme_options.keys()),
        index=list(theme_options.values()).index(st.session_state.theme)
    )
    st.session_state.theme = theme_options[selected_icon]
    st.markdown('</div>', unsafe_allow_html=True)

def apply_theme():
    """Apply selected theme CSS globally"""
    if st.session_state.theme == "Dark":
        st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] {background-color: #111111 !important;}
            [data-testid="stSidebar"] {background-color: #1c1c1c !important;}
            [data-testid="stHeader"], [data-testid="stToolbar"] {background-color: #111111 !important;}
            .css-1d391kg, .css-ffhzg2 {color: #f5f5f5 !important;}
            .stButton>button {background-color: #1abc9c !important; color: white !important;}
            </style>
        """, unsafe_allow_html=True)
    elif st.session_state.theme == "White":
        st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] {background-color: #ffffff !important; color: #000000 !important;}
            [data-testid="stSidebar"] {background-color: #f0f2f6 !important; color: #000000 !important;}
            [data-testid="stHeader"], [data-testid="stToolbar"] {background-color: #ffffff !important; color: #000000 !important;}
            .css-1d391kg, .css-ffhzg2, .stMarkdown, p, h1, h2, h3, h4, h5, h6, span {color: #000000 !important;}
            .stButton>button {background-color: #1abc9c !important; color: white !important;}
            </style>
        """, unsafe_allow_html=True)

# ---------------- DASHBOARD UI ----------------
def dashboard_ui():
    # Render theme selector at top-right
    render_theme_selector()
    apply_theme()
    # Lottie container styling (keeps your app look)
    st.markdown("""
    <style>
    /* Sidebar container fix (ensures alignment) */
    [data-testid="stSidebar"] {
        padding-top: 20px;
    }

    /* Divi-style full-width buttons */
    [data-testid="stSidebar"] .stButton>button {
        display: block;
        width: 150% !important;      /* All same width */
        height: 50px !important;     /* All same height */
        background-color: #0056b3 !important;
        color: #fff !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 8px;          /* Rectangle look */
        border: none;
        text-align: center;
        margin: 5px 0;               /* Equal spacing between buttons */
        transition: all 0.3s ease-in-out;
    }

    /* Hover effect */
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #007bff !important;
        transform: translateY(-2px);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
    }

    /* Active button highlight */
    [data-testid="stSidebar"] .stButton>button:focus {
        background-color: #0e6655 !important;
        color: #fff !important;
        outline: none;
    }
    </style>
""", unsafe_allow_html=True)
    
    # ---------------- Sidebar Welcome Card ----------------
    st.sidebar.markdown(
        f"""
        <div style="
            background-color: #26b3e6;
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 20px;
        ">
        👋 Welcome, Ashee!
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- CSS for Centered & Equal-Sized Buttons ----------------
    st.sidebar.markdown(
        """
        <style>
        /* Make sidebar a centered column */
        [data-testid="stSidebar"] {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 18px;
        }
        /* Target Streamlit button elements strongly and force fixed size */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] div.stButton > button {
            box-sizing: border-box !important;
            width: 200px !important;       /* fixed width */
            min-width: 200px !important;
            max-width: 200px !important;
            height: 52px !important;       /* fixed height */
            margin: 10px 0 !important;     /* even spacing */
            padding: 0 14px !important;    /* keep inner padding consistent */
            display: flex !important;      
            justify-content: center !important; /* center text horizontally */
            align-items: center !important;     /* center text vertically */
            white-space: nowrap !important;     /* prevent wrap */
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            background-color: #26b3e6 !important; /* your color */
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            border-radius: 12px !important;
            border: none !important;
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        /* Ensure inner span/div inside button fills full width and centers content */
        [data-testid="stSidebar"] .stButton > button > span,
        [data-testid="stSidebar"] .stButton > button > div {
            display: inline-flex !important;
            width: 100% !important;
            justify-content: center !important;
            align-items: center !important;
        }
        /* Hover */
        [data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 14px rgba(0,0,0,0.18) !important;
            background-color: #17a0cf !important;
        }
        /* Extra gap before logout */
        .logout-spacer { height: 36px; width: 100%; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Navigation title
    st.sidebar.markdown('<div style="width:100%; padding-left:12px; color:#800080; font-weight:700; font-size:23px; margin-bottom:6px;">Navigation</div>', unsafe_allow_html=True)
    # Buttons (these are normal Streamlit buttons)
    if st.sidebar.button("🏠  Home", key="sidebar_Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("📊  Dashboard", key="sidebar_Dashboard"):
        st.session_state.page = "Dashboard"

    if st.sidebar.button("📈 Insights", key="sidebar_Insights"):
        st.session_state.page = "Insights"

    if st.sidebar.button("👤  Profile", key="sidebar_Profile"):
        st.session_state.page = "Profile"
    if st.sidebar.button("💬  Feedback", key="sidebar_Feedback"):
        st.session_state.page = "Feedback"

    # Spacer so Logout is separated
    st.sidebar.markdown('<div class="logout-spacer"></div>', unsafe_allow_html=True)
    if st.sidebar.button("📕  Logout", key="sidebar_Logout"):
        st.session_state.logged_in = False
        st.session_state.mode = "Login"
        st.rerun()

    #--------------- Home-----------------
    if st.session_state.page == "Home":
        def home_content():
            st.markdown(
                "<h1 style='text-align: center; font-size: 45px;'>🏠 Project Insights & Analysis</h1>",
                unsafe_allow_html=True,
            )
            # Animation
            lottie_home = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
            st_lottie(lottie_home, speed=1, width=900, height=350, key="home_animation")
            # Description (centered and larger text)
            st.markdown(
                "<h2 style='font-size: 28px;'>📌 Project Description</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size: 20px; line-height: 1.6;'>"
                "This project is a <b>Streamlit-based Login and Signup System</b> with a modern UI. "
                "It integrates interactive dashboards, insights visualization, and AI chatbot support. "
                "The application is designed to provide a seamless and engaging experience for users."
                "</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h2 style='font-size:28 px;'>📊 Dashboard Overview</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size: 20px; line-height: 1.6;'>"
                "This interactive Power BI dashboard provides a comprehensive visualization of key metrics and insights, enabling users to explore trends, patterns, and performance at a glance. "
                "Designed for clarity and interactivity, it helps in making data-driven decisions efficiently."
                "</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<h2 style='font-size:28 px;'>🎯 Objectives</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size: 20px; line-height: 1.6;'>"
                "1. Develop a web app with a clean UI for user management. <br>" 
                "2. Ensure persistent storage of user data using TinyDB. <br>"  
                "3. Integrate Power BI dashboards for analytics. <br>"
                "4. Collect and manage user feedback effectively."
                "</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<h2 style='font-size:28 px;'>✨ Key Features</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size: 20px; line-height: 1.6;'>"
                "🟢 Signup and Login with validation. <br>"
                "🟢 Interactive sidebar navigation. <br>"
                "🟢 Embedded Power BI dashboards for real-time insights. <br>"
                "🟢 Feedback collection form. <br>"
                "🟢 Responsive and modern design. "
                "</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<h2 style='font-size:28 px;'>💡 Insights</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size: 20px; line-height: 1.6;'>"
                "➡️ User registrations are steadily increasing each month. <br>"
                "➡️ Feedback shows growing engagement and interaction. <br>"
                "➡️ The system can be extended for role-based dashboards in future. "
                "</p>",
                unsafe_allow_html=True
            )
        centered_layout(home_content)

    #------------------Dashboard----------------------------------------
    elif st.session_state.page == "Dashboard":
        # Heading (centered)
        st.markdown(
            "<h1 style='text-align:center; font-size:45px;'>📊 Dashboard</h1>",
            unsafe_allow_html=True
        )
        # Centered GIF using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "https://cdnl.iconscout.com/lottie/premium/thumb/web-dashboard-animation-gif-download-4596740.gif",
                use_container_width=True  # updated parameter
            )
        # ---------------- Left-aligned content ----------------
        st.subheader("Power BI Dashboard Overview")
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGE0ZWJlOWUtYjYxNS00Mzc1LTg2ODktMjA0YjNhNzQxNTFiIiwidCI6ImRiYTUxZDMwLTA2MGMtNDVhNC1hOTUyLTUyMWU4YWQ1OWE2OCJ9"

        st.markdown(f"""
            <div class="powerbi-container">
                <iframe title="PowerBI Dashboard"
                    width="100%" height="700"
                    src="{powerbi_url}"
                    frameborder="0" allowFullScreen="true"></iframe>
            </div>
        """, unsafe_allow_html=True)

     #--------------------Insights Section----------------------------------------
    elif st.session_state.page == "Insights":
        def insights_content():
            # Title with bigger font
            st.markdown(
                "<h1 style='text-align:center; font-size:45px;'>📈 Insights & Key Learnings</h1>",
                unsafe_allow_html=True
            )
            # 🚀 User Engagement Trends
            st.markdown("<h2 style='font-size:28px;'>🚀 User Engagement Trends</h2>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-size:20px; line-height:1.8;'>"
                "Our analytics reveal a <b>steady increase in user engagement</b> over the last few weeks.<br>"
                "The login frequency indicates that users are returning consistently,<br>"
                "suggesting growing trust in the platform."
                "</p>",
                unsafe_allow_html=True
            )
            # 📊 Dashboard Utilization
            st.markdown("<h2 style='font-size:28px;'>📊 Dashboard Utilization</h2>", unsafe_allow_html=True)
            st.markdown(
                """
                <ul style='font-size:20px; line-height:1.8;'>
                    <li>Monthly Active Users (MAU)</li>
                    <li>Feedback Sentiment Analysis</li>
                    <li>Sign-up Growth Patterns</li>
                </ul>
                """,
                unsafe_allow_html=True
            )
            # 🎯 Business Insights
            st.markdown("<h2 style='font-size:28px;'>🎯 Business Insights</h2>", unsafe_allow_html=True)
            st.markdown(
                """
                <ul style='font-size:20px; line-height:1.8;'>
                    <li><b>Sign-up growth</b> is strongest at the beginning of each month.</li>
                    <li><b>Feedback sentiment</b> is largely positive, but UI performance could improve.</li>
                    <li><b>Returning user ratio</b> is 60%+, showing strong retention.</li>
                </ul>
                """,
                unsafe_allow_html=True
            )
            # ✨ Recommendations
            st.markdown("<h2 style='font-size:28px;'>✨ Recommendations</h2>", unsafe_allow_html=True)
            st.markdown(
                """
                <ol style='font-size:20px; line-height:1.8;'>
                    <li>Strengthen onboarding with guided walkthroughs</li>
                    <li>Enhance dashboard performance to reduce load time</li>
                    <li>Introduce role-based dashboards</li>
                    <li>Encourage feedback loops for evolving user needs</li>
                </ol>
                """,
                unsafe_allow_html=True
            )
        # Wrap into center layout
        centered_layout(insights_content)

    #-----------------------Profile------------------
    elif st.session_state.page == "Profile":
        # Personal Information (centered in a card)
        def profile_info_content():
            st.markdown(
                "<h1 style='text-align:center; font-size:36px;'>👤 Profile</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style="
                    background-color: #595959;
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    text-align: center;
                    width: 80%;
                    margin: auto;
                    margin-bottom: 30px;
                ">
                    <h2 style="font-size:26px; margin-bottom:15px;">Personal Information</h2>
                    <p style="font-size:20px; line-height:1.8; margin:0;">
                        <b>Name:</b> Mohammad Ashee <br>
                        <b>Username:</b> Ashee_Md <br>
                        <b>Email:</b> asheemohammad123@gmail.com <br>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        centered_layout(profile_info_content)  # 👈 Profile card centered

        # Update Profile Section (centered but no card)
        def update_profile_content():
            st.markdown("<h2 style='text-align:center; font-size:36px; margin-top:30px;'>Update Profile Information</h2>", unsafe_allow_html=True)

            with st.form("update_profile_form"):
                st.markdown(
                    """
                    <div style="display:flex; justify-content:center; flex-direction:column; align-items:center; gap:10px; width:100%;">
                    """,
                    unsafe_allow_html=True
                )

                new_name = st.text_input("Full Name", key="update_name", max_chars=50, help="Enter your full name")
                new_username = st.text_input("Username", key="update_username", max_chars=30, help="Enter your username")
                new_email = st.text_input("Email", key="update_email", max_chars=50, help="Enter your email")
                submitted = st.form_submit_button("Update Profile")
                if submitted:
                    st.success("✅ Profile updated successfully!")
                st.markdown("</div>", unsafe_allow_html=True)

        centered_layout(update_profile_content)  # Form centered cleanly

    #--------------Feedback----------------------
    elif st.session_state.page == "Feedback":
        def feedback_content():
            st.markdown(
                "<h1 style='text-align:center; font-size:36px;'>💬 Feedback</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    width: 60%;
                    font-size:28px;
                    margin: auto;
                ">
                """,
                unsafe_allow_html=True
            )
            # Feedback text area
            feedback = st.text_area("Enter your feedback here:", height=150, key="feedback_text")
            # Submit button
            if st.button("Submit Feedback", key="submit_feedback_btn"):
                st.success("✅ Thanks for your feedback!")
            st.markdown("</div>", unsafe_allow_html=True)
        centered_layout(feedback_content)
    
    #--------------------Logout-----------------
    elif st.session_state.page == "Logout":
        st.session_state.logged_in = False
        st.session_state.mode = "Login"
        st.rerun()
        pass

# ---------------- MAIN APP ----------------
if not st.session_state.logged_in:
    auth_ui()  # your auth UI
else:
    dashboard_ui()
