---
name: mineru-parser
description: Parse PDF documents into markdown using MinerU API. Use when users need to extract text, tables, and formulas from PDFs for blog posts, team documentation, or content analysis. Handles task submission, status checking, and markdown retrieval. Supports OCR and VLM model for high accuracy.
---

# MinerU Parser

## Overview

Parse PDF, DOC, DOCX, PPT, PPTX, and image files into markdown format using the MinerU API. Extract text, tables, formulas, and structured content with support for OCR and VLM models.

## Token Setup

**REQUIRED**: MinerU API requires authentication via API token.

### Getting Your Token
1. Visit the MinerU website and register/login
2. Navigate to your account settings or API section
3. Generate or copy your API token

### Recommended: Environment Variable
Set the token as an environment variable before starting work:

```bash
export MINERU_API_KEY="your_api_token_here"
```

In Python, retrieve it with:
```python
import os
token = os.environ.get("MINERU_API_KEY")
if not token:
    raise ValueError("MINERU_API_KEY environment variable not set")
```

### Alternative: Direct Input
If the environment variable is not set, prompt the user for their token:
```python
import os
token = os.environ.get("MINERU_API_KEY")
if not token:
    # Ask user for token
    token = input("Please enter your MinerU API token: ")
```

**Security Note**: Never hardcode tokens in scripts or commit them to version control.

## Workflow

Parsing documents with MinerU involves three steps:

1. **Submit parsing task** - POST request with file URL and parameters
2. **Check task status** - Poll the status endpoint until complete
3. **Retrieve results** - Download markdown/JSON and other formats

## Step 1: Submit Parsing Task

Create a parsing task by sending a POST request to the MinerU API:

```python
import requests
import os

# Get API token from environment variable
token = os.environ.get("MINERU_API_KEY")
if not token:
    raise ValueError("MINERU_API_KEY environment variable not set. Please set it or provide your token.")

url = "https://mineru.net/api/v4/extract/task"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

data = {
    "url": "FILE_URL",  # URL to the file to parse
    "model_version": "vlm"  # Options: "pipeline" (default) or "vlm"
}

response = requests.post(url, headers=headers, json=data)
task_id = response.json()["data"]["task_id"]
```

### Required Parameters

- `url`: File URL (supports .pdf, .doc, .docx, .ppt, .pptx, .png, .jpg, .jpeg)
- Authorization header with Bearer token

### Optional Parameters

Configure parsing behavior with these parameters:

- `model_version`: "pipeline" (default) or "vlm"
- `is_ocr`: Enable OCR (default: false, pipeline only)
- `enable_formula`: Formula recognition (default: true, pipeline only)
- `enable_table`: Table recognition (default: true, pipeline only)
- `language`: Document language (default: "ch")
- `page_ranges`: Specify pages e.g., "2,4-6" or "2--2" (from page 2 to second-to-last)
- `extra_formats`: Additional output formats from ["docx", "html", "latex"]
- `data_id`: Custom identifier for the parsing job
- `callback`: URL for result notifications
- `seed`: Random string for callback signature verification (required when using callback)

### Response

```json
{
  "code": 0,
  "data": {
    "task_id": "a90e6ab6-44f3-4554-b459-b62fe4c6b436"
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}
```

## Step 2: Check Task Status

Poll the status endpoint to check parsing progress:

```python
import time

status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"

while True:
    response = requests.get(status_url, headers=headers)
    data = response.json()["data"]
    
    state = data["state"]
    
    if state == "done":
        result_url = data["full_zip_url"]
        break
    elif state == "failed":
        error_msg = data["err_msg"]
        raise Exception(f"Parsing failed: {error_msg}")
    elif state == "running":
        progress = data["extract_progress"]
        print(f"Progress: {progress['extracted_pages']}/{progress['total_pages']}")
    
    time.sleep(3)  # Wait 3 seconds before next check
```

### Task States

- `pending`: Task is queued
- `running`: Currently parsing
- `converting`: Converting to output formats
- `done`: Parsing complete
- `failed`: Parsing failed (check `err_msg`)

## Step 3: Retrieve Results

Download the results ZIP file:

```python
import requests
import zipfile
from io import BytesIO

# Download ZIP file
zip_response = requests.get(result_url)
zip_file = zipfile.ZipFile(BytesIO(zip_response.content))

# Extract contents
zip_file.extractall("output_directory")

# The ZIP contains:
# - auto/ directory with markdown and JSON files
# - images/ directory with extracted images
# - Additional formats if requested (docx, html, latex)
```

## Output Format

The results ZIP contains:

- **auto/[filename].md**: Extracted markdown content
- **auto/[filename]_content_list.json**: Structured content metadata
- **images/**: Extracted images referenced in markdown
- **[filename].docx/html/latex**: Additional formats if requested

## Limitations

- Max file size: 200MB
- Max pages: 600 pages
- Daily quota: 2000 pages at high priority per account
- GitHub/AWS URLs may timeout due to network restrictions
- Direct file upload not supported (must use URL)

## Best Practices

### Token Management
- **Recommended**: Use `MINERU_API_KEY` environment variable
- Always check if token is set before making API calls
- Never hardcode tokens in scripts
- Prompt user for token if environment variable is not set

### Polling Strategy
- Use 3-5 second intervals to check task status
- Implement timeout logic for long-running tasks
- Display progress updates to user when available

### Error Handling
- Validate API responses before accessing data
- Check response status codes
- Handle failed parsing states gracefully
- Provide clear error messages to users

## Example Usage

**Complete end-to-end example:**

```python
import os
import requests
import time
import zipfile
from io import BytesIO

# Step 0: Get API token
token = os.environ.get("MINERU_API_KEY")
if not token:
    print("MINERU_API_KEY not found in environment variables")
    token = input("Please enter your MinerU API token: ")

# Step 1: Submit parsing task
url = "https://mineru.net/api/v4/extract/task"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

data = {
    "url": "https://example.com/document.pdf",
    "model_version": "vlm"
}

response = requests.post(url, headers=headers, json=data)
task_id = response.json()["data"]["task_id"]
print(f"Task submitted: {task_id}")

# Step 2: Poll for completion
status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"

while True:
    response = requests.get(status_url, headers=headers)
    data = response.json()["data"]
    state = data["state"]
    
    if state == "done":
        result_url = data["full_zip_url"]
        print("Parsing complete!")
        break
    elif state == "failed":
        print(f"Parsing failed: {data['err_msg']}")
        exit(1)
    elif state == "running":
        progress = data.get("extract_progress", {})
        if progress:
            print(f"Progress: {progress['extracted_pages']}/{progress['total_pages']}")
    
    time.sleep(3)

# Step 3: Download and extract results
zip_response = requests.get(result_url)
zip_file = zipfile.ZipFile(BytesIO(zip_response.content))
zip_file.extractall("output_directory")
print("Results saved to output_directory/")
```

**Advanced configuration:**

```python
data = {
    "url": "https://example.com/document.pdf",
    "model_version": "pipeline",
    "is_ocr": True,
    "enable_formula": True,
    "enable_table": True,
    "language": "en",
    "page_ranges": "1-10,15,20-25",
    "extra_formats": ["docx", "html"]
}
```
