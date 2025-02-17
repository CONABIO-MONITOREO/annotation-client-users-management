CREATE TABLE "user"(id serial, 
    username varchar(100) not null,
    id_user_external bigint,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    "role" varchar(20) not null
);

ALTER TABLE "user" ADD COLUMN "password" varchar(100) not null; 

INSERT INTO "user"(username, "role", "password") VALUES ('promero@conabio.gob.mx', 'ADMIN', md5('Qwerty123'));
INSERT INTO "user"(username, "role", "password") VALUES ('svizcaino@conabio.gob.mx', 'ADMIN', md5('Qwerty123'));
INSERT INTO "user"(username, "role", "password") VALUES ('mmunguia@conabio.gob.mx', 'ADMIN', md5('Qwerty123'));

INSERT INTO "user"(username, "role", "password") VALUES ('zs10011598@gmail.com', 'ENCARGADO', md5('Qwerty123'));

CREATE TABLE cummulus_relation(id serial, cummulus_name varchar(10), user_id BIGINT);