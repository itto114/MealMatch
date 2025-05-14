import streamlit as st
import pandas as pd

# สมมุติว่ามีโมเดลและ X_encoded แล้ว (ถ้าจริงจะต้องโหลดโมเดลจาก joblib/pickle)
# model = ... 
# X_encoded = ...

st.title("🍽️ MealMatch - มื้อไหนดี?")

# ตัวเลือกจากผู้ใช้
user_location = st.selectbox("บริเวณที่ต้องการจะไป", ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
user_choice = st.selectbox("เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "อาหารญี่ปุ่น"])
user_budget = st.radio("งบประมาณต่อมื้อ (บาท)", ["50 - 100", "100 - 200", "200+"])
user_time = st.selectbox("เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

# เมื่อกดปุ่ม
if st.button("ทำนายความเหมาะสมของร้าน"):
    # สร้าง DataFrame จาก input ผู้ใช้
    user_input = pd.DataFrame([{
        "location": user_location,
        "choice": user_choice,
        "budget": user_budget,
        "time": user_time
    }])

    # One-hot encoding ให้เหมือนกับที่ฝึกโมเดลไว้
    user_input_encoded = pd.get_dummies(user_input)
    
    # เติม column ที่ขาด (เนื่องจาก One-hot อาจไม่ครบทุก category ที่มีใน train)
    for col in X_encoded.columns:
        if col not in user_input_encoded.columns:
            user_input_encoded[col] = 0
    
    user_input_encoded = user_input_encoded[X_encoded.columns]  # เรียงลำดับ columns ให้ตรงกัน

    # ทำนาย
    prediction = model.predict(user_input_encoded)[0]
    
    # แสดงผลลัพธ์
    if prediction == 1:
        st.success("ร้านที่เหมาะกับคุณ! 🎉")
        
        # แสดงตัวเลือกที่เป็นร้านแนะนำ (สมมุติ)
        matching_restaurants = ["ร้าน A", "ร้าน B", "ร้าน C"]
        selected = st.radio("เลือกร้านที่คุณสนใจมากที่สุด", matching_restaurants)

        st.info(f"คุณเลือก: {selected}")

        if st.button("ไม่มีร้านไหนตรงใจเลย 😢"):
            st.warning("ขอบคุณสำหรับความคิดเห็น! เราจะปรับปรุงระบบแนะนำให้ดีขึ้น 💡")

    else:
        st.warning("อาจจะไม่ใช่ร้านที่ตรงใจ ลองเปลี่ยนตัวเลือกดูนะ 😊")
        if st.button("ไม่มีร้านไหนตรงใจเลย 😢"):
            st.warning("ขอบคุณสำหรับความคิดเห็น! เราจะปรับปรุงระบบแนะนำให้ดีขึ้น 💡")

