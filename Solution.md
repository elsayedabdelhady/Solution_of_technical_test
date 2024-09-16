# Technical Test DevOps Orchestration
This project demonstrates the orchestration of a backend API and a data API using Kubernetes, Helm, and Ansible. It also includes monitoring using Prometheus and Grafana.

## Prerequisites 
* Windows Subsystem for Linux (WSL) or linux machine
* Docker 
* Kubernetes 
* Helm
* Ansible
* Prometheus 
* Grafana


## Steps
`` ansible-playbook main_playbook.yaml ``
it will start the helm chart and it contains 2 deployment (backend api & data api) and 2 service for them and 2 ingress.

### Monitoring with Prometheus and Grafana

1. Add Helm repositories and update
``` helm repo add prometheus-community https://prometheus-community.github.io/helm-charts ```
``` helm repo add grafana https://grafana.github.io/helm-charts ```
``` helm repo update ```
2. ``` helm install prometheus prometheus-community/kube-prometheus-stack ```
3. ``` helm install grafana grafana/grafana --set adminPassword='admin' --set service.type=LoadBalancer ```

### Access Grafana Dashboard
1. Find the Grafana service's external IP:
``` kubectl get svc --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" ```
2. Open your browser and go to `http://<external-ip>:3000`.
3. Log in with the username `admin` and password `admin`.

### Add Prometheus Data Source to Grafana
1. Go to Grafana's home page.
2. Click on "Add your first data source".
3. Select "Prometheus".
4. Set the URL to http://prometheus-server.default.svc.cluster.local
5. Click "Save & Test".

### Create a Dashboard to Monitor Resource Utilization
1. Create a new dashboard in Grafana.
2. Add a new panel with the following Prometheus query to monitor CPU utilization for pods with the label `k8s-app=kube-Devops`:

``` sum(rate(container_cpu_usage_seconds_total{pod=~".*", k8s_app="kube-Devops"}[5m])) by (pod) ```

3. Add another panel to monitor memory utilization:
``` sum(container_memory_usage_bytes{pod=~".*", k8s_app="kube-Devops"}) by (pod) ```

4. Save the dashboard.

# Commands I used
1. docker commands:
   * create the image : `cd backend_api` `docker build -t backendapi:latest .`
   * run the image to test if it works : `docker run -p 5000:5000 backendapi:latest`
   * test the url or from postman
   * Push the Docker Image to a Registry : `docker tag backendapi:latest elsayed2020/backendapi:latest`
   ` docker push elsayed2020/backendapi:latest ` 
2. Helm commands:
   * Lint the Helm Chart: `helm lint ./helm_chart` 
   * Install the Helm Chart: `helm install technical-test ./helm_chart`
   * Check the Deployment: ` kubectl get pods`  `kubectl get services`
   * Update Prometheus to use the persistent storage
      `helm upgrade prometheus prometheus-community/prometheus --set server.persistentVolume.enabled=true --set server.persistentVolume.storageClass=local-storage --set server.persistentVolume.existingClaim=prometheus-pvc`
   * Update Grafana to use the persistent storage
     `helm upgrade grafana grafana/grafana --set persistence.enabled=true,persistence.storageClassName="local-storage",persistence.existingClaim="grafana-pvc"`   
3. Kubernetes commands 
   * create the pv and pvc:
      ` kubectl apply -f persistent_volume/pv-prometheus.yaml `
      ` kubectl apply -f persistent_volume/pvc-prometheus.yaml `
      ` kubectl apply -f persistent_volume_claim/pv-grafana.yaml `
      ` kubectl apply -f persistent_volume_claim/pvc-grafana.yaml `
   * get ingresses
      `kubectl get ingresses`
   * Port Forward to Access Services: 
      `kubectl port-forward svc/backend-api 8080:80 `
      `kubectl port-forward svc/data-api 8081:80`
4. Run the Health Check Script:
    `sudo ./health_check.sh`


