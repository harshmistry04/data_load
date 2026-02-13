from utils.db_connector import db_engine, job_run
import uuid
from datetime import datetime
import pandas as pd

def main():
    print("Hello from data-load!")
    run = job_run(      run_id=uuid.uuid4(),
                        job_name='New York',
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        run_status='SUCCESS',
                        retry_count=0,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                        )
    engine = db_engine()
    engine.add_entry(run)
    result = engine.read_all_entries("""SELECT * FROM ai_agent_schema.job_run;""")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(result)

if __name__ == "__main__":
    main()
