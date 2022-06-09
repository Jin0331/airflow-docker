from utils.alerts import SlackAlert
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta

# slack token
with open("/opt/airflow/dags/SLACK_TOKEN", "r") as f:
    token = f.readline()
alert = SlackAlert('#airflow_test', token)

# DAGs
args = {'owner': 'Target ID',
        'start_date': days_ago(n=1),
        'on_success_callback': alert.success_msg,
        'on_failure_callback': alert.fail_msg
        }

