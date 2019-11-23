#!/bin/bash
set -x -e

# Copyright 2019 Marck Vaisman
# AWS EMR Bootstrap Script based on Tom Zeng's script
# located at https://github.com/tomz/aws-big-data-blog/blob/master/aws-blog-emr-jupyter/install-jupyter-emr5.sh
# This script is designed to start a jupyter notebook running in the backgroud without a password for the hadoop user
# that is bound to pyspark

sudo pip-3.6 install findspark jupyter matplotlib pandas scikit-learn bokeh statsmodels scipy numpy seaborn

cd ~
wget http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar
jar xf graphframes-0.7.0-spark2.4-s_2.11.jar


cd -
screen -dm bash -c "HADOOP_HOME=/usr/lib/hadoop SPARK_HOME=/usr/lib/spark jupyter-notebook --no-browser --port=8765 --ip=0.0.0.0 --NotebookApp.token=''"

echo Cluster Customization completed at `date`

echo "
-------------- POST STARTUP SCRIPT COMPLETE --------------------
*** You are still logged into the master node of EMR cluster ***
To access Jupyter notebook, logoout from the master node as soon
as you see this message with the exit command.
Once you disconnect from the master node, ssh back in using
agent and port forwarding. Remember to type `ssh-add` before:
ssh -A -L8765:localhost:8765 hadoop@...
and then open a web browser and go to http://localhost:8765
----------------------------------------------------------------
"
