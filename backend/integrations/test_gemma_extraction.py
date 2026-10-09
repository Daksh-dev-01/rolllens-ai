from pathlib import Path
import httpx

BASE_URL = "http://127.0.0.1:8000/api/v1"

pdf_path = Path(input("Enter full path to test PDF: ").strip().strip('"'))

if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
    raise SystemExit("FAIL: Invalid PDF path.")

with httpx.Client(timeout=180) as client:
    print("\n1. Uploading PDF...", flush=True)

    with pdf_path.open("rb") as f:
        response = client.post(
            f"{BASE_URL}/documents",
            files={"file": (pdf_path.name, f, "application/pdf")},
        )

    print("Upload HTTP:", response.status_code)
    if not response.is_success:
        print(response.text[:1500])
        raise SystemExit("FAIL: Upload")

    payload = response.json()
    data = payload.get("data", payload)
    document_id = data.get("id")
    page_count = int(data.get("page_count", 0))

    if not document_id or page_count < 1:
        print("Unexpected upload response:", payload)
        raise SystemExit("FAIL: Missing document ID or pages")

    print("Document ID:", document_id)
    print("Pages:", page_count)

    page = int(input(f"Page to extract (1-{page_count}): "))
    if not 1 <= page <= page_count:
        raise SystemExit("FAIL: Invalid page number")

    print("\n2. Calling extraction endpoint...", flush=True)
    response = client.post(
        f"{BASE_URL}/documents/{document_id}/pages/{page}/extract"
    )

    print("Extraction HTTP:", response.status_code)
    if not response.is_success:
        print(response.text[:2000])
        raise SystemExit("FAIL: Extraction")

    payload = response.json()
    result = payload.get("data", payload)
    records = result.get("records", [])

    print("\n--- EXTRACTION RESULT ---")
    print("Success:", payload.get("success"))
    print("Records:", len(records))
    print("Human review required:", result.get("requires_human_review"))

    for index, record in enumerate(records[:3], 1):
        print(f"\nRecord {index}:")
        print(record)

    if records:
        print("\nPASS: Structured records returned.")
    else:
        print("\nRequest succeeded, but no records were returned.")
        print("Inspect the response and backend logs.")

