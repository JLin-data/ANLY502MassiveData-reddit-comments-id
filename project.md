# ANLY502 - Massive Data Analytics<br>Big Data Project

This project gives you the opportunity to work with a pretty large dataset of JSON data (~500GB) using the tools we've learned in class.


## Dataset and Background

You will be working with the [Reddit](www.reddit.com) comments archive. 

You can visit [this link](https://archive.org/details/2015_reddit_comments_corpus) and [this link](https://thenextweb.com/insider/2015/07/10/you-can-now-download-a-dataset-of-1-65-billion-reddit-comments-beware-the-redditor-ai/) to read more the dataset. The files are hosted [here](https://files.pushshift.io/reddit/comments/), however, the files are compressed and not accessible directly from your clusters.

We have taken the files for Oct/Nov/Dev 2018 and Jan 2019, downloaded them from the archive, decompressed them, and made them available to you in various formats:

* Plain text at `s3://mv559/reddit/plain-text/`
	* `RC_2018-10`
	* `RC_2018-11`
	* `RC_2018-12`
	* `RC_2019-01` 
* LZO compressed at `s3://mv559/reddit/lzo/`
	* Compressed files: 
		* `RC_2018-10.lzo`
		* `RC_2018-11.lzo`
		*  `RC_2018-12.lzo`
		*   `RC_2019-01.lzo` 
	* LZO Index files: 
		* `RC_2018-10.lzo.index`
		*  `RC_2018-11.lzo.index`
		*   `RC_2018-12.lzo.index`
		*    `RC_2019-01.lzo.index` 

A sample data directory is also available at: `s3://mv559/reddit/sample-data/` with a 1 million subset of records:

* Plain text: `1m-line-sample.json`
* LZO Compressed: `1m-line-sample.json.lzo`

**These files are NOT in a public S3 bucket. Throughout the course, all other files have been in a public bucket, but that means that our account gets charged every time you access these files. For the project, we are giving you read-access credentials and show you how to read files located in another account's bucket, and the S3 charges will hit your account. The S3 charges to you are nominal, but for our account for all users is pretty significant.**

### AWS Access Credentials

The following credentials grant you read only access to the files:

* AWS ACCESS KEY: AKIAQYYJWECSO4ERCXUU
* AWS SECRET ACCESS KEY: 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

### Accessing files from the command line

If you want to work with the files with the command line (on the master node), you must add environment variables, and use the `s3a://` prefix.

```
[hadoop@ip-172-31-39-134 ~]$ export AWS_ACCESS_KEY_ID=AKIAQYYJWECSO4ERCXUU
[hadoop@ip-172-31-39-134 ~]$ export AWS_SECRET_ACCESS_KEY=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

[hadoop@ip-172-31-39-134 ~]$ hadoop fs -ls s3a://mv559/reddit/
Found 4 items
drwxrwxrwx   - hadoop hadoop          0 2019-04-08 16:38 s3a://mv559/reddit/lzo
drwxrwxrwx   - hadoop hadoop          0 2019-04-08 16:38 s3a://mv559/reddit/plain-text
drwxrwxrwx   - hadoop hadoop          0 2019-04-08 16:38 s3a://mv559/reddit/sample-data
drwxrwxrwx   - hadoop hadoop          0 2019-04-08 16:38 s3a://mv559/reddit/zst

```

### Accessing files from Spark

To read the files from within Spark, after you create your Spark Session and/or Spark Context, you can add this code:

```python
sc._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId", "AKIAQYYJWECSO4ERCXUU")
sc._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", "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")
sc._jsc.hadoopConfiguration().set("fs.s3.awsAccessKeyId", "AKIAQYYJWECSO4ERCXUU")
sc._jsc.hadoopConfiguration().set("fs.s3.awsSecretAccessKey", "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")
sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", "AKIAQYYJWECSO4ERCXUU")
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", "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")
```

Then, you can read the files by using the right API (RDD, SQL, etc.) with the `s3://` prefix:

`test = spark.read.json("s3://mv559/reddit/sample-data/1m-line-sample.json")`


### Working with LZO compressed files in Spark

To take advantage of the splittability of LZO files in Spark (the prefered method - it's faster overall), you need to use a special RDD function. **Note: this only works for RDD methods, not SparkSQL or DataFrame methods.**

You need to provide the credentials as specified above before you do this.

```python
json_lzo = sc.newAPIHadoopFile("s3://mv559/reddit/sample-data/1m-line-sample.json.lzo", 
                               "com.hadoop.mapreduce.LzoTextInputFormat", 
                               "org.apache.hadoop.io.LongWritable", 
                               "org.apache.hadoop.io.Text")
```

We recommend that you read in the JSON files as an RDD from the LZO files, process them as you see fit, and store them as parquet files in your own S3 bucket.


### General Recommendations

* Use spot pricing for your cluster. With m4.xlarge machines, each machine costs $0.20/hr per machine time, plus the EMR fee of $0.06 for a total of $0.26 per machine per hour. You can save money with spot pricing (just on machine time, not on EMR cost.) Keep track of your spend!.
* Refer to the [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/index.html) and [Spark Documentation](https://spark.apache.org/docs/latest/)
* Start early on this project, not two days before it is due.
* Consider saving intermediate datasets in your S3 buckets, in [Apache Parquet](https://parquet.apache.org/) format. 
* Consider saving a model object in S3 after you train it, especially if training takes a while. To save a model object, use the following code: `model.save("s3://[[your-s3-bucket]]/model_location/")`
* When creating the Machine Learning pipelines, you may want to try it first on a small sample of your training data to make sure the pipelines work as planned. To create a tiny DataFrame, use the `limit` method: `df.limit(100)` (this creates a small DataFrame with the first 100 rows from df.)
* If you need to re-start your Jupyter notebook for any reason, make sure you close the Spark connection first **before** restarting the kernel. To do this, type either `sc.stop()` or `spark.stop()` in a cell. If you don't do this, YARN will not release resources previously allocated.
* Use the sample data in `s3://mv559/sample-data/` to get acquainted with the data, and to test out your code before you run it at scale.
* As stated above, use the LZO compressed files to begin with.


## Requirements

The goal of this project is to identify one or more question of interest based on the Reddit data, and use the tools we've learned in class to produce an interesting result. You are welcome to use any of the tools we learned in class (MapReduce, Hadoop Streaming, PIG, Hive, Spark - all APIs). 

While the project is open ended, there are some parameters and guidelines to help plan and organize your approach. The project needs to have, at a minimum, the following:

* **Exploratory Analysis (8 points):** Explore, assess and visualiza the data. Aggregate, count, and summarize. Create graphs, tables, etc and explain your findings in writing. Clean data if necessary. 
* **Model (8 points):** Build any type of model you feel is appropriate and meaningful. You can perform any type of supervised or unsupervised approach. You must have evaluation metrics for supervised approaches and/or visualizations for unsupervised learning approaches. You are welcome to try different modeling techniques that you are comfortable with. 
* **Writeup (4 points):** Create a short writeup of your analysis with the following elements:
	- Name
	- Introduction
	- Code (you should list your code files here, and these must be in your submitted repository with appropriate comments.)
	- Methods section:
		- How you cleaned, prepared the dataset with samples of intermediate data
		- Tools you used for analyzing the dataset and the justification (tools, models, etc.)
		- How you modeled the dataset, what techniques did you use and why?
		- Did you have a hypothesis that you were tryig to prove?
		- Or did you just visualize the dataset?
	- Results section:
		- What you found.
		- How you validated what you found (if you validated what you found)
	- Future work: what would you do differently?

* **Extra Credit (up to 2 pts):** You can run multiple models or use different and reasonable feature combinations and conduct an error analysis to get the extra credit.

### Some guidelines for approaching the project

This is a snippet from a chapter that Prof. Vaisman wrote for the [Bad Data Handbook](http://shop.oreilly.com/product/0636920024422.do). We hope this provide some guidance.

_There are many kind of analytical exercises you can do. Some begin as an exploration without a specific question in mind; but it could be argued that even when exploring, there are some questions in mind that are not formulated. Other exercises begin with a specific question in mind, and end up answering another question. Regardless, before you embark on a research investigation, you should have some idea of where you are going. You need to be practical and know when to stop and move onto something else. But again, start with some end in mind. Just because you have a lot of data does not mean you have to do analysis just for analysis’ sake. Very often, this kind of approach ends with wasted time and no results._

## Submitting the Project

You will be getting a blank `README.md` file in your repository when you accept the assignment with GitHub classroom. There will also be a `project.md` file in the repository with the same contents of this assignment file. 

The files to be committed and pushed to the repository for the project are:

* `README.md` which is your project writeup file. 
* `instance-metadata.json`
* Any code/notebook file referenced in the __code__ section of your writeup. We should be able to follow the code with the writeup.
* Do NOT commit data files to the repository

**NO LATE DAYS CAN BE USED FOR THE PROJECT**

## Grading Criteria

The project will be graded holistically with the following rubric:

Grade of A:

* Writeup covers all areas above
* Language is clear, figures support research/investigation
* There is discussion on specifics of the analysis, and analysis decisions are justified
* Properly formatted

Grade of B:

* One major deficiency and/or
* Writeup and/or analysis is missing significant discussion/justification around analysis performed and/or
* Minor flaws in layout/presentation of analysis

Grade of C:

* Two deficient areas and/or
* Major flaws in layout/presentation of analysis

Grade of D:

* Three or more deficient areas

For the purposes of grading, a **deficiency** can mean any of the following:

- Instructions are not followed
- There are more files in your repository than need to be
- Missing sections of the writeup
- Poor and sloppy writing and/or presentation
- Many spelling and grammatical errors
- Code is not documented with comments
- Missing model performance metrics
- Doing an analysis and/or model just for the sake of doing it, without thinking through and providing justification
