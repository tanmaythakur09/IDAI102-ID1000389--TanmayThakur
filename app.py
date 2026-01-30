import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ShopImpact – Conscious Shopping",
    page_icon="🌱",
    layout="wide"
)

# ================= STYLING =================
st.markdown("""
<style>
.main { background-color: #f4faf6; }

section[data-testid="stSidebar"] {
    background-color: #e8f5e9;
}

.stButton > button {
    background-color: #2e7d32;
    color: white;
    border-radius: 10px;
    padding: 0.5em 1.2em;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1b5e20;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "data" not in st.session_state:
    st.session_state.data = {}

# ================= USERS =================
USERS = {
    "tanmay": "1234",
    "student": "password"
}

# ================= LOGIN PAGE =================
def login_page():
    st.markdown("<h1 style='text-align:center;'>🌍 ShopImpact</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;color:gray;'>Conscious Shopping Dashboard</h4>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🌱 Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.data.setdefault(username, [])
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ================= MAIN APP =================
def main_app():
    user = st.session_state.user
    purchases = st.session_state.data[user]

    # ---------- SIDEBAR ----------
    st.sidebar.markdown("## 🌱 ShopImpact")
    st.sidebar.markdown(f"👤 **User:** {user}")

    page = st.sidebar.radio(
        "📍 Navigation",
        ["📊 Dashboard", "🛒 Log Purchase", "♻️ Greener Tips"]
    )

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    impact_factor = {
        "Clothing": 3.0,
        "Electronics": 4.5,
        "Groceries": 1.5,
        "Footwear": 2.5,
        "Second-hand": 0.8
    }

    # ================= LOG PURCHASE =================
    if page == "🛒 Log Purchase":
        st.header("🛒 Log a Purchase")

        col1, col2 = st.columns(2)
        product = col1.selectbox("📦 Product Type", impact_factor.keys())
        brand = col2.text_input("🏷️ Brand Name")

        price = st.number_input("💰 Price (₹)", min_value=0.0, step=50.0)

        st.caption(f"🌍 Estimated CO₂ Impact: **{price * impact_factor[product]:.1f} units**")

        if st.button("➕ Add Purchase") and price > 0:
            purchases.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Product": product,
                "Brand": brand.title(),
                "Price": price,
                "CO2": price * impact_factor[product]
            })
            st.success("Purchase added successfully 🌿")

        st.divider()

        if st.button("🌱 Add Eco-Friendly Demo Purchase"):
            purchases.append({
                "Date": "Demo",
                "Product": "Second-hand",
                "Brand": "Thrift Store",
                "Price": 500,
                "CO2": 200
            })
            st.info("Eco-friendly demo purchase added")

    # ================= DASHBOARD =================
    if page == "📊 Dashboard":
        st.header("📊 Monthly Impact Dashboard")

        if not purchases:
            st.warning("No purchases logged yet.")
            return

        df = pd.DataFrame(purchases)

        total_spend = df["Price"].sum()
        total_impact = df["CO2"].sum()
        eco_score = max(0, 100 - int(total_impact / 150))

        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Total Spend (₹)", f"{total_spend:.0f}")
        c2.metric("🌍 CO₂ Impact", f"{total_impact:.0f}")
        c3.metric("🌱 Eco Score", f"{eco_score}/100")

        st.subheader("CO₂ Impact by Category")
        st.bar_chart(df.groupby("Product")["CO2"].sum())

        st.subheader("Eco Score Progress")
        st.progress(eco_score / 100)

        if eco_score >= 75:
            st.success("🌿 Excellent! You're an eco-conscious shopper!")
        elif eco_score >= 40:
            st.warning("🌼 Good effort—there's room to improve!")
        else:
            st.error("🚨 High impact detected—try greener choices!")

        with st.expander("📄 View Purchase History"):
            st.dataframe(df, use_container_width=True)

    # ================= GREENER TIPS =================
    if page == "♻️ Greener Tips":
        st.header("♻️ Greener Shopping Tips")

        tips = [
            "Buy second-hand clothing 👕",
            "Choose refurbished electronics 🔌",
            "Avoid fast fashion 🚫",
            "Carry reusable bags 🛍️",
            "Support local brands 🏪"
        ]

        st.success(random.choice(tips))
        st.caption("Small choices today create a big impact 🌍")

# ================= APP FLOW =================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()

st.markdown("---")
st.caption("🌱 ShopImpact • Conscious Shopping Dashboard")


