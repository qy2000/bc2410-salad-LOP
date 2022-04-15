# Making salads great again!

Optimisation of Salad Stop's business model in order to help improve their workflows

### 1. Overview

Descriptive Analytics: Visualisation and formulation of business problem

1. Relationship between complicated menus and purchase probability

2. Trends of time-dependent demand of ingredient

Predictive Analytics: Data modelling and forecasting

1. Predict purchase probabilities given Salad Stop's menu size

2. Forecast future demand of ingredients

Prescriptve Analytics: Optimisation 

1. Linear Optimisation - shorten menu choices provided by Salad Stop with customized constraints

2. Stochastic Optimisation - optimise the amount of ingredients to import in the following day/week/month

Proof of Concept solution

- Web application with a proper UI serving our optimisation models for end users 

- Install all relevant libraries before running commands

  ```
  cd poc
  flask run 
  ```
  
- `/` home directory for linear model

- `/stochastic` directory for stochastic model

- Demonstration WIP

### 2. Development using Git Branching

This is to prevent conflicts when we are pulling/pushing code. Finalised model/code will be merged into master later on.

- git branch YOUR_NAME

- git checkout YOUR_NAME

  - all uncommitted changes will remain in your git workspace

- git add .

- git commit -m "COMMIT MESSAGE"

- git push origin YOUR_NAME

### 3. Dev Notes

1. NotImplementedError: Cannot convert a symbolic Tensor (lstm_2/strided_slice:0) to a numpy array

    - This is a result of conflicting numpy versions (RSOME requires the numpy version to be 1.16 where as the LSTM model requires numpy version to be 1.18

    - Fix: Solved by modifying tensorflow/python/framework/ops.py as seen [here](https://localcoder.org/notimplementederror-cannot-convert-a-symbolic-tensor-lstm-2-strided-slice0-t)

