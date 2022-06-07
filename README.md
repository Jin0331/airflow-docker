# airflow-docker

### master

```
rm -rf logs/ dags/ plugins/ script/ && mkdir logs/ dags/ plugins/ script/
docker-compose -f docker-compose.yaml up -d
```

### worker

```
rm -rf logs/ dags/ plugins/ script/ && mkdir logs/ dags/ plugins/ script/
docker-compose -f docker-compose-worker.yaml up
