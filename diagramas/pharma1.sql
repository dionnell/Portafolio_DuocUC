




create sequence sec_id_pres start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_med start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_entrega start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_reserva start with 1 increment by 1 maxvalue 99999 minvalue 1;


insert into medicamento values (sec_id_med.nextval, 'Paracetamol', ' se utiliza para tratar los s�ntomas de la gripe y el resfr�o', '500 mg' , 20, 0);
insert into medicamento values (sec_id_med.nextval, 'Tapsin', ' se utiliza para tratar los s�ntomas de la gripe y el resfr�o', '500 mg' , 25, 0);
insert into medicamento values (sec_id_med.nextval, 'Hassapirin ', 'es muy �til para personas con EAC o con antecedentes de accidente cerebrovascular', '500 mg' , 30, 0);
insert into medicamento values (sec_id_med.nextval, 'Ibuprofeno ', 'se utiliza para tratar los s�ntomas de estados inflamatorios dolorosos', '200 mg' , 20, 0);
insert into medicamento values (sec_id_med.nextval, 'Cardioaspirina ', 'inhibe la adhesi�n y la aglutinaci�n de las plaquetas en la sangre', '100 mg' , 40, 0);
insert into medicamento values (sec_id_med.nextval, 'Fortotal Senior', 'Multivitam�nico + Minerales + Q-10 + Arandanos', '60 gr' , 60, 0);
insert into medicamento values (sec_id_med.nextval, 'Fortotal Mujer', 'Multivitam�nico + Minerales + Q-10 + Arandanos', '60 gr' , 60, 0);
insert into medicamento values (sec_id_med.nextval, 'Proctogel Triben�sido', 'Mejora la circulaci�n de la sangre en las venas, tiene un efecto anest�sico', '5 gr' , 15, 0);
insert into medicamento values (sec_id_med.nextval, 'Clear Eyes Nafazolina', 'Alivio temporal de la congesti�n, enrojecimiento e irritaci�n oculares', '15 ml' , 35, 0);
insert into medicamento values (sec_id_med.nextval, 'Istefral Sulpirida', 'Tratamiento de los trastornos depresivos con s�ntomas psic�ticos', '50 mg' , 60, 0);

insert into funcionario values (18849719,'5','daniel','tokio','akito','lala','18849719','poki');
insert into medico values (19819219,'6','daniela','tokia','akita','lalo','oftalmologo','19819219','poki');





