create table installation(
  id integer primary key,
  nom varchar(50) unique,
  arrondissement varchar(50),
  _type varchar(10),
  informations text
);
