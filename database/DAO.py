from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAeroporti(num):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.*, count(distinct f.AIRLINE_ID) as NumAirlines
                    from extflightdelays.airports a, extflightdelays.flights f 
                    where f.ORIGIN_AIRPORT_ID = a.ID or f.DESTINATION_AIRPORT_ID = a.ID
                    group by a.ID 
                    having NumAirlines >= %s 
                    order by a.AIRPORT asc """

        cursor.execute(query, (num,))

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(a1, a2):
        conn = DBConnect.get_connection()

        result = None

        cursor = conn.cursor(dictionary=True)
        query = """ select count(*) as tot
                    from extflightdelays.flights f
                    where (f.ORIGIN_AIRPORT_ID = %s and f.DESTINATION_AIRPORT_ID = %s) 
                    or (f.ORIGIN_AIRPORT_ID = %s and f.DESTINATION_AIRPORT_ID = %s) """

        cursor.execute(query, (a1, a2, a2, a1))

        for row in cursor:
            result = row["tot"]

        cursor.close()
        conn.close()
        return result

