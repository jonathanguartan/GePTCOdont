import json
from webbrowser import get
from django.db.models.query_utils import Q
from Application.pdf import crearPDF

__author__ = 'TOSHIBA'

from django.http import HttpResponse
from Application.models import Paciente
from django.shortcuts import render_to_response
from json import JSONEncoder
import json


def index(request):
    request.session.load()

    return render_to_response('Paciente/lista.html', {'usuario': request.session })

def form(request, pk=None):
    request.session.load()

    objeto = {}
    editar = False
    if pk is not None:
        objeto = Paciente.objects.get(pk=pk);
        editar = True

    return render_to_response('Paciente/formulario.html', {'objeto': objeto, 'editar': editar, 'usuario': request.session })


def guardar(request):
    try:
        paciente = Paciente()

        if request.POST.get('editar', 'False') == 'True':
            pass

        elif len( Paciente.objects.filter(Q(nro_historia=request.POST.get('nro_historia'))) ) > 0:
             return HttpResponse(json.dumps('Nro de Historia repetida'), mimetype="text/plain")

        elif len( Paciente.objects.filter(Q(cedula=request.POST.get('cedula'))) ) > 0:
             return HttpResponse(json.dumps('Cédula ya se encuentra registrada'), mimetype="text/plain")

        paciente.nro_historia = request.POST.get('nro_historia')
        paciente.cedula = request.POST.get('cedula')
        paciente.nombres = request.POST.get('nombres')
        paciente.apellidos = request.POST.get('apellidos')
        paciente.sexo = request.POST.get('sexo')
        paciente.ciudad = request.POST.get('ciudad')
        paciente.direccion = request.POST.get('direccion')
        paciente.telefono = request.POST.get('telefono')
        paciente.email = request.POST.get('email')
        paciente.save()

        return HttpResponse('true', mimetype="text/plain")

    except:
        return HttpResponse(json.dumps('Hubo un error al guardar'), mimetype="text/plain")


def eliminar(request):
    try:
        pk = request.POST.get('nro_historia')
        paciente = Paciente.objects.get(pk=pk)
        paciente.delete()

        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")


def leer(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page')
    rows = request.GET.get('rows')
    lista = Paciente.objects.filter(Q(nro_historia__icontains=query) | Q(cedula__icontains=query) | Q(nombres__icontains=query) | Q(apellidos__icontains=query)).order_by('nro_historia')

    valor = {
        'rows': list(lista[(int(page) - 1) * (int(rows)) : (int(page)) * (int(rows))].values()),
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), mimetype="text/plain")


def imprimir(request):
    query = request.GET.get('query', '')
    lista = Paciente.objects.filter(Q(nro_historia__icontains=query) | Q(cedula__icontains=query) | Q(nombres__icontains=query) | Q(apellidos__icontains=query)).order_by('nro_historia')

    lista = list(lista.values())

    dataHead = [
        {
            'field': 'nro_historia',
            'text': 'Historia',
            'width': 100
        },
        {
            'field': 'cedula',
            'text': 'Cédula',
            'width': 80
        },
        {
            'field': 'apellidos',
            'text': 'Apellidos',
            'width': 160
        },
        {
            'field': 'nombres',
            'text': 'Nombres',
            'width': 160
        }
    ]

    pdf = crearPDF('Listado de Pacientes', dataHead, lista, '', query);

    response = HttpResponse(mimetype='application/pdf')
    response.write(pdf)
    #response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response
