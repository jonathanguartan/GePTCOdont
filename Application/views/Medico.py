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
    editar = False
    if pk is not None:
        objeto = Medico.objects.get(pk=pk);
        editar = True

    return render_to_response('Medico/formulario.html', {'objeto': objeto, 'editar': editar, })


def guardar(request):
    try:

        if request.POST.get('editar', 'False') == 'True':
            pass

        elif len( Medico.objects.filter(cedula=request.POST.get('cedula')) ) > 0:
             return HttpResponse(json.dumps('Cédula ya se encuentra registrada'), mimetype="text/plain")


        lista = Medico.objects.filter(cedula=request.POST.get('cedula'))

        if len(lista) > 0:
            medico = lista[0]

            if request.POST.get('login') == medico.login:
                pass
            else:
                if len( Medico.objects.filter(login=request.POST.get('login')) ) > 0:
                     return HttpResponse(json.dumps('Login ya se encuentra registrado'), mimetype="text/plain")

        else:
            medico = Medico()

            if len( Medico.objects.filter(Q(login=request.POST.get('login')))  ) > 0:
                return HttpResponse(json.dumps('Login ya se encuentra registrado'), mimetype="text/plain")

            medico.cedula = request.POST.get('cedula')
            medico.password = medico.cedula

        medico.nombres = request.POST.get('nombres')
        medico.apellidos = request.POST.get('apellidos')
        medico.login = request.POST.get('login')

        medico.save()


        return HttpResponse('true', mimetype="text/plain")
    except:
        return HttpResponse('Hubo un error al guardar', mimetype="text/plain")


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
