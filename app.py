import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MealMatch 🍽️", layout="centered")
st.title("🍽️ MealMatch - มื้อไหนดี?")

# === ตั้งค่า session_state ===
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_store" not in st.session_state:
    st.session_state.selected_store = None
if "restart" not in st.session_state:
    st.session_state.restart = False

def reset():
    st.session_state.submitted = False
    st.session_state.selected_store = None
    st.session_state.restart = True

# === ข้อมูลร้านอาหาร ===
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

# === STEP 1: แบบสอบถาม ===
if not st.session_state.submitted:
    with st.form("user_form"):
        user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
        user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
        user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
        user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])
        
        submitted = st.form_submit_button("🔍 ค้นหาร้านอาหาร")
        if submitted:
            st.session_state.submitted = True
            st.session_state.user_inputs = {
                "location": user_location,
                "choice": user_choice,
                "budget": user_budget,
                "time": user_time
            }

# === STEP 2: แสดงผลลัพธ์หลังจาก submit ===
elif st.session_state.submitted and not st.session_state.selected_store:
    inputs = st.session_state.user_inputs
    matched_restaurants = filter_restaurants(
        inputs["location"], inputs["choice"], inputs["budget"], inputs["time"]
    )

    if matched_restaurants:
        st.success("ร้านที่ตรงกับคุณมีดังนี้ 🍜")
        selected = st.radio("📌 เลือกร้านที่คุณสนใจ:", matched_restaurants)

        if st.button("✅ ฉันเลือกร้านนี้"):
            st.session_state.selected_store = selected
            feedback = pd.DataFrame([{
                **inputs,
                "selected_store": selected
            }])
            if os.path.exists("user_feedback.csv"):
                feedback.to_csv("user_feedback.csv", mode="a", header=False, index=False)
            else:
                feedback.to_csv("user_feedback.csv", index=False)
            st.rerun()
    else:
        st.error("ไม่พบร้านอาหารที่ตรงกับตัวเลือกของคุณ 😥")
        if st.button("❌ ไม่มีร้านไหนที่ตรงใจ"):
            st.session_state.selected_store = "ไม่มีร้านที่ตรงใจ"
            feedback = pd.DataFrame([{
                **inputs,
                "selected_store": "ไม่มีร้านที่ตรงใจ"
            }])
            if os.path.exists("user_feedback.csv"):
                feedback.to_csv("user_feedback.csv", mode="a", header=False, index=False)
            else:
                feedback.to_csv("user_feedback.csv", index=False)
            st.rerun()

# === STEP 3: แสดงหลังจากเลือกเสร็จแล้ว ===
elif st.session_state.selected_store:
    st.success(f"คุณเลือกร้าน: {st.session_state.selected_store} ✅ ขอบคุณสำหรับการเลือก!")

    # 🔁 ปุ่มเริ่มทำแบบสอบถามใหม่
    if st.button("🔁 เริ่มทำแบบสอบถามใหม่"):
        reset()
        st.rerun()

    # 📝 แสดง Feedback หลังเลือกเท่านั้น
    if os.path.exists("user_feedback.csv") and os.path.getsize("user_feedback.csv") > 0:
        st.markdown("---")
        st.markdown("### 📝 ความคิดเห็นจากผู้ใช้งานก่อนหน้า")
        feedback_df = pd.read_csv("user_feedback.csv")
        st.dataframe(feedback_df)
        st.info(f"📊 จำนวนครั้งที่มีการทำแบบสอบถาม: {len(feedback_df)} ครั้ง")

# 📝 แสดง Feedback หลังจากผู้ใช้เลือกผลลัพธ์
if os.path.exists("user_feedback.csv") and os.path.getsize("user_feedback.csv") > 0:
    st.markdown("---")
    st.markdown("### 📝 ความคิดเห็นจากผู้ใช้งานก่อนหน้า")
    feedback_df = pd.read_csv("user_feedback.csv")
    st.dataframe(feedback_df)
    st.info(f"📊 จำนวนครั้งที่มีการทำแบบสอบถาม: {len(feedback_df)} ครั้ง")

    # 🔐 สำหรับเจ้าของระบบ: ใส่รหัสเพื่อเข้าถึงฟังก์ชันล้างข้อมูล
    with st.expander("🔐 เข้าสู่ระบบผู้ดูแล (สำหรับล้างข้อมูล)"):
        admin_password = st.text_input("itto114", type="147258369z")
        if admin_password == "your_secret_code":  # เปลี่ยนรหัสนี้ตามต้องการ
            if st.button("🗑️ ล้างข้อมูลแบบสอบถามทั้งหมด"):
                os.remove("user_feedback.csv")
                st.warning("ข้อมูลทั้งหมดถูกลบแล้ว ❌")
                st.rerun()
        elif admin_password:
            st.error("รหัสผ่านไม่ถูกต้อง ❌")
