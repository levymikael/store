drop database if exists store;
create database store;

USE store;
drop table if exists category;

create table category(
cat_id INT primary key NOT NULL AUTO_INCREMENT,
category varchar(30)
);

