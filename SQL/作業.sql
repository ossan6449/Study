create table ignore_case_products (
    item_cd varchar(100)
    ,name varchar(255)
);


insert into ignore_case_products(item_cd, name)
values
('item1', '���')
,('item2', '�����S')
,('item3', '�ݺ�')
,('item4', 'APPLE')
,('item5', 'Apple')
,('item6', 'apple')
,('item7', '�`�o�o�k�d')
,('item8', '����������')
,('item9', '�`��������')
;

-- �J�i
select * from ignore_case_products where name like '�����S';
-- ���p�J�i
select * from ignore_case_products where name like '�ݺ�';
-- �p��
select * from ignore_case_products where name like 'apple';
-- �啶������������ʂ��Ȃ�(ilike)
select * from ignore_case_products where name ilike 'apple';
-- �啶������������ʂ��Ȃ�(ilike)
select * from ignore_case_products where name ilike '����������';



select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('���');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('�����S');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('�ݺ�');

-- like������
select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('����') || '%';


select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('Apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('APPLE');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('����������');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('�`��������');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('�`�o�o�k�d');


insert into ignore_case_products(item_cd, name)
select
  format('item%s', i)
  ,format('�e�X�g���i%s', i)
from
  generate_series(10, 100000) as i
;

SELECT * FROM ignore_case_products

explain analyze select * from ignore_case_products where name = '�����S';
17.425ms

explain analyze select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('�����S');
3572.687ms


explain analyze select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('����') || '%';
3705.607ms

truncate table ignore_case_products;
