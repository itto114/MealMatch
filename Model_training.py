import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# ตัวแปรในการเก็บข้อมูล
user_data = {
    'user_choice': [],
    'predicted_choice': [],
    'is_correct': []
}

# ฟังก์ชันเก็บข้อมูลและคำนวณ
def store_and_calculate(user_choice, predicted_choice):
    # เก็บข้อมูลการตอบกลับ
    user_data['user_choice'].append(user_choice)
    user_data['predicted_choice'].append(predicted_choice)
    
    # เช็คว่าโมเดลทำนายถูกต้องหรือไม่
    is_correct = 1 if user_choice == predicted_choice else 0
    user_data['is_correct'].append(is_correct)

# ตัวอย่างการเก็บข้อมูล
store_and_calculate('อาหารตามสั่ง', 'อาหารตามสั่ง')
store_and_calculate('ปิ้งย่าง', 'อาหารตามสั่ง')
store_and_calculate('อาหารญี่ปุ่น', 'อาหารญี่ปุ่น')

# แปลงข้อมูลเป็น DataFrame
df_user_data = pd.DataFrame(user_data)

# คำนวณ Classification Rate, Precision, Recall, F1-Score
y_true = df_user_data['user_choice']  # ค่าจริงจากผู้ใช้
y_pred = df_user_data['predicted_choice']  # ค่าทำนายจากโมเดล

# คำนวณ Precision, Recall, F1-Score
precision = precision_score(y_true, y_pred, average='binary', pos_label='อาหารตามสั่ง')
recall = recall_score(y_true, y_pred, average='binary', pos_label='อาหารตามสั่ง')
f1 = f1_score(y_true, y_pred, average='binary', pos_label='อาหารตามสั่ง')

# คำนวณ Classification Rate (Accuracy)
accuracy = (df_user_data['is_correct'].sum()) / len(df_user_data)

# แสดงผลลัพธ์
print(f"Classification Rate (Accuracy): {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")
