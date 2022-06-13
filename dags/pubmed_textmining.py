from pathlib import Path
from utils.alerts import SlackAlert
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.helpers import chain
from airflow.models import DAG
from airflow.utils.dates import days_ago
from docker.types import Mount 
from datetime import datetime, timedelta

# slack token
with open("/opt/airflow/dags/SLACK_TOKEN", "r") as f:
    token = f.readline()
alert = SlackAlert('#airflow_alert', token)

# # mkdir
# TEXTMINING_PATH = '/opt/airflow/data/textmining'
# Path(TEXTMINING_PATH).mkdir(parents=True, exist_ok=True)

# function
def multiple_task(cancer_type):
  t = list()
  for cancer in cancer_type:
    t.append(DockerOperator(
      docker_url='tcp://docker-proxy:2375', #Set your docker URL
      image='sempre813/textmining:0610',
      command='Rscript R/pubmed_apriori_docker.R ' + cancer,
      # mounts = [
      #   Mount(
      #     source = TEXTMINING_PATH,
      #     target = '/home/rstudio/RAW_DATA',
      #     type = 'bind'
      #     )],
      auto_remove = True,
      task_id='textmining-' + cancer,
      dag=dag
      ))
  return t



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

# DAGs
task_list = multiple_task(cancer_type)
t1 >> task_list[0]
for i in range(len(task_list) - 1):
    task_list[i] >> task_list[i + 1]

#  Test code
# t1 >> multiple_task(["BLCA"]) #test code
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