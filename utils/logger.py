from sqlalchemy import (
    Column, BigInteger, String, Text, Integer,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging
import traceback
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ApplicationLog(Base):
    __tablename__ = "application_log"
    __table_args__ = {"schema": "ai_agent_schema"}

    id = Column(BigInteger, primary_key=True)
    run_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    log_level = Column(String(10), nullable=False)
    file_name = Column(String(255))
    function_name = Column(String(255))
    line_number = Column(Integer)
    message = Column(Text, nullable=False)

class SQLAlchemyLogHandler(logging.Handler):
    def __init__(self, engine, run_id=None):
        super().__init__(level=logging.INFO)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.run_id = run_id

    def emit(self, record):
        try:
            log = ApplicationLog(
                run_id=self.run_id,
                log_level=record.levelname,
                file_name=record.pathname,
                function_name=record.funcName,
                line_number=record.lineno,
                message = record.getMessage(),
            )
            self.session.add(log)
            self.session.commit()
        except Exception:
            self.session.rollback()
            # never let logging crash the app
            print("Logging to DB failed")
            traceback.print_exc()

def setup_logging(engine, run_id):
    logger = logging.getLogger("ai-agent")
    logger.setLevel(logging.INFO)

    db_handler = SQLAlchemyLogHandler(engine, run_id=run_id)
    db_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    db_handler.setFormatter(formatter)

    logger.addHandler(db_handler)
    logger.propagate = False
    return logger

