import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# ข้อมูลร้านอาหาร (สมมุติเป็นข้อมูลตัวอย่าง)
data = {
    "location": ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "100 - 200", "200+", "50 - 100", "100 - 200"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "เย็น", "กลางวัน", "เย็น"],
    "selected_store": [1, 0, 1, 0, 1, 0]  # 1 = ตรงใจ, 0 = ไม่ตรงใจ
}

# สร้าง DataFrame
df = pd.DataFrame(data)

# ทำ One-hot Encoding สำหรับข้อมูลที่เป็นข้อความ
df_encoded = pd.get_dummies(df.drop('selected_store', axis=1))

# ตัวแปรที่ใช้เป็น feature และ target
X = df_encoded
y = df['selected_store']

# แบ่งข้อมูลเป็นชุดฝึกและทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้างโมเดล
model = RandomForestClassifier(n_estimators=100, random_state=42)

# ฝึกโมเดล
model.fit(X_train, y_train)

# บันทึกโมเดล
pickle.dump(model, "restaurant_model.pkl")

print("โมเดลได้ถูกบันทึกเป็น 'restaurant_model.pkl'")
