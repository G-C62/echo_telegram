create table channels(
id int (10) not null auto_increment,
channel_name varchar(255) not null unique,
primary key (id)
);
create table users(
id int(10) not null auto_increment,
user_id varchar(50) not null unique,
pw varchar(255) not null,
name varchar(20) not null,
rank int(1) check (rank in(1,2,3,4,5,6,7)),
status varchar(40) check (status in('place', 'meeting', 'away', 'outside')),
channel_id int(10),
seat_location varchar(10) unique,
primary key(id),
foreign key(channel_id) references channels(id)
);
create table events(
id int (10) not null auto_increment,
category varchar(40) check (category in('meeting', 'away', 'outside', 'notice')),
place varchar(50),
subject varchar(50),
start_time time,
created_time timestamp,
iscomplete boolean not null default false,
channel_id int(10) not null,
user_id int(10) not null,
attendants varchar(255),
primary key(id),
foreign key(channel_id) references channels(id),
foreign key(user_id) references users(id)
);