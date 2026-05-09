docker pull jupyter/pyspark-notebook:lab-4.0.7


docker run -it --rm \
  -p 8888:8888 \
  -v "$PWD":/home/jovyan/work \
  jupyter/pyspark-notebook:lab-4.0.7