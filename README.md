# airflow-docker

### master

```
# NFS 설정
# apt-get install nfs-common nfs-kernel-server rpcbind portmap
mkdir airflow-compose
chmod -R 777 airflow-compose

# nano /etc/exports
airflow-compose 192.168.0.0/16(rw,sync,no_subtree_check)

exportfs -a
systemctl restart nfs-kernel-server

rm -rf logs/ dags/ plugins/ script/ && mkdir logs/ dags/ plugins/ script/
chmod -R 777 logs/ dags/ plugins/ script/
docker-compose -f docker-compose.yaml up -d
```

### worker - 사용 OS에 따라 NFS 설정방법 다름


```
mkdir airflow-compose
mount ${MASTER_HOST}:airflow-compose airflow-compose # on Linux
sudo mount -t nfs -o resvport,rw,nfc ${MASTER_HOST}:airflow-compose airflow-compose # on MAC

docker-compose -f docker-compose-worker.yaml up
