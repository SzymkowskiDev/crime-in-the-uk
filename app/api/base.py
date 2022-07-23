from sqlalchemy import (create_engine,MetaData,Table, Column, Integer, Numeric, String,
                ForeignKey, DateTime, PrimaryKeyConstraint,
                UniqueConstraint, CheckConstraint, Boolean, Constraint, select)

from datetime import datetime

#postgresql://username:password@host:port/dbname[?paramspec]

class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()
    events = Table('events', metadata,
        Column('event_id', Integer(), primary_key=True),
        Column('name',String(30),nullable=False),
        Column('category',String(30),nullable=False)
        )
    def db_init(self):
        conn_string = "postgresql+psycopg2://app_user:abc123@postgres_final:5432/postgres"
        # postgresql+psycopg2://root:abc123@postgres_final/postgres
        self.engine = create_engine(conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
    
dal = DataAccessLayer()
