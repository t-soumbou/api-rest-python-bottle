import sqlite3 as lite

class GenericDao(object):
    def __init__(self, entity_type):
        self._entity_type = entity_type
        self._entity = entity_type.__name__.lower()

    def do_select_all(self, query):
        """
        Loads all the occurrences existing in the database
        :param query:
        :return: all the occurrences existing in the database
        """
        conn, cur = None, None
        req, list_entities = query, []
        try:
            conn, cur = get_connection()
            cur.execute(req)
            row = cur.fetchall()
            list_entities = [self._entity_type(*row) for row in row if row is not None]
        except lite.Error as e:
            print(e)
        finally:
            close_connection(conn)
        return list_entities

    def do_select(self, req, params):
        """
        Loads the given bean from the database using its primary key
        :param req:
        :param params:
        :return: loaded entity
        """
        entity_selected, conn, cur = None, None, None
        try:
            conn, cur = get_connection()
            cur.execute(req, params)
            row_selected = cur.fetchone()
            if row_selected is not None:
                entity_selected = self._entity_type(*row_selected)
        except lite.Error as e:
            print(e)
        finally:
            close_connection(conn)
        return entity_selected


def do_delete(req, params):
    """
    Deletes the given entity in the database (SQL DELETE)
    :param req:
    :param params:
    :return: return code (i.e. the row count affected by the DELETE operation : 0 or 1 )
    """
    row_deleted, conn, cur = 0, None, None
    try:
        conn, cur = get_connection()
        cur.execute(req, params)
        conn.commit()
        row_deleted = conn.total_changes
    except lite.Error as e:
        print(e)
        conn.rollback()
    finally:
        close_connection(conn)
    return row_deleted


def do_insert_incr(req, params):
    """
    Inserts the given entity in the database (SQL INSERT) with an auto-incremented columns
    :param req:
    :param params:
    :return: _id of insered entity
    """
    res, entity_id, conn, cur = False, -1, None, None
    try:
        conn, cur = get_connection()
        cur.execute(req, params)
        conn.commit()
        entity_id = cur.lastrowid
        res= True
    except lite.Error as e:
        print(e)
        conn.rollback()
    finally:
        close_connection(conn)
    return entity_id, res


def do_insert(req, params):
    """
    Inserts the given bean in the database
    :param req:
    :param params:
    :return:
    """
    result, conn, cur = False, None, None
    try:
        conn, cur = get_connection()
        cur.execute(req, params)
        conn.commit()
        result= True
    except lite.Error as e:
        print(e)
        conn.rollback()
    finally:
        close_connection(conn)
    return result


def do_exists(req, params):
    """
    Checks if the given bean exists in the database
    :param req:
    :param params:
    :return: true if the given entity exist
    """
    conn, cur, is_exist = False, None, None
    try:
        conn, cur = get_connection()
        cur.execute(req, params)
        is_exist = cur.fetchall().__len__() > 0
    except lite.Error as e:
        print(e)
    finally:
        close_connection(conn)
    return is_exist


def do_count_all(req):
    """
    Counts all the occurrences in the table
    :param req:
     :return: number of occurence in the table
     """
    conn, cur, entity_number = None, None, 0
    try:
        conn, cur = get_connection()
        cur.execute(req)
        entity_number = cur.fetchall().__len__()
    except lite.Error as e:
        print(e)
    finally:
        close_connection(conn)
    return entity_number


def do_update(req, params):
    """
    Updates the given entity in the database (SQL UPDATE)
    :param req:
    :param params:
    :return: return code (i.e. the row count affected by the UPDATE operation : 0 or 1 )
    """
    row_updated, conn, cur = 0, None, None
    try:
        conn, cur = get_connection()
        cur.execute(req, params)
        conn.commit()
        row_updated = conn.total_changes
    except lite.Error as e:
        print(e)
        conn.rollback()
    finally:
        close_connection(conn)
    return row_updated


def get_connection():
    """
    Get a database connection
    :return: database object connection
    """
    try:
        conn = lite.connect("./sqlite.db")
        cur = conn.cursor()
        return conn, cur
    except lite.Error as e:
        print(e)
    return None, None


def close_connection(conn):
    """ Commit changes and close connection to the database """
    if conn:
        try:
            conn.close()
        except lite.Error as e:
            print(e)