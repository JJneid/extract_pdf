import streamlit as st
import pandas as pd
import PyPDF2
import io
from openai import OpenAI
import tempfile
import os

# Llama configuration
LLAMA_CONFIG = {
    "base_url": "http://3.15.181.146:8000/v1/",
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct"
}

# Default prompts for general data extraction
DEFAULT_PROMPTS = [
    {
        "title": "Key Points",
        "prompt": "Extract the main key points or takeaways from the text. List each point separately.",
        "format": "- Point 1\n- Point 2\n- Point 3\netc."
    },
    {
        "title": "Named Entities",
        "prompt": "Extract important named entities (people, organizations, locations, dates) mentioned in the text. Group them by type.",
        "format": "People: [names]\nOrganizations: [org names]\nLocations: [places]\nDates: [dates]"
    },
    {
        "title": "Summary",
        "prompt": "Provide a concise summary of the main content in 2-3 sentences.",
        "format": "Clear, concise summary text"
    }
]

def initialize_session_state():
    """Initialize session state variables."""
    if 'prompts' not in st.session_state:
        st.session_state.prompts = DEFAULT_PROMPTS.copy()

def get_llama_client():
    """Initialize and return the Llama client."""
    return OpenAI(base_url=LLAMA_CONFIG["base_url"], api_key='None')

def extract_info_from_pdf(pdf_file, prompts):
    """Extract information from a PDF file using Llama."""
    # Read PDF content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        tmp_file.seek(0)
        
        pdf_reader = PyPDF2.PdfReader(tmp_file.name)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    os.unlink(tmp_file.name)
    
    # Get Llama client
    client = get_llama_client()
    
    # Prepare the extraction prompt
    system_message = """You are an AI assistant that extracts structured information from text.
    Extract the requested information precisely according to the specified formats.
    If information is not found, respond with 'Not found in text'.
    Be concise and focused in your responses."""
    
    extraction_prompt = f"""Analyze the following text and extract the requested information:

{text[:15000]}...

Please extract the following information, following the exact format specified for each:

{chr(10).join([f'{i+1}. {prompt["prompt"]} Format: {prompt["format"]}' for i, prompt in enumerate(prompts)])}"""

    try:
        response = client.chat.completions.create(
            model=LLAMA_CONFIG["model"],
            temperature=0,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": extraction_prompt}
            ]
        )
        
        response_text = response.choices[0].message.content
        
        # Extract answers from the response
        answers = response_text.split('\n')
        answers = [ans.split('. ', 1)[1] if '. ' in ans else ans 
                  for ans in answers if ans.strip() and not ans.startswith('Here')]
        
        return answers
    
    except Exception as e:
        st.error(f"Error with Llama API: {str(e)}")
        return None

def main():
    st.title("PDF Data Extractor (Llama)")
    
    # Initialize session state
    initialize_session_state()
    
    # Display current prompts
    st.subheader("Extraction Prompts")
    
    prompts_to_use = []
    for i, prompt in enumerate(st.session_state.prompts):
        with st.expander(f"{prompt['title']}"):
            new_prompt = st.text_area(
                "Prompt",
                value=prompt["prompt"],
                key=f"prompt_{i}",
                help="What information should be extracted?"
            )
            new_format = st.text_input(
                "Format",
                value=prompt["format"],
                key=f"format_{i}",
                help="How should the extracted information be formatted?"
            )
            use_prompt = st.checkbox("Use this prompt", value=True, key=f"use_{i}")
            
            if use_prompt:
                prompts_to_use.append({
                    "title": prompt["title"],
                    "prompt": new_prompt,
                    "format": new_format
                })
    
    # File uploader
    st.subheader("Upload PDF Files")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Select one or more PDF files to process"
    )
    
    if uploaded_files and st.button("Extract Data", help="Click to start extraction"):
        if not prompts_to_use:
            st.warning("Please select at least one prompt to use.")
            return
            
        data = []
        progress_bar = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            progress_text = st.empty()
            progress_text.text(f"Processing {file.name}...")
            
            try:
                answers = extract_info_from_pdf(file, prompts_to_use)
                
                if answers:
                    file_data = {"Filename": file.name}
                    for prompt, answer in zip(prompts_to_use, answers):
                        file_data[prompt["title"]] = answer
                    data.append(file_data)
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
            
            progress_bar.progress((i + 1) / len(uploaded_files))
            progress_text.empty()
        
        if data:
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Display the results
            st.subheader("Extracted Data")
            st.dataframe(df, use_container_width=True)
            
            # Download button
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            
            st.download_button(
                label="Download Excel file",
                data=excel_buffer,
                file_name="extracted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download the extracted data as an Excel file"
            )

if __name__ == "__main__":
    main()