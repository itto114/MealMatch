import streamlit as st
import pandas as pd

st.set_page_config(page_title="MealMatch 🍽️", layout="centered")
st.title("🍽️ MealMatch - มื้อไหนดี?")

# === ตัวเลือกจากผู้ใช้ ===
user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

# === ข้อมูลร้านอาหารตัวอย่าง ===
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "100 - 200", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "เย็น", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}

df = pd.DataFrame(data)

# === ฟังก์ชันกรองร้าน ===
def filter_restaurants(location, food_type, price_range, time_of_day):
    return df[
        (df['location'] == location) &
        (df['choice'] == food_type) &
        (df['budget'] == price_range) &
        (df['time'] == time_of_day)
    ]['name'].tolist()

# === การแสดงผลลัพธ์ ===
if st.button("🔍 ค้นหาร้านอาหาร"):
    matched_restaurants = filter_restaurants(user_location, user_choice, user_budget, user_time)

    if matched_restaurants:
        st.success("ร้านที่ตรงกับคุณมีดังนี้ 🍜")
        selected_store = st.radio("เลือกร้านที่คุณสนใจ:", matched_restaurants)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ เลือกร้านนี้"):
                st.info(f"คุณเลือกร้าน: {selected_store} ✅ ขอบคุณสำหรับการเลือก!")
        with col2:
            if st.button("❌ ไม่มีร้านไหนที่ตรงใจ"):
                st.warning("ขอบคุณสำหรับความคิดเห็น! ระบบจะนำไปปรับปรุงต่อไป 🙏")

    else:
        st.error("ไม่พบร้านอาหารที่ตรงกับตัวเลือกของคุณ 😥 ลองเปลี่ยนตัวเลือกดูนะ")
