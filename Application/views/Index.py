from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from Application.models import Medico


def index(request):
    if request.session.get('login', '') == '':
        #return redirect('/login')
        return render_to_response('Publico/index.html')

    else:
        request.session.load()
        return render_to_response('index.html', { 'usuario': request.session })


def servicios(request):
    return render_to_response('Publico/servicios.html')

def quienessomos(request):
    return render_to_response('Publico/quienes-somos.html')

def contactenos(request):
    return render_to_response('Publico/contactenos.html')



def login(request):
    request.session.load()

    if request.session.get('login', '') != '':
        return redirect('/')


    if request.method == 'POST':

        login = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if not login == '' or not password == '':

            try:
                medico = Medico.objects.get(login=login, password=password)


                request.session['login'] = medico.login
                request.session['password'] = medico.password
                request.session['cedula'] = medico.cedula
                request.session['nombres'] = medico.apellidos + ' ' + medico.nombres
                request.session.save()

                return redirect('/')
            except:
                return render_to_response('login.html', {'error': 'Login o Password incorrecto'})

        else:
            return render_to_response('login.html', {'error': 'No se ha ingresado datos'})

    else:
        return render_to_response('login.html')

def logout(request):
    request.session.load()
    request.session.delete()

    return redirect('/')

def password(request):

    if request.method == 'POST':

        response = HttpResponse(mimetype='text/plain')

        try:
            request.session.load()

            login = request.session.get('login', '')
            password = request.session.get('password', '')

            if password == request.POST.get('passwordold'):

                if request.POST.get('password') == request.POST.get('passwordrepeat'):
                    medico = Medico.objects.get(login=login, password=password)
                    medico.password = request.POST.get('password', password)
                    medico.save()

                    response.write('true')

                    request.session['password'] = medico.password
                else:
                    response.write('Las contraseñas no coinciden')

            else:
                response.write('Contraseña de usuario no válida')

        except:
            response.write('false')


        return response

    else:
        return render_to_response('password.html')

