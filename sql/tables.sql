create table users(
id integer primary key auto_increment,
    tel_id integer,
    name varchar(255),
    username varchar(255),
    is_auth integer,
    is_admin integer,
    is_delete integer
);

create table passwords(
	id integer primary key auto_increment,
    value varchar(255),
    is_used integer
);