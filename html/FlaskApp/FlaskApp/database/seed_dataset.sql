# clear all rows, then seed dataset.

delete
from dataset_access;

delete
from dataset;

insert into dataset (name, description, upload_time, update_time, filepath)
values ('MNIST', 'handwritten digit images', '2020/03/22 10:03:01', '2020/03/22 10:03:01', 'static/txt/demo.txt');

insert into dataset (name, description, upload_time, update_time, filepath)
VALUES ('MS-COCO', 'object detection', '2020/03/01 17:10:15', '2020/03/01 17:10:15', 'static/csv/demo.csv');

insert into dataset (name, description, upload_time, update_time, filepath)
VALUES ('CIFAR-10', 'image classification dataset', '2020/02/01 15:21:03', '2020/03/01 17:21:04', 'static/pdf/demo.pdf');

insert into dataset (name, description, upload_time, update_time, filepath)
VALUES ('IMDB Reviews', 'IMDB movie reviews dataset', '2019/01/03 17:30:05', '2020/03/05 19:20:33', 'static/img/demo1.jpg');


insert into dataset_access (user_id, dataset_id, status)
select user.recno, dataset.id, 'granted'
from user,
     dataset;
