# from pathlib import Path
# from PyPDF2 import PdfReader

# reader = PdfReader(Path("/Users/phillipmcdonough/Desktop/McDonough_Phil_J.pdf"))
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

# print(f"Number of pages: {number_of_pages}")
# print(f"Text: {text}")


# from docx import Document

# doc = Document("/Users/phillipmcdonough/Desktop/McDonough_Phil_J.docx")
# text = "\n".join([p.text for p in doc.paragraphs])
# print(text)


from pathlib import Path
test = Path("/Users/phillipmcdonough/Desktop/test.txt")

if test.suffix == ".txt":
    with open(test, "r") as file:
        t = file.read()
print(t)
