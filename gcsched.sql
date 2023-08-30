create database gcsched;

\u gcsched

create table reservation (id int not null auto_increment, resdate date, resTime int, duration int, firstname varchar(31), lastname varchar(31), phone varchar(16), email varchar(64), primary key (id));
create table block (id int not null auto_increment, blkdate date, duration int, starttime int, numblocks int, primary key (id));

insert into block (blkdate, duration, starttime, numblocks) values ("2023-09-09", blkDuration, 600, 24);
insert into block (blkdate, duration, starttime, numblocks) values ("2023-09-10", blkDuration, 840, 24);

quit
