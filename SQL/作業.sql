create table ignore_case_products (
    item_cd varchar(100)
    ,name varchar(255)
);


insert into ignore_case_products(item_cd, name)
values
('item1', '‚è‚ñ‚²')
,('item2', 'ƒŠƒ“ƒS')
,('item3', 'ØİºŞ')
,('item4', 'APPLE')
,('item5', 'Apple')
,('item6', 'apple')
,('item7', '‚`‚o‚o‚k‚d')
,('item8', '‚‚‚‚Œ‚…')
,('item9', '‚`‚‚‚Œ‚…')
;

-- ƒJƒi
select * from ignore_case_products where name like 'ƒŠƒ“ƒS';
-- ”¼ŠpƒJƒi
select * from ignore_case_products where name like 'ØİºŞ';
-- ‰pš
select * from ignore_case_products where name like 'apple';
-- ‘å•¶š¬•¶š‚ğ‹æ•Ê‚µ‚È‚¢(ilike)
select * from ignore_case_products where name ilike 'apple';
-- ‘å•¶š¬•¶š‚ğ‹æ•Ê‚µ‚È‚¢(ilike)
select * from ignore_case_products where name ilike '‚‚‚‚Œ‚…';



select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('‚è‚ñ‚²');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ƒŠƒ“ƒS');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ØİºŞ');

-- like‚à‚·
select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('ƒŠƒ“') || '%';


select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('Apple');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('APPLE');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('‚‚‚‚Œ‚…');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('‚`‚‚‚Œ‚…');
select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('‚`‚o‚o‚k‚d');


insert into ignore_case_products(item_cd, name)
select
  format('item%s', i)
  ,format('ƒeƒXƒg¤•i%s', i)
from
  generate_series(10, 100000) as i
;

SELECT * FROM ignore_case_products

explain analyze select * from ignore_case_products where name = 'ƒŠƒ“ƒS';
17.425ms

explain analyze select * from ignore_case_products where sf_translate_case(name) = sf_translate_case('ƒŠƒ“ƒS');
3572.687ms


explain analyze select * from ignore_case_products where sf_translate_case(name) like '%' || sf_translate_case('ƒŠƒ“') || '%';
3705.607ms

truncate table ignore_case_products;
