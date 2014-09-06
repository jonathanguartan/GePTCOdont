from datetime import datetime, timedelta
from django.db.models.query_utils import Q
from django.utils import dateparse
from setuptools.command.build_ext import if_dl
from Application.pdf import crearPDF


__author__ = 'TOSHIBA'

from django.http import HttpResponse
from Application.models import Turno, Paciente, Medico
from django.shortcuts import render_to_response
from json import JSONEncoder
import json


def index(request):
    request.session.load()

    pacientes = Paciente.objects.all();
    medicos = Medico.objects.all();

    return render_to_response('Turno/lista.html', {'pacientes': pacientes, 'medicos': medicos, 'usuario': request.session })


def form(request, pk=None):
    request.session.load()

    objeto = {}
    obj = {}

    if pk is not None:
        objeto = Turno.objects.get(pk=pk);
        obj['nro_turno'] = objeto.nro_turno
        obj['fecha_hora'] = str(objeto.fecha_hora)
        obj['paciente'] = objeto.paciente_id
        obj['medico'] = objeto.medico_id
        obj['cumplido'] = objeto.cumplido

    pacientes = Paciente.objects.all();
    medicos = Medico.objects.all();

    return render_to_response('Turno/formulario.html', {'objeto': obj, 'pacientes': pacientes, 'medicos': medicos, 'usuario': request.session })


def guardar(request):
    try:
        turno = Turno()

        if not request.POST.get("nro_turno") == '':
            turno.nro_turno = request.POST.get('nro_turno', None)

        turno.fecha_hora = dateparse.parse_datetime(request.POST.get('fecha_hora'))
        turno.paciente_id = request.POST.get('paciente')
        turno.medico_id = request.POST.get('medico')

        turno.save()

        return HttpResponse('true', mimetype="text/plain")
    except Exception:
        Exception
        return HttpResponse('false', mimetype="text/plain")


def comprobarFecha(request):
    nro_turno = request.POST.get('nro_turno', '0')
    fecha_hora = request.POST.get('fecha_hora', '')

    try:
        turnos = Turno.objects.filter(fecha_hora__contains=dateparse.parse_datetime(fecha_hora))

        if len(turnos) < 1:
            return HttpResponse('true', mimetype="text/plain")
        else:
            if str(turnos[0].nro_turno) == nro_turno:
                return HttpResponse('true', mimetype="text/plain")
            else:
                return HttpResponse('false', mimetype="text/plain")
    except:
        return HttpResponse('true', mimetype="text/plain")


def proponerFecha(request):

    turnos = Turno.objects.all().order_by('-fecha_hora')

    string = ''
    if len(turnos) < 1:
        fecha_hora = datetime.now()

        string = str(fecha_hora.date()) + ' ' + str(fecha_hora.time())
    else:
        fecha_hora = turnos[0].fecha_hora + timedelta(hours=1);
        string = str(fecha_hora.date()) + ' ' + str(fecha_hora.time())

    return HttpResponse(json.dumps(string), mimetype="text/plain")


def eliminar(request):
    try:
        pk = request.POST.get('nro_turno')
        turno = Turno.objects.get(pk=pk)
        turno.delete()

        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")


def leer(request):
    request.session.load()

    if request.session.get('login') == 'Administrador':
        medico = request.GET.get('medico', '')
    else:
        medico = request.session.get('cedula')
    query = request.GET.get('query', '')
    fecha_hora = request.GET.get('fecha_hora', '')
    cumplido = request.GET.get('cumplido', '')
    page = request.GET.get('page')
    rows = request.GET.get('rows')

    lista = Turno.objects.filter(Q(paciente__cedula__icontains=query) | Q(paciente__apellidos__icontains=query) | Q(paciente__nombres__icontains=query)).order_by('nro_turno')
    if not medico == '':
        lista = lista.filter(medico_id=medico)
    if not fecha_hora == '':
        lista = lista.filter(fecha_hora__contains=dateparse.parse_date(fecha_hora))
    if not cumplido == '':
        lista = lista.filter(cumplido=bool(int(cumplido)))


    lista_ = lista[(int(page) - 1) * (int(rows)) : (int(page)) * (int(rows))];
    rows = []
    for l in lista_:
        row = {}

        row['nro_turno'] = l.nro_turno
        row['paciente_id'] = l.paciente_id
        row['paciente'] = l.paciente.apellidos + ' ' + l.paciente.nombres
        row['medico_id'] = l.medico_id
        row['medico'] = l.medico.apellidos + ' ' + l.medico.nombres
        row['fecha_hora'] = str(l.fecha_hora.date()) + ' ' + str(l.fecha_hora.time())

        c = 'No'
        if l.cumplido == True:
            c = 'Si'
        row['cumplido'] = c

        rows.append(row)

    valor = {
        'rows': rows,
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), mimetype="text/plain")


def imprimir(request):
    query = request.GET.get('query', '')
    medico = request.GET.get('medico', '')
    fecha_hora = request.GET.get('fecha_hora', '')
    cumplido = request.GET.get('cumplido', '')

    querys = []
    lista = Turno.objects.filter(Q(paciente__cedula__icontains=query) | Q(paciente__apellidos__icontains=query) | Q(paciente__nombres__icontains=query)).order_by('nro_turno')
    if not query == '':
        querys.append( 'filtro: ' + query )
    if not medico == '':
        querys.append( 'cédula del medico: ' + medico )
        lista = lista.filter(medico_id=medico)
    if not fecha_hora == '':
        querys.append( 'fecha y hora: ' + fecha_hora )
        lista = lista.filter(fecha_hora__contains=dateparse.parse_date(fecha_hora))
    if not cumplido == '':
        if bool(int(cumplido)):
            querys.append( 'cumplido: ' + 'Sí' )
        else:
            querys.append( 'cumplido: ' + 'No' )
        lista = lista.filter(cumplido=bool(int(cumplido)))

    rows = []
    for l in lista:
        row = {}

        row['nro_turno'] = l.nro_turno
        row['paciente'] = l.paciente.apellidos + ' ' + l.paciente.nombres
        row['medico'] = l.medico.apellidos + ' ' + l.medico.nombres
        row['fecha_hora'] = str(l.fecha_hora.date()) + ' ' + str(l.fecha_hora.time())

        c = 'No'
        if l.cumplido == True:
            c = 'Si'
        row['cumplido'] = c

        rows.append(row)


    dataHead = [
        {
            'field': 'nro_turno',
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

    pdf = crearPDF('Listado de Turnos', dataHead, rows, '', querys);

    response = HttpResponse(mimetype='application/pdf')
    response.write(pdf)

    return response
