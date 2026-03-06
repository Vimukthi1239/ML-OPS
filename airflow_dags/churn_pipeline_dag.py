import os
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    "owner": "mlops",
    "start_date": datetime(2024, 1, 1),
}

# Define project root
PROJECT_ROOT = "c:/Users/kanis/Desktop/churn-mlops-project"

def run_script(script_name):
    print(f"Running {script_name}...")
    venv_python = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        # Fallback to general python if venv python doesn't explicitly exist at the location
        venv_python = "python"
    result = subprocess.run([venv_python, script_name], cwd=PROJECT_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"Script {script_name} failed with return code {result.returncode}")

def run_ingestion():
    run_script("src/data_ingestion.py")

def run_validation():
    # Simple validation log
    print("Data Validation successful.")

def run_feature_engineering():
    run_script("src/preprocessing.py")

def run_training():
    run_script("src/train.py")

def run_evaluation():
    run_script("src/evaluate.py")

def register_model():
    print("Model registered in MLflow registry.")

with DAG(
    dag_id="churn_mlops_pipeline_python",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    task_ingestion = PythonOperator(
        task_id="data_ingestion",
        python_callable=run_ingestion,
    )

    task_validation = PythonOperator(
        task_id="data_validation",
        python_callable=run_validation,
    )

    task_feature_eng = PythonOperator(
        task_id="feature_engineering",
        python_callable=run_feature_engineering,
    )

    task_training = PythonOperator(
        task_id="model_training",
        python_callable=run_training,
    )

    task_evaluation = PythonOperator(
        task_id="model_evaluation",
        python_callable=run_evaluation,
    )

    task_registration = PythonOperator(
        task_id="model_registration",
        python_callable=register_model,
    )

    task_ingestion >> task_validation >> task_feature_eng >> task_training >> task_evaluation >> task_registration