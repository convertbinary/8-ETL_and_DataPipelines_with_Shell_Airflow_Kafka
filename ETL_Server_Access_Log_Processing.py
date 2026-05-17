# import block

from datetime import timedelta, datetime
# The DAG object; we'll need this to instantiate a DAG
# from airflow.models import DAG
# Operators; you need this to write tasks!
# from airflow.operators.bash_operator import BashOperator (not working for airflow 3.2.1)
from airflow.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
# This makes scheduling easy
# from airflow.utils.dates import days_ago (not working for airflow 3.2.1)
# for download task
import subprocess
# for dag
from airflow.sdk import DAG
import urllib.request

target_path = "/tmp/web-server-access-log.txt"
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt'

def download(url, target_path):
    with urllib.request.urlopen(url) as file:
        with open(target_path, "wb") as new_file:
            new_file.write(file.read())

# def download():
#     url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt'
#     myfilepath = subprocess.run(["wget", url], check=True)


# create dag definition block, the dag run daily
# dag = DAG(
#     'ETL-Server-Access-Log',
#     default_args=default_args,
#     description='ETL-Server-Access-Log',
#     schedule_interval=timedelta(days=1),
# )

# The DAG object; we'll need this to instantiate a DAG
# from example of airflow 3.2.1  https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html
dag = DAG(
    'ETL-Server-Access-Log',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="ETL-Server-Access-Log",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["ETL-Server-Access-Log"],
)

# create the download task
download = PythonOperator(
    task_id='download',
    python_callable=download,
    op_kwargs={'url': url, 'target_path': target_path},
    dag=dag,
)
# create the extract task
extract = BashOperator(
    task_id='extract',
    bash_command='cut -d"#" -f1,4 /tmp/web-server-access-log.txt > /tmp/visitorid.txt',
    dag=dag,
)
# create the transform task
transform = BashOperator(
    task_id='transform',
    bash_command='tr [A-Z] [a-z] < /tmp/visitorid.txt > /tmp/visitorid_transformed.txt',
    dag=dag,
)
# create the load task

# create the task pipleline block
download >> extract >> transform