from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
from reportlab.lib.styles import ParagraphStyle


Title = "Hello world"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
 canvas.saveState()
 canvas.setFont('Times-Bold',16)
 canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
 canvas.setFont('Times-Roman',9)
 canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
 canvas.restoreState()

def myLaterPages(canvas, doc):
 canvas.saveState()
 canvas.setFont('Times-Roman', 9)
 canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
 canvas.restoreState()


def go():
 doc = SimpleDocTemplate("phello.pdf")
 Story = [Spacer(1,2*inch)]
 style = styles["Normal"]
 pstyle = ParagraphStyle(name="parastyle", parent=styles["Normal"], fontSize=15, alignment=TA_CENTER)
 # for i in range(100):
 #    bogustext = ("This is Paragraph number %s. " % i) *20
 #    p = Paragraph(bogustext, style)
 #    Story.append(p)
 #    Story.append(Spacer(1,0.2*inch))

 data = [
     [
        Paragraph("0,0<super>2</super>", pstyle), Paragraph("0,1", style), Paragraph("0,2", style)
     ],[
         Paragraph("1,0", style), Paragraph("1,1", style), Paragraph("1,2", style)
     ],[
         Paragraph("2,0", style), Paragraph("2,1", style), Paragraph("2,2", style)
     ],[
         Paragraph("3,0", style), Paragraph("3,1", style), "3,2"
     ]
 ]
 t = Table(data=data, style=[('SPAN', (0,0), (1,1)),('GRID', (0,0), (-1,-1), 1, colors.black), ('ALIGN', (0,0), (-1, -1), 'CENTER'), ('VALIGN', (0,0), (-1, -1), 'MIDDLE')])
 # Story.append(t)


 big_data = [
    [t, ""],
     [Spacer(1, 4*inch, "")]
    ]
 t2 = Table(data=big_data, style=[
                                ("GRID", (0,0), (-1,-1), 1, colors.black),
                                  ("SPAN", (0,1), (1,1)),
                                  ("SPAN", (0,0), (1,0)),
                                  ("LEFTPADDING", (0,0), (1,0), 0),
                                    ("RIGHTPADDING", (0, 0), (1, 0), 0),
     ("BOTTOMPADDING", (0, 0), (1, 0), 0),
     ("TOPPADDING", (0, 0), (1, 0), 0),

                                  ])
 Story.append(t2)
 doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


go()