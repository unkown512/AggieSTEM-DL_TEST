drop table if exists action_record;

drop table if exists dataset_access;

drop table if exists dataset;

drop table if exists profile;

drop table if exists question;

drop table if exists request_data;

drop table if exists security;

drop table if exists user;


create table dataset
(
    id          int auto_increment
        primary key,
    name        text                               not null,
    description text                               null,
    upload_time datetime default CURRENT_TIMESTAMP not null,
    update_time datetime                           null,
    filepath    varchar(50)                        null
);

create table profile
(
    external_link varchar(250) null comment 'Link to website, cv, or research papers',
    ref_name      varchar(25)  null comment 'external_link display name',
    user_id       bigint       not null comment 'link to user table not unique',
    recno         bigint auto_increment comment 'Unique record number (row)'
        primary key
)
    engine = MyISAM;

create table question
(
    question1 varchar(25) not null,
    question2 varchar(25) not null,
    question3 varchar(25) not null,
    recno     bigint auto_increment comment 'Unique record number (row)'
        primary key
)
    engine = MyISAM;

create table request_data
(
    first_name          varchar(30)                          not null,
    last_name           varchar(30)                          not null,
    org_name            varchar(50)                          not null,
    status              varchar(8)                           not null,
    phone               varchar(12)                          not null,
    email_address       varchar(50)                          not null,
    address             varchar(100)                         not null,
    data_elements       varchar(100)                         not null,
    research_topics     text                                 not null,
    authors             text                                 not null,
    data_needed         text                                 not null,
    data_how            text                                 not null,
    data_details1_name  varchar(30)                          not null,
    data_details1_email varchar(50)                          not null,
    data_details1_inst  varchar(50)                          not null,
    data_details1_phone varchar(12)                          not null,
    data_details2_name  varchar(30)                          not null,
    data_details2_email varchar(50)                          not null,
    data_details2_inst  varchar(50)                          not null,
    data_details2_phone varchar(12)                          not null,
    data_storage        text                                 not null,
    start_date          varchar(13)                          not null,
    end_date            varchar(13)                          null,
    needed_date         varchar(13)                          null,
    destroyed_date      varchar(13)                          null,
    date_created        timestamp  default CURRENT_TIMESTAMP not null,
    isactive            varchar(1) default '0'               not null,
    user_id             bigint                               not null comment 'link to user table not unique',
    pdf_filename        varchar(30)                          not null,
    approved            varchar(1) default '0'               not null,
    recno               bigint auto_increment comment 'Unique record number (row)'
        primary key,
    download_link       varchar(100)                         null
)
    engine = MyISAM;

create table security
(
    password       varchar(350)           not null comment 'pw',
    question1      varchar(25)            not null comment 'q1 answer',
    question2      varchar(25)            not null comment 'q2 answer',
    question3      varchar(25)            not null comment 'q3 answer',
    request_new_pw varchar(1) default '0' not null comment 'flag to change password',
    user_id        bigint                 not null comment 'FK to user table',
    access_level   smallint   default 0   not null,
    code           varchar(30)            not null,
    recno          bigint auto_increment comment 'Unique record number (row)'
        primary key,
    constraint user_id
        unique (user_id)
)
    engine = MyISAM;

create table user
(
    username          varchar(20)                          not null comment 'First Initial + Last Name',
    position          varchar(3)                           not null comment 'Researcher (R), Senior Doc (S), Director (D)',
    email             varchar(321)                         not null comment 'Unique email address',
    phone_number      varchar(11)                          not null comment 'Contact Number',
    privacy_agreement varchar(1)                           not null comment 'Cache and privacy info.',
    contact_agreement varchar(1)                           not null comment 'text messages and email notifications',
    last_login        timestamp  default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment 'last login UTC time',
    deleted           varchar(1) default '0'               not null,
    is_logged_in      varchar(1) default '0'               not null,
    recno             bigint auto_increment comment 'Unique record number (row)'
        primary key,
    constraint email
        unique (email),
    constraint phone_number
        unique (phone_number)
);

create table action_record
(
    record_id int auto_increment
        primary key,
    user_id   bigint                              null,
    action    varchar(20)                         not null,
    parameter varchar(50)                         null,
    time      timestamp default CURRENT_TIMESTAMP not null,
    constraint action_record_user_recno_fk
        foreign key (user_id) references user (recno)
);

create table dataset_access
(
    id         int auto_increment
        primary key,
    user_id    bigint not null,
    dataset_id int    null,
    status     text   not null,
    constraint dataset_access_ibfk_1
        foreign key (user_id) references user (recno),
    constraint dataset_access_ibfk_2
        foreign key (dataset_id) references dataset (id)
);

create index dataset_id
    on dataset_access (dataset_id);

create index user_id
    on dataset_access (user_id);


