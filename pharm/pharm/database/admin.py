from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import DetallePrescripcion, EntregaMedicamento, Funcionario, Medicamento, Medico, Paciente, Prescripcion, ReservaMedicamento
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(DetallePrescripcion)
admin.site.register(EntregaMedicamento)
admin.site.register(Funcionario)
admin.site.register(Medicamento)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Prescripcion)
admin.site.register(ReservaMedicamento)