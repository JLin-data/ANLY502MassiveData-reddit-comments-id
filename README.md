
# ANLY502 - Massive Data Analytics Big Data Project: Predicting the most popular review in Reddit
--------------------------------------

Author: Jingjing Lin

Email: jl2445@georgetown.edu



## INTRODUCTION

For social media like Reddit, "stickied" review -- the most popular review at the top of review sections, has the most number of view counts, which not shows wits of author's but also brings traffic even profits for authors. This project aims to use some features of review including the length of review, the controversiality, etc. to predict whether this review is stickied or not. To some extent, this small model can potentially help reviewers identify some features of the most popular review.




## CODE DEVELOPMENT
As we could see from the MiniProject scripts, there are four main parts in the code.

### #1, Environment setting up
- This part including the pyspark setting up and loading data through S3.

- Functions and packages such as "findspark.init()" and "from pyspark import SparkContext" have been applied to the basic environment set up.

- "spark.read.json" has been applied to read JSON file (raw data).

- m4.xlarge with 1 master nodes and 10 nodes, one time running over 3 hours if you wanna rerun the results, mostly in model fitting part.

### #2, Exploratory Data Analysis (EDA)

#### Methdology 1: Coding Exploratory (Table)

- "Have a look"

Before starting topic-making or other further exploratory analysis, I applied to use "describe()" "show()" and "printSchema()" to generate an overview of datasets. This dataset contains 40 columns and 1 million rows.

- "Data cleaning"

Since either column with zero NA values or with a very large number of NA values, I chose to remove columns with NA values by using "is null()" and "drop()", as well as remove NA and FALSE rows in "archived".

- "Further exploratory"

"distinct().count()" has been applied for looking the number of distinctive value for each column. Through this aggregation function, which allowed me to get the binary classifications or multiple classifications for each column by using groupby(), crosstab(), especially for the numerical columns like "controversiality" and "stickied".

The frequency in the stickied column is (false|218381|) and (true|  761|), based on this, I came up the idea of the topic: to predict the stickied label in each review.

#### Methdology 2: Visualization (Graph)

For the numerical columns, visualization is a great method to access the distribution of datasets.
The histogram has been used for checking numerical columns with statistical meaning, for example, the "retrieved_on" column has been excluded because it is the user id.
"Score" column has been taken into consideration for feature engineering since it is the only one column with the varied distribution.

-------------------------------

### #3, Feature Engineering

There are two features added.

#### 1 New column "score_class" 

Since the most number of values are centralized between 0 to 20, and the distribution of score are scattered, it is sensitive to classify score column. The baseline I applied here is the score value below 0 or above 0.

#### 2 New column "body_length" 

A new feature included: the number of words in each review might be a factor.
I have used < reddit = reddit.withColumn("body_length", length("body")) >to add the new column.


---------------
### #4, Hypothesis

 - Hypothesis generating through EDA

After having an overview of data structures, the meaning of each column and distribution, to predict if a review has a stickied label is an appealing aspect. In the end, I choose 1) "controversiality" -- related having a high number of upvotes and downvotes. Indicated the community having a mixed reaction to the comment, 2) "score classification" -- presenting the overall score of comments judged by Reddit rating, 3) "subreddit" -- the theme of review,  4) "body_lengh" -- identifies the length of review, those five features. In my opinion, they are connected in a certain way, for example, the one with controversiality label may not in the stickied place. 

Therefore I have model those factors into a logistical regression model then use test data and cross-validation two methods to access the performance of the model and find the best parameters and its coefficients in this model predicting.



 - Datasets preparation 
 
I have tried two ways to decide on what kind of subsets this hypothesis needs.

  1. Datasets subsets: There are 476259744 rows in the 4-month datasets. Based on the similar distribution of "score" (see in(35) and in(40) in ipynb file), I took the sample set of 20% data (around 100 million) with the seed set to 329, keep all archived value columns.

  2. Filter dataset with True in the archived column -- makes sure this question is no longer changed. The stickied label may change for the review if the questions on Reddit is still available to add a new answer.
  
  In the end, I choose the #2 even though the volume of available datasets are much smaller. In my opinion, it is not reasonable to just force to keep the large datasets because it is a massive datasets project, without considering the goal of this project and the model. In real-world work, it is possible to handle massive datasets into small pieces by certain conditions. Hence, for supporting my model and theory behind this, I used the "filter" function to get meaningful data (210,000) instead of using the sample datasets.

------------------------------
### #5, Model

#### New dataframe
After preprocessing datasets (including feature engineering), I created a new dataframe only contains 5 columns (4 parameters + 1 label) will be used in the model.

The clean_reddit.printSchema() shows following

---------------------------

 (1) controversiality: string (nullable = true)
 
 (2) score_class: string (nullable = false)
 
 (3) subreddit: string (nullable = true)
 
 (4) body_length: integer (nullable = true)
 
 (5) stickied: string (nullable = true)
 
-----------------------------


#### Build pipeline model

1. Preparation
StringIndexer all categorical columns
OneHotEncoder all categorical index columns
VectorAssembler all feature columns into one vector column

 - Adding non-numeric data with indexer (Build StringIndexer stages)
 - Encodering all indexed columns (Build OneHotEncoder stages)
 - Vectorizing columns as feature (Build VectorAssembler stage)
 
2. Pipeline model

##### Pipeline fitting Method 1: 
- pipeline.fit()
- fit in with features and lables
  - final_columns = feature_columns + ['features', 'label']

##### Split Training and Test data 

Using random seed to split datasets into 70% training (48561158) and 30% test data (20805289), then fitted training datasets into the logistic model and make validation with test data.

Making the ROC Curve based on the logistic regression model.

##### Extra: Build cross-validation model

 - Parameter grid 
 - Building different parameter models
 - Making BinaryClassificationEvaluator
 - Fitting the Cross-validation model by training and validating the model with test data
 - Find Intercept and coefficients of the regression model using "bestmodel" function
 - Choosing Best parameters from the best model

##### PS: EXTRA Pipeline fitting Method:
combined all factors(categorials+ numericals)


## Results and Discussion
The logistical regression is 

In sample test set:

[ - Training set ROC: 0.9818533387934892
 - Test_SET (Area Under ROC): 0.9418670005002574 ]

In all datasets:

[  - Training set ROC: 0.9989146361911969
- Test_SET (Area Under ROC): 0.9534092467247536]


The Intercept: -5.309090585400705
coefficients: [ 0.08421218  0.18999762 -0.11647764 -0.13277351  0.15321921]

The best RegParam is:  0.0 
The best ElasticNetParam is: cv_model.bestModel._java_obj.getElasticNetParam()

-------------------
  
Result shows  that the logistic model performs well on predicting label "stickied", it accounts for 95% Area under ROC for test data. However, obviously, there is a slightly overfitting problem since a higher error rate in test datasets. The reason for the overfitting problem is highly likely in "subreddit" because there are 22871 different values in it. Therefore, this part will be future work if we want to solve this overfitting problem.
In the linear regression model for cross-validation, the best parameter is 0.0 among regParam, [0, 1, 2] and elasticNetParam, [0, 0.5] different parameter combinations. The Intercept and coefficients are -5.3 and  [ 0.08421218  0.18999762 -0.11647764 -0.13277351  0.15321921] respectively.




## Conlusion and Future work


Apart from the slightly overfitting problem, the project is still a heavy time-consuming work. That is because the "subreddit" contains 22871 different values and the 'body-length" is numerical instead of as a string label, even though only 210,000 rows are fitted into the model. It takes around 30 minutes to make the pipeline and built ROC, and hours to run the cross-validation model and prediction.

The technique used for textual analysis and prediction has evolved a long way from pure statistical methods, such as linear regression, logistic regression, towards advanced machine learning models, such as neural networks, which are regarded as the principal method of many Natural Language Processing research. Another idea for future work is using "tokenize" function for comments texts, such as vectorizing tf-idf or setting part of speech labels frequency matrix, instead of using the whole subreddit label. It might identify the stickied label and make the model more general without the overfitting problem. 






