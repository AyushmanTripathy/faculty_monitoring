drop table otp_requests;
drop table student;
drop table faculty;

create table otp_requests (
  token varchar(256) not null,
  otp int not null
);

create table student (
  email varchar(256) not null,
  password_hash varchar(256) not null,
  key char(64) not null,
  name varchar(256) not null
);

create table faculty (
  email varchar(256) not null,
  password_hash varchar(256) not null,
  key char(64) not null,
  name varchar(256) not null,
  incampus int not null default 0
);
