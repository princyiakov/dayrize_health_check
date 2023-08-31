# Dayrize Health  Check APP 

1. Download and Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Run the following 
```
git clone https://github.com/princyiakov/dayrize_health_check.git
cd dayrize_health_check
docker build -t data-health-check .
docker run -p 8501:8501 data-health-check
```
3. Open [http://localhost:8501/](http://localhost:8501/) on browser
