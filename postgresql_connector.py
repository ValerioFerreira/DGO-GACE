import os
import psycopg2

def upload_data():
    host = os.environ.get("PG_HOST", "10.193.0.20")
    port = os.environ.get("PG_PORT", "5432")
    user = os.environ.get("PG_USER", "ctic")
    password = os.environ.get("PG_PASSWORD", "@cticcbmpe#")
    dbname = os.environ.get("PG_DBNAME", "mapa_forca_api_development")

    db_conn_str = f"host={host} port={port} user={user} password={password} dbname={dbname}"

    conn = None

    try:
        conn = psycopg2.connect(db_conn_str)
        print("Conexão bem-sucedida!")

        query = """
        SELECT DISTINCT ON (lancamento.id) lancamento.id AS id,
        lancamento.date AS data,
        shift.name || ' (' || shift.start_time || ' às ' || shift.end_time || ')' AS turno,
        station.city AS local_atuacao,
        ome.acronym AS OME,
        ome.parent_ome_name AS diretoria,
        COUNT(DISTINCT militar.id) AS efetivo,
        COUNT(DISTINCT viatura.id) AS viaturas,
        'ordinário' AS regime_de_servico
        FROM launches lancamento
        LEFT JOIN launch_militaries militar ON lancamento.id = militar.launch_id
        LEFT JOIN service_shifts shift ON lancamento.service_shift_id = shift.id_scriptcase
        LEFT JOIN stations station ON lancamento.service_station_id = station.id_scriptcase
        LEFT JOIN omes ome ON station.ome_id_scriptcase = ome.id_scriptcase
        LEFT JOIN launch_vehicles viatura ON lancamento.id = viatura.launch_id
        WHERE lancamento.date = '2024-01-22'
        AND lancamento.discarded_at IS NULL
        AND militar.status = 1
        AND militar.discarded_at IS NULL
        GROUP BY lancamento.id, lancamento.date, shift.name, shift.start_time, shift.end_time, station.city, ome.acronym,
        ome.parent_ome_name;
        """

        cursor = conn.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

    finally:
        if conn is not None:
            conn.close()
            print("Conexão fechada.")

    return results