# airflow-docker

### master

```
# NFS 설정
# apt-get install nfs-common nfs-kernel-server rpcbind portmap
mkdir airflow-compose
chmod -R 777 airflow-docker/dags

# nano /etc/exports
airflow-docker/dags 192.168.0.0/24(rw,sync,no_subtree_check)

sudo exportfs -a
sudo systemctl restart nfs-kernel-server

docker-compose up airflow-init
docker-compose -f docker-compose.yaml up -d
```

* **DAG** 작성 후 필이 permision 권한 줄 것

### worker - 사용 OS에 따라 NFS 설정방법 다름


```
mkdir airflow-docker/dags
sudo mount ${MASTER_HOST}:airflow-docker/dags airflow-docker/dags # on Linux
sudo mount -t nfs -o resvport,rw,nfc ${MASTER_HOST}:airflow-docker/dags airflow-docker/dags # on MAC

docker-compose up airflow-init
docker-compose -f docker-compose-worker.yaml up
