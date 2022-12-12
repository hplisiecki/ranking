import os
import PyPDF2


pdf_dir = r'D:\data\ranking\swps'


for idx, file in enumerate(os.listdir(pdf_dir)):
    if '.pdf' in file:
        pdfFileObj = open(os.path.join(pdf_dir, file), 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        # text = []
        text = ''
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            # text.append(pageObj.extractText())
            text += pageObj.extractText()
        # if idx == 8:
        break


for t in text:
    t = t.encode('ascii', 'ignore').decode('ascii')
    print(t)
    input()

t = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

# create regex for removing [\x number number] characters
import re
regex = r'\\x[0-9][0-9]'
# remove these from the text string
modified_string = re.sub(regex, '', test_string)

# save text to file as utf-8
with open('text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

# load
with open('text.txt', 'r', encoding = 'utf-8') as f:
    text = f.read()
t = text.encode('utf-32')
t = text.encode('ascii', 'ignore').decode('ascii')
print(t)

t = text.encode('utf-8')
t = t.replace('\\n', '\n')
