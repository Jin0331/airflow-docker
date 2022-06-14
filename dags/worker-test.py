from utils.alerts import SlackAlert
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from pprint import pprint

# slack token
with open("/opt/airflow/dags/SLACK_TOKEN", "r") as f:
    token = f.readline()

alert = SlackAlert('#airflow_alert', token)

# default arg
args = {'owner': 'wmbio',
        'start_date': days_ago(n=1),
        'on_success_callback': alert.success_msg,
        'on_failure_callback': alert.fail_msg
        }

dag = DAG(dag_id='worker-test',
          default_args=args,
          schedule_interval='@daily')

t1 = BashOperator(
  task_id = "master-worker1-5",
  bash_command = 'date',
  queue = 'server1.5',
  dag = dag
)

t2 = BashOperator(
  task_id = "worker2-6",
  bash_command = 'date',
  queue = 'server2.6',
  dag = dag
)

t3 = BashOperator(
  task_id = "worker3-7",
  bash_command = 'date',
  queue = 'server3.7',
  dag = dag
)

t4 = BashOperator(
  task_id = "worker4-NAS",
  bash_command = 'date',
  queue = 'server4.NAS',
  dag = dag
)

t1 >> [t2, t3, t4]