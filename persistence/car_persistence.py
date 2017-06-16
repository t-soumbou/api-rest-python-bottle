import commons.generic_dao as dao_commons
from entities.car import Car


class CarPersistence:
    def __init__(self, car):
        self.dao = dao_commons.GenericDao(car)

    def find_by_id(self, _id):
        """
        Tries to find an entity using its Id / Primary Key
        :param _id:
        :return: entity
        """
        entity = new_instance_with_primary_key(_id)
        req, params = build_select_req(entity)
        return self.dao.do_select(req, params)

    def find_all(self):
        """
        Finds all entities.
        :return:  all entities
        """
        return self.dao.do_select_all(build_select_all())

    def find(self, entity):
        """
        Tries to find the given entity
        :param entity:
        :param self:
        :return: entity
        """
        req, params = build_select_req(entity)
        return self.dao.do_select(req, params)


def insert(entity):
    """
    Insert the given entity in the database
    :param entity: to be inserted (supposed to have a valid Id/PK )
    :return: entity
    """
    if entity.car_id is None:
        req, params = build_insert_req(entity)
        _id, res = dao_commons.do_insert_incr(req, params)
        print(res)
        if res:
            entity.car_id = _id
            return entity
        else:
            return None
    else:
        req, params = build_insert_req(entity)
        res = dao_commons.do_insert(req, params)
        if res is True:
            return entity
        return None


def create(entity):
    """
    Creates the given entity in the database
    :param entity: to be created (supposed to have a valid Id/PK )
    :return: entity
    """
    return insert(entity)


def update(entity):
    """
    Updates the given entity in the database
    :param entity: to be updated (supposed to have a valid Id/PK )
    :return: true if the entity has been updated, false if not found and not updated
    """
    req, params = buil_update_req(entity)
    result = dao_commons.do_update(req, params)
    return result > 0


def save(entity):
    """
    Saves the given entity in the database (create or update)
    :param entity: to be saved (supposed to have a valid Id/PK )
    :return: entity
    """
    if exists(entity):
        return update(entity)
    else:
        return insert(entity)


def delete_by_id(_id):
    """
    Deletes an entity using its Id / Primary Key
    :param _id:
    :return: true if the entity has been deleted, false if not found and not deleted
    """
    entity = new_instance_with_primary_key(_id)
    req, params = build_delete_req(entity)
    result = dao_commons.do_delete(req, params)
    return result > 0


def delete(entity):
    """
    Deletes an entity using the Id / Primary Key stored in the given object
    :param entity: to be deleted (supposed to have a valid Id/PK )
    :return: true if the entity has been deleted, false if not found and not deleted
    """
    req, params = build_delete_req(entity)
    result = dao_commons.do_delete(req, params)
    return result > 0


def exists_by_id(_id):
    """
    check if an entity exists with the given Id / Primary Key
    :param _id:
    :return: true if an entity exists with the given Id / Primary Key
    """
    entity = new_instance_with_primary_key(_id)
    req, params = build_select_req(entity)
    return dao_commons.do_exists(req, params)


def exists(entity):
    """
    check if the given entity exist
    :param entity:
    :return: true if the given entity exist
    """
    req, params = build_select_req(entity)
    return dao_commons.do_exists(req, params)


def count_all():
    """
    Counts all the entity present in the entity table
    :return: the number of rows in the entity table
    """
    req = build_select_all()
    return dao_commons.do_count_all(req)


def build_select_all():
    """
    Build the SQL SELECT REQUEST to be used to retrieve all the occurrences
    :return: the SQL SELECT REQUEST to be used to retrieve all the occurrences
    """
    return "select * from car"


def build_select_req(entity):
    """
    Build the SQL SELECT REQUEST to be used to retrieve the entity data from the database
    :param entity:
    :return: the SQL SELECT REQUEST to be used to retrieve the entity data from the database
    """
    ins_dict = vars(entity)
    params = [i for i in ins_dict.values() if i is not None]
    req = "select * from car where car_id = ?"
    return req, params


def build_insert_req(entity):
    """
    Build the SQL INSERT REQUEST to be used to insert the entity in the database
    :param entity:
    :return: the SQL INSERT REQUEST to be used to insert the entity in the database
    """
    ins_dict = vars(entity)
    params = [i for i in ins_dict.values()]
    req = "insert into car ( car_id, car_maker, car_model, car_year ) values ( ?, ?, ?,? )"
    return req, params


def buil_update_req(entity):
    """
    Build the SQL UPDATE REQUEST to be used to update the entity from the database
    :param entity:
    :return: the SQL UPDATE REQUEST to be used to update the entity from the database
    """
    ins_dict, i = vars(entity), ''
    params = [i for i in ins_dict.values()]
    params.append(params[0])
    req = "update car set car_id = ?, car_maker = ?, car_model = ?, car_year= ? where car_id = ?"
    return req, params


def build_delete_req(entity):
    """
    Build the SQL DELETE REQUEST to be used to delete the entity from the database
    :param entity:
    :return: the SQL DELETE REQUEST to be used to delete the entity from the database
    """
    ins_dict, i = vars(entity), ''
    params = [i for i in ins_dict.values() if i is not None]
    req = "delete from car where car_id = ?"
    return req, params


def new_instance_with_primary_key(_id):
    """
    build new entity with the given _id
    :param _id:
    :return: entity with the given _id
    """
    return Car(_id, None, None, None)
