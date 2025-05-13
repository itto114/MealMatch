import streamlit as st
import pandas as pd

st.title("🍽️ MealMatch - ร้านไหนดี?")

# ตัวเลือกต่าง ๆ
location = st.selectbox("บริเวณที่ต้องการจะไป", ["ประตู 1","ประตู 2","ประตู 3","ประตู 4"])
food_type = st.selectbox("เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน (เช่น ส้มตำ ลาบ ก้อย)", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
price_range = st.radio("งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"] )
time_of_day = st.selectbox("เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

# สร้าง DataFrame สำหรับร้านอาหาร
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "100 - 200", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "เย็น", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}

df = pd.DataFrame(data)

# ฟังก์ชันกรองร้านอาหาร
def filter_restaurants(location, food_type, price_range, time_of_day):
    filtered = df[(df['location'] == location) & 
                  (df['choice'] == food_type) & 
                  (df['budget'] == price_range) & 
                  (df['time'] == time_of_day)]
    return filtered['name'].tolist()

# การเลือกตัวเลือกจากผู้ใช้
if st.button("ค้นหาร้านอาหาร"):
    results = filter_restaurants(location, food_type, price_range, time_of_day)
    if results:
        st.success(f"ร้านที่ตรงกับเงื่อนไข: {', '.join(results)}")
    else:
        st.warning("ไม่พบร้านที่ตรงกับเงื่อนไข")
