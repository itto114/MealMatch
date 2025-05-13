import streamlit as st
import pandas as pd

st.title("🍽️ MealMatch - มื้อไหนดี?")

# ตัวเลือกต่าง ๆ
location = st.selectbox("บริเวณที่ต้องการจะไป", ["ประตู 1","ประตู 2","ประตู 3","ประตู 4"])
choice = st.selectbox("เลือกประเภทอาหาร", ["อาหารตามสั่ง", "อาหารอีสาน (เช่น ส้มตำ ลาบ ก้อย)", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"])
budget = st.radio("งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
time = st.selectbox("เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

if st.button("ค้นหาร้านอาหาร"):
    st.success(f"แนะนำร้านอาหารบริเวณ \"{location}\" ประเภท \"{choice}\" ในช่วง \"{time}\" ที่อยู่ในงบ \"{budget}\" 👍")


# สร้าง DataFrame สำหรับร้านอาหาร
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "food_type": ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "price_range": ["50 - 100", "100 - 200", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "เย็น", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}

df = pd.DataFrame(data)

# ฟังก์ชันกรองร้านอาหาร
def filter_restaurants(location, food_type, price_range, time_of_day):
    filtered = df[(df['location'] == location) &
                  (df['food_type'] == food_type) &
                  (df['price_range'] == price_range) &
                  (df['time'] == time_of_day)]
    return filtered['name'].tolist()

# การเลือกตัวเลือกจากผู้ใช้
location = "ประตู 1"
food_type = "อาหารตามสั่ง"
price_range = "50 - 100"
time_of_day = "กลางวัน"

# เรียกใช้ฟังก์ชันกรองข้อมูล
results = filter_restaurants(location, food_type, price_range, time_of_day)
print("ร้านที่ตรงกับเงื่อนไข: ", results)
