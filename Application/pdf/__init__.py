from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

__author__ = 'COMPAQ'

from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def crearPDF(head, dataHead, data, foot, query=''):
    story = []

    story.append(Spacer(0,10))

    cabecera = cabeceraPDF(head)
    story.append(cabecera)

    if(not query == ''):
        story.append(Spacer(0,10))

        consultas = queryBody(query)
        for cons in consultas:
            story.append(cons)

    story.append(Spacer(0,20))

    cuerpo = bodyPDF(dataHead, data)
    story.append(cuerpo)

    story.append(Spacer(0,20))

    pie = footPDF(foot)
    story.append(pie)

    return buildPDF(story)



def cabeceraPDF(head):
    estiloHoja = getSampleStyleSheet()

    estilo = estiloHoja['Heading2']
    estilo.pageBreakBefore=0
    estilo.keepWithNext=0
    estilo.backColor = colors.toColorOrNone('#FFFEE6')
    estilo.textColor = colors.toColorOrNone('#8F5700')
    estilo.alignment = TA_CENTER
    return Paragraph(head, estilo)


def queryBody(query):
    ret = []

    estiloHoja = getSampleStyleSheet()

    estilo = estiloHoja['Definition']
    estilo.pageBreakBefore=0
    estilo.keepWithNext=0
    estilo.textColor = colors.toColorOrNone('#8F5700')
    estilo.alignment = TA_LEFT

    if not isinstance(query, list):
        data = 'Resultados obtenidos dado el siguiente filtro: "' + query + '"'
        ret.append(Paragraph(data, estilo))

    else:
        if len(query) > 0:
            data = 'Resultados obtenidos dado: '
            ret.append( Paragraph(data, estilo) )

            for q in query:
                ret.append( Paragraph(' -- '  + q, estilo) )


    return ret


def bodyPDF(dataHead, data):

    rows = len(data)
    cols = len(dataHead)
    dataRaw = []

    widths = []
    headraw = []
    fields = []
    aligns = []

    if len(data) > 0:

        for dh in dataHead:
            fields.append( dh.get('field', None) )
            headraw.append( dh.get('text', None) )
            widths.append( dh.get('width', None) )
            aligns.append( dh.get('align', 'LEFT') )

        dataRaw.append( headraw )

        for d in data:
            raw = []

            for f in fields:
                raw.append( d.get( f, '') )

            dataRaw.append(raw)

        tabla = Table(data=dataRaw, colWidths=widths);

        tabla.setStyle([('ALIGN',(0, 0), (cols-1, 0), 'CENTER')])
        tabla.setStyle([('TEXTCOLOR',(0, 0), (cols-1, 0),colors.toColorOrNone('#00438a'))])
        tabla.setStyle([('TEXTCOLOR',(0, 0), (cols-1, 0),colors.toColorOrNone('#00438a'))])
        tabla.setStyle([('LINEBELOW',(0, 0), (cols-1, 0), 2, colors.chocolate)])


        for c in range(0, cols):
            tabla.setStyle([('ALIGN', (c, 0), (c, rows), aligns[c])])

        tabla.setStyle([('BACKGROUND',(0,1),(cols-1, rows), colors.white)])
        tabla.setStyle([('BOX',(0,1),(cols-1, rows), 0.10, colors.gray)])
        tabla.setStyle([('INNERGRID',(0,1),(cols-1, rows), 0.10, colors.toColorOrNone('#BABABA'))])

        return tabla

    else:
        estiloHoja = getSampleStyleSheet()
        texto = 'No hay registros'

        estilo = estiloHoja['BodyText']
        estilo.alignment = TA_RIGHT
        return Paragraph(texto, estilo)


def footPDF(foot):
    estiloHoja = getSampleStyleSheet()

    estilo = estiloHoja['BodyText']
    estilo.alignment = TA_RIGHT
    return Paragraph(foot, estilo)


def buildPDF(story):
    doc=SimpleDocTemplate("PDF.pdf",pagesize=A4,showBoundary=0)
    doc.build(story)

    return doc.canv.getpdfdata()