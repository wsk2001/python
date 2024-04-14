import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.numPages
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

if __name__ == "__main__":
    pdf_file_path = input("Input PDF file path: ")
    try:
        extracted_text = extract_text_from_pdf(pdf_file_path)
        print("Text extracted from PDF:\n", extracted_text)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error occurs:", e)
