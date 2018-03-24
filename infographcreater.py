from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
pdf = Canvas("bgColour.pdf")
pdf.setFillColor(HexColor("#99b0e7"))
path = pdf.beginPath()
path.moveTo(0*cm,0*cm)
path.lineTo(0*cm,30*cm)
path.lineTo(25*cm,30*cm)
path.lineTo(25*cm,0*cm)
#this creates a rectangle the size of the sheet
pdf.drawPath(path,True,True)
pdf.showPage()
pdf.save()