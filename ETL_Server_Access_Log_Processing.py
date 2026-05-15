# import block

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# create the dag arguments block
default_args = {
    'ower':'Yu',
    'start_date':days_ago(0),
    'email':['mymail'],
    'retries':1,
    'retry_delay':timedelta(minutes=5),
}

# create dag definition block, the dag run daily
dag = DAG(
    'ETL-Server-Access-Log',
    default_args=default_args,
    description='ETL-Server-Access-Log',
    schedule_interval=timedelta(days=1),
)

# create the download task
download = BashOperator(
    task_id='download',
    bash_command='wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"',
    dag = dag,
)
# create the extract task
extract = BashOperator(
    task_id='extract',
    bash_command='cut -d"#" -f1,4 web-server-access-log.txt > visitorid.txt',
    dag=dag,
)
# create the transform task
transform = BashOperator(
    task_id='transform',
    bash_command='echo visitorid.txt | tr [A-Z] [a-z]',
    dag=dag,
)
# create the load task

# create the task pipleline block
download >> extract >> transform