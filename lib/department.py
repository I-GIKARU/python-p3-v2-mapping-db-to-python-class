from __init__ import CURSOR, CONN


class Department:

    all = {}  # Dictionary to cache Department instances by id

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location
        if id:
            Department.all[id] = self

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Department instances."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Department instances."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row or update an existing one in the departments table."""
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
            Department.all[self.id] = self
        else:
            self.update()
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Initialize a new Department instance and save it to the database."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance."""
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        if self.id in Department.all:
            del Department.all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance from a database row."""
        id, name, location = row
        if id in cls.all:
            return cls.all[id]
        else:
            return cls(name, location, id)

    @classmethod
    def get_all(cls):
        """Return a list of Department instances for every row in the database."""
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Department instance by ID or None if not found."""
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Department instance by name or None if not found."""
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
