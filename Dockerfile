FROM apache/airflow:2.10.5

# Installer les outils de build nécessaires et les en-têtes de développement Python
USER root
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    gcc \
    && apt-get clean




# Vérifiez que python3-dev est installé
RUN dpkg -l | grep python3-dev

# Revenir à l'utilisateur airflow
USER airflow

COPY requirements.txt /

# Installer les packages Python
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
