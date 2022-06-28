create table users
(
    id          int auto_increment
        primary key,
    name        varchar(255)                        null,
    email       text                                null,
    create_date timestamp default CURRENT_TIMESTAMP null,
    password    varchar(120)                        null
);

INSERT INTO myflaskappdb.users (id, name, email, create_date, password) VALUES (3, 'Yael', 'yael@post.gbu.ac.il', '2022-06-14 18:15:56', '121212');
INSERT INTO myflaskappdb.users (id, name, email, create_date, password) VALUES (4, 'Jesica', 'jesi@bgu.ac.il', '2022-06-14 18:43:39', '4572634587263894');
INSERT INTO myflaskappdb.users (id, name, email, create_date, password) VALUES (5, 'arseni', 'yossi@aaa.aaa', '2022-06-21 11:09:43', '1234');
INSERT INTO myflaskappdb.users (id, name, email, create_date, password) VALUES (7, 'a', 'a@a.a', '2022-06-21 12:13:50', '1234');
