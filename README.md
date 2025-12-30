# MinerU Parser

[English](README.md) | [中文](README_zh.md)

A PDF document parsing tool based on Claude Agent SDK and MinerU Skill, supporting parsing PDF documents into Markdown format.

## ⚠️ Important Notice

**This project only supports online version**. PDF documents must be accessed via URL. Local file upload is not supported.

## 📋 Prerequisites

- Python 3.7+
- `MINERU_API_KEY` environment variable (required)

## 🔑 Configure API Key

Before using this project, you must configure the MinerU API key:

```bash
export MINERU_API_KEY='your_api_key_here'
```

### Getting Your API Key

1. Visit [MinerU website](https://mineru.net) and register/login
2. Navigate to your account settings or API section
3. Generate or copy your API key

### Verify Configuration

Run the following command to verify that the API key is correctly set:

```bash
echo $MINERU_API_KEY
```

If the output is empty, please set the environment variable again.

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd mineru-parser
```

### Step 2: Install Dependencies

Install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install `claude-agent-sdk` and its dependencies.

### Step 3: Configure API Key

Set the `MINERU_API_KEY` environment variable. See the [Configure API Key](#-configure-api-key) section above for detailed instructions.

## 💻 Usage

### Basic Usage

1. Ensure `MINERU_API_KEY` environment variable is set
2. Modify the PDF URL in `demo.py`
3. Run the script:

```bash
python demo.py
```

### Command Line Options

```bash
# Run invoice parsing
python demo.py

# Test skill availability
python demo.py --test

# Show help information
python demo.py --help
```

## 📝 Example

`demo.py` demonstrates how to use MinerU Skill to parse invoice PDFs:

- Extract basic invoice information (invoice code, invoice number, issue date)
- Extract buyer and seller information
- Extract product details
- Extract tax amount and total amount information
- Extract signature information

Parsing results will be saved to the `invoice_parsed/` directory.

## 🔧 Configuration

The project uses Claude Agent SDK's Skills feature with the following configuration:

- **Skills Source**: Loaded from project directory `.claude/skills/`
- **Permission Mode**: `bypassPermissions` (automatically accept all operations)
- **Supported Tools**: Skill, view, create_file, str_replace

## 📚 Features

- ✅ Support for PDF, DOC, DOCX, PPT, PPTX, and image files
- ✅ Extract text, tables, formulas, and structured content
- ✅ Support for OCR and VLM models
- ✅ Output in Markdown format
- ✅ Automatically save parsing results

## ⚠️ Limitations

- Only supports online documents accessed via URL
- Local file upload is not supported
- Maximum file size: 200MB
- Maximum pages: 600 pages
- Daily quota: 2000 pages (high priority)

## 🐛 Troubleshooting

### Error: MINERU_API_KEY not set

```
❌ Error: MINERU_API_KEY environment variable not set
```

**Solution**:
```bash
export MINERU_API_KEY='your_api_key'
```

### PDF URL Not Accessible

Ensure the PDF URL is publicly accessible and your network connection is working properly.

### Skill Not Available

Run the test command to check:
```bash
python demo.py --test
```

Ensure the `.claude/skills/mineru-parser/` directory exists and is configured correctly.

## 📄 License

Please refer to the project license file.

## 🤝 Contributing

Issues and Pull Requests are welcome!
