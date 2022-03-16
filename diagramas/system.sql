
alter session set "_ORACLE_SCRIPT"=true;


CREATE USER pharma2 IDENTIFIED BY pharma2;
GRANT RESOURCE TO pharma2;
GRANT CONNECT TO pharma2;
GRANT DBA TO pharma2;