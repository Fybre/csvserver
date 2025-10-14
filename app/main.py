from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv, json, os, uuid, glob
from pathlib import Path

description = """

"""

app = FastAPI(
        title="CSV REST Server API", 
        description="A simple REST API server to upload CSV files and access their data as JSON.",
        version="1.0.0",
        license_info={
            "name": "Apache 2.0",
            "identifier": "MIT",
        }
)


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def list_csv_files():
    files = []
    for meta_file in glob.glob(os.path.join(DATA_DIR, "*.json")):
        with open(meta_file) as f:
            meta = json.load(f)
            files.append(meta)
    return files


# --- REST endpoints ---

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    filename: str | None = Form(None)
):
    # If filename is specified, overwrite
    if filename:
        assigned_filename = filename
    else:
        assigned_filename = str(uuid.uuid4())

    csv_path = os.path.join(DATA_DIR, f"{assigned_filename}.csv")
    meta_path = os.path.join(DATA_DIR, f"{assigned_filename}.json")

    # Save uploaded CSV file
    with open(csv_path, "wb") as f:
        f.write(await file.read())

    # Save metadata
    meta = {
        "original_filename": file.filename,
        "stored_filename": f"{assigned_filename}.csv",
        "endpoint": assigned_filename
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return {"message": "File uploaded successfully", "meta": meta}


@app.get("/list")
def list_files():
    return list_csv_files()


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    """Delete both CSV and JSON metadata for a given filename."""
    csv_path = os.path.join(DATA_DIR, f"{filename}.csv")
    meta_path = os.path.join(DATA_DIR, f"{filename}.json")

    deleted = []
    missing = []

    # Delete CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)
        deleted.append(csv_path)
    else:
        missing.append(csv_path)

    # Delete metadata file
    if os.path.exists(meta_path):
        os.remove(meta_path)
        deleted.append(meta_path)
    else:
        missing.append(meta_path)

    if not deleted:
        raise HTTPException(status_code=404, detail="No files found for deletion")

    return {
        "message": "Deletion complete",
        "deleted": deleted,
        "missing": missing
    }


@app.get("/uploadpage", response_class=HTMLResponse, include_in_schema=False)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/listpage", response_class=HTMLResponse, include_in_schema=False)
def list_page(request: Request):
    files = list_csv_files()
    return templates.TemplateResponse("list.html", {"request": request, "files": files})


@app.get("/{filename}")
async def get_csv_data(filename: str):
    """Return JSON array from a CSV file."""
    csv_path = os.path.join(DATA_DIR, f"{filename}.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail=f"CSV file '{filename}' not found")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return JSONResponse(content=rows)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return upload_page(request)
