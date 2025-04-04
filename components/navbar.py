import streamlit as st

def render_navbar():
    """
    Renders the navigation bar component with user info and navigation options.
    Only shows when user is logged in.
    """
    # Custom CSS for navbar
    st.markdown("""
        <style>
        /* Hide sidebar when not logged in */
        .sidebar:not(:has(.sidebar-content)) {
            display: none !important;
        }
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 1rem;
        }
        /* Logo section */
        .logo-section {
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid #e1e4e8;
            margin-bottom: 1rem;
        }
        .logo-section h1 {
            color: #1f77b4;
            font-size: 1.5rem;
            margin: 0;
            padding: 0;
        }
        /* Navigation menu */
        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .nav-item {
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            color: #333;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .nav-item:hover {
            background-color: #f0f2f6;
            color: #1f77b4;
        }
        .nav-item.active {
            background-color: #1f77b4;
            color: white;
        }
        /* User info section */
        .user-info {
            margin-top: auto;
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            border: 1px solid #e1e4e8;
        }
        .user-info p {
            margin: 0;
            text-align: center;
        }
        .user-info .email {
            color: #1f77b4;
            font-weight: bold;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # # Logo and Title
        # st.markdown("""
        #     <div class="logo-section">
        #         <h1>🔬 Prakriti Identification</h1>
        #     </div>
        # """, unsafe_allow_html=True)

        # Navigation Menu
        # st.markdown("""
        #     <div class="nav-menu">
        #         <a class="nav-item" href="?page=Home">🏠 Home</a>
        #         <a class="nav-item" href="?page=Assessment">📸 Assessment</a>
        #         <a class="nav-item" href="?page=History">📜 History</a>
        #         <a class="nav-item" href="?page=Profile">👤 Profile</a>
        #         <a class="nav-item" href="?page=Settings">⚙️ Settings</a>
        #         <a class="nav-item" href="?page=Logout">🚪 Logout</a>
        #     </div>
        # """, unsafe_allow_html=True)

        # User Info
        if "user" in st.session_state:
            st.markdown(f"""
                <div class="user-info">
                    <p style='color: #666;'>Logged in as:</p>
                    <p class="email">{st.session_state["user"]["email"]}</p>
                </div>
            """, unsafe_allow_html=True)

    # Get current page from URL parameters
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["Home"])[0]
    return page 