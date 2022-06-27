FROM python:3
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY src/ app/
WORKDIR /app
ENV PYTHONPATH /app
CMD ["python3", "main.py"]