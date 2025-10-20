# GHL Form to PDF Converter

A Python script to fetch **Go High Level (GHL)** form submissions and generate formatted PDFs for each submission.

---

## Features
- Fetches submissions from a GHL form via API
- Saves submissions as a JSON file
- Generates PDFs including:
  - Basic submission info
  - Signature images
  - Uploaded files

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/nickbeetel/ghl_form_to_pdf_converter.git
cd ghl_form_to_pdf_converter
```

2. **Create a virtual environment (optional but recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `config.py` with your GHL API info:**
```bash
GHL_URL = "https://api.gohighlevel.com/v1"
GHL_API_KEY = "YOUR_API_KEY"
GHL_LOCATION_ID = "YOUR_LOCATION_ID"
```

## Usage
```bash
python converter.py
```

**This will:**
1. Fetch submissions from your GHL form
2. Save cleaned submissions JSON to json_outputs/formatted_submissions.json
3. Generate PDFs in the pdf_submissions/ folder

## Notes
- `json_outputs/` and `pdf_submissions/` folders are included in `.gitignore` to avoid committing sensitive data.
- Make sure your GHL API key has permissions to access form submissions.
- Signature images and file uploads are automatically downloaded and added to the PDFs.