from PyPDF2 import PdfFileMerger
import os


x = [a for a in os.listdir() if a.endswith(".pdf")]
x = sorted(x, key=str.lower)
print(x)

merger = PdfFileMerger(strict=False)

for pdf in x:
    merger.append(open(pdf, 'rb'))

with open("result.pdf", "wb") as fout:
    merger.write(fout)