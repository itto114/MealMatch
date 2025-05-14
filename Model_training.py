import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# === ข้อมูลร้านอาหาร ===
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "กลางวัน", "เย็น", "เช้า"],
    "label": [1, 1, 1, 0, 1, 0]  # 1 = เหมาะสม, 0 = ไม่เหมาะสม (สามารถเปลี่ยนตามเงื่อนไขของคุณ)
}

df = pd.DataFrame(data)

# === การแปลงข้อมูล ===
# ใช้ LabelEncoder เพื่อแปลงข้อมูลเช่น 'location', 'choice', 'budget', 'time' ให้เป็นตัวเลข
le_location = LabelEncoder()
le_choice = LabelEncoder()
le_budget = LabelEncoder()
le_time = LabelEncoder()

df['location'] = le_location.fit_transform(df['location'])
df['choice'] = le_choice.fit_transform(df['choice'])
df['budget'] = le_budget.fit_transform(df['budget'])
df['time'] = le_time.fit_transform(df['time'])

# === การเตรียมข้อมูลสำหรับเทรน ===
X = df[['location', 'choice', 'budget', 'time']]  # Features
y = df['label']  # Target variable (1 = เหมาะสม, 0 = ไม่เหมาะสม)

# แบ่งข้อมูลเป็นชุดฝึกและทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === สร้างและเทรนโมเดล ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === ทดสอบโมเดล ===
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# === บันทึกโมเดล ===
joblib.dump(model, 'mealmatch_model.pkl')
