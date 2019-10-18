from sqlalchemy import create_engine
import webbrowser

CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    drivername="postgres",
    user="lesko",
    passwd="ma19ne99",
    host="localhost",
    port="5432",
    db_name="househunt",
)


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """

    return create_engine(CONNECTION_STRING)


if __name__ == "__main__":
    engine = db_connect()
    query = """
    SELECT DISTINCT ON (t.price, t.land_area, t.house_area)
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
         lower(t.region) similar to '%%osred%%|%%lj-ok%%'
         AND t.seller <> 'ZP'
         AND lower(t.settlement) not similar to '%%ig%%|%%litija%%'
         AND lower(t.administrative_unit) not like '%%litija%%'
         AND t.price between 90000 and 150000
         AND (t.land_area/t.house_area) >= 6
         AND t.land_area > 600
         AND t.house_area > 80;
         --AND lower(t.description) like '%%gozd%%'
         -- AND t.url LIKE '%%bolha%%'
    --ORDER BY l_vs_h DESC;
    """
    with engine.connect() as con:
        rs = con.execute(query)

    for i, row in enumerate(rs):
        print(row)
        if i < 7:
            webbrowser.open(f"{row[0]}")
        else:
            print("Not opening...")
