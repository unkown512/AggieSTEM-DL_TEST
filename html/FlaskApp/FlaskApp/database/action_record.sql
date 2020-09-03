drop table action_record;

create table action_record
(
    record_id int auto_increment
        primary key,
    user_id bigint null,
    action varchar(20) not null,
    parameter varchar(50) null,
    time timestamp default current_timestamp not null,
    constraint action_record_user_recno_fk
        foreign key (user_id) references user (recno)
);

# for testing purpose

insert into action_record (user_id, action, parameter) VALUES (5, 'download', 'readme.md');