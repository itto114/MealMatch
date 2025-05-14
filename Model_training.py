import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# สร้าง DataFrame ที่ใช้ในการฝึกโมเดล
data = {
    "location": ["ประตู 1", "ประตู 1", "ประตู 3", "ประตู 4", "ประตู 1", "ประตู 2"],
    "choice": ["อาหารตามสั่ง", "อาหารตามสั่ง", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"],
    "budget": [1, 2, 1, 3, 2, 1],  # 1: 50-100, 2: 100-200, 3: 200+
    "time": [1, 2, 3, 1, 2, 3],  # 1: เช้า, 2: กลางวัน, 3: เย็น
    "feedback": [1, 1, 0, 1, 0, 0]  # 1: เลือก, 0: ไม่เลือก
}

df = pd.DataFrame(data)

# แยกคุณสมบัติและเป้าหมาย
X = df[["location", "choice", "budget", "time"]]  # feature columns
y = df["feedback"]  # target column (การเลือก/ไม่เลือก)

# แปลงข้อมูลไม่เป็นตัวเลขให้เป็นตัวเลข (one-hot encoding)
X = pd.get_dummies(X)

# แบ่งข้อมูลเป็นชุดฝึก (train) และชุดทดสอบ (test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ฝึกโมเดล KNN
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# ทำนายผลลัพธ์
y_pred = model.predict(X_test)

# คำนวณค่าต่าง ๆ เช่น accuracy, precision, recall, F1-score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# แสดงผลลัพธ์
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
