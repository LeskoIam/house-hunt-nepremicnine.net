SELECT
    t.url,
    t.administrative_unit,
    t.municipality,
    t.price,
    t.settlement,
    t.house_area,
    t.land_area,
    (t.land_area/t.house_area) as l_vs_h,
    t.description
FROM
     public.raw_househunt t
WHERE
     lower(t.region) similar to '%osred%|%lj-ok%'
     AND t.seller <> 'ZP'
     AND lower(t.settlement) not similar to '%ig%|%litija%'
     AND lower(t.administrative_unit) not like '%litija%'
     AND t.price between 90000 and 150000
     AND (t.land_area/t.house_area) between 6 and 20
     AND t.land_area > 600
     AND t.house_area > 80
     AND lower(t.description) like '%gozd%'
     -- AND t.url LIKE '%bolha%'
ORDER BY l_vs_h DESC;


SELECT
    distinct (t.land_area/t.house_area) as l_vs_h

    --distinct (t.land_area/t.house_area)
FROM
    public.raw_househunt t;


SELECT
    *
FROM
    public.raw_househunt t
WHERE
    t.seller = '3000 Celje';


SELECT DISTINCT ON (t.land_area, t.price) *
FROM raw_househunt t
WHERE
      t.price <> -1 AND
      t.land_area <> -1 AND
      t.house_area <> -1;

SELECT *
FROM raw_househunt t;