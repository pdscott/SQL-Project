
import unittest
import mysql.connector as mariadb

from unittest_base import SQLUnitTestBase
from Project.apps import Apps


class TestApps(SQLUnitTestBase):

    @staticmethod
    def _connect_to_test_db():
        con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='nfschnoo', password='001027748',
                              database='nfschnoo')
        return con

    def test_add_zip(self):
        apps = Apps(self._con, True)
        df = apps.add_zip({'zip': '27511', 'city': 'Cary', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Cary', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        apps.cursor.close()

    def test_update_zip(self):
        apps = Apps(self._con, True)
        # Add zip
        df = apps.add_zip({'zip': '27511', 'city': 'Raleigh', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Raleigh', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        # Update zip
        df = apps.update_zip({'city': 'Cary'}, {'zip': '27511'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Cary', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        apps.cursor.close()

    def test_delete_zip(self):
        apps = Apps(self._con, True)
        df = apps.add_zip({'zip': '27511', 'city': 'Cary', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        df = apps.delete_zip({'zip': '27511'})
        self.assertEqual(0, len(df.index))
        df = apps._execute_select_query('*', 'ZipToCityState')
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_report_occupancy_by_hotel(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_hotel('2017-01-16')
        self.assertEqual(8, len(df.index))
        self.assertEqual('Wolf Inn Miami Panthers', df['Hotel Name'].ix[5])
        self.assertEqual(1, df['Rooms Occupied'].ix[5])
        self.assertEqual(1, df['Total Rooms'].ix[5])
        self.assertEqual(100.0, df['% Occupancy'].ix[5])
        self._con.commit()
        apps.cursor.close()



if __name__ == '__main__':
    unittest.main()