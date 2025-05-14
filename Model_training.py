import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle

# ข้อมูลร้านอาหาร
data = {
    "name": ["ร้าน A", "ร้าน B", "ร้าน C", "ร้าน D", "ร้าน E", "ร้าน F"],
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": ["50 - 100", "50 - 100", "50 - 100", "200+", "100 - 200", "50 - 100"],
    "time": ["กลางวัน", "กลางวัน", "เช้า", "กลางวัน", "เย็น", "เช้า"]
}

df = pd.DataFrame(data)

# แปลงข้อมูลเป็นตัวเลข
df['location'] = df['location'].map({"ประตู 1": 0, "ประตู 2": 1, "ประตู 3": 2, "ประตู 4": 3})
df['choice'] = df['choice'].map({"อาหารตามสั่ง": 0, "อาหารอีสาน": 1, "อาหารจานเดียว": 2, "ปิ้งย่าง": 3, "อาหารเกาหลี": 4, "อาหารญี่ปุ่น": 5})
df['budget'] = df['budget'].map({"50 - 100": 0, "100 - 200": 1, "200+": 2, "ไม่เกิน 50": 3})
df['time'] = df['time'].map({"กลางวัน": 0, "เช้า": 1, "เย็น": 2})

# แยก X (ตัวแปรอิสระ) และ y (ตัวแปรที่ต้องการทำนาย)
X = df[['location', 'choice', 'budget', 'time']]
y = df['name']

# แบ่งข้อมูลเป็น Train และ Test Set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้าง KNN โมเดล
knn = KNeighborsClassifier(n_neighbors=3)

# ฝึกโมเดล
knn.fit(X_train, y_train)

# บันทึกโมเดล
with open('knn_model.pkl', 'wb') as f:
    pickle.dump(knn, f)

print("โมเดลได้ถูกฝึกและบันทึกแล้ว")
