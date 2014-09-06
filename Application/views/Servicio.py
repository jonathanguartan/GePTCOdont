import json
from webbrowser import get
from Application.pdf import crearPDF

__author__ = 'TOSHIBA'

from django.http import HttpResponse
from Application.models import Servicio
from django.shortcuts import render_to_response
from json import JSONEncoder
import json


def index(request):
    return render_to_response('Servicio/lista.html')

def form(request, pk=None):

    objeto = {}
    if pk is not None:
        objeto = Servicio.objects.get(pk=pk);

    return render_to_response('Servicio/formulario.html', {'objeto': objeto})


def guardar(request):
    try:
        servicio = Servicio()

        if not request.POST.get("id") == '':
            servicio.id = request.POST.get('id', None)

        servicio.nombre = request.POST.get('nombre')
        servicio.precio = float(request.POST.get('precio'))
        servicio.save()

        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")

def eliminar(request):
    try:
        pk = request.POST.get('id')
        servicio = Servicio.objects.get(pk=pk)
        servicio.delete()

        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")


def leer(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page')
    rows = request.GET.get('rows')
    lista = Servicio.objects.filter(nombre__icontains=query).order_by('nombre')

    valor = {
        'rows': list(lista[(int(page) - 1) * (int(rows)) : (int(page)) * (int(rows))].values()),
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), mimetype="text/plain")


def imprimir(request):
    query = request.GET.get('query', '')
    lista = Servicio.objects.filter(nombre__icontains=query).order_by('nombre')

    lista = list(lista.values())


    dataHead = [
        {
            'field': 'nombre',
            'text': 'Nombre',
            'width': 300
        },
        {
            'field': 'precio',
            'text': 'Precio',
            'width': 50,
            'align': 'RIGHT'
        }
    ]

    pdf = crearPDF('Listado de Servicios', dataHead, lista, '', query);

    response = HttpResponse(mimetype='application/pdf')
    response.write(pdf)
    #response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response
