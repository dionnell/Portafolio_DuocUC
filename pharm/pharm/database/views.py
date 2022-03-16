from django.conf import settings

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from database.models import Paciente, Prescripcion, DetallePrescripcion, EntregaMedicamento, ReservaMedicamento, Medicamento
from django.contrib.auth.decorators import login_required


from django.db import connection
import cx_Oracle
from django.contrib.auth import authenticate, login

from io import BytesIO
from django.template.loader import get_template

from xhtml2pdf import pisa 

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required(login_url='/')
def medico(request):

    return render(request, 'medico.html')

@login_required(login_url='/')
def funcionario(request):
    return render(request, 'funcionario.html')


def login_medico(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User = authenticate(username=username, password=password)
        if User is not None:
            if User.is_medical == True:
                login(request, User)
                return redirect('paciente')
            if User.is_pharma == True:
                login(request, User)
                return redirect('listafun')
        else:
            return render(request, 'iniciosesionmedico.html')
    else:
        return render(request, 'iniciosesionmedico.html')

    

@login_required(login_url='/')
def paciente_view(request):

    data = {}

    if request.method == 'POST':
        rut_pac = request.POST.get('rut_pac')
        DV = request.POST.get('DV')
        pri_nombre = request.POST.get('pri_nombre')
        seg_nombre = request.POST.get('seg_nombre')
        ape_paterno = request.POST.get('ape_paterno')
        ape_materno = request.POST.get('ape_materno')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        inscripcion_fam = request.POST.get('inscripcion_fam')
        salida = agregar_paciente(rut_pac, DV, pri_nombre, seg_nombre, ape_paterno,
                                  ape_materno, edad, sexo, telefono, email, inscripcion_fam)
        if salida == 1:
            data['mensaje'] = "Agregado corectamente"
        else:
            data['mensaje'] = "No se ha podido agregar"

    return render(request, 'paciente_form.html', data)

def agregar_paciente(rut_pac, DV, pri_nombre, seg_nombre, ape_paterno, ape_materno, edad, sexo, telefono, email, inscripcion_fam):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_paciente", [rut_pac, DV, pri_nombre, seg_nombre,
                                         ape_paterno, ape_materno, edad, sexo, telefono, email, inscripcion_fam, salida])
    return salida.getvalue()

@login_required(login_url='/')
def entrega_view(request):
    data = {
           'usuario':filtro_usuario(),
    }

    if request.method == 'POST':
        id_entrega = request.POST.get('id_entrega')
        id_pres = request.POST.get('id_pres')
        rut_func = request.POST.get('rut_func')
        salida = agregar_entrega(id_entrega, id_pres, rut_func)
        if salida == 1:
            return redirect('deta_entrega_view')
        else:
            data['mensaje'] = "No se ha podido agregar"
    return render(request, 'entrega_form.html', data)

@login_required(login_url='/')
def deta_entrega_view(request):
    data = {
        'pres': ultima_ent(),
    }

    if request.method == 'POST':
        id_det_ent = request.POST.get('id_det_ent')
        id_entrega = request.POST.get('id_entrega')
        retiro = request.POST.get('retiro')
        salida = agregar_detalle_ent(id_det_ent, id_entrega, retiro)
        if salida == 1:
            data['mensaje'] = "Agregado corectamente"
        else:
            data['mensaje'] = "No se ha podido agregar"
    return render(request, 'deta_entrega_form.html', data)


def agregar_entrega(id_entrega, id_pres, rut_func):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_entrega", [
                    id_entrega, id_pres, rut_func, salida])
    return salida.getvalue()

def agregar_detalle_ent(id_det_ent, id_entrega, retiro):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_detalle_ent", [
                    id_det_ent, id_entrega, retiro, salida])
    return salida.getvalue()


def listar_entregas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_entregas", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@login_required(login_url='/')
def reserva_view(request, id_det_ent):
    data = {
        'filtro' : listar_reservas_id(id_det_ent)
    }

    if request.method == 'POST':
        id_det_ent = request.POST.get('id_det_ent')
        id_entrega = request.POST.get('id_entrega')
        estado = request.POST.get('estado')
        salida = modificar_reser(id_det_ent, id_entrega, estado)
        if salida == 1:
            data['mensaje'] = "modificado corectamente"
            data['filtro'] = listar_reservas_id(id_det_ent)
        else:
            data['mensaje'] = "No se a podido modificado"

    return render(request, 'reserva_form.html', data)

def agregar_reserva(id_reserva, id_entrega, detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_reserva", [
                    id_reserva, id_entrega, detalle, salida])
    return salida.getvalue()

@login_required(login_url='/')
def medicamento_view(request):
    data = {}

    if request.method == 'POST':
        id_med = request.POST.get('id_med')
        nombre = request.POST.get('nombre')
        detalle = request.POST.get('detalle')
        gramaje = request.POST.get('gramaje')
        stock = request.POST.get('stock')
        fabricante = request.POST.get('fabricante')
        componentes = request.POST.get('componentes') 
        tipo = request.POST.get('tipo')
        salida = agregar_medicamentos(
            id_med, nombre, detalle, gramaje, stock, fabricante, componentes, tipo)
        if salida == 1:
            data['mensaje'] = "Agregado corectamente"
        else:
            data['mensaje'] = "No se ha podido agregar"
    return render(request, 'medicamento_form.html', data)

@login_required(login_url='/')
def prescripcioncreate(request):
    data = {
        'usuario':filtro_usuario(),
    }

    if request.method == 'POST':
        id_pres = request.POST.get('id_pres')
        rut_medico = request.POST.get('rut_medico')
        rut_pac = request.POST.get('rut_pac')
        salida = agregar_prescripcion(id_pres, rut_medico, rut_pac)
        if salida == 1:
            return redirect('detaprescripcioncreate')
        else:
            data['mensaje'] = "No se ha podido agregar"
    return render(request, 'prescripcion_form.html', data)

@login_required(login_url='/')
def detaprescripcioncreate(request):
    data = {
        'medicamentos': mostrar_medicamentos(),
        'pres': ultima_pres(),
    }

    if request.method == 'POST':
        id_pres = request.POST.get('id_pres')
        id_med = request.POST.get('id_med')
        descripcion = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        salida = agregar_detalle(id_pres, id_med, descripcion, cantidad)
        if salida == 1:
            data['mensaje'] = "Agregado corectamente"
        else:
            data['mensaje'] = "No se ha podido agregar"
    return render(request, 'detaprescripcion_form.html', data)

def agregar_prescripcion(id_pres, rut_medico, rut_pac):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_prescripcion", [id_pres, rut_medico, rut_pac, salida])
    return salida.getvalue()

def agregar_detalle(id_pres, id_med, descripcion, cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_detalle", [
                    id_pres, id_med, descripcion, cantidad, salida])
    return salida.getvalue()

@login_required(login_url='/')
def medicamento_list_funcionario(request):
    data = {
        'medicamentos': mostrar_medicamentos(),
        'mermas': cant_merma()
    }
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        data['medicamentos'] = buscar_medicamentos(nombre)
        data['mermas'] = cant_merma()
    return render(request, 'medicamento_list_fun.html', data)

def mostrar_medicamentos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_medicamentos", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

@login_required(login_url='/')
def prescripcionList(request):
    data = {
        'prescripciones': listar_prescripciones()
    }
    if request.method == 'POST':
        rut_pac = request.POST.get('rut_pac')
        data['prescripciones'] = buscar_prescripciones(rut_pac)
    return render(request, 'prescripcion_list.html', data)

@login_required(login_url='/')
def medicamento_edit(request, id_med):
    data = {
        'filtro': listar_medicamentos_id(id_med),
    }
    if request.method == 'POST':
        stock = request.POST.get('stock')
        cantidad = request.POST.get('cantidad') 
        salida = modificar_medicamentos(
            id_med, stock, cantidad)
        if salida == 1:
            data['mensaje'] = "modificado corectamente"
            data['filtro'] = listar_medicamentos_id(id_med)
        else:
            data['mensaje'] = "No se a podido modificado"

    return render(request, 'medicamento_edit.html', data)

@login_required(login_url='/')
def medicamento_list(request):
    data = {
        'medicamentos': mostrar_medicamentos(),
    }
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        data['medicamentos'] = buscar_medicamentos(nombre)

    return render(request, 'medicamento_list.html', data)

def agregar_medicamentos(id_med, nombre, detalle, gramaje, stock, fabricante, componentes, tipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_medicamentos", [
                    id_med, nombre, detalle, gramaje, stock, fabricante, componentes, tipo, salida])
    return salida.getvalue()

def listar_prescripciones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_prescripciones", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def informe_medicamentos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("informe_medicamentos", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def informe_stock(request):
    data = {
        'informe': informe_medicamentos(),
        'mermas':cant_merma(),
        'medicamentos': mostrar_medicamentos()
    }
    pdf = render_to_pdf('informe_stock.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def listar_reservas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_reservas", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def informe_reserva(request):
    data = {
        'reservas': listar_reservas(),
    }
    pdf = render_to_pdf('informe_reserva.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def listar_medicamentos_id(id_med):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_medicamentos_id", [out_cur, id_med])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def modificar_medicamentos(id_med, stock, cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("modificar_medicamentos", [
                    id_med, stock, cantidad, salida])
    return salida.getvalue()

def filtro_medico(user_medic):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("filtro_medico", [out_cur, user_medic])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def filtro_usuario():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("user_activo", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def cant_merma():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_merma", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def modificar_reser(id_det_ent, id_entrega, estado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("modificar_reserva", [
                    id_det_ent, id_entrega, estado, salida])
    return salida.getvalue()


def listar_reservas_id(id_reserva):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_reservas_id", [out_cur, id_reserva])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def agregar_merma(merma_id, id_med, cantidad, detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("agregar_merma", [
                    merma_id, id_med, cantidad, detalle, salida])
    return salida.getvalue()

@login_required(login_url='/')
def mermacreate(request):
    data = {
        'medicamentos': mostrar_medicamentos()
    }

    if request.method == 'POST':
        merma_id = request.POST.get('merma_id')
        id_med = request.POST.get('id_med')
        cantidad = request.POST.get('cantidad')
        detalle = request.POST.get('detalle')
        salida = agregar_merma(merma_id, id_med, cantidad, detalle)
        if salida == 1:
            data['mensaje'] = "Agregado corectamente"
        else:
            data['mensaje'] = "No se ha podido agregar"

    return render(request, 'merma_form.html', data)

@login_required(login_url='/')
def lista_reserva(request):
    data = {
        'reservas': listar_reservas(),
    }
    if request.method == 'POST':
        rut_pac = request.POST.get('rut_pac')
        data['reservas'] = buscar_reservas(rut_pac)
    return render(request, 'reserva_list.html', data)


def render_to_pdf (template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None


def ultima_pres():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ultima_pres", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def filtro_id_pres(id_pres):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("filtro_id_pres", [out_cur,id_pres])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def filtro_solo_id_pres(id_pres):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("filtro_solo_id_pres", [out_cur,id_pres])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def pres_pdf(request, id_pres):
    data = {
        'pres': filtro_solo_id_pres(id_pres),
        'filtro': filtro_id_pres(id_pres),
    }
    pdf = render_to_pdf('pres_pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def ultima_ent():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ultima_ent", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def ultima_id_ent(id_entrega):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ultima_id_ent", [out_cur,id_entrega])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def ent_pdf(request, id_entrega):
    data = {
        'pres': ultima_ent(),
        'ent': ultima_id_ent(id_entrega),
    }
    pdf = render_to_pdf('ent_pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def ultima_res():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("ultima_res", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def res_pdf(request):
    data = {
        'res': ultima_res(),
    }
    pdf = render_to_pdf('res_pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def send_email(mail):
    context = {'mail': mail}

    template = get_template('correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Cesfam Reserva Medicamento',
        'Reserva Cesfam',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

@login_required(login_url='/')
def correo_reserv(request, id_det_ent):

    data = {
        'filtro' : reservas_correo(id_det_ent)
    }

    if request.method =='POST':
        mail = request.POST.get('mail')

        send_email(mail)

    return render(request, 'correo_reserv.html', data)


def reservas_correo(id_det_ent):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("reservas_correo", [out_cur, id_det_ent])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def filtro_med_id(id_med):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("filtro_med_id", [out_cur,id_med])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def buscar_medicamentos(nombre):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("buscar_medicamentos", [out_cur,nombre])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def buscar_prescripciones(rut_pac):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("buscar_prescripciones", [out_cur,rut_pac])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def buscar_reservas(rut_pac):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("buscar_reservas", [out_cur,rut_pac])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

