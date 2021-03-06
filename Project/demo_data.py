"""
demo_data.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the demo_data.py file:
This is independent Python program that must be executed completely apart from
the rest of the Project programs. This Python script loads the Demo Data given
by a teaching staff into the DBMS as a pre-demo data that must exist in the
tables prior the Project Demo.
The file contains the Demo Data that is used for generating the initial state
of the DBMS prior the project demo. The program does the following:
1) _drop_tables() function drops all of the existing tables to clean up DBMS of
any existing data. If any of the tables do not exist prior of dropping it, it
ignores the error and continues dropping the remaining tables.
2) _create_tables() function creates all tables used in this project in the
required order. All of the tables get created with accordance of the Project
Design stated in the Project Report 1 and Project Report 2.
3) load_demo_data() function does a clean up and creates all the tables by
calling internal private helper functions _drop_tables() and _create_tables().
It loads the Demo Data into the DBMS used as the initial state during the
project demo.

@version: 1.0
@todo: Demo
@since: March 24, 2018

@status: Complete
@requires: Connection to MariaDB server at the NCSU. If default database
           parameters are changed, ignore both options below (unless DBMS used
           is at the NCSU MySQL Server).
           Option 1: Establish connection through NCSU VPN.
                     Installation of Cisco AnyConnect VPN Software is required.
                     Installation instructions of Cisco AnyConnect can be
                     found here:
https://oit.ncsu.edu/campus-it/campus-data-network/network-security/vpn/

           Option 2: Pull or copy source code to the NCSU remote machine and
                     run it there:
scp * unity_id@remote.eos.ncsu.edu:/afs/unity.ncsu.edu/users/u/unity_id/CSC540
@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu
@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott
"""

import mysql.connector as maria_db


def _drop_tables(db):
    """
    Drops all tables in the proper order.

    This is private function of the script and not intended to be referenced
    by any of the Project programs. It is referenced only by load_demo_data()
    function.
    On an error (e.g., table does not exist), it continues dropping the
    remaining tables by ignoring the error. The ultimate result of this
    function is all previously stored data must be removed from DBMS.

    Parameters:
        :param db: The database connection

    Returns:
        :return: None
    """
    cursor = db.cursor()
    try:
        cursor.execute('DROP TABLE Serves')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Transactions')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Reservations')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Customers')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Staff')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Rooms')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE Hotels')
    except maria_db.Error:
        pass
    try:
        cursor.execute('DROP TABLE ZipToCityState')
    except maria_db.Error:
        pass
    db.commit()


def _create_tables(db):
    """
    Creates all tables used in this project in the required order.

    This is private function of the script and not intended to be referenced
    by any of the Project programs. It is referenced only by load_demo_data()
    function.
    All of the tables get created with accordance of the Project Design stated
    in the Project Report 1 and Project Report 2. The following CREATE queries
    are directly taken from the Project Report 2 without any modifications.

    Parameters:
        :param db: The database connection

    Returns:
        :return: None
    """
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE ZipToCityState (
            zip VARCHAR(10) PRIMARY KEY,
            city VARCHAR(32) NOT NULL,
            state VARCHAR(2) NOT NULL,
            CHECK(LENGTH(zip)>=5 AND LENGTH(city)>0 AND LENGTH(state)=2)
        );""")
    cursor.execute("""
        CREATE TABLE Hotels (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            street VARCHAR(64) NOT NULL,
            zip VARCHAR(10) NOT NULL,
            phone_number VARCHAR(32) NOT NULL, 
            CONSTRAINT fk_hotels_ziptocitystate_zip FOREIGN KEY (zip) 
                REFERENCES ZipToCityState(zip) ON UPDATE CASCADE 
                ON DELETE RESTRICT,
            CONSTRAINT uc_hotels UNIQUE (street, zip),
            CHECK(LENGTH(name)>0 AND LENGTH(street)>0 AND 
            LENGTH(phone_number)>0)	
        );""")
    cursor.execute("""
        CREATE TABLE Rooms (
            hotel_id INT,
            room_number SMALLINT UNSIGNED,
            category VARCHAR(64) NOT NULL,
            occupancy TINYINT UNSIGNED NOT NULL,
            rate DECIMAL(8,2) UNSIGNED NOT NULL,
            PRIMARY KEY (hotel_id, room_number),
            CONSTRAINT fk_rooms_hotels_id FOREIGN KEY (hotel_id) 
                REFERENCES Hotels(id) ON UPDATE CASCADE ON DELETE CASCADE,
            CHECK(LENGTH(category)>0 AND (occupancy BETWEEN 1 AND 9))
        );""")

    cursor.execute("""
        CREATE TABLE Staff (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            title VARCHAR(64) NOT NULL,
            date_of_birth DATE NOT NULL,
            department VARCHAR(64) NOT NULL,
            phone_number VARCHAR(32) NOT NULL,
            street VARCHAR(64) NOT NULL,
            zip VARCHAR(10) NOT NULL,
            works_for_hotel_id INT NOT NULL,
            assigned_hotel_id INT,
            assigned_room_number SMALLINT UNSIGNED,
            CONSTRAINT fk_staff_ziptocitystate_zip FOREIGN KEY (zip) 
                REFERENCES ZipToCityState(zip) ON UPDATE CASCADE 
                ON DELETE RESTRICT,
            CONSTRAINT fk_staff_hotels_id FOREIGN KEY (works_for_hotel_id) 
                REFERENCES Hotels(id) ON UPDATE CASCADE ON DELETE CASCADE,
            CONSTRAINT fk_staff_rooms_hotel_id_room_number 
                FOREIGN KEY (assigned_hotel_id, assigned_room_number) 
                REFERENCES Rooms(hotel_id,room_number) ON UPDATE CASCADE 
                ON DELETE SET NULL,
            CHECK(LENGTH(name)>0 AND LENGTH(title)>0 AND LENGTH(department)>0 
                AND LENGTH(phone_number)>0 AND LENGTH(street)>0)
        );""")

    cursor.execute("""
        CREATE TABLE Customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(32) NOT NULL,
            email VARCHAR(64) NOT NULL,
            street VARCHAR(64) NOT NULL,
            zip VARCHAR(10) NOT NULL,
            ssn VARCHAR(11) UNIQUE NOT NULL,
            account_number VARCHAR(128) UNIQUE,
            is_hotel_card BOOLEAN,
            CONSTRAINT fk_customers_ziptocitystate_zip FOREIGN KEY (zip) 
                REFERENCES ZipToCityState(zip) ON UPDATE CASCADE 
                ON DELETE RESTRICT,
            CHECK(LENGTH(name)>0 AND LENGTH(phone_number)>0 AND 
                LENGTH(email)>3 AND LENGTH(street)>0 AND LENGTH(ssn)=11 AND 
                LENGTH(account_number)>0 AND email LIKE '%@%')
        );""")

    cursor.execute("""
        CREATE TABLE Reservations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            number_of_guests TINYINT UNSIGNED NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            check_in_time DATETIME,
            check_out_time DATETIME,
            hotel_id INT NOT NULL,
            room_number SMALLINT UNSIGNED NOT NULL,
            customer_id INT NOT NULL,
            CONSTRAINT fk_reservations_rooms_hotel_id_room_number FOREIGN KEY 
                (hotel_id, room_number) REFERENCES Rooms(hotel_id, room_number) 
                ON UPDATE CASCADE ON DELETE RESTRICT,
            CONSTRAINT fk_reservations_customers_id FOREIGN KEY (customer_id) 
                REFERENCES Customers(id) ON UPDATE CASCADE ON DELETE RESTRICT,
            CHECK((number_of_guests BETWEEN 1 AND 9) AND 
                start_date < end_date AND 
                check_in_time >= CAST(start_date AS DATETIME) AND 
                check_out_time >= CAST(end_date AS DATETIME))
        );""")

    cursor.execute("""
        CREATE TABLE Transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(8,2) UNSIGNED NOT NULL,
            type VARCHAR(128) NOT NULL,
            date DATETIME NOT NULL,
            reservation_id INT NOT NULL,
            CONSTRAINT fk_transactions_reservation_id 
            FOREIGN KEY (reservation_id) REFERENCES Reservations(id) 
                ON UPDATE CASCADE ON DELETE CASCADE,
            CHECK(LENGTH(type)>0)
        );""")

    cursor.execute("""
        CREATE TABLE Serves (
            staff_id INT NOT NULL,
            reservation_id INT NOT NULL,
            CONSTRAINT fk_serves_staff_id FOREIGN KEY (staff_id) 
                REFERENCES Staff(id) ON UPDATE CASCADE ON DELETE CASCADE,
            CONSTRAINT fk_serves_reservation_id FOREIGN KEY (reservation_id) 
                REFERENCES Reservations(id) ON UPDATE CASCADE ON DELETE CASCADE,
            CONSTRAINT uc_serves UNIQUE (staff_id, reservation_id)
        );""")
    db.commit()


def load_demo_data(db):
    """
    Loads the Demo Data into the DBMS used as the initial state during the
    project demo.

    This function does the following:
    1) Drops all project tables by calling internal private helper function
    _drop_tables()
    2) Creates the tables by calling internal private helper function
    _create_tables()
    3) Loads the Demo Data given by a teaching staff as a pre-demo data that
    must exist in the tables prior the Project Demo.

    Parameters:
        :param db: The database connection

    Returns:
        :return: None
    """

    _drop_tables(db)
    _create_tables(db)

    cursor = db.cursor()
    print "Loading Demo Data"
    # ZipToCityState
    zip_data = [
        ['27xxx', 'Raleigh', 'NC'],
        ['54xxx', 'Rochester', 'NY'],
        ['28xxx', 'Greensboro', 'NC'],  # Zip: 27
        ['32xxx', 'Raleigh', 'NC'],
        ['78xxx', 'Rochester', 'NY'],
        ['14xxx', 'Dallas', 'TX'],
    ]

    hotel_data = [
        [1, 'Hotel A', '21 ABC St', '27xxx', '919'],
        [2, 'Hotel B', '25 XYZ St', '54xxx', '718'],
        [3, 'Hotel C', '29 PQR St', '28xxx', '984'],  # Zip: 27
        [4, 'Hotel D', '28 GHW St', '32xxx', '920'],
    ]

    room_data = [
        [1, 1, 'Economy', 1, 100],
        [1, 2, 'Deluxe', 2, 200],
        [2, 3, 'Economy', 1, 100],
        [3, 2, 'Executive', 3, 1000],  # Available: no
        [4, 1, 'Presidential', 4, 5000],
        [1, 5, 'Deluxe', 2, 200],
    ]

    customer_data = [
        [1001, 'David', '1980-01-30', '123', 'david@gmail.com', '980 TRT St',
         '27xxx', '593-9846-xx', '1052', False],  # Zip: None
        [1002, 'Sarah', '1971-01-30', '456', 'sarah@gmail.com', '7720 MHT St',
         '28xxx', '777-8352-xx', '3020', True],  # Zip: None
        [1003, 'Joseph', '1987-01-30', '789', 'joseph@gmail.com', '231 DRY St',
         '78xxx', '858-9430-xx', '2497', False],
        [1004, 'Lucy', '1985-01-30', '213', 'lucy@gmail.com', '24 BST Dr',
         '14xxx', '440-9328-xx', None, None],  # Cash
    ]

    staff_data = [
        [100, 'Mary', '1978-04-01', 'Management', 'Manager', '654',
         '90 ABC St', '27xxx', 1],  # Age: 40
        [101, 'John', '1973-02-14', 'Management', 'Manager', '564',
         '798 XYZ St', '54xxx', 2],  # Age: 45
        [102, 'Carol', '1963-01-23', 'Management', 'Manager', '546',
         '351 MH St', '28xxx', 3],  # Age: 55, Zip: 27
        [103, 'Emma', '1963-04-02', 'Management', 'Front Desk Staff', '546',
         '49 ABC St', '27xxx', 1],  # Age: 55
        [104, 'Ava', '1963-02-03', 'Catering', 'Catering Staff', '777',
         '425 RG St', '27xxx', 1],  # Age: 55
        [105, 'Peter', '1966-01-01', 'Management', 'Manager', '724',
         '475 RG St', '27xxx', 4],
        [106, 'Olivia', '1990-09-13', 'Management', 'Front Desk Staff', '799',
         '325 PD St', '27xxx', 4],  # Age: 27
    ]

    reservation_data = [
        [1, 1, '2017-05-10', '2017-05-13',
         '2017-05-10 15:17:00', '2017-05-13 10:22:00', 1, 1, 1001],
        [2, 2, '2017-05-10', '2017-05-13',
         '2017-05-10 16:11:00', '2017-05-13 09:27:00', 1, 2, 1002],
        [3, 1, '2016-05-10', '2016-05-14',
         '2016-05-10 15:45:00', '2016-05-14 11:10:00', 2, 3, 1003],
        [4, 2, '2018-05-10', '2018-05-12',
         '2018-05-10 14:30:00', '2018-05-12 10:00:00', 3, 2, 1004],
    ]

    transaction_data = [
        [16, 'Dry Cleaning', '2017-05-12 16:54:14', 1],
        [15, 'Gym', '2017-05-10 19:05:38', 1],
        [15, 'Gym', '2017-05-11 08:43:45', 2],
        [10, 'Room Service', '2016-05-13 21:36:54', 3],
        [5, 'Phone Bills', '2018-05-11 14:32:11', 4],
    ]

    for row in zip_data:
        cursor.execute('INSERT INTO ZipToCityState(zip, city, state)'
                       'VALUES(%s, %s, %s)', row)

    for row in hotel_data:
        cursor.execute('INSERT INTO Hotels(id, name, street, zip, phone_number)'
                       'VALUES(%s, %s, %s, %s, %s)', row)

    for row in room_data:
        cursor.execute("INSERT INTO "
                       "Rooms(hotel_id, room_number, category, occupancy, rate)"
                       "VALUES(%s, %s, %s, %s, %s)", row)

    for row in staff_data:
        cursor.execute("INSERT INTO "
                       "Staff(id, name, date_of_birth, department, "
                       "title, phone_number, street, zip, works_for_hotel_id)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       row)

    for row in customer_data:
        cursor.execute("INSERT INTO "
                       "Customers(id, name, date_of_birth, phone_number,"
                       "email, street, zip, ssn, "
                       "account_number, is_hotel_card)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       row)

    for row in reservation_data:
        cursor.execute("INSERT INTO "
                       "Reservations(id, number_of_guests, "
                       "start_date, end_date,"
                       "check_in_time, check_out_time, "
                       "hotel_id, room_number, customer_id)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

    for row in transaction_data:
        cursor.execute("INSERT INTO "
                       "Transactions(amount, type, date, reservation_id)"
                       "VALUES(%s, %s, %s, %s)", row)

    cursor.close()
    db.commit()


if __name__ == '__main__':
    con = maria_db.connect(host='classdb2.csc.ncsu.edu', user='ngtitov',
                           password='001029047', database='ngtitov')
    load_demo_data(con)
