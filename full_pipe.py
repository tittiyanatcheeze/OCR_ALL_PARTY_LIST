import os
import io
import json
import regex as re
import pandas as pd
from pdf2image import convert_from_path
from google.cloud import vision
from google.protobuf.json_format import MessageToDict


# ===============================
# CONFIG
# ===============================
PDF_PATH = "ss.pdf"
POPPLER_PATH = r"X:\poppler-25.12.0\Library\bin"

IMAGE_DIR = "images"
OCR_DIR = "ocr"
OUTPUT_DIR = "output"
OUTPUT_CSV = "output/candidates.csv"

DPI = 300
Y_THRESHOLD = 12

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(OCR_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================
# GOOGLE VISION
# ===============================
client = vision.ImageAnnotatorClient()

# ===============================
# THAI UTILS
# ===============================
THAI_NUM = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")

def clean_thai(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"(?<=\p{Thai})\s+(?=\p{Thai})", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.translate(THAI_NUM).strip()

# ===============================
# STEP 1: PDF → IMAGES
# ===============================
def pdf_to_images():
    print("STEP 1: PDF → images")
    if len(os.listdir(IMAGE_DIR)) > 0:
        print("  images already exist, skip")
        return

    images = convert_from_path(
        PDF_PATH,
        dpi=DPI,
        poppler_path=POPPLER_PATH
    )

    for i, img in enumerate(images, start=1):
        name = f"page_{i:03d}.png"
        img.save(os.path.join(IMAGE_DIR, name), "PNG")
        print("  saved", name)

# ===============================
# STEP 2: OCR (resume ได้)
# ===============================
def ocr_images():
    print("\nSTEP 2: OCR images")
    images = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")])
    total = len(images)

    for idx, img_name in enumerate(images, start=1):
        json_name = img_name.replace(".png", ".json")
        json_path = os.path.join(OCR_DIR, json_name)

        if os.path.exists(json_path):
            print(f"[{idx}/{total}] skip {img_name}")
            continue

        print(f"[{idx}/{total}] OCR {img_name} ...")

        with open(os.path.join(IMAGE_DIR, img_name), "rb") as f:
            image = vision.Image(content=f.read())

        response = client.document_text_detection(image=image)
        data = MessageToDict(response.full_text_annotation._pb)


        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"    saved {json_name}")

# ===============================
# OCR STRUCTURE UTILS
# ===============================
def extract_words(annotation):
    words = []
    for page in annotation.get("pages", []):
        for block in page.get("blocks", []):
            for para in block.get("paragraphs", []):
                for word in para.get("words", []):
                    text = "".join(s["text"] for s in word["symbols"])
                    box = word["boundingBox"]["vertices"]
                    x = sum(v.get("x", 0) for v in box) / 4
                    y = sum(v.get("y", 0) for v in box) / 4
                    words.append({"text": text, "x": x, "y": y})
    return words

def group_lines(words):
    words = sorted(words, key=lambda w: (w["y"], w["x"]))
    lines, current = [], []

    for w in words:
        if not current:
            current = [w]
        elif abs(w["y"] - current[-1]["y"]) <= Y_THRESHOLD:
            current.append(w)
        else:
            lines.append(current)
            current = [w]

    if current:
        lines.append(current)

    return lines

# ===============================
# PARSING LOGIC
# ===============================
def extract_party(text):
    m = re.search(r"ตามที่พรรค\s+(.*?)\s+ได้ยื่น", text)
    return m.group(1).strip() if m else None

def parse_rows(lines, party):
    rows = []
    buf = None

    for line in lines:
        text = clean_thai(" ".join(w["text"] for w in line))
        m = re.match(r"^(\d+)\s+(.*)", text)

        if m:
            if buf:
                rows.append(buf)
            buf = {
                "party": party,
                "order": m.group(1),
                "content": m.group(2)
            }
        else:
            if buf:
                buf["content"] += " " + text

    if buf:
        rows.append(buf)

    return rows

def split_name_address(content):
    m = re.match(r"((นาย|นางสาว|นาง|พัน|พล|ว่าที่).*?)(\d+.*)", content)
    if m:
        return m.group(1).strip(), m.group(3).strip()
    return content.strip(), ""

# ===============================
# STEP 3: OCR → CSV
# ===============================
def parse_to_csv():
    print("\nSTEP 3: Parse OCR → CSV")
    all_rows = []
    current_party = None

    files = sorted([f for f in os.listdir(OCR_DIR) if f.endswith(".json")])

    for fname in files:
        with open(os.path.join(OCR_DIR, fname), encoding="utf-8") as f:
            data = json.load(f)

        full_text = clean_thai(data.get("text", ""))
        party = extract_party(full_text)
        if party:
            current_party = party

        words = extract_words(data)
        lines = group_lines(words)
        rows = parse_rows(lines, current_party)

        for r in rows:
            name, addr = split_name_address(r["content"])
            all_rows.append({
                "party": r["party"],
                "order": r["order"],
                "name": name,
                "address": addr
            })

    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("✔ saved", OUTPUT_CSV)

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    pdf_to_images()
    ocr_images()
    parse_to_csv()
