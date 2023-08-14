create database gcsched;

\u gcsched

create table reservation (id int not null auto_increment, resdate date, resTime int, duration int, name varchar(31), phone varchar(16), email varchar(64), primary key (id));
create table block (id int not null auto_increment, blkdate date, start int, end time, primary key (id));

quit
