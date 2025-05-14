import streamlit as st
import pandas as pd
import pickle

# โหลดโมเดลที่ฝึกไว้
with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

# === ตัวเลือกจากผู้ใช้ ===
user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

# === การแปลงข้อมูลที่ผู้ใช้เลือก ===
location_map = {"ประตู 1": 0, "ประตู 2": 1, "ประตู 3": 2, "ประตู 4": 3}
choice_map = {"อาหารตามสั่ง": 0, "อาหารอีสาน": 1, "อาหารจานเดียว": 2, "ปิ้งย่าง": 3, "อาหารเกาหลี": 4, "อาหารญี่ปุ่น": 5}
budget_map = {"50 - 100": 0, "100 - 200": 1, "200+": 2, "ไม่เกิน 50": 3}
time_map = {"กลางวัน": 0, "เช้า": 1, "เย็น": 2}

# ทำให้ข้อมูลของผู้ใช้เป็นตัวเลข
user_data = [[location_map[user_location], choice_map[user_choice], budget_map[user_budget], time_map[user_time]]]

# ทำนายร้าน
predicted_restaurant = knn_model.predict(user_data)

# แสดงผลใน Streamlit
st.write(f"ร้านที่แนะนำ: {predicted_restaurant[0]}")
