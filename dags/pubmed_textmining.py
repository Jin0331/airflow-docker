from email.mime import image
from utils.alerts import SlackAlert
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.helpers import chain
from airflow.models import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# slack token
with open("/opt/airflow/dags/SLACK_TOKEN", "r") as f:
    token = f.readline()
alert = SlackAlert('#airflow_alert', token)

# DAGs
args = {'owner': 'Target ID',
        'start_date': days_ago(n=1),
        'on_success_callback': alert.success_msg,
        'on_failure_callback': alert.fail_msg,
        'queue': 'server2.6'
        }

dag = DAG(dag_id='pubmed_textmining',
          default_args=args,
          schedule_interval='@weekly')


#function
cancer_type = ['ACC',	'BLCA',	'BRCA', 'CESC',	'CHOL',	'COAD',	'READ',	'HNSC',	'LIHC',	'LUAD',	'LUSC',	'DLBC',
                	'OV',	'PAAD',	'PRAD',	'SKCM',	'STAD',	'GBM']

def multiple_task(cancer_type):
  t = list()
  for cancer in cancer_type:
    t.append(DockerOperator(
      # api_version='1.19',
      docker_url='tcp://docker-proxy:2375', #Set your docker URL
      image='sempre813/textmining:0610',
      command='Rscript R/pubmed_apriori_docker.R ' + cancer,
      auto_remove = True,
      task_id='textmining-' + cancer,
      dag=dag
      ))
  return t


# DockerOperator
t1 = DockerOperator(
  # api_version='1.19',
  docker_url='tcp://docker-proxy:2375', #Set your docker URL
  command='cowsay hello',
  image='docker/whalesay',
  network_mode='bridge',
  task_id='docker_status',
  dag=dag
)

task_list = multiple_task(cancer_type)

t1 >> task_list[0]
for i in range(len(task_list) - 1):
    task_list[i] >> task_list[i + 1]


# task_list1 = multiple_task(cancer_type[:9])
# task_list2 = multiple_task(cancer_type[9:])

# # task_list1
# t1 >> task_list1[0]
# for i in range(len(task_list1) - 1):
#     task_list1[i] >> task_list1[i + 1]

# # task_list1
# t1 >> task_list2[0]
# for i in range(len(task_list2) - 1):
#     task_list2[i] >> task_list2[i + 1]