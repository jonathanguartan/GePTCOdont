import json
from webbrowser import get
from django.db.models.query_utils import Q
from Application.pdf import crearPDF

__author__ = 'TOSHIBA'

from django.http import HttpResponse
from Application.models import Medico
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('Medico/lista.html')


def form(request, pk=None):

    objeto = {}
    if pk is not None:
        objeto = Medico.objects.get(pk=pk);

    return render_to_response('Medico/formulario.html', {'objeto': objeto})


def guardar(request):
    try:
        lista = Medico.objects.filter(cedula=request.POST.get('cedula'))

        if len(lista) > 0:
            medico = lista[0]

        else:
            medico = Medico()
            medico.cedula = request.POST.get('cedula')
            medico.password = medico.cedula

        medico.nombres = request.POST.get('nombres')
        medico.apellidos = request.POST.get('apellidos')
        medico.login = request.POST.get('login')

        medico.save()


        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")


def eliminar(request):
    try:
        pk = request.POST.get('cedula')
        medico = Medico.objects.get(pk=pk)
        medico.delete()

        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('false', mimetype="text/plain")


def leer(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page')
    rows = request.GET.get('rows')
    lista = Medico.objects.filter(Q(cedula__icontains=query) | Q(nombres__icontains=query) | Q(apellidos__icontains=query)).order_by('cedula')

    valor = {
        'rows': list(lista[(int(page) - 1) * (int(rows)) : (int(page)) * (int(rows))].values()),
        'total': lista.count()
    }

    return HttpResponse(json.dumps(valor), mimetype="text/plain")


def imprimir(request):
    query = request.GET.get('query', '')
    lista = Medico.objects.filter(Q(cedula__icontains=query) | Q(nombres__icontains=query) | Q(apellidos__icontains=query)).order_by('cedula')

    lista = list(lista.values())

    dataHead = [
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
        },
        {
            'field': 'login',
            'text': 'Login',
            'width': 100
        }
    ]

    pdf = crearPDF('Listado de Médicos', dataHead, lista, '', query);

    response = HttpResponse(mimetype='application/pdf')
    response.write(pdf)
    #response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response
