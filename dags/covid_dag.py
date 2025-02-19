import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def function_import_file(ti):# Le ti c'est l'objet de la fonction PythonOperator
    df = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5")
    df = df.to_dict(orient="records")  # Convertit le DataFrame en dictionnaires car xcom attend un dictionnaire et non un dataframe
    ti.xcom_push(key="dataframe", value=df) #la key sert de code pour reconaitre quel push

def transform(ti):
    df = ti.xcom_pull(task_ids="import_file", key="dataframe") #on recupere l'objet du pythonoperator qui a id import file et pour clé dataframe
    df=pd.DataFrame(df)# Convertit le dict en dataframe
    data = df[['date', 'incid_hosp']]
    if os.path.exists("./data/hospitalisation.csv"):#export du dataframe dans un fichier csv
        data.to_csv("./data/hospitalisation.csv", mode="a", header=False, index=False)
    else:
        data.to_csv("./data/hospitalisation.csv", header=True, index=False)
    logging.info("Data saved in hospitalisation.csv 🥳")
    plt.figure();
    plt.plot(data['date'], data['incid_hosp'], marker='o', linestyle='-', color='b')
    plt.savefig('./data/hospitalisation.png')
   

with DAG("covid_dag", start_date=datetime(2022, 1, 1), schedule_interval="@hourly", catchup=False) as dag: #catchup false permet de pas avoir un effect retroactif
    good_import_file=PythonOperator(task_id="import_file", python_callable=function_import_file)#creation d'un dag import file qui utilise la fonction function_import_file
    the_transform=PythonOperator(task_id='transform_file', python_callable=transform)
      

    good_import_file >> the_transform  # Défini la dépendance entre les tâches
