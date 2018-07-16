from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHHook, SSHOperator

from datetime import timedelta, datetime


pub_sub_dag = DAG(dag_id="pub-sub-spamer",
                  description="Publish data to Pub/Sub",
                  schedule_interval=timedelta(seconds=15),
                  start_date=datetime(2017, 2, 1),
                  max_active_runs=1,
                  default_view="gantt",
                  orientation="LR",
                  catchup=True)


ssh_hook_instance_1 = SSHHook(ssh_conn_id="pub_sub_ssh",
                   username="xnuinside",
                   remote_host="35.226.71.118")

ssh_command = "cd gcplay && export PYTHONPATH=${PYTHONPATH}:./gcplay " \
              "&& env/bin/python gcplay/gcplay/publisher.py"

ssh_task = SSHOperator(dag=pub_sub_dag,
                       ssh_hook=ssh_hook_instance_1,
                       command=ssh_command,
                       ssh_conn_id="pub_sub_ssh",
                       task_id="run_publisher",
                       schedule_interval="once")
