import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MealMatch 🍽️", layout="centered")
st.title("🍽️ MealMatch - มื้อไหนดี?")

# Session state สำหรับควบคุม flow
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_feedback" not in st.session_state:
    st.session_state.selected_feedback = None

# === ข้อมูลร้านอาหาร ===
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}
df = pd.DataFrame(data)

# === แบบสอบถาม ===
if not st.session_state.submitted:
    with st.form("user_form"):
        user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", df["location"].unique())
        user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", df["choice"].unique())
        user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", df["budget"].unique())
        user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", df["time"].unique())

        submitted = st.form_submit_button("🔍 ค้นหาร้านอาหาร")
        if submitted:
            st.session_state.submitted = True
            st.session_state.user_inputs = {
                "location": user_location,
                "choice": user_choice,
                "budget": user_budget,
                "time": user_time
            }

# === หลังส่งแบบสอบถาม ===
if st.session_state.submitted:
    user_inputs = st.session_state.user_inputs
    filtered = df[
        (df["location"] == user_inputs["location"]) &
        (df["choice"] == user_inputs["choice"]) &
        (df["budget"] == user_inputs["budget"]) &
        (df["time"] == user_inputs["time"])
    ]

    matched_restaurants = filtered["name"].tolist()

    if matched_restaurants:
        st.success("ร้านที่ตรงกับคุณมีดังนี้ 🍜")
        selected = st.radio("เลือกร้านที่คุณสนใจ:", matched_restaurants)

        if selected:
            st.session_state.selected_feedback = selected
            st.info(f"คุณเลือกร้าน: {selected} ✅ ขอบคุณสำหรับการเลือก!")

            # === บันทึก feedback ===
            feedback = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "location": user_inputs["location"],
                "choice": user_inputs["choice"],
                "budget": user_inputs["budget"],
                "time": user_inputs["time"],
                "selected": selected
            }

            feedback_df = pd.DataFrame([feedback])
            if os.path.exists("user_feedback.csv"):
                feedback_df.to_csv("user_feedback.csv", mode="a", header=False, index=False)
            else:
                feedback_df.to_csv("user_feedback.csv", index=False)

            # === แสดง Feedback ทั้งหมด ===
            if os.path.exists("user_feedback.csv"):
                st.markdown("---")
                st.markdown("### 📝 ความคิดเห็นจากผู้ใช้งานก่อนหน้า")
                all_feedback = pd.read_csv("user_feedback.csv")
                st.dataframe(all_feedback)
                st.info(f"📊 จำนวนครั้งที่มีการทำแบบสอบถาม: {len(all_feedback)} ครั้ง")

                with st.expander("🔐 เข้าสู่ระบบผู้ดูแล (สำหรับล้างข้อมูล)"):
                    admin_password = st.text_input("กรุณาใส่รหัสผ่าน", type="password")
                    if admin_password == "your_secret_code":  # เปลี่ยนเป็นรหัสของคุณ
                        if st.button("🗑️ ล้างข้อมูลแบบสอบถามทั้งหมด"):
                            os.remove("user_feedback.csv")
                            st.warning("ข้อมูลทั้งหมดถูกลบแล้ว ❌")
                            st.rerun()
                    elif admin_password:
                        st.error("รหัสผ่านไม่ถูกต้อง ❌")

            # ปุ่มทำใหม่
            st.markdown("---")
            if st.button("🔄 เริ่มทำแบบสอบถามใหม่"):
                st.session_state.submitted = False
                st.session_state.selected_feedback = None
                st.rerun()

    else:
        st.error("ไม่พบร้านอาหารที่ตรงกับตัวเลือกของคุณ 😥 ลองเปลี่ยนตัวเลือกดูนะ")
        if st.button("❌ ไม่มีร้านไหนที่ตรงใจ"):
            st.session_state.selected_feedback = "ไม่มีร้านไหนที่ตรงใจ"
            st.warning("ขอบคุณสำหรับความคิดเห็น! ระบบจะนำไปปรับปรุงต่อไป 🙏")
            st.markdown("---")
            if st.button("🔄 เริ่มทำแบบสอบถามใหม่"):
                st.session_state.submitted = False
                st.session_state.selected_feedback = None
                st.rerun()
