# flask_datadog_demo
This project is to learn about flask api monitoring using datadog

# Build docker and deploy for testing purposes
docker compose up --build -d 

# Deploy Kubernetes for the service and deployment
kubectl apply -f flask-datadog-demo-service.yaml 
kubectl apply -f flask-datadog-demo-deployment.yaml

# Deploy in Kubernetes using Helm Yaml using docker registry on dockerhub
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<api_key> \
  --set datadog.site="us5.datadoghq.com" \
  --set agents.apm.enabled=true \
  --set agents.logs.enabled=true \
  --set agents.process.enabled=true \
  --set agents.containerLogs.enabled=true \
  --set clusterAgent.enabled=true

![Kubernetes Image](/.images/container_running.png)

Login to Datadog and create datadog dashboard and create some metrics:
![Docker Dashboard Image](/.images/datadog_dashboard_docker.png)

You can also see the Container Overview to check the metrics availability
![Kubernetes Overview Image](/.images/container_overview.png)

Check the docker overview as well:
![Docker Overview](/.images/docker_overview.png)