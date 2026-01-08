# โปรเจกต์ OCR รายชื่อผู้สมัครรับเลือกตั้ง (Party List)

โปรเจกต์นี้ใช้สำหรับดึงข้อมูลรายชื่อผู้สมัครรับเลือกตั้งแบบบัญชีรายชื่อจากไฟล์ PDF (สส. 4/24) โดยใช้ **Gemini 2.5 Flash API** ในการทำ OCR และประมวลผลข้อมูล

## ส่วนประกอบของโปรเจกต์ (`full_pipe.py`)

กระบวนการทำงานหลัก:

1.  **PDF to Images**: แปลงไฟล์ PDF ต้นฉบับเป็นรูปภาพรายหน้า
2.  **OCR & Processing**: ใช้ **Gemini 2.5 Flash API** ในการดึงข้อมูลและจัดหมวดหมู่จากรูปภาพ
3.  **Output**: ส่งออกข้อมูลเป็นไฟล์ Excel (`allptl.xlsx`)

## ไฟล์สำคัญ

- `สส 4 ทับ 24.pdf`: ไฟล์เอกสารต้นฉบับ
- `output/allptl.xlsx`: ไฟล์ผลลัพธ์ที่ได้จากการประมวลผล
- `full_pipe.py`: สคริปต์หลักในการทำงาน

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