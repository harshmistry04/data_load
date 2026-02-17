from utils.db_connector import db_engine, job_run
import uuid
from datetime import datetime
import pandas as pd
import threading
from utils.logger import setup_logging

execution_id = uuid.uuid4()
thread_local = threading.local()

def main():
    thread_local.run_id = str(execution_id)
    engine = db_engine()
    logger = setup_logging(engine.engine, execution_id)
    logger.info("Starting data-load!")
    run = job_run(      run_id=execution_id,
                        job_name='New York',
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        run_status='SUCCESS',
                        retry_count=0,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                        )
    
    try:
        logger.info("Connected to Database!")
        engine.add_entry(run)
        logger.info("Entry made to Database!")
        logger.info("Reading from Database!")
        result = engine.read_all_entries("""SELECT * FROM ai_agent_schema.job_run;""")
    except Exception as e:
        logger.error(e)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(result)

if __name__ == "__main__":
    main()
