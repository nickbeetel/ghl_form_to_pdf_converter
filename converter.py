import json
import requests
import os
from fpdf import FPDF
import config
from io import BytesIO


def fetch_and_convert():
    OUTPUT_DIR = "json_outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "formatted_submissions.json")

    url = f"{config.GHL_URL}/forms/submissions"
    params = {
        "locationId": config.GHL_LOCATION_ID,
        "limit": 100,
        "page": 1
    }
    headers = {
        "Authorization": f"Bearer {config.GHL_API_KEY}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    cleaned = []
    for s in data.get("submissions", []):
        o = s.get("others", {})
        cleaned.append({
            "id": s.get("id"),
            "name": s.get("name"),
            "email": o.get("email"),
            "phone": o.get("phone"),
            "business_name": o.get("cxIAXvbjvb2vLSY66lkE") or o.get("dbVJAAxG5Dqx0jVg9evF"),
            "address": o.get("address"),
            "city": o.get("fJbUIjK2a941YDsVdQ0y"),
            "state": o.get("state"),
            "country": o.get("country"),
            "postal_code": o.get("postal_code"),
            "date_of_birth": o.get("date_of_birth"),
            "entity_type": o.get("IvlXqqkYpOrghIMp19M4"),
            "industry": o.get("ccLc9F5CIgvrfpyK3o4c"),
            "signature_url": next(iter(o.get("j2lyvbMjXub1WFX7KSaP", {}).values()), {}).get("url") if isinstance(o.get("j2lyvbMjXub1WFX7KSaP"), dict) else None,
            "file_uploads": [
                filedata.get("url")
                for field in ["olu4EtLwSh6WbGGZd5IG", "d8srILk2VvnXJ0nvSFwo"]
                for filedata in (o.get(field, {}) or {}).values()
            ],
            "createdAt": s.get("createdAt"),
        })

    with open(json_path, "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Saved {len(cleaned)} formatted submissions to {json_path}")
    return json_path


def download_image_bytes(url):
    """Download an image and return as bytes for FPDF."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"⚠️ Failed to download image {url}: {e}")
    return None


def add_image_from_url(pdf, url, x=10, w=100):
    """Download an image, save temporarily, add to PDF, then delete temp file."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            tmp_file = "temp_img.png"
            with open(tmp_file, "wb") as f:
                f.write(response.content)
            pdf.image(tmp_file, x=x, w=w)
            os.remove(tmp_file)
    except Exception as e:
        print(f"⚠️ Failed to add image from {url}: {e}")


def generate_pdfs(json_path):
    OUTPUT_DIR = "pdf_submissions"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(json_path, "r") as f:
        submissions = json.load(f)

    for submission in submissions:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        fields = [
            ("Name", submission.get("name")),
            ("Email", submission.get("email")),
            ("Phone", submission.get("phone")),
            ("Business Name", submission.get("business_name")),
            ("Address", submission.get("address")),
            ("City", submission.get("city")),
            ("State", submission.get("state")),
            ("Country", submission.get("country")),
            ("Postal Code", submission.get("postal_code")),
            ("Date of Birth", submission.get("date_of_birth")),
            ("Entity Type", submission.get("entity_type")),
            ("Industry", submission.get("industry")),
            ("Created At", submission.get("createdAt")),
        ]

        for label, value in fields:
            pdf.cell(0, 8, f"{label}: {value}", ln=True)

        if submission.get("signature_url"):
            pdf.ln(5)
            pdf.cell(0, 8, "Signature:")
            pdf.ln(2)
            add_image_from_url(pdf, submission["signature_url"], x=10, w=100)

        for i, file_url in enumerate(submission.get("file_uploads", []), 1):
            pdf.ln(5)
            pdf.cell(0, 8, f"File Upload {i}:")
            pdf.ln(2)
            add_image_from_url(pdf, file_url, x=10, w=100)

        pdf_path = os.path.join(OUTPUT_DIR, f"{submission['id']}.pdf")
        pdf.output(pdf_path)
        print(f"✅ Generated PDF: {pdf_path}")


if __name__ == "__main__":
    json_file_path = fetch_and_convert()
    generate_pdfs(json_file_path)
