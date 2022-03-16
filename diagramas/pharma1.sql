




create sequence sec_id_pres start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_med start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_entrega start with 1 increment by 1 maxvalue 99999 minvalue 1;
create sequence sec_id_reserva start with 1 increment by 1 maxvalue 99999 minvalue 1;


insert into medicamento values (sec_id_med.nextval, 'Paracetamol', ' se utiliza para tratar los síntomas de la gripe y el resfrío', '500 mg' , 20, 0);
insert into medicamento values (sec_id_med.nextval, 'Tapsin', ' se utiliza para tratar los síntomas de la gripe y el resfrío', '500 mg' , 25, 0);
insert into medicamento values (sec_id_med.nextval, 'Hassapirin ', 'es muy útil para personas con EAC o con antecedentes de accidente cerebrovascular', '500 mg' , 30, 0);
insert into medicamento values (sec_id_med.nextval, 'Ibuprofeno ', 'se utiliza para tratar los síntomas de estados inflamatorios dolorosos', '200 mg' , 20, 0);
insert into medicamento values (sec_id_med.nextval, 'Cardioaspirina ', 'inhibe la adhesión y la aglutinación de las plaquetas en la sangre', '100 mg' , 40, 0);
insert into medicamento values (sec_id_med.nextval, 'Fortotal Senior', 'Multivitamínico + Minerales + Q-10 + Arandanos', '60 gr' , 60, 0);
insert into medicamento values (sec_id_med.nextval, 'Fortotal Mujer', 'Multivitamínico + Minerales + Q-10 + Arandanos', '60 gr' , 60, 0);
insert into medicamento values (sec_id_med.nextval, 'Proctogel Tribenósido', 'Mejora la circulación de la sangre en las venas, tiene un efecto anestésico', '5 gr' , 15, 0);
insert into medicamento values (sec_id_med.nextval, 'Clear Eyes Nafazolina', 'Alivio temporal de la congestión, enrojecimiento e irritación oculares', '15 ml' , 35, 0);
insert into medicamento values (sec_id_med.nextval, 'Istefral Sulpirida', 'Tratamiento de los trastornos depresivos con síntomas psicóticos', '50 mg' , 60, 0);

insert into funcionario values (18849719,'5','daniel','tokio','akito','lala','18849719','poki');
insert into medico values (19819219,'6','daniela','tokia','akita','lalo','oftalmologo','19819219','poki');





