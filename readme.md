# Llama PDF Data Extractor

A Streamlit application that extracts structured information from PDF documents using the Llama language model. The app allows users to customize extraction prompts and export results to Excel.

## Features

- **PDF Processing**: Process multiple PDF files in batch
- **Customizable Extraction**:
  - Key Points extraction
  - Named Entities recognition
  - Text Summarization
- **Interactive Interface**:
  - Enable/disable specific prompts
  - Customize prompt text and format
  - Real-time progress tracking
- **Export Capabilities**:
  - View results in an interactive table
  - Export to Excel spreadsheet
  - Each PDF gets its own row with columns matching prompts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llama-pdf-extractor.git
cd llama-pdf-extractor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Requirements
- Python 3.10.7
- Dependencies listed in requirements.txt:
  ```
  streamlit==1.31.0
  pandas==2.0.3
  PyPDF2==3.0.1
  openai==1.12.0
  openpyxl==3.1.2
  ```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Using the interface:
   - Review and customize the default prompts if needed
   - Check/uncheck prompts to include in extraction
   - Upload one or more PDF files
   - Click "Extract Data" to begin processing
   - Download results as Excel file

### Default Extraction Prompts

The application comes with three default prompts:

1. **Key Points**
   - Extracts main takeaways from the text
   - Format: Bulleted list of key points

2. **Named Entities**
   - Identifies people, organizations, locations, and dates
   - Format: Grouped by entity type

3. **Summary**
   - Generates a concise summary of the content
   - Format: 2-3 sentences of clear text

### Customizing Prompts

Each prompt has two customizable components:
- **Prompt Text**: The instruction for information extraction
- **Format**: The expected structure of the response

You can:
- Modify existing prompts through the interface
- Enable/disable prompts for specific extractions
- Adjust formatting requirements

## API Configuration

The application uses a Llama model hosted at a specified endpoint:
```python
LLAMA_CONFIG = {
    "base_url": "http://3.15.181.146:8000/v1/",
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct"
}
```

No API key is required for this implementation.

## Data Processing

1. **PDF Text Extraction**
   - Extracts text content from PDF files
   - Processes all pages in each document

2. **Information Extraction**
   - Uses Llama model for structured information extraction
   - Follows specified prompt formats
   - Handles multiple extraction tasks per document

3. **Results Processing**
   - Organizes extracted information into a structured format
   - Creates downloadable Excel file
   - Maintains file-level organization of extracted data

## Error Handling

The application includes error handling for:
- PDF processing errors
- API communication issues
- Invalid prompt configurations
- Empty or unreadable files

## Limitations

- Maximum text input length: 15,000 characters per chunk
- PDF text extraction quality depends on the PDF format
- Processing time increases with document length and number of prompts
- Session state is not persistent between restarts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Uses Meta's Llama model for extraction
- PDF processing with PyPDF2
- Excel export with openpyxl
