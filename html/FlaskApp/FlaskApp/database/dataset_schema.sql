drop table if exists dataset_access;

drop table if exists dataset;

ALTER TABLE user
    ENGINE = InnoDB;

CREATE TABLE dataset
(
    id          integer primary key auto_increment,
    name        text not null,
    description text,
    upload_time datetime,
    update_time datetime
);


create table dataset_access
(
    id         integer primary key auto_increment,
    user_id    bigint not null,
    foreign key (user_id) references user (recno),
    dataset_id integer,
    foreign key (dataset_id) references dataset (id),
    status     text   not null
);

# show engine innodb status;
# show table status where name = 'user';