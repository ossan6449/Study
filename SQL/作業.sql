create table ignore_case_products (
    item_cd varchar(100)
    ,name varchar(255)
);


insert into ignore_case_products(item_cd, name)
values
('item1', 'りんご')
,('item2', 'リンゴ')
,('item3', 'ﾘﾝｺﾞ')
,('item4', 'APPLE')
,('item5', 'Apple')
,('item6', 'apple')
,('item7', 'ＡＰＰＬＥ')
,('item8', 'ａｐｐｌｅ')
,('item9', 'Ａｐｐｌｅ')
;

-- カナ
select * from ignore_case_products where name like 'リンゴ';
-- 半角カナ
select * from ignore_case_products where name like 'ﾘﾝｺﾞ';
-- 英字
select * from ignore_case_products where name like 'apple';
-- 大文字小文字を区別しない(ilike)
select * from ignore_case_products where name ilike 'apple';
-- 大文字小文字を区別しない(ilike)
select * from ignore_case_products where name ilike 'ａｐｐｌｅ';



select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('りんご');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('リンゴ');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ﾘﾝｺﾞ');

-- likeも試す
select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('リン') || '%';


select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('Apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('APPLE');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ａｐｐｌｅ');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('Ａｐｐｌｅ');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ＡＰＰＬＥ');


insert into ignore_case_products(item_cd, name)
select
  format('item%s', i)
  ,format('テスト商品%s', i)
from
  generate_series(10, 100000) as i
;

SELECT * FROM ignore_case_products

explain analyze select * from ignore_case_products where name = 'リンゴ';
17.425ms

explain analyze select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('リンゴ');
3572.687ms


explain analyze select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('リン') || '%';
3705.607ms

truncate table ignore_case_products;
