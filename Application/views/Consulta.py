from datetime import datetime
from django.db.models.query_utils import Q
from django.utils import dateparse
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table
from Application.pdf import crearPDF, bodyPDF, buildPDF, cabeceraPDF


__author__ = 'TOSHIBA'

from django.http import HttpResponse
from Application.models import Turno, Paciente, Medico, Consulta, Servicio, Producto, Detalle_Servicio, Detalle_Producto
from django.shortcuts import render_to_response
import json


def index(request):
    request.session.load()

    pacientes = Paciente.objects.all();
    medicos = Medico.objects.all();

    return render_to_response('Consulta/lista.html', {'pacientes': pacientes, 'medicos': medicos, 'usuario': request.session  })


def indexPorPaciente(request, paciente):
    request.session.load()

    return render_to_response('Consulta/listaPorPaciente.html', {'paciente': paciente})


def form(request, pk=None):
    request.session.load()

    obj = {}
    obj['fecha_hora'] = str(datetime.now())
    obj['servicios'] = []
    obj['productos'] = []
    obj['total'] = 0

    if pk is not None:
        objeto = Consulta.objects.get(pk=pk);
        obj['nro_consulta'] = objeto.nro_consulta
        obj['fecha_hora'] = str(objeto.fecha_hora)
        obj['medico'] = objeto.medico_id
        obj['paciente'] = objeto.paciente_id
        obj['diagnostico'] = objeto.diagnostico
        obj['observacion'] = objeto.observacion
        obj['total'] = objeto.total

        servicios_consulta = Detalle_Servicio.objects.filter(consulta_id=objeto.nro_consulta)
        productos_consulta = Detalle_Producto.objects.filter(consulta_id=objeto.nro_consulta)

        for ser in servicios_consulta:
            temp = {
                'servicio_id': ser.servicio_id,
                'servicio_nombre': ser.servicio.nombre,
                'servicio_precio': ser.servicio.precio
            }
            obj['servicios'].append(temp)

        for pro in productos_consulta:
            temp = {
                'producto_id': pro.producto_id,
                'producto_nombre': pro.producto.nombre,
                'producto_precio': pro.producto.precio,
                'producto_cantidad': pro.cantidad,
                'producto_total': pro.cantidad * pro.producto.precio
            }
            obj['productos'].append(temp)


    turno = request.GET.get('turno', False);
    paciente_id = request.GET.get('paciente_id', False);
    medico_id = request.GET.get('medico_id', False);

    pacientes = Paciente.objects.all();
    medicos = Medico.objects.all();
    servicios = Servicio.objects.all();
    productos = Producto.objects.all();

    return render_to_response('Consulta/formulario.html', {'objeto': obj, 'pacientes': pacientes, 'medicos': medicos, 'servicios': servicios, 'productos': productos, 'turno': turno, 'medico_id': medico_id, 'paciente_id': paciente_id, 'usuario': request.session })


def guardar(request):
    try:
        if request.POST.get('nro_turno', False):
            turno = Turno.objects.get(nro_turno=request.POST.get('nro_turno', 0))
            turno.cumplido = True
            turno.save()

        """ Cabecera """
        consulta = Consulta()

        if not request.POST.get('nro_consulta') == '':
            consulta.nro_consulta = request.POST.get('nro_consulta', None)

        consulta.fecha_hora = dateparse.parse_datetime( request.POST.get('fecha_hora') )
        consulta.paciente_id = request.POST.get('paciente')
        consulta.medico_id = request.POST.get('medico')
        consulta.diagnostico = request.POST.get('diagnostico','')
        consulta.observacion = request.POST.get('observacion','')
        consulta.total = request.POST.get('total',0)

        consulta.save()

        """ Detalle """
        Detalle_Servicio.objects.filter(consulta_id=consulta.nro_consulta).delete()
        Detalle_Producto.objects.filter(consulta_id=consulta.nro_consulta).delete()

        servicios_consulta = json.loads( request.POST.get('servicios', '[]') )
        productos_consulta = json.loads( request.POST.get('productos', '[]') )

        for ser in servicios_consulta:
            Detalle_Servicio.objects.create(
                servicio_id= ser['servicio_id'],
                consulta_id=consulta.nro_consulta
            );

        for pro in productos_consulta:
            Detalle_Producto.objects.create(
                producto_id= pro['producto_id'],
                cantidad= pro['producto_cantidad'],
                consulta_id= consulta.nro_consulta
            );
            producto = Producto.objects.get(pk=pro['producto_id'])
            producto.cantidad = producto.cantidad - float(pro['producto_cantidad'])
            producto.save()

        return HttpResponse(json.dumps(producto.pk), content_type="text/plain")
    except:
        return HttpResponse('false', content_type="text/plain")


def leer(request):
    request.session.load()
    if request.session.get('login') == 'Administrador':
        medico = request.GET.get('medico', '')
    else:
        medico = request.session.get('cedula')
    query = request.GET.get('query', '')
    fecha_hora = request.GET.get('fecha_hora', '')
    page = request.GET.get('page')
    rows = request.GET.get('rows')

    lista = Consulta.objects.filter(Q(paciente__nro_historia__icontains=query) | Q(paciente__cedula__icontains=query) | Q(paciente__apellidos__icontains=query) | Q(paciente__nombres__icontains=query)).order_by('nro_consulta', 'fecha_hora')
    if not medico == '':
        lista = lista.filter(medico_id=medico)
    if not fecha_hora == '':
        lista = lista.filter(fecha_hora__contains=dateparse.parse_date(fecha_hora))


    if len(lista) > 0:
        lista_ = lista[(int(page) - 1) * (int(rows)) : (int(page)) * (int(rows))];
    else:
        lista_ = []

    rows = []
    for l in lista_:
        row = {}

        row['nro_consulta'] = l.nro_consulta
        row['paciente_id'] = l.paciente_id
        row['paciente'] = l.paciente.apellidos + ' ' + l.paciente.nombres
        row['medico_id'] = l.medico_id
        row['medico'] = l.medico.apellidos + ' ' + l.medico.nombres
        row['fecha_hora'] = str(l.fecha_hora.date()) + ' ' + str(l.fecha_hora.time())
        row['diagnostico'] = l.diagnostico
        row['observacion'] = l.observacion
        row['total'] = l.total

        rows.append(row)

    valor = {
        'rows': rows,
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), content_type="text/plain")


def leerPorPaciente(request, paciente=None):

    lista = Consulta.objects.filter(paciente_id=paciente).order_by('nro_consulta', 'fecha_hora')

    rows = []
    for l in lista:
        row = {}

        row['nro_consulta'] = l.nro_consulta
        row['paciente_id'] = l.paciente_id
        row['paciente'] = l.paciente.apellidos + ' ' + l.paciente.nombres
        row['medico_id'] = l.medico_id
        row['medico'] = l.medico.apellidos + ' ' + l.medico.nombres
        row['fecha_hora'] = str(l.fecha_hora.date()) + ' ' + str(l.fecha_hora.time())
        row['diagnostico'] = l.diagnostico
        row['observacion'] = l.observacion
        row['total'] = l.total

        rows.append(row)

    valor = {
        'rows': rows,
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), content_type="text/plain")


def imprimir(request):
    query = request.GET.get('query', '')
    medico = request.GET.get('medico', '')
    fecha_hora = request.GET.get('fecha_hora', '')

    querys = []
    lista = Consulta.objects.filter(Q(paciente__nro_historia__icontains=query) | Q(paciente__cedula__icontains=query) | Q(paciente__apellidos__icontains=query) | Q(paciente__nombres__icontains=query)).order_by('nro_consulta', 'fecha_hora')
    if not query == '':
        querys.append( 'filtro: ' + query )
    if not medico == '':
        querys.append( 'cédula del medico: ' + medico )
        lista = lista.filter(medico_id=medico)
    if not fecha_hora == '':
        querys.append( 'fecha y hora: ' + fecha_hora )
        lista = lista.filter(fecha_hora__contains=dateparse.parse_date(fecha_hora))

    rows = []
    for l in lista:
        row = {}

        row['nro_consulta'] = l.nro_consulta
        row['paciente'] = l.paciente.apellidos + ' ' + l.paciente.nombres
        row['medico'] = l.medico.apellidos + ' ' + l.medico.nombres
        row['fecha_hora'] = str(l.fecha_hora.date()) + ' ' + str(l.fecha_hora.time())
        row['diagnostico'] = l.diagnostico
        row['observacion'] = l.observacion
        row['total'] = l.total

        rows.append(row)

    dataHead = [
        {
            'field': 'nro_consulta',
            'text': 'Nro.',
            'width': 60
        },
        {
            'field': 'fecha_hora',
            'text': 'Fecha y Hora',
            'width': 110
        },
        {
            'field': 'paciente',
            'text': 'Paciente',
            'width': 200,
        },
        {
            'field': 'medico',
            'text': 'Medico',
            'width': 200
        }
    ]

    pdf = crearPDF('Listado de Consultas', dataHead, rows, '', querys);

    response = HttpResponse(content_type='application/pdf')
    response.write(pdf)

    return response


def imprimirUno(request, pk=None):

    try:
        objeto = Consulta.objects.get(pk=pk);

        servicios = []
        productos = []

        servicios_consulta = Detalle_Servicio.objects.filter(consulta_id=objeto.nro_consulta)
        productos_consulta = Detalle_Producto.objects.filter(consulta_id=objeto.nro_consulta)

        for ser in servicios_consulta:
            temp = {
                'servicio_id': ser.servicio_id,
                'servicio_nombre': ser.servicio.nombre,
                'servicio_precio': ser.servicio.precio
            }
            servicios.append(temp)

        for pro in productos_consulta:
            temp = {
                'producto_id': pro.producto_id,
                'producto_nombre': pro.producto.nombre,
                'producto_precio': pro.producto.precio,
                'producto_cantidad': pro.cantidad,
                'producto_total': pro.cantidad * pro.producto.precio
            }
            productos.append(temp)


        """
        Construccion del PDF
        """

        serviciosHead = [
            {
                'field': 'servicio_id',
                'text': 'Nro.',
                'width': 60
            },
            {
                'field': 'servicio_nombre',
                'text': 'Servicio',
                'width': 250
            },
            {
                'field': 'servicio_precio',
                'text': 'Precio',
                'width': 100,
            }
        ]

        productosHead = [
            {
                'field': 'producto_id',
                'text': 'Nro.',
                'width': 60
            },
            {
                'field': 'producto_nombre',
                'text': 'Producto',
                'width': 200
            },
            {
                'field': 'producto_precio',
                'text': 'Precio',
                'width': 50,
            },
            {
                'field': 'producto_cantidad',
                'text': 'Cantidad',
                'width': 50,
            },
            {
                'field': 'producto_total',
                'text': 'Total',
                'width': 50,
            }
        ]



        table = [
            ['Nro Consulta: ', str(objeto.nro_consulta) ],
            ['Fecha y Hora: ', str(objeto.fecha_hora) ],
            ['Médico: ', str(objeto.medico.apellidos) + ' ' + str(objeto.medico.nombres) ],
            ['Paciente: ', str(objeto.paciente.apellidos) + ' ' + str(objeto.paciente.nombres) ],
            ['Diagnóstico: ', str(objeto.diagnostico) ],
            ['Observación: ', str(objeto.observacion) ],
        ]
        tabla = Table(data=table, hAlign='LEFT');
        tabla.setStyle( [('TEXTCOLOR',(0, 0), (0, 5), colors.toColorOrNone('#00438a'))] )

        tableTotal = [
            ['Total: ', str(objeto.total) ],
        ]
        tablaTotal = Table(data=tableTotal, hAlign='RIGHT');
        tablaTotal.setStyle( [('TEXTCOLOR',(0, 0), (0, 0), colors.toColorOrNone('#00438a'))] )


        story = []
        story.append( cabeceraPDF('Consulta') )
        story.append(Spacer(0,20))
        story.append(tabla)
        story.append(Spacer(0,20))
        story.append( Paragraph('Servicios', getSampleStyleSheet()['Heading3']) )
        story.append( bodyPDF(serviciosHead, servicios) )
        story.append(Spacer(0,20))
        story.append( Paragraph('Productos', getSampleStyleSheet()['Heading3']) )
        story.append( bodyPDF(productosHead, productos) )
        story.append(Spacer(0,20))
        story.append( tablaTotal )


        #Impresion
        pdf = buildPDF( story )
        response = HttpResponse(content_type='application/pdf')
        response.write(pdf)

        return response

    except:
        return HttpResponse('false', content_type="text/plain")