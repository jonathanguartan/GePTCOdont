from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^$', 'Application.views.Index.index'),
    url(r'^index/$', 'Application.views.Index.index'),
    url(r'^login/$', 'Application.views.Index.login'),
    url(r'^logout/$', 'Application.views.Index.logout'),
    url(r'^password/$', 'Application.views.Index.password'),

    url(r'^public/servicios/$', 'Application.views.Index.servicios'),
    url(r'^public/quienessomos/$', 'Application.views.Index.quienessomos'),
    url(r'^public/contactenos/$', 'Application.views.Index.contactenos'),


    url(r'^servicios/$', 'Application.views.Servicio.index'),
    url(r'^servicios/form/(?P<pk>[0-9]+)/$', 'Application.views.Servicio.form'),
    url(r'^servicios/form/$', 'Application.views.Servicio.form'),
    url(r'^servicios/leer/$', 'Application.views.Servicio.leer'),
    url(r'^servicios/guardar/$', 'Application.views.Servicio.guardar'),
    url(r'^servicios/eliminar/$', 'Application.views.Servicio.eliminar'),
    url(r'^servicios/imprimir/$', 'Application.views.Servicio.imprimir'),

    url(r'^productos/$', 'Application.views.Producto.index'),
    url(r'^productos/form/(?P<pk>[0-9]+)/$', 'Application.views.Producto.form'),
    url(r'^productos/form/$', 'Application.views.Producto.form'),
    url(r'^productos/leer/$', 'Application.views.Producto.leer'),
    url(r'^productos/guardar/$', 'Application.views.Producto.guardar'),
    url(r'^productos/eliminar/$', 'Application.views.Producto.eliminar'),
    url(r'^productos/imprimir/$', 'Application.views.Producto.imprimir'),

    url(r'^medicos/$', 'Application.views.Medico.index'),
    url(r'^medicos/form/(?P<pk>[0-9]+)/$', 'Application.views.Medico.form'),
    url(r'^medicos/form/$', 'Application.views.Medico.form'),
    url(r'^medicos/leer/$', 'Application.views.Medico.leer'),
    url(r'^medicos/guardar/$', 'Application.views.Medico.guardar'),
    url(r'^medicos/eliminar/$', 'Application.views.Medico.eliminar'),
    url(r'^medicos/imprimir/$', 'Application.views.Medico.imprimir'),

    url(r'^pacientes/$', 'Application.views.Paciente.index'),
    url(r'^pacientes/form/(?P<pk>[0-9]+)/$', 'Application.views.Paciente.form'),
    url(r'^pacientes/form/$', 'Application.views.Paciente.form'),
    url(r'^pacientes/leer/$', 'Application.views.Paciente.leer'),
    url(r'^pacientes/guardar/$', 'Application.views.Paciente.guardar'),
    url(r'^pacientes/eliminar/$', 'Application.views.Paciente.eliminar'),
    url(r'^pacientes/imprimir/$', 'Application.views.Paciente.imprimir'),

    url(r'^turnos/$', 'Application.views.Turno.index'),
    url(r'^turnos/form/(?P<pk>[a-zA-Z0-9]+)/$', 'Application.views.Turno.form'),
    url(r'^turnos/form/$', 'Application.views.Turno.form'),
    url(r'^turnos/leer/$', 'Application.views.Turno.leer'),
    url(r'^turnos/guardar/$', 'Application.views.Turno.guardar'),
    url(r'^turnos/comprobarfecha/$', 'Application.views.Turno.comprobarFecha'),
    url(r'^turnos/proponerfecha/$', 'Application.views.Turno.proponerFecha'),
    url(r'^turnos/eliminar/$', 'Application.views.Turno.eliminar'),
    url(r'^turnos/imprimir/$', 'Application.views.Turno.imprimir'),

    url(r'^consultas/$', 'Application.views.Consulta.index'),
    url(r'^consultas/paciente/(?P<paciente>[a-zA-Z0-9]+)/$', 'Application.views.Consulta.indexPorPaciente'),
    url(r'^consultas/form/(?P<pk>[a-zA-Z0-9]+)/$', 'Application.views.Consulta.form'),
    url(r'^consultas/form/$', 'Application.views.Consulta.form'),
    url(r'^consultas/leer/$', 'Application.views.Consulta.leer'),
    url(r'^consultas/leer/(?P<paciente>[a-zA-Z0-9]+)/$', 'Application.views.Consulta.leerPorPaciente'),
    url(r'^consultas/guardar/$', 'Application.views.Consulta.guardar'),
    url(r'^consultas/imprimir/$', 'Application.views.Consulta.imprimir'),
    url(r'^consultas/imprimir/(?P<pk>[a-zA-Z0-9]+)/$', 'Application.views.Consulta.imprimirUno'),
    # url(r'^$', 'GePTCOdont.views.home', name='home'),
    # url(r'^GePTCOdont/', include('GePTCOdont.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
