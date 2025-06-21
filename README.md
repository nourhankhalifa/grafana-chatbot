# 🤖 Grafana Chatbot for Natural Language Log Queries

This project enables querying **Loki logs in Grafana** using natural language prompts. It includes:

- A **Grafana panel plugin** for user input
- A **FastAPI agent** that translates natural language to LogQL using an LLM (OpenAI or Ollama)
- Deployment configurations using **Helm** for Grafana and Loki

---

## 🔧 Repository Structure

```

grafana-chatbot/
├── agent/                     # FastAPI app for LLM query handling
│   ├── main.py
│   ├── routes/
│   │   └── query.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── chatbot-panel/            # Grafana panel plugin (React-based)
│   └── src/
│       └── module.tsx
│
├── helm/                     # Helm values files
│   ├── grafana-values.yaml
│   └── loki-values.yaml
│
└── README.md

````

---

## 🧠 Requirements

- Docker
- Helm
- Kubernetes cluster (local or remote)
- Python 3.11+ for local testing
- OpenAI API key or Ollama (LLM backend)

---

## 🚀 1. Setup: FastAPI Agent

### Install dependencies:

```bash
cd agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### Set environment variables:

Create a `.env` file:

```
LOKI_URL=http://localhost:3100
OPENAI_API_KEY=your_openai_key_here
```

### Run locally:

```bash
uvicorn agent.main:app --reload
```

---

## 🐳 2. Dockerize the Agent

From inside the `agent/` directory:

### Dockerfile (already included):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./agent
EXPOSE 8000
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build Docker image:

```bash
docker build -t agent:latest .
```

---

## ☸️ 3. Deploy Agent to Kubernetes

### Create secret for OpenAI:

```bash
kubectl create secret generic openai-api-key \
  --from-literal=OPENAI_API_KEY=your_openai_key_here
```

### Apply deployment and service:

```yaml
# k8s/agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logql-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: logql-agent
  template:
    metadata:
      labels:
        app: logql-agent
    spec:
      containers:
      - name: logql-agent
        image: agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: LOKI_URL
          value: "http://loki.monitoring.svc.cluster.local:3100"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-api-key
              key: OPENAI_API_KEY
---
apiVersion: v1
kind: Service
metadata:
  name: logql-agent
spec:
  selector:
    app: logql-agent
  ports:
  - port: 80
    targetPort: 8000
```

Apply it:

```bash
kubectl apply -f deployment.yaml
```

---

## 📦 4. Grafana Plugin Panel (Chatbot)

### Build plugin:

```bash
cd chatbot-panel
yarn install
yarn dev
```

Or for production:

```bash
yarn build
```

### Add plugin to Grafana via Helm:

Add this to your `grafana-values.yaml`:

```yaml
plugins:
  - custom-chatbot-panel

extraInitContainers:
  - name: plugin-copy
    image: busybox
    command: ["/bin/sh", "-c"]
    args:
      - >
        mkdir -p /var/lib/grafana/plugins/custom-chatbot-panel &&
        cp -r /var/lib/custom-plugins/* /var/lib/grafana/plugins/custom-chatbot-panel
    volumeMounts:
      - name: plugin-volume
        mountPath: /var/lib/grafana/plugins
      - name: custom-plugins
        mountPath: /var/lib/custom-plugins

extraVolumeMounts:
  - name: custom-plugins
    mountPath: /var/lib/custom-plugins

extraVolumes:
  - name: custom-plugins
    hostPath:
      path: /full/path/to/chatbot-panel/dist

persistence:
  enabled: false
```

---

## 📈 5. Install Grafana with Helm

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm upgrade --install grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  -f helm/grafana-values.yaml
```

---

## 📊 6. Install Loki with Helm

```bash
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  -f helm/loki-values.yaml
```

---

## 🧪 7. Test & Access

### Port forward Grafana:

```bash
kubectl port-forward -n monitoring svc/grafana 3000:80
```

Then open [http://localhost:3000](http://localhost:3000)

### Set up Loki data source:

* **Name**: `loki`
* **URL**: `http://loki.monitoring.svc.cluster.local:3100`
* **Access**: `Server`

---

## 🧠 Prompt Examples

```text
"Show all logs from namespace monitoring in the last 5 minutes"
"summarize what happened in loki-0 in the last 5 minute"
"explain what happened in grafana in last 15 minutes"
"Get logs from loki-0 for the past 2 hours"
```

---

## 📬 Contributing

Pull requests welcome! Open issues for feedback, bugs, or ideas.

---