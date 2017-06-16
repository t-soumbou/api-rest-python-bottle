import unittest
import persistence.car_persistence as commons_car_service
from entities.car import Car

class PersistenceTest(unittest.TestCase):

    def setUp(self):
        """Initialisation des tests."""

    def testPersistenceService(self):
        print("test car_service ")
        car_service = commons_car_service.CarPersistence(Car)
        #test la methode count_all
        self.assertTrue(commons_car_service.count_all() == 0)

        car_entity = Car(100, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", None)

        #test la methode insert

    def test_find_all(self):
        """test la methode find_all """

    def test_find(self, record):
        """test la methode find"""

    def test_insert(self, record):
        """test la methode insert"""

    def test_create(self, record):
        """test la methode create"""

    def test_update(self, record):
        """test la methode update"""

    def test_save(self, record):
        """test la methode save"""

    def test_delete_by_id(self, _id):
        """test la methode delete_by_id"""

    def test_delete(self, record):
        """test la methode delete"""

    def test_exists_by_id(self, _id):
        """test la methode exists_by_id"""

    def test_exists(self, record):
        """test la methode exists"""

    def test_count_all(self):
        """test la methode count_all"""

