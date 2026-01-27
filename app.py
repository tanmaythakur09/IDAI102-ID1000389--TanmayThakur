import streamlit as st
import datetime
import random
import pandas as pd
import os

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="ShopImpact 🌱",
    layout="wide"
)

st.title("🌍 ShopImpact – Conscious Shopping Dashboard")
st.write("Track your purchases, understand their environmental impact, and make greener choices.")

# -------------------- DATA STRUCTURES --------------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []

impact_multipliers = {
    "Clothing": 1.5,
    "Electronics": 2.5,
    "Groceries": 0.8,
    "Footwear": 1.8,
    "Second-hand Items": 0.3
}

green_alternatives = {
    "Clothing": ["Organic Cotton Brands", "Thrift Stores"],
    "Electronics": ["Refurbished Devices", "Energy Star Products"],
    "Groceries": ["Local Produce", "Organic Markets"],
    "Footwear": ["Vegan Shoes", "Recycled Material Brands"],
    "Second-hand Items": ["Reuse & Resale Platforms"]
}

eco_tips = [
    "Buying second-hand can reduce carbon footprint significantly 🌱",
    "Local products usually travel less and pollute less 🚲",
    "Quality over quantity helps the planet 💚",
    "Refurbished electronics save resources ⚡"
]

# -------------------- INPUT SECTION --------------------
st.subheader("🛒 Log a Purchase")

col1, col2, col3 = st.columns(3)

with col1:
    product_type = st.selectbox("Product Type", list(impact_multipliers.keys()))

with col2:
    brand = st.text_input("Brand Name")

with col3:
    price = st.number_input("Price (₹)", min_value=0.0, step=1.0)

if st.button("Add Purchase"):
    impact = price * impact_multipliers[product_type]
    purchase = {
        "Date": datetime.date.today(),
        "Product": product_type,
        "Brand": brand,
        "Price": price,
        "CO2 Impact": impact
    }
    st.session_state.purchases.append(purchase)
    st.success("Purchase added successfully!")
    st.info(random.choice(eco_tips))

# -------------------- DASHBOARD --------------------
st.subheader("📊 Monthly Impact Dashboard")

if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)
    total_spend = df["Price"].sum()
    total_impact = df["CO2 Impact"].sum()

    colA, colB = st.columns(2)
    colA.metric("💰 Total Spend (₹)", round(total_spend, 2))
    colB.metric("🌫 Total CO₂ Impact", round(total_impact, 2))

    st.bar_chart(df.groupby("Product")["CO2 Impact"].sum())

    # -------------------- BADGES --------------------
    st.subheader("🏅 Your Eco Badge")

    if total_impact < 200:
        st.success("🌟 Eco Saver Badge Earned!")
    elif total_impact < 500:
        st.warning("👍 Low Impact Shopper")
    else:
        st.error("⚠ High Impact Alert – Try Greener Choices!")

    # -------------------- GREEN SUGGESTIONS --------------------
    st.subheader("🌿 Greener Alternatives")
    st.write(", ".join(green_alternatives[product_type]))

else:
    st.info("No purchases logged yet.")

if st.button("Draw Eco Leaf"):
    draw_leaf()


