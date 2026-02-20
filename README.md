# CSV Server

A lightweight FastAPI application for uploading, listing, and serving CSV data as JSON endpoints. Now features a modern drag-and-drop interface and per-endpoint authorization.

## Features

- **Drag & Drop Upload**: Upload CSV files via a dashed drop zone or traditional file browser.
- **Custom Endpoints**: Specify an optional filename to create a predictable URL for your data.
- **Per-Endpoint Authorization**: Secure specific datasets with a custom `X-Auth-Key`.
- **JSON Transformation**: Automatically converts CSV rows into a JSON array of objects.
- **Management UI**: Simple interface to view all uploaded files and their authorization status.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd csvserver
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Using Python (local)
Start the server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker Compose
Build and run the container:

```bash
docker-compose up --build
```

Access the UI at: `http://localhost:8000`

## API Usage

### Upload a File
**POST** `/upload`
- `file`: The CSV file (multipart/form-data)
- `filename` (optional): The ID to use for the endpoint.
- `auth_key` (optional): A string to protect the endpoint.

### Access Data
**GET** `/{filename}`
- If an `auth_key` was set during upload, you must include the following header:
  `X-Auth-Key: <your_key>`

**Example with curl:**
```bash
curl -H "X-Auth-Key: secret123" http://localhost:8000/my-data
```

### List Files
**GET** `/list`
Returns metadata for all uploaded files.

### Delete a File
**DELETE** `/delete/{filename}`
Removes both the CSV data and its metadata.

## Project Structure

- `app/main.py`: Core FastAPI application logic.
- `app/templates/`: Jinja2 HTML templates for the UI.
- `app/data/`: Storage for uploaded CSVs and JSON metadata.
- `app/static/`: Static assets (CSS/JS).
