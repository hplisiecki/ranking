import PyPDF2
import os
def remove_pages_from_pdf(input_pdf, pages_to_remove, output_pdf):
    pdfFileObj = open(input_pdf, 'rb')
    reader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
    writer = PyPDF2.PdfFileWriter()

    for i in range(reader.getNumPages()):
        if i >= pages_to_remove[0] and i <= pages_to_remove[1]:
            writer.addPage(reader.getPage(i))

    with open(output_pdf, 'wb') as out_pdf:
        writer.write(out_pdf)

to_remove = [{"file": r'D:\data\ranking\pdfs\v1-1\-8943323297214106293.pdf', "pages": (10, 23)},
             {"file": r'D:\data\ranking\pdfs\v1-1\1602746341419773044.pdf', "pages": (5, 7)},
             {"file": r'D:\data\ranking\pdfs\v1-1\4844967028235799514.pdf', "pages": (72, 90)},
            {"file": r'D:\data\ranking\pdfs\v1-1\5884129635949712743.pdf', "pages": (46, 56)},
            {"file": r'D:\data\ranking\pdfs\v1-1\7526865343748024152.pdf', "pages": (10, 20)},
             {"file": r'D:\data\ranking\pdfs\v1-1\10-31261_ijrel-2018-5-2-04.pdf', "pages": (49, 61)},
            {"file": r'D:\data\ranking\pdfs\v1\10-1002_pbc-27989.pdf', "pages": (465, 466)},
            {"file": r'D:\data\ranking\pdfs\v1-1\-4396831252506773656.pdf', "pages": (104, 115)},
            {"file": r'D:\data\ranking\pdfs\v1\10-1002_per-2174.pdf', "pages": (20, 21)},
            {"file": r'D:\data\ranking\pdfs\v1\10-1002_per-2128.pdf', "pages": (11, 13)},]


for task in to_remove:
    remove_pages_from_pdf(task["file"], task["pages"], os.path.join(r'D:\data\ranking\pdfs\modified', os.path.basename(task["file"])))

# input_pdf = r'D:\data\ranking\pdfs\v1\10-1002_pbc-27989.pdf'  # Replace with your PDF file path
# pages_range_to_leave = (465, 466)
# output_pdf = 'data/output.pdf'  # Replace with your desired output file path
#
# remove_pages_from_pdf(input_pdf, pages_range_to_leave, output_pdf)
