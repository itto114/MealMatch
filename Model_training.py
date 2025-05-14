import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# อ่านข้อมูลจากไฟล์ CSV ที่เก็บ feedback
feedback_file = "user_feedback.csv"
feedback_df = pd.read_csv(feedback_file)

# ตรวจสอบว่ามีข้อมูลที่จำเป็นหรือไม่
required_columns = ["location", "choice", "budget", "time", "selected_restaurant"]
if not all(col in feedback_df.columns for col in required_columns):
    raise ValueError(f"ไฟล์ {feedback_file} ขาดข้อมูลที่จำเป็น")

# แปลงข้อมูลที่เป็นข้อความให้เป็นตัวเลข
# ตัวอย่างการแปลงค่า: location, choice, time และ budget
location_map = {"ประตู 1": 0, "ประตู 2": 1, "ประตู 3": 2, "ประตู 4": 3}
choice_map = {"อาหารตามสั่ง": 0, "อาหารอีสาน": 1, "อาหารจานเดียว": 2, "ปิ้งย่าง": 3, "อาหารเกาหลี": 4, "อาหารญี่ปุ่น": 5}
budget_map = {"ไม่เกิน 50": 0, "50 - 100": 1, "100 - 200": 2, "200+": 3}
time_map = {"เช้า": 0, "กลางวัน": 1, "เย็น": 2}

# แปลงข้อมูลจาก categorical เป็น numeric
feedback_df['location'] = feedback_df['location'].map(location_map)
feedback_df['choice'] = feedback_df['choice'].map(choice_map)
feedback_df['budget'] = feedback_df['budget'].map(budget_map)
feedback_df['time'] = feedback_df['time'].map(time_map)

# สร้าง X (features) และ y (target)
X = feedback_df[["location", "choice", "budget", "time"]]
y = feedback_df["selected_restaurant"]

# แบ่งข้อมูลเป็น train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้างโมเดล KNN
knn = KNeighborsClassifier(n_neighbors=3)

# ฝึกโมเดล
knn.fit(X_train, y_train)

# ทดสอบโมเดล
y_pred = knn.predict(X_test)

# แสดงผลลัพธ์การคำนวณ
report = classification_report(y_test, y_pred, target_names=feedback_df["selected_restaurant"].unique())
print(report)

# บันทึกโมเดล (ถ้าต้องการ)
import joblib
joblib.dump(knn, "knn_model.pkl")
