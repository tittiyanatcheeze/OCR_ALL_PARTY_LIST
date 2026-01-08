# OCR All Party List

This project extracts candidate information from PDF documents (specifically Thai election party lists) using OCR.

## Pipeline (`full_pipe.py`)

The pipeline consists of three main steps:

1.  **PDF to Images**: Converts the input PDF into individual page images.
2.  **OCR**: Uses Google Cloud Vision API to extract text from images.
3.  **Parsing**: Parses the OCR results to extract party names, candidate names, and addresses, exporting them to a CSV file.

## Prerequisites

-   Python 3.x
-   Google Cloud Vision API credentials
-   Poppler (for `pdf2image`)

## Setup

1.  Install dependencies:
    ```bash
    pip install pandas pdf2image google-cloud-vision regex
    ```
2.  Set up Google Cloud credentials.
3.  Configure `POPPLER_PATH` and `PDF_PATH` in `full_pipe.py` if necessary.

## Usage

Run the full pipeline:

```bash
python full_pipe.py
```

## Output

Results are saved to `output/candidates.csv`.
