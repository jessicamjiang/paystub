import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file: #open as a binary file
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    print(text)
    return text

def extract_information(text):
    withholding_patterns_current = {
        "Federal Income Tax": r"(?:Fed Withholdng|Federal Withholding|Fed Income Tax)\s+(\d+\.\d{2})",
        "State Income Tax": r"(?:GA Withholdng|State Withholding)\s+(\d+\.\d{2})",
        "Social Security": r"(?:Fed Social Sec|Social|Social Security)\s+(\d+\.\d{2})",
        "Medicare": r"Medicare\s*([\d\.]+)"
    }
    withholding_patterns_ytd = {
        "Federal Income Tax YTD": r"(?:Fed Withholdng|Federal Withholding|Fed Income Tax)\s+(\d+\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})",
        "State Income Tax YTD": r"(?:GA Withholdng|State Withholding)\s+(\d+\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})",
        "Social Security YTD": r"(?:Fed Social Sec|Social|Social Security)\s+(\d+\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})",
        "Medicare YTD": r"Medicare\s+(\d+\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})"
        }

    withholding_data_current = {}

    for key, pattern in withholding_patterns_current.items():
        match = re.search(pattern, text)
        if match:
            withholding_data_current[key] = match.group(1)
        else:
            withholding_data_current[key] = 0.0

    withholding_data_ytd = {}

    for key, pattern in withholding_patterns_ytd.items():
        match = re.search(pattern, text)
        if match:
            try:
                withholding_data_ytd[key] = match.group(2)
            except:
                IndexError
        else:
            withholding_data_ytd[key] = 0.0

    return withholding_data_current, withholding_data_ytd


pdf_path = r'C:\Users\jessi\source\repos\paystub-analyzer\Verizon_paycheck.pdf' # Replace with your PDF file path
extracted_text = extract_text_from_pdf(pdf_path)
withholding_data_current, withholding_data_ytd = extract_information(extracted_text)

if isinstance(withholding_data_current, str):
    print(withholding_data_current)
else:
    for key, value in withholding_data_current.items():
        #print(f"{key}: {value:.2f}")
        print(f"{key}: {value}")

if isinstance(withholding_data_ytd, str):
    print(withholding_data_ytd)
else:
    for key, value in withholding_data_ytd.items():
        #print(f"{key}: {value:.2f}")
        print(f"{key}: {value}")
