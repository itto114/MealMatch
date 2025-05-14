import streamlit as st
from Model_training import train_model  # Import ฟังก์ชันจาก Model_training.py

# ตัวเลือกจากผู้ใช้
location = st.selectbox("เลือกบริเวณที่ต้องการ")
food_type = st.selectbox("เลือกประเภทอาหาร")
budget = st.radio("งบประมาณ")
time_of_day = st.selectbox("เวลาที่มักออกไปทาน")

# เมื่อผู้ใช้กดค้นหาร้าน
if st.button("ค้นหาร้านอาหาร"):
    # เรียกใช้โมเดลจาก Model_training.py
    model_result = train_model(location, food_type, budget, time_of_day)
    
    # แสดงผลลัพธ์
    if model_result:
        st.write(f"ร้านที่ตรงกับเงื่อนไข: {model_result}")
    else:
        st.write("ไม่พบร้านที่ตรงกับเงื่อนไข")
