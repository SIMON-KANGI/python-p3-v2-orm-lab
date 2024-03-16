from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )
        
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self,year):
        if type(year) is int:
            self._year=year
        else:
            raise ValueError("year must be an integer")
        
    @property
    def summary(self):
        return self._summary
    
    @summary.setter
    def summary(self,summary):
        if len(summary)>0:
            self._summary=summary
        else:
            raise ValueError("summary must be there")
    
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql_query="""insert into reviews(year, summary, employee_id) values(?,?,?)"""
        CURSOR.execute(sql_query,(self.year,self.summary,self.employee_id))
        CONN.commit()
        self.id= CURSOR.lastrowid
        type(self).all[self.id] = self
    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review=cls(year,summary,employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        review= cls.all.get(row[0])
        if review:
            review.year=row[1]
            review.summary=row[2]
            review.employee_id=row[3]
        else:
            review=cls(row[1],row[2],row[3])
            review.id=row[0]
            cls.all[review.id]=review
        return review
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        sql ="""
            SELECT * from reviews
            where id=?
        """
        row= CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql ="""
            UPDATE reviews
            SET year=?, summary=? ,employee_id=?
            WHERE id=?
        """
        CURSOR.execute(sql,(self.year,self.summary,self.employee_id, self.id))
        CONN.commit()
    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql ="""
            DELETE FROM reviews
            WHERE id=?
        """
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id=None
    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        sql="""
            SELECT * from reviews
            """
        rows=CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
        
        

