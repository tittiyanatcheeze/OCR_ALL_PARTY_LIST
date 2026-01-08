# โปรเจกต์ OCR รายชื่อผู้สมัครรับเลือกตั้ง (Party List)

โปรเจกต์นี้ใช้สำหรับดึงข้อมูลรายชื่อผู้สมัครรับเลือกตั้งแบบบัญชีรายชื่อจากไฟล์ PDF (สส. 4/24) โดยใช้ Google Cloud Vision API ในการทำ OCR และจัดหมวดหมู่ข้อมูล

## ส่วนประกอบของโปรเจกต์ (`full_pipe.py`)

กระบวนการทำงานหลักแบ่งเป็น 3 ขั้นตอน:

1.  **PDF to Images**: แปลงไฟล์ PDF ต้นฉบับเป็นรูปภาพรายหน้า
2.  **OCR**: ใช้ Google Cloud Vision API ดึงข้อความจากรูปภาพ และบันทึกเป็นไฟล์ JSON
3.  **Parsing**: นำข้อมูลจาก JSON มาประมวลผลเพื่อแยกชื่อพรรค, ลำดับ, ชื่อ-นามสกุล และที่อยู่ แล้วส่งออกเป็นไฟล์ CSV/Excel

## ไฟล์สำคัญ

- `สส 4 ทับ 24.pdf`: ไฟล์เอกสารต้นฉบับ
- `full_pipe.py`: สคริปต์หลักในการทำงาน
- `output/allptl.xlsx`: ไฟล์ผลลัพธ์ที่ได้จากการประมวลผล
- `OCR.ipynb`: Notebook สำหรับทดสอบและตรวจสอบการทำงาน

## การติดตั้งและใช้งาน

1. ติดตั้ง Library ที่จำเป็น:
   ```bash
   pip install pandas pdf2image google-cloud-vision regex openpyxl
   ```
2. ตั้งค่า Google Cloud Credentials
3. ตรวจสอบพาธของ Poppler และไฟล์ PDF ในโค้ด `full_pipe.py`
4. รันสคริปต์:
   ```bash
   python full_pipe.py
   ```