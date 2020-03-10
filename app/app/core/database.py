import psycopg2

DB_CREDENTIALS = {'user': 'docker', 'password': 'docker', 'host': 'db', 'port': '5432', 'database': 'gis'}


def execute_query(query_select, query_parameters):
    # TODO: Check that the database is already populated
    records = []
    try:
        connection = psycopg2.connect(**DB_CREDENTIALS)
        cursor = connection.cursor()
        cursor.execute(query_select, query_parameters)
        records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return records


def get_postal_code_id_from_db(lat, lon):
    # TODO: make ST_Contains work!!!
    # TODO: Check the coordinates system
    # query = "SELECT id FROM postal_codes WHERE ST_Contains(the_geom::geometry, ST_SetSRID('POINT(-3.66 40.36)'::geometry, 4326))"
    query = "SELECT id " \
            "FROM postal_codes " \
            "WHERE ST_Distance(ST_SetSRID('POINT(%s %s)'::geometry, 4326), the_geom::geometry) = " \
            "     (SELECT min(ST_Distance(ST_SetSRID('POINT(%s %s)'::geometry, 4326), the_geom::geometry)) " \
            "      FROM postal_codes)"
    params = (lon, lat, lon, lat)
    postal_code_id = execute_query(query, params)
    try:
        return postal_code_id[0][0]
    except Exception as e:
        print("No postal code id could be retrieved")
        return None


def get_postal_code_from_db(postal_code_id):
    query = "SELECT code FROM postal_codes WHERE id = %s "
    params = (postal_code_id,)
    postal_code = execute_query(query, params)
    if len(postal_code) == 0:
        print("No postal code could be retrieved")
        return None
    return postal_code[0][0]


def get_turnover_by_month_gender_from_db(postal_code_id):
    query = "SELECT ps.p_month, ps.p_gender, ROUND(SUM(ps.amount)) " \
            "FROM paystats as ps " \
            "WHERE ps.postal_code_id = %s " \
            "GROUP BY ps.p_month, ps.p_gender " \
            "ORDER BY ps.p_month, ps.p_gender"
    params = (postal_code_id,)
    turnover = execute_query(query, params)
    if len(turnover) == 0:
        print("No data could be retrieved")
        return None
    return turnover


def get_turnover_by_age_gender_from_db(postal_code_id):
    query = "SELECT ps.p_age, ps.p_gender, ROUND(SUM(ps.amount)) " \
            "     , CASE WHEN ps.p_age='<=24' THEN '0' ELSE ps.p_age END AS age_order " \
            "FROM paystats as ps " \
            "WHERE ps.postal_code_id = %s " \
            "GROUP BY ps.p_age, ps.p_gender " \
            "ORDER BY age_order, ps.p_gender"
    params = (postal_code_id,)
    turnover = execute_query(query, params)
    if len(turnover) == 0:
        print("No data could be retrieved")
        return None
    return turnover


def get_total_turnover_from_db(postal_code_id):
    query = "SELECT ROUND(SUM(ps.amount)) " \
            "FROM paystats as ps " \
            "WHERE ps.postal_code_id = %s "
    params = (postal_code_id,)
    turnover = execute_query(query, params)
    if turnover is None:
        print("No data could be retrieved")
        return None
    print(turnover)
    return turnover[0][0]


def get_map_from_db(postal_code):
    query = "SELECT pc.code, ST_AsGeoJSON(the_geom) AS geometry, t.total_turnover " \
            "FROM postal_codes AS pc," \
            "    (SELECT  pc.code AS code, ROUND(SUM(ps.amount)) AS total_turnover" \
            "       FROM  postal_codes AS pc," \
            "             paystats AS ps" \
            "       WHERE ps.postal_code_id = pc.id" \
            "       GROUP BY pc.code) AS t " \
            "WHERE t.code = pc.code AND (pc.code::varchar LIKE %s)"
    params = (postal_code,)
    map = execute_query(query, params)
    if len(map) == 0:
        print("No data could be retrieved")
        return None
    return map