# A failed attempt (so far) to predict Github Pull Request latency. 
The **ideal** subject of interest of this study would be the relationship between the morphology of the diff changes and the degree of complexity experienced by reviewers. The **actual** subject is the **relationship between the diff changes and the merge latency**, as we neither have data survey about reviews complexity nor intention to annoy reviewers (so far) to gather it. Because of this limitation (among others) **poor results** were found. 

### Dataset
[scrapper](scrapper.py) fetch all pull requests from three well-known js repositories. There are about 11K rows of data regarding PR stats (like `diff changes`,  `latency`,  `commits` and more).

### Exploratory data analysis
[exploratory_data_analysis notebook](exploratory_data_analysis.ipynb) makes both simple descriptive and comparative analysis. It also removes outliers by applying a set of constraints to keep only those PRs which have been merged in an active repository and present a nonextreme diff changes. Regarding correlations following **features are the most correlated ones: `additions` (0.11), `labels count`(0.13) and `commits count` (0.12)**
    
### XGBoost results
[XGBoost_approach notebook](XGBoost_approach.ipynb) performs a regression and a classification analysis, in both cases with poor results: the former shows an `RMSE` of 7.5 hours per latency prediction when the mean of PR latency is about 8.3 hours, the latter show an accuracy of 60% for a binomial category (PR latency below/above average).