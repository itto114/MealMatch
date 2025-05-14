from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

# ฟังก์ชันที่ฝึกโมเดล KNN
def train_model(location, food_type, budget, time_of_day):
    # สร้างข้อมูลการฝึก
    data = {
        "location": ["ประตู 1", "ประตู 2", "ประตู 3", "ประตู 4"],
        "food_type": ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง"],
        "budget": ["50 - 100", "100 - 200", "50 - 100", "200+"],
        "time_of_day": ["เช้า", "กลางวัน", "เย็น", "กลางวัน"],
        "label": [1, 2, 1, 2]  # ตัวอย่าง label สำหรับ KNN
    }
    
    # สร้าง DataFrame
    df = pd.DataFrame(data)
    
    # แปลงข้อมูลเป็นค่าตัวเลข
    X = df[["location", "food_type", "budget", "time_of_day"]]
    y = df["label"]
    
    # สร้างและฝึกโมเดล
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)
    
    # ทำนายผลลัพธ์
    prediction = model.predict([[location, food_type, budget, time_of_day]])
    
    return prediction
