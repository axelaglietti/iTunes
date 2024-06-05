from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(d):
        cnn = DBConnect.get_connection()
        cursor = cnn.cursor(dictionary=True)
        result = []
        query = """
                SELECT a.*, sum(t.Milliseconds) as totD
                FROM album a, track t 
                WHERE a.AlbumId = t.AlbumId
                GROUP BY a.AlbumId 
                HAVING totD > %s"""
        cursor.execute(query, (d,))
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        cnn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        cnn = DBConnect.get_connection()
        cursor = cnn.cursor(dictionary=True)
        result = []
        query = """
                SELECT distinctrow t.AlbumId AS a1, t2.AlbumId AS a2
                FROM playlisttrack p, track t, playlisttrack p2, track t2 
                WHERE p.PlaylistId = p2.PlaylistId AND p.TrackId = t.TrackId AND p2.TrackId = t2.TrackId #PER LA JOIN
                AND t.AlbumId < t2.AlbumId """
        cursor.execute(query)
        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))
        cursor.close()
        cnn.close()
        return result