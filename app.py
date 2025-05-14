import streamlit as st
import pandas as pd

# สร้าง page config
st.set_page_config(page_title="MealMatch 🍽️", layout="centered")
st.title("🍽️ MealMatch - มื้อไหนดี?")

# === ข้อมูลร้านอาหารตัวอย่าง ===
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}

df = pd.DataFrame(data)

# === การเก็บข้อมูล Feedback ===
feedback_file = "user_feedback.csv"
# ตรวจสอบว่าไฟล์มีอยู่แล้วหรือไม่ ถ้าไม่ให้สร้างใหม่
try:
    feedback_df = pd.read_csv(feedback_file)
except FileNotFoundError:
    feedback_df = pd.DataFrame(columns=["location", "choice", "budget", "time", "selected_restaurant"])

# === ตัวเลือกจากผู้ใช้ ===
user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

# === ฟังก์ชันกรองร้าน ===
def filter_restaurants(location, food_type, price_range, time_of_day):
    return df[
        (df['location'] == location) & 
        (df['choice'] == food_type) & 
        (df['budget'] == price_range) & 
        (df['time'] == time_of_day)
    ]['name'].tolist()

# === การแสดงผลลัพธ์ ===
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    matched_restaurants = filter_restaurants(user_location, user_choice, user_budget, user_time)

    if matched_restaurants:
        selected_store = st.radio("เลือกร้านที่คุณสนใจ:", matched_restaurants)
        
        # แสดง feedback จากผู้ใช้งานก่อนหน้า
        st.subheader("📝 ความคิดเห็นจากผู้ใช้งานก่อนหน้า")
        st.write(feedback_df)

        if st.button("✅ เลือกร้านนี้"):
            # บันทึกข้อมูล feedback ใหม่
            feedback_df = feedback_df.append({
                "location": user_location,
                "choice": user_choice,
                "budget": user_budget,
                "time": user_time,
                "selected_restaurant": selected_store
            }, ignore_index=True)

            feedback_df.to_csv(feedback_file, index=False)
            st.info(f"คุณเลือกร้าน: {selected_store} ✅ ขอบคุณสำหรับการเลือก!")

        if st.button("❌ ทำใหม่"):
            # รีเซ็ตการทำแบบสอบถาม
            st.session_state.form_submitted = False
            st.experimental_rerun()

else:
    # เมื่อยังไม่ได้เลือก
    if st.button("🔍 ค้นหาร้านอาหาร"):
        st.session_state.form_submitted = True
        st.experimental_rerun()
