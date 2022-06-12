from utils.alerts import SlackAlert
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
import time
from pprint import pprint

# slack token
with open("/opt/airflow/dags/SLACK_TOKEN", "r") as f:
    token = f.readline()

alert = SlackAlert('#airflow_alert', token)

args = {'owner': 'wmbio',
        'start_date': days_ago(n=1),
        'queue': 'server2.6',
        'on_success_callback': alert.success_msg,
        'on_failure_callback': alert.fail_msg
        }

dag = DAG(dag_id='DockerOperator_test2',
          default_args=args,
          schedule_interval='@daily')


### DAG
def print_fruit(fruit_name, **kwargs):
    print('=' * 60)
    print('fruit_name:', fruit_name)
    print('=' * 60)
    pprint(kwargs)
    print('=' * 60)
    return 'print complete!!!'

def sleep_seconds(seconds, **kwargs):
    print('=' * 60)
    print('seconds:' + str(seconds))
    print('=' * 60)
    pprint(kwargs)
    print('=' * 60)
    print('sleeping...')
    time.sleep(seconds)
    return 'sleep well!!!'

t1 = PythonOperator(task_id='task_1',
                    provide_context=True,
                    python_callable=print_fruit,
                    op_kwargs={'fruit_name': 'apple'},
                    dag=dag)
# DockerOperator
t2 = DockerOperator(
    # api_version='1.19',
    docker_url='tcp://docker-proxy:2375', #Set your docker URL
    command='echo TEST DOCKER SUCCESSFUL',
    image='centos:latest',
    # command='cowsay hello',
    # image='docker/whalesay',
    # network_mode='bridge',
    task_id='docker_op_tester',
    dag=dag
)

t1 >> t2