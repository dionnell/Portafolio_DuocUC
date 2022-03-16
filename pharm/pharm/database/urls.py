from django.conf.urls import include, url
from django.urls import include, path
from database.views import medicamento_list, index, medico, funcionario, paciente_view, entrega_view, reserva_view, medicamento_view, prescripcioncreate, detaprescripcioncreate, deta_entrega_view
from database.views import medicamento_list_funcionario,medicamento_edit, prescripcionList, informe_stock, informe_reserva, login_medico, mermacreate, lista_reserva, pres_pdf, ent_pdf, res_pdf, correo_reserv

urlpatterns = [
        url(r'^medico$', medico, name='medico'),
        url(r'^funcionario$', funcionario, name='funcionario'),
        url(r'^lista$', medicamento_list, name='lista'),
        url(r'^paciente$', paciente_view, name='paciente'),
        url(r'^entrega$', entrega_view, name='entrega'),
        url(r'^reserva/(?P<id_det_ent>\d+)/$', reserva_view, name='reserva'),
        url(r'^crearmedicamento$', medicamento_view, name='medicamento_create'),
        url(r'^prescripcion$', prescripcioncreate, name='prescripcion'),
        url(r'^listafun$', medicamento_list_funcionario, name='listafun'),
        url(r'^editar/(?P<id_med>\d+)/$', medicamento_edit, name='editar'),
        url(r'^prescripcionList$', prescripcionList, name='prescripcionList'),
        url(r'^informe_stock$', informe_stock, name='informe_stock'),
        url(r'^informe_reserva$', informe_reserva, name='informe_reserva'),
        url(r'^$', login_medico, name='index'),
        url(r'^merma$', mermacreate, name='merma'),
        url(r'^reservalist$', lista_reserva, name='reservalist'),
        url(r'^pres_pdf/(?P<id_pres>\d+)/$', pres_pdf, name='pres_pdf'),
        url(r'^ent_pdf/(?P<id_entrega>\d+)/$', ent_pdf, name='ent_pdf'),
        url(r'^res_pdf$', res_pdf, name='res_pdf'),
        url(r'^correo_reserv/(?P<id_det_ent>\d+)/$', correo_reserv, name='correo_reserv'),
        url(r'^detaprescripcioncreate$', detaprescripcioncreate, name='detaprescripcioncreate'),
        url(r'^deta_entrega_view$', deta_entrega_view, name='deta_entrega_view'),





]
