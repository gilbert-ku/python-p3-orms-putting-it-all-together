import sqlite3

# Connect to the SQLite database
CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

# Define a Dog class
class Dog:

    def __init__(self, name="joey", breed="cocker spaniel"):
        # Initialize a Dog instance with default values
        self.id = None  # Initialize id as None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        # Create the 'dogs' table if it does not exist
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(create_table_sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop the 'dogs' table if it exists
        drop_table_sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(drop_table_sql)
        CONN.commit()

    def save(self):
        # Insert a new record for the current dog instance into the 'dogs' table
        insert_sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(insert_sql, (self.name, self.breed))
        CONN.commit()
        
        # Update the dog instance with the last inserted row id
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        # Create a new dog instance and save it to the database
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # Create a new Dog instance from a database row
        dog = cls(row[1], row[2])  # Assuming the name is in column 1 and breed is in column 2
        dog.id = row[0]  # Set the ID from the row
        return dog

    @classmethod
    def get_all(cls):
        # Retrieve all records from the 'dogs' table and return a list of Dog instances
        select_all_sql = """
            SELECT * FROM dogs
        """
        CURSOR.execute(select_all_sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        # Find and return a Dog instance by its name
        select_by_name_sql = """
            SELECT * FROM dogs
            WHERE name = ?
        """
        CURSOR.execute(select_by_name_sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        # Find and return a Dog instance by its ID
        select_by_id_sql = """
            SELECT * FROM dogs
            WHERE id = ?
        """
        CURSOR.execute(select_by_id_sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        # Find and return a Dog instance by its name and breed
        select_by_name_and_breed_sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ?
        """
        CURSOR.execute(select_by_name_and_breed_sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        # Find a Dog instance by name and breed; if not found, create one
        existing_dog = cls.find_by_name_and_breed(name, breed)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        # Update the database record for the current dog instance
        update_sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(update_sql, (self.name, self.breed, self.id))
        CONN.commit()




