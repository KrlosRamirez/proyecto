from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from io import BytesIO

# Create your views here.
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.units import inch
from ..Censo.models import *
from ..Clap.models import *

import datetime
import time

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
var = os.path.join(BASE_DIR, '..\static')

#pdf de los censos

class Censo_p(View):
    def _header_footer(self,canvas,doc):
        canvas.saveState()
        canvas.setTitle("PDF")
        styles = getSampleStyleSheet()
        archivo_imagen = (var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Censo',styles['Heading1'])
            clientes.append(header)
            allclientes = Jefe_familia.objects.all()
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            header5=Paragraph('Lista de familias censadas',styles['Heading4'])
            clientes.append(header5)
            for i in allclientes:
                header7=Paragraph('Jefe de familia: '+str(i.cedula_jefe_familia)+', '+str(i.nombre_jefe_familia),styles['Heading3'])
                clientes.append(header7)

                header8=Paragraph('Carga Familiar ',styles['Heading4'])
                clientes.append(header8)
                header9=Paragraph('',styles['Heading4'])
                clientes.append(header9)
                listas = []
                count = 0
                integrantes = Integrante.objects.filter(jefe_familia=i)
                if integrantes:
                    for a in integrantes:
                        count = count+1
                        vari = (count,a.cedula,a.nombre_integrante,a.apellido_integrante,a.edad,a.is_hijo)
                        listas.append(vari)

                        #TABLA NUMERO 1
                        headings1 = ('N','        Cedula       ','              Nombre          ','              Apellido            ','Edad','     Parentesco    ')
                        t1 = Table([headings1] + listas)
                        t1.setStyle(TableStyle(
                            [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                            ]
                            ))
                        header5=Paragraph('',styles['Heading4'])


                    clientes.append(t1)
                    clientes.append(header5)
                    clientes.append(header5)
                    clientes.append(header5)


            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response

#Reporte de lista de productos:

class Productos_p(View):
    def _header_footer(self,canvas,doc):
        canvas.saveState()
        canvas.setTitle("PDF")
        styles = getSampleStyleSheet()
        archivo_imagen = (var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Productos',styles['Heading1'])
            clientes.append(header)
            allclientes = Producto.objects.all()
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            header5=Paragraph('Lista de productos registrados',styles['Heading4'])
            clientes.append(header5)
            listas = []
            count = 0
            for i in allclientes:
                count = count+1
                vari = (count,i.unidad, i.nombre)
                listas.append(vari)

            #TABLA NUMERO 1
            headings1 = ('N','                       Unidad de Medida                             ','                                        Nombre                                    ')
            t1 = Table([headings1] + listas)
            t1.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            clientes.append(t1)

            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response

#reportes de bolsa asignada a jefe

class Asigna_p(View):
    def _header_footer(self,canvas,doc):
        canvas.setTitle("PDF")
        canvas.saveState()
        styles = getSampleStyleSheet()
        archivo_imagen = (var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Bolsas asignadas',styles['Heading1'])
            clientes.append(header)
            allclientes = Asigna_Bolsa.objects.all()
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            header5=Paragraph('Lista de bolsa asignadas',styles['Heading4'])
            clientes.append(header5)
            listas = []
            count = 0
            for i in allclientes:
                if i.finalizado == False:
                    count = count+1
                    vari = (count,i.jefe_familia.cedula_jefe_familia,i.jefe_familia.nombre_jefe_familia,i.bolsa.codigo,i.bolsa.fecha)
                    listas.append(vari)

            #TABLA NUMERO 1
            headings1 = ('N','             Cedula           ','             Nombre           ','       Codigo Bolsa           ','       Fecha   ')
            t1 = Table([headings1] + listas)
            t1.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            clientes.append(t1)
            clientes.append(header5)
            clientes.append(header5)
            cantidad = len(listas)
            header5=Paragraph('Cantidad de Registros: '+str(cantidad),styles['Heading4'])
            clientes.append(header5)

            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response


#reporte de pago realizado

class Pago_p(View):
    def _header_footer(self,canvas,doc):
        canvas.saveState()
        canvas.setTitle("PDF")
        styles = getSampleStyleSheet()
        archivo_imagen = (var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Pagos',styles['Heading1'])
            clientes.append(header)
            allclientes = Pago_Bolsa.objects.all()
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            header5=Paragraph('Lista de pagos realizados',styles['Heading4'])
            clientes.append(header5)
            listas = []
            count = 0
            for i in allclientes:
                if i.bolsa.finalizado == False:
                    count = count+1
                    vari = (count,i.bolsa.jefe_familia.cedula_jefe_familia,i.bolsa.jefe_familia.nombre_jefe_familia,i.fecha,i.metodo)
                    listas.append(vari)

            #TABLA NUMERO 1
            headings1 = ('N','                   Cedula                ','                 Nombre                  ','             Fecha                    ','       Metodo   ')
            t1 = Table([headings1] + listas)
            t1.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            clientes.append(t1)
            clientes.append(header5)
            clientes.append(header5)
            cantidad = len(listas)
            header5=Paragraph('Cantidad de Registros: '+str(cantidad),styles['Heading4'])
            clientes.append(header5)

            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response

#reportes de entregas realizadas

class Entrega_p(View):
    def _header_footer(self,canvas,doc):
        canvas.saveState()
        canvas.setTitle("PDF")
        styles = getSampleStyleSheet()
        archivo_imagen = (var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Entregas',styles['Heading1'])
            clientes.append(header)
            allclientes = Entrega_Bolsa.objects.all()
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            header5=Paragraph('Lista de entregas realizadas',styles['Heading4'])
            clientes.append(header5)
            listas = []
            count = 0
            for i in allclientes:
                if i.jefe_familia.bolsa.finalizado == False:
                    count = count+1
                    vari = (count,i.jefe_familia.bolsa.jefe_familia.cedula_jefe_familia,i.jefe_familia.bolsa.jefe_familia.nombre_jefe_familia,i.fecha,i.observacion)
                    listas.append(vari)

            #TABLA NUMERO 1
            headings1 = ('N','                   Cedula                ','                 Nombre                  ','             Fecha                    ','       Observacion   ')
            t1 = Table([headings1] + listas)
            t1.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            clientes.append(t1)
            clientes.append(header5)
            clientes.append(header5)
            cantidad = len(listas)
            header5=Paragraph('Cantidad de Registros: '+str(cantidad),styles['Heading4'])
            clientes.append(header5)

            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response

#reporte detalle de lo que contiene la bolsa

class DetaleBolsa_p(View):
    def _header_footer(self,canvas,doc):
        canvas.saveState()
        canvas.setTitle("PDF")
        styles = getSampleStyleSheet()
        archivo_imagen = str(var)+'/img/clap.png'
        canvas.drawImage(archivo_imagen, 35, 700, width=550,preserveAspectRatio=True)
        #iglesia
        header20 = Paragraph('Fecha: '+ time.strftime("%x"), styles['Normal'])
        w, h = header20.wrap(doc.width-320, doc.topMargin)
        header20.drawOn(canvas, 520, doc.height + doc.topMargin+15 )
        footer = Paragraph('', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def get(self,request,pk):
        print ("Genero el PDF")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=110,
                                bottomMargin=40,
                                )
        if request.user:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Reporte de Bolsa',styles['Heading1'])
            clientes.append(header)
            allclientes = Bolsa.objects.get(pk=pk)
            varr = 'Codigo de la Bolsa: '+str(allclientes.codigo)   
            varr2 = ' Precio de la Bolsa: '+str(allclientes.precio_bolsa)
            header1=Paragraph(str(varr),styles['Heading4'])
            header2=Paragraph(str(varr2),styles['Heading4'])
            clientes.append(header1)
            clientes.append(header2)
            header5=Paragraph('',styles['Heading4'])
            clientes.append(header5)
            var = DetalleBolsa.objects.filter(factura=pk)
            listas = []
            count = 0
            count2 =0
            for i in var:
                count = count+1

                vari = (count,i.nombre,i.cantidad)
                listas.append(vari)
            bolsa3 = Asigna_Bolsa.objects.filter(bolsa=pk)
            count1 = 0
            lista2=[]
            for bol in bolsa3:
                count1 = count1+1
                if bol.pagado == True:
                    pagado = 'Si'
                else:
                    pagado='No'
                if bol.entregado == True:
                    entregado = 'Si'
                else:
                    entregado = 'No'
                asigna= (count1,bol.jefe_familia.cedula_jefe_familia,bol.jefe_familia.nombre_jefe_familia,pagado,entregado)
                lista2.append(asigna)
                print ('N ',count1,' ',bol.jefe_familia.nombre_jefe_familia)
                
            print ('el precio total es:', count2)

            header5=Paragraph('Lista de Productos',styles['Heading4'])
            clientes.append(header5)
            header21=Paragraph('',styles['Heading2'])
            clientes.append(header21)
            #TABLA NUMERO 2 
            headings1 = ('N','                         Nombre del producto                        ','                            Cantidad                               ')
            t1 = Table([headings1] + listas)
            t1.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            clientes.append(t1)
            header7=Paragraph('',styles['Heading4'])
            clientes.append(header7)
            header7=Paragraph('',styles['Heading4'])
            clientes.append(header7)
            clientes.append(header7)
            header8=Paragraph('Cantidad total: '+str(allclientes.total),styles['Heading4'])
            clientes.append(header8)
            clientes.append(header7)
            header83=Paragraph('Lista de Jefes de Familia',styles['Heading4'])
            clientes.append(header83)
            clientes.append(header7)



            headings3 = ('N','                Cedula            ','                 Nombre                  ','    Pagada       ', '           Entregada           ')
            t2 = Table([headings3] + lista2)
            t2.setStyle(TableStyle(
                [   ('GRID', (0, 0), (5, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.red)
                ]
                ))
            clientes.append(t2)




            

            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        else:
            clientes = []
            styles = getSampleStyleSheet()
            header=Paragraph('Lista de usuarios registrados',styles['Heading1'])
            clientes.append(header)
            doc.build(clientes,onFirstPage=self._header_footer,onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
        response.write(buff.getvalue())
        buff.close()
        return response

class NumberedCanvas(canvas.Canvas):


    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []


    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()


    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.drawRightString(211 * mm, 4 * mm + (0.1 * inch),"Pagina %d de %d" % (self._pageNumber, page_count))