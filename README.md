# End-to-End Customer Churn Prediction MLOps Pipeline

This repository contains the completed End-to-End Customer Churn Prediction project.

## Project Architecture
The project strictly follows the mandatory architecture requirements:
- **Git** & **DVC** for Code and Data Versioning
- **MLflow** for Experiment Tracking (Parameters, Metrics, Models, Confusion Matrices, ROC curves)
- **Airflow** for Workflow Orchestration
- **DAGsHub** for remote hosting
- **FastAPI** & **Docker** for REST API Deployment

## 1. Local Setup Instructions
Before running the pipeline, ensure your virtual environment is active and all requirements are installed:
```bash
pip install -r requirements.txt
```

## 2. Running the DVC Pipeline (Data Engineering & Model Training)
The entire data ingestion, preprocessing, training, and evaluation runs via DVC.
```bash
dvc repro
```
*This will execute `src/data_ingestion.py`, `src/preprocessing.py`, `src/train.py`, and `src/evaluate.py` in the correct order.*

## 3. Investigating MLflow Tracking
MLflow logs accuracy, precision, recall, f1, ROC-AUC, and parameters for each model, selecting the best one and saving its artifact. It also creates plots for Confusion Matrix and ROC curve.
```bash
mlflow ui
```
*Open `http://localhost:5000` to view the UI.*

## 4. Running Airflow Orchestration
The Airflow DAG is implemented in `airflow_dags/churn_pipeline_dag.py` using `PythonOperator`. It is configured to run the scripts step-by-step.
```bash
airflow webserver -D
airflow scheduler -D
```
*Access the UI at `http://localhost:8080`, enable `churn_mlops_pipeline_python`, and trigger it.*

## 5. Running the REST API (Docker)
The best model and scalar are utilized in `api/main.py` via FastAPI. It expects a single customer JSON, scales numerical features correctly, matches the training encoding, and generates a churn prediction. It also includes the **Bonus feature**: LLM-based retention incentive via OpenAI (returns a template if `OPENAI_API_KEY` is not set).

To build and run via Docker:
```bash
docker build -t churn-mlops-api .
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key-here" churn-mlops-api
```
Alternatively, test locally without Docker:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Test using the Swagger UI at `http://localhost:8000/docs`.

## 6. DAGsHub Integration
To push this pipeline to your DAGsHub repository:
1. Initialize/configure your DVC remote for DAGsHub.
```bash
dvc remote add origin https://dagshub.com/<username>/<repo>.dvc
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <username>
dvc remote modify origin --local password <token>
```
2. Push Git and DVC:
```bash
dvc push
git add .
git commit -m "End-to-end MLOps implementation complete"
git push origin main
```
