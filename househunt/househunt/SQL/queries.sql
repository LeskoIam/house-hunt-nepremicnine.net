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
     public.dev_househunt t
WHERE
     --lower(t.region) similar to '%osred%|%lj-ok%' AND
     --t.seller <> 'ZP' AND
     lower(t.settlement) not similar to '%ig%|%litija%'
     AND lower(t.administrative_unit) not like '%litija%'
     AND t.price between 90000 and 150000
     AND (t.land_area/t.house_area) between 6 and 30
     AND t.land_area > 600
     AND t.house_area > 80
     AND lower(t.description) like '%opti%'
     -- AND t.url LIKE '%bolha%'
ORDER BY l_vs_h DESC;

SELECT
    *
FROM (
    SELECT
        lower(t.settlement),
        count(t.settlement) as cnt,
        avg(t.price) as avg_price,
        avg(t.price/t.house_area)*avg(t.house_area) as avg_price_from_avg_m2,
        avg(t.house_area) as avg_house_area,
        avg(t.price/t.house_area) as avg_price_m2,
        avg(t.land_area/t.house_area) as avg_l_vs_h
    FROM
        public.dev_househunt t
    GROUP BY lower(t.settlement)
     ) t1
WHERE
    t1.cnt > 0
ORDER BY t1.cnt;

-- AIzaSyDzXBn2yGUUKSpf9pM1nXf3fIq2lj-EfEQ

SELECT DISTINCT ON (t.land_area, t.house_area, t.price) *
FROM
    public.dev_househunt t
WHERE
    lower(t.settlement) = 'ptuj'
ORDER BY
    t.price DESC;


SELECT DISTINCT ON (t.land_area, t.house_area, t.price) *
FROM dev_househunt t
WHERE
      t.price <> -1 AND
      t.land_area <> -1 AND
      t.house_area <> -1;

SELECT *
FROM dev_househunt t;