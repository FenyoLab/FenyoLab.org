#!C:\Python27\python.exe -u
import sys, os
from pyPdf import PdfFileWriter, PdfFileReader

dir='pdf'
doc1 = PdfFileReader(file('Laboratory-for-Computational-Proteomics-Header.pdf', "rb"))
pages1=doc1.getNumPages()
listing = os.listdir(str(dir))
for document2 in listing:
	print document2
	output = PdfFileWriter()
	doc2 = PdfFileReader(file(dir+'/'+document2, "rb"))
	pages2=doc2.getNumPages()

	for i in range(pages1):
		output.addPage(doc1.getPage(i))
	for i in range(pages2):
		output.addPage(doc2.getPage(i))

	outputStream = file('pdf-processed/'+document2, "wb")
	output.write(outputStream)
	outputStream.close()