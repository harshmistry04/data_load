from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import os


class db_engine:
    def __init__(self):
        self.user = os.getenv('user','postgres')
        self.password = os.getenv('password','pgadmin')
        self.DATABASE_URL = f'postgresql+psycopg2://{self.user}:{self.password}@localhost:5432/ai_agent_db'
        self.engine = create_engine(self.DATABASE_URL)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_entry(self, model):
        self.session.add(model)
        self.session.commit()

    def read_entry(self, model, run_id):
        return self.session.query(model).filter(model.run_id == run_id).all()

    def read_all_entries(self, query):
        return pd.read_sql(query, self.engine)


class job_run(declarative_base()):
    __tablename__ = 'job_run'
    __table_args__ = {'schema': 'ai_agent_schema'}
    run_id = Column(String, primary_key=True)
    job_name = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    run_status = Column(String)
    retry_count = Column(Integer)
    created_at  = Column(String)
    updated_at = Column(String)
