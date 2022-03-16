from django import forms
from database.models import Paciente, Prescripcion, DetallePrescripcion, EntregaMedicamento, ReservaMedicamento, Medicamento



class pacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente

        fields = [
            'rut_pac',
            'dv',
            'pri_nombre',
            'seg_nombre',
            'ape_paterno',
            'ape_materno',
            'edad',
            'sexo',
            'telefono',
            'email',
            'inscripcion_fam'
        ]
        labels = {
            'rut_pac':'Rut del paciente',
            'dv':'digito verificador del rut',
            'pri_nombre':'Primer nombre',
            'seg_nombre':'Segundo Nombre',
            'ape_paterno':'Apellido paterno',
            'ape_materno':'Apellido materno',
            'edad':'Edad',
            'sexo':'Sexo',
            'telefono':'Telefono',
            'email':'Email',
            'inscripcion_fam':'Inscripcion familiar'
        }
        widgets = {
            'rut_pac':forms.NumberInput(),
            'dv':forms.Select(),
            'pri_nombre':forms.TextInput(),
            'seg_nombre':forms.TextInput(),
            'ape_paterno':forms.TextInput(),
            'ape_materno':forms.TextInput(),
            'edad':forms.NumberInput(),
            'sexo':forms.Select(),
            'telefono':forms.NumberInput(),
            'email':forms.EmailInput(),
            'inscripcion_fam':forms.Select()
        }

class pressForm(forms.ModelForm):

    class Meta:
        model = Prescripcion

        fields = [

            'rut_medico',
            'rut_pac'
        ]
        labels = {

            'rut_medico':'Rut medico',
            'rut_pac':'rut paciente'
        }
        widgets = {

            'rut_medico':forms.NumberInput(),
            'rut_pac':forms.NumberInput()
        }

class detalleForm(forms.ModelForm):

    class Meta:
        model = DetallePrescripcion

        fields = [
            
            'id_med',
            'descripcion',
            'cantidad'
        ]
        labels = {
            
            'id_med':'medicamento',
            'descripcion':'despcripcion de la prescripcion',
            'cantidad':'cantidad de medicamento'
        }
        widgets = {
            
            'id_med':forms.Select(),
            'descripcion':forms.TextInput(),
            'cantidad':forms.NumberInput()
        }

class entregaForm(forms.ModelForm):

    class Meta:
        model = EntregaMedicamento

        fields = [
            
            'id_pres',
            'rut_func',

        ]
        labels = {
            
            'id_pres':'ID Prescripcion',
            'rut_func':'Rut del funcionario',
 
        }
        widgets = {
            
            'id_pres':forms.Select(),
            'rut_func':forms.NumberInput(),

        }

class reservaForm(forms.ModelForm):

    class Meta:
        model = ReservaMedicamento

        fields = [
            
            'id_entrega',
            'detalle'
        ]
        labels = {
            
            'id_entrega':'ID entrega',
            'detalle':'Informacion de la reserva',
        }
        widgets = {
            
            'id_entrega':forms.Select(),
            'detalle':forms.TextInput(),
        }

class medicamentoForm(forms.ModelForm):

    class Meta:
        model = Medicamento

        fields = [
            
            'nombre',
            'detalle',
            'gramaje',
            'stock',
            'merma'
        ]
        labels = {
           
            'nombre':'nombre medicamento',
            'detalle':'detalle medicamento',
            'gramaje':'gramaje del medicamento',
            'stock':'cantidad de medicamento',
            'merma':'medicamento vencido/dañado'
        }
        widgets = {
           
            'nombre':forms.TextInput(),
            'detalle':forms.TextInput(),
            'gramaje':forms.TextInput(),
            'stock':forms.NumberInput(),
            'merma':forms.NumberInput()
        }

