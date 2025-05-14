import streamlit as st

st.title("🍽️ MealMatch - มื้อไหนดี?")

# ตัวเลือกจากผู้ใช้

user\_location = st.selectbox("บริเวณที่ต้องการจะไป", \["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"])
user\_choice = st.selectbox("เลือกประเภทอาหาร", \["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "อาหารญี่ปุ่น"])
user\_budget = st.radio("งบประมาณต่อมื้อ (บาท)", \["50 - 100", "100 - 200", "200+"])
user\_time = st.selectbox("เวลาที่มักออกไปกิน", \["เช้า", "กลางวัน", "เย็น"])

# เมื่อกดปุ่ม

if st.button("ทำนายความเหมาะสมของร้าน"):
\# สร้าง DataFrame จาก input ผู้ใช้
user\_input = pd.DataFrame(\[{
"location": user\_location,
"choice": user\_choice,
"budget": user\_budget,
"time": user\_time
}])

```
# One-hot encoding ให้เหมือนกับที่ฝึกโมเดลไว้
user_input_encoded = pd.get_dummies(user_input)

# เติม column ที่ขาด (เนื่องจาก One-hot อาจไม่ครบทุก category ที่มีใน train)
for col in X_encoded.columns:
    if col not in user_input_encoded.columns:
        user_input_encoded[col] = 0

user_input_encoded = user_input_encoded[X_encoded.columns]  # เรียงลำดับ columns ให้ตรงกัน

# ทำนาย
prediction = model.predict(user_input_encoded)[0]

# แสดงผล
if prediction == 1:
    st.success("ร้านนี้เหมาะกับคุณ! 🎉")
else:
    st.warning("อาจจะไม่ใช่ร้านที่ตรงใจ ลองเปลี่ยนตัวเลือกดูนะ 😊")
```

ขอฝากโค้ดนี้ไว้ก่อนนะ
