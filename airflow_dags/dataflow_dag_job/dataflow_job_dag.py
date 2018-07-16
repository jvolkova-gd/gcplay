from airflow.contrib.operators.dataflow_operator import DataFlowJavaOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from datetime import datetime, timedelta


dataflow_dag = DAG(dag_id="dataflow_pipeline",
                   start_date=datetime(2017, 2, 2),
                   schedule_interval=timedelta(seconds=1),
                   max_active_runs=1,
                   catchup=True)

print_path_task = BashOperator(dag=dataflow_dag,
                               bash_command="pwd",
                               task_id="test_upstream_task_pwd")

jar_task = DataFlowJavaOperator(dag=dataflow_dag,
                                jar="/home/airflow/gcs/dags/"
                                    "jar/beam_playground-1.0.jar",
                                dataflow_default_options= {
                                    "project": "hybrid-elysium-118418"},
                                task_id="dataflow_pipeline")

print_path_task.set_downstream(jar_task)
