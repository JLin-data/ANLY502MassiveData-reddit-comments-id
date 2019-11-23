# Assignment - Hadoop Streaming

You will be performing Hadoop Streaming exercises in this assignment. 

1. Start an Amazon Elastic MapReduce (EMR) Cluster using Quickstart as described in the [Hadoop Streaming Lab](https://github.com/bigdatateaching/lab-hadoop-streaming), but choose 5 nodes (1 master and 4 core). 
2. `ssh` to the **Master Node** of your cluster using _ssh agent forwarding_ as described in the [setup lab](https://github.com/bigdatateaching/lab-setting-up). 
3. Once you connect to the Master Node, install git: 

	```
	$ sudo yum install -y git
	```
4. Configure git (this needs to be done every time you install git on a new resource)

	```
	$ git config --global user.name "your-github-username"
	$ git config --global user.email "your-gu-email"
	```
	
5. Clone this repository to your Master Node

	```
	$ git clone ...
	```
	
6. Change directory into the repository
7. Do you work. Remember, all files must be within the repository directory otherwise git will not see them.

* Remember to commit and push back to GitHub as you are doing your work. **If you terminate the cluster and you did not push to GitHub, you will lose all your work.**
* **Also, remember that data in the cluster's HDFS will be lost when the cluster terminates. If you want to keep data, store it in S3.**


## Provide the Master Node and Cluster Metadata

Once you are ssh'd into the master node, query the instance metadat and write to a file:

```
curl http://169.254.169.254/latest/dynamic/instance-identity/document/ > instance-metadata.json
```

Also, since you are using a cluster, please provide some metadata files about your cluster. Run the following commands:

```
cat /mnt/var/lib/info/instance.json > master-instance.json
cat /mnt/var/lib/info/extraInstanceData.json > extra-master-instance.json
```

## Problem 1 - The _quazyilx_ scientific instrument (3 points)

For this problem, you will be working with data from the _quazyilx_ instrument. The files you will use contain hypothetic measurements of a scientific instrument called a _quazyilx_ that has been specially created for this class. Every few seconds the quazyilx makes four measurements: _fnard_, _fnok_, _cark_ and _gnuck_. The output looks like this:

    YYYY-MM-DDTHH:MM:SSZ fnard:10 fnok:4 cark:2 gnuck:9

(This time format is called [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) and it has the advantage that it is both unambiguous and that it sorts properly. The Z stands for _Greenwich Mean Time_ or GMT, and is sometimes called _Zulu Time_ because the [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) word for **Z** is _Zulu_.)

When one of the measurements is not present, the result is displayed as negative 1 (e.g. `-1`). 

The quazyilx has been malfunctioning, and occasionally generates output with a `-1` for all four measurements, like this:

    2015-12-10T08:40:10Z fnard:-1 fnok:-1 cark:-1 gnuck:-1

There are four different versions of the _quazyilx_ file, each of a different size. As you can see in the output below the file sizes are 50MB (1,000,000 rows), 4.8GB (100,000,000 rows), 18GB (369,865,098 rows) and 36.7GB (752,981,134 rows). The only difference is the length of the number of records, the file structure is the same. 

```
[hadoop@ip-172-31-1-240 ~]$ hadoop fs -ls s3://bigdatateaching/quazyilx/
Found 4 items
-rw-rw-rw-   1 hadoop hadoop    52443735 2018-01-25 15:37 s3://bigdatateaching/quazyilx/quazyilx0.txt
-rw-rw-rw-   1 hadoop hadoop  5244417004 2018-01-25 15:37 s3://bigdatateaching/quazyilx/quazyilx1.txt
-rw-rw-rw-   1 hadoop hadoop 19397230888 2018-01-25 15:38 s3://bigdatateaching/quazyilx/quazyilx2.txt
-rw-rw-rw-   1 hadoop hadoop 39489364082 2018-01-25 15:41 s3://bigdatateaching/quazyilx/quazyilx3.txt
```

Your job is to find all of the times where the four instruments malfunctioned together using `grep` with Hadoop Streaming. 

You will run a Hadoop Streaming job using the 18GB fil as input.

Here are the requirements for this Hadoop Streaming job:

* The *mapper* is the `grep` function. 
* It is a map only job and must be run as such. (Think about why this is a map only job.)

You need to issue the command to submit the job with the appropriate parameters. [The reference for Hadoop Streaming commands is here.](https://hadoop.apache.org/docs/r2.7.3/hadoop-streaming/HadoopStreaming.html).

Paste the command you issued into a text file called `hadoop-streaming-command.txt`.  

Once the Hadoop Streaming job finishes, create a text file called `quazyilx-failures.txt` with the results which **must be sorted by date and time.**

The files to be committed to the repository for this problem are `hadoop-streaming-command.txt` and `quazyilx-failures.txt`.

## Problem 2 - Log file analysis (7 points)

The file `s3://bigdatateaching/forensicswiki/2012_logs.txt` is a year's worth of Apache logs for the [forensicswiki website](http://forensicswiki.org/wiki/Main_Page). Each line of the log file correspondents to a single `HTTP GET` command sent to the web server. The log file is in the [Combined Log Format](https://httpd.apache.org/docs/1.3/logs.html#combined).

Your goal in this problem is to report the number of hits for each month. Your final job output should look like this:

    2010-01,xxxxxx
    2010-02,yyyyyy
    ...

Where `xxxxxx` and `yyyyyy` are replaced by the actual number of hits in each month.

You need to write a Python `mapper.py` and `reducer.py` with the following requirements:

* You must use regular expressions to parse the logs and extract the date, and cannot hard code any date logic 
* Your mapper should read each line of the input file and output a key/value pair **tab separated format**
* Your reducer should tally up the number of hits for each key and output the results in a **comma separated format**

You need to run the Hadoop Streaming job with the appropriate parameters.

Once the Hadoop Streaming job finishes, create a text file called `logfile-counts.csv` with the results which **must be sorted by date.**

The files to be committed to the repository for this problem are `mapper.py`, `reducer.py` and `logfile-counts.csv`.


## Submitting the Assignment

Make sure you commit **only the files requested**, and push your repository to GitHub!

The files to be committed to the repository for this assignment are:

* `instance-metadata.json`
* `master-instance.json`
* `extra-master-instance.json`
* `hadoop-streaming-command.txt`
* `quazyilx-failures.txt`
* `mapper.py`
* `reducer.py`
* `logfile-counts.csv`


## Grading Rubric

-   We will look at the results files and/or scripts. If the result files are exactly what is expected, in the proper format, etc., we may run your scripts to make sure they produce the output. If everything works, you will get full credit for the problem.
-   If the submitted results are not what is expected, we will look at and run your code and provide partial credit wherever possible and applicable.
-   Points **will** be deducted for each the following reasons:
    -   Instructions are not followed
    -   Output is not in expected format (not sorted, missing fields, wrong delimiter, unusual characters in the files, etc.)
    -   There are more files in your repository than need to be
    -   There are additional lines in the results files (whether empty or not)
    -   Files in repository are not the requested filename
    -   Homework is late (unless you are using a late day and provide notice in advance)



	