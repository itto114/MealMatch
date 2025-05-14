import pandas as pd
import streamlit as st

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
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "กลางวัน", "เย็น", "เช้า"]
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

# === เก็บข้อมูล feedback ทุกครั้งที่ผู้ใช้เลือก ===
feedback_file = "user_feedback.csv"
if not pd.io.common.file_exists(feedback_file):
    feedback_df = pd.DataFrame(columns=["location", "choice", "budget", "time", "selected_store"])
else:
    feedback_df = pd.read_csv(feedback_file)

# === การแสดงผลลัพธ์ ===
if st.button("🔍 ค้นหาร้านอาหาร"):
    matched_restaurants = filter_restaurants(user_location, user_choice, user_budget, user_time)

    if matched_restaurants:
        st.success("ร้านที่ตรงกับคุณมีดังนี้ 🍜")
        selected_store = st.radio("เลือกร้านที่คุณสนใจ:", matched_restaurants)

        # เก็บข้อมูล feedback ใน DataFrame
        store_data = {
            'location': user_location,
            'choice': user_choice,
            'budget': user_budget,
            'time': user_time,
            'selected_store': selected_store
        }

        feedback_df = feedback_df.append(store_data, ignore_index=True)
        feedback_df.to_csv(feedback_file, index=False)

        st.success(f"คุณเลือกร้าน: {selected_store} ✅ ขอบคุณสำหรับการเลือก!")

    else:
        st.error("ไม่พบร้านอาหารที่ตรงกับตัวเลือกของคุณ 😥 ลองเปลี่ยนตัวเลือกดูนะ")

# === การแสดง feedback ทั้งหมด ===
st.subheader("Feedback จากผู้ใช้ทั้งหมด:")
if len(feedback_df) > 0:
    st.dataframe(feedback_df)

# === แสดงจำนวนครั้งที่ผู้ใช้เข้ามาทำแบบสอบถาม ===
total_responses = len(feedback_df)
st.write(f"จำนวนครั้งที่มีการตอบแบบสอบถามทั้งหมด: {total_responses} ครั้ง")

# === ปุ่มรีเซ็ตข้อมูล ===
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    # ลบไฟล์ feedback และสร้างใหม่
    feedback_df = pd.DataFrame(columns=["location", "choice", "budget", "time", "selected_store"])
    feedback_df.to_csv(feedback_file, index=False)
    st.success("ข้อมูลทั้งหมดได้ถูกรีเซ็ตเรียบร้อยแล้ว! 🎉")
