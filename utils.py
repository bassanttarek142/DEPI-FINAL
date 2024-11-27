import re
from llama_index.core import SimpleDirectoryReader





def clean_text_arabic(text):
    # Normalization
    text = re.sub(r'[أإآا]', 'ا', text)  # Normalize Arabic letters
    text = re.sub(r'[ى]', 'ي', text)
    text = re.sub(r'[ؤئ]', 'ء', text)
    text = re.sub(r'ة', 'ه', text)

    # Remove specified special characters
    special_characters = r'[!@#$%^&*()_ـ+\-={}\[\]:;"\'<>,.?/\\|`~]'
    text = re.sub(special_characters, '', text)  # Remove special characters
    
    # Remove non-Arabic characters except basic punctuation
    text = re.sub(r'[^\u0600-\u06FF0-9a-zA-Z\s]', '', text)  # Allow Arabic letters, English letters, digits, and spaces
    
    # Remove new lines and excess whitespace
    text = re.sub(r'[\r\n]+', ' ', text)  # Remove new lines
    text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and strip
    
    return text

def read_pdf(pdf_path):
    reader = SimpleDirectoryReader(input_files=[pdf_path])
    documents = reader.load_data()
    
    text = ''
    
    for document in documents:
        text += document.text
        
    # Clean the text using the clean_text_arabic function
    cleaned_text = clean_text_arabic(text)
    
    # Save the cleaned text to a .txt file
    file_name = pdf_path.split('.')[0]
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Text written to {file_name}.txt")
    
    return cleaned_text




