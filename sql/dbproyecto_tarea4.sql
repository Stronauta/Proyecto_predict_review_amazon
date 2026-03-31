CREATE DATABASE bd_proyecto;
USE bd_proyecto;

create table usuarios(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    clave VARCHAR(255) NOT NULL
);

create table predicciones(
	id_predict int auto_increment primary key,
    texto varchar(150) not null,
    prediccion varchar(150) not null
);

select * from usuarios 

insert into usuarios(nombre ,usuario, clave) values ('Samir Ernesto', 'admin', 'SA1234');