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
# replace the \ in string with \\
raw_text = text.encode('unicode_escape').decode('utf-8')
import re
regex = r'\\x[0-9]{2}'
modified_text = re.sub(regex, '', raw_text)
# revert unicode escape
modified_text = modified_text.encode('utf-8').decode('unicode_escape')

# save text to file as utf-8
with open('text.txt', 'w', encoding='utf-8') as f:
    f.write(modified_text)
# encode to utf-8
encoded_text = modified_text.encode('utf-8', 'ignore').decode('utf')

regex = r'\\x[0-9]{2}'
modified_text = re.sub(regex, '', test_string)

for t in text:
    t = t.encode('ascii', 'ignore').decode('ascii')
    print(t)
    input()

t = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

# create regex for removing \x03 and \x45

a = r'abc\x03def\x45gh\x123i'
# replace all occurences

test_string = 'TABLE 6 | Results of regression analyses predicting sample size, switching frequency, choices maximizing EV and experienced mean returns in Experiment 2.\nSample size Switching frequency EV choices Experienced mean returns\nPredictor b 95% CI p b 95% CI p b 95% CI p b 95% CI p\nIntercept 22.01\x03\x03(15.51, 28.52) <0.001 0.40\x03\x03(0.32, 0.48) <0.001 4.46\x03\x03(4.11, 4.81) <0.001 5.47 (4.98, 5.97) <0.001\nNumeracy 9.67\x03\x03(3.20, 16.13) 0.003 \x000.11\x03(\x000.19,\x000.03) 0.011 0.17 ( \x000.17, 0.52) 0.325 0.2 ( \x000.3, 0.69) 0.430\nGroup (Fear) 9.16 ( \x003.84, 22.18) 0.165 \x000.08 (\x000.24, 0.08) 0.363 \x000.28 (\x000.98, 0.40) 0.417 \x000.38 (\x001.38, 0.62) 0.453\nNumeracy\x03Group 13.28\x03(0.36, 26.22) 0.044 0.00 ( \x000.16, 0.18) 0.915 0.12 ( \x000.58, 0.80) 0.742 0.44 ( \x000.54, 1.44) 0.373\nR2= 0.169\x03\x03R2= 0.091 R2= 0.019 R2= 0.022\nGroup was coded as 0.5 (Fear)'


modified_string = re.sub(regex, '', test_string)


# remove these from the text string
modified_string = re.sub(regex, '', test_string)



# load
with open('text.txt', 'r', encoding = 'utf-8') as f:
    text = f.read()
t = text.encode('utf-32')
t = text.encode('ascii', 'ignore').decode('ascii')
print(t)

t = text.encode('utf-8')
t = t.replace('\\n', '\n')
