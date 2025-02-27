# -*- coding: utf-8 -*-
"""2407751_HarshanaBhandari.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13RnNyrSD8f9E5uLNNGYIzN_LCcV2i1kC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectFromModel

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df=pd.read_csv("/content/drive/MyDrive/Final Assignment/updated_pollution_dataset.csv")

df.head()

num_rows,num_columns=df.shape
print("The total number of rows present in the dataset: ",num_rows)
print("The total number of columns present in the dataset: ",num_columns)

df.info()

total_null_values = df.isnull().sum().sum()
print("Total number of missing values: ",total_null_values)

df.isnull().sum()

#fill the null values for numerical columns
df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
df['Humidity'] = df['Humidity'].fillna(df['Humidity'].mean())
df['PM2.5'] = df['PM2.5'].fillna(df['PM2.5'].mean())
df['PM10'] = df['PM10'].fillna(df['PM10'].mean())
df['NO2'] = df['NO2'].fillna(df['NO2'].mean())
df['SO2'] = df['SO2'].fillna(df['SO2'].mean())
df['CO'] = df['CO'].fillna(df['CO'].mean())
df['Proximity_to_Industrial_Areas']=df['Proximity_to_Industrial_Areas'].fillna(df['Proximity_to_Industrial_Areas'].mean())

missing= df.isnull().sum().sum()
print("Missing value after data cleaning:", missing)

df.duplicated().sum()

#for categorical column
print("Categorical columns:")
df.select_dtypes(exclude=['number'])

# for numerical column
print("Numeric columns:")
df.select_dtypes(include=['number'])

#display summary statistics of the dataset
df.describe()

# Count occurrences of each Air Quality category
air_quality_counts = df["Air Quality"].value_counts()

# Print the counts
print(air_quality_counts)

import matplotlib.pyplot as plt
import seaborn as sns

# Plot the count of each Air Quality category
plt.figure(figsize=(8, 5))
sns.barplot(x=air_quality_counts.index, y=air_quality_counts.values, palette="viridis")
plt.title("Air Quality Category Count")
plt.xlabel("Air Quality Categories")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

"""This bar chart displays the count of different air quality categories. The"Good" category has the highest count, followed by "Moderate," "Poor," and "Hazardous" in decreasing order"""

# Selecting only numeric columns for correlation calculation
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Compute the correlation matrix
correlation_matrix = numeric_df.corr()

# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

"""This heatmap visualizes the correlation between different air quality and environmental features.
Strong positive correlations between PM2.5 and PM10 (0.97) and NO2 and CO (0.71) indicate they tend to increase together.
Negative correlations, such as Proximity to Industrial Areas and CO (-0.71) and Proximity to Industrial Areas and NO2 (-0.61), suggest that locations near industrial areas have higher pollution levels.
Other moderate correlations exist among features like Temperature, Humidity, and SO2.
This heatmap helps identify relationships that can be useful for predictive modeling or environmental analysis.
"""

# Set figure size
plt.figure(figsize=(15, 10))

# Create box plots for each numeric feature grouped by Air Quality
for i, feature in enumerate(numeric_df, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(x=df["Air Quality"], y=df[feature], palette="viridis")
    plt.title(f"{feature} by Air Quality")
    plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()
plt.show()

# Set figure size
plt.figure(figsize=(15, 10))

# Plot histograms for each numeric feature
for i, feature in enumerate(numeric_df, 1):
    plt.subplot(3, 3, i)
    plt.hist(df[feature].dropna(), bins=30, color='purple', alpha=0.7, edgecolor='black')
    plt.title(f"Histogram of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")

# Adjust layout
plt.tight_layout()
plt.show()

"""This collection of histograms visualizes the distribution of various environmental and air quality parameters.
Temperature, Humidity, NO2, and SO2 exhibit a roughly normal distribution.
PM2.5 and PM10 are right-skewed, indicating a higher frequency of lower values with occasional extreme pollution levels.
CO shows a multimodal distribution, suggesting different pollution sources or regions with distinct air quality levels.
Proximity to Industrial Areas has a bimodal pattern, indicating clustered data points.
Population Density is approximately normal but slightly skewed.
These distributions help in understanding data spread, outliers, and potential preprocessing needs for modeling.
"""

#  Example: Scatter plot between PM2.5 and AQI
plt.figure(figsize=(10, 6))
plt.scatter(df['PM2.5'], df['Air Quality'], color='blue', alpha=0.5)

# Adding labels and title
plt.xlabel('PM2.5 (µg/m³)')
plt.ylabel('Air Quality')
plt.title('Scatter Plot: PM2.5 vs AQ')

# Show the plot
plt.show()

"""This scatter plot shows how air quality ratings (Poor, Hazardous, Good, or Moderate) relate to PM2.5 pollution levels. PM2.5 measures tiny air particles in micrograms per cubic meter (μg/m³). The horizontal bands show that specific PM2.5 ranges correspond to each air quality category, with lower PM2.5 levels generally indicating better air quality. Most measurements cluster at lower PM2.5 levels, though some extreme cases reach up to 300 μg/m³."""

#  Example: Scatter plot between PM2.5 and AQI
plt.figure(figsize=(10, 6))
plt.scatter(df['SO2'], df['Air Quality'], color='blue', alpha=0.5)

# Adding labels and title
plt.xlabel('SO2')
plt.ylabel('Air Quality')
plt.title('Scatter Plot: SO2 vs AQ')

# Show the plot
plt.show()

"""This scatter plot shows how air quality ratings relate to SO2 (sulfur dioxide) levels. Similar to the PM2.5 plot, it shows distinct horizontal bands for each air quality category (Poor, Hazardous, Good, and Moderate), with each band corresponding to specific SO2 concentration ranges. The SO2 measurements range from 0 to about 40 units, and like the previous graph, there's a clear categorization system where different SO2 levels determine the air quality rating.

Build a Model from Stratch
"""

#drop target variable in order to define the feature matrix
X = df.drop(columns=['Air Quality'],axis=1)
#define target variable
y = df['Air Quality']
import numpy as np
def softmax(z):
  exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
  return exp_z / np.sum(exp_z, axis=1, keepdims=True)

import numpy as np
def test_softmax():

# Test input
  test_cases = [
  (np.array([[0, 0, 0]]), "All zeros"),
  (np.array([[1, 2, 3]]), "Simple case"),
  (np.array([[1000, 1000, 1000]]), "Large identical values"),
               (np.array([[-1000, -1000, -1000]]), "Small identical values"),
  (np.array([[1, 0, -1]]), "Mixed positive and negative")]
  for i, (z, description) in enumerate(test_cases):
    print(f"Test {i + 1}: {description}")
    result = softmax(z)
# Check that probabilities sum to 1
    assert np.allclose(result.sum(axis=1), 1), f"Failed: Probabilities do not sum to 1 in {description}"
# Check non-negativity
    assert np.all(result >= 0), f"Failed: Negative probabilities in {description}"
    print("Passed.")
print("All tests passed for softmax function.")
test_softmax()

def loss_softmax(y_true, y_pred):

  return -np.sum(y_true * np.log(y_pred + 1e-10)) # Add epsilon to prevent log(0)

def test_loss_softmax():

# Test Case 1: Perfect prediction
  y_true = np.array([0, 1, 0]) # True label (one-hot encoded)
  y_pred = np.array([0.1, 0.8, 0.1]) # Predicted probabilities
  expected_loss = -np.log(0.8) # Expected loss for perfect prediction
  assert np.isclose(loss_softmax(y_true, y_pred), expected_loss), "Test Case 1 Failed"
# Test Case 2: Incorrect prediction
  y_true = np.array([1, 0, 0]) # True label (one-hot encoded)
  y_pred = np.array([0.3, 0.4, 0.3]) # Predicted probabilities
  expected_loss = -np.log(0.3) # Expected loss for incorrect prediction
  assert np.isclose(loss_softmax(y_true, y_pred), expected_loss), "Test Case 2 Failed"
# Test Case 3: Edge case with near-zero probability
  y_true = np.array([0, 1, 0]) # True label (one-hot encoded)
  y_pred = np.array([0.01, 0.98, 0.01]) # Predicted probabilities
  expected_loss = -np.log(0.98) # Expected loss for edge case
  assert np.isclose(loss_softmax(y_true, y_pred), expected_loss), "Test Case 3 Failed"
  print("All test cases passed!")
# Run the test
test_loss_softmax()

# Cost Function for Softmax (Average Loss)
import numpy as np
def cost_softmax(X, y, W, b):
  n, d = X.shape
  z = np.dot(X, W) + b
  y_pred = softmax(z)
  return -np.sum(y * np.log(y_pred + 1e-10)) / n

def test_cost_softmax():
  # Test Case 1: Small dataset with perfect predictions
  X = np.array([[1, 2], [2, 3], [3, 4]]) # Feature matrix (n=3, d=2)
  y = np.array([[1, 0], [0, 1], [1, 0]]) # True labels (n=3, c=2, one-hot encoded)
  W = np.array([[1, -1], [-1, 1]]) # Weight matrix (d=2, c=2)
  b = np.array([0, 0]) # Bias vector (c=2)
  z = np.dot(X, W) + b
  y_pred = softmax(z) # Predicted probabilities
  expected_cost = -np.sum(y * np.log(y_pred + 1e-10)) / X.shape[0] # Compute expected cost
  assert np.isclose(cost_softmax(X, y, W, b), expected_cost), "Test Case 1 Failed"
  # Test Case 2: All-zero weights and bias
  X = np.array([[1, 0], [0, 1], [1, 1]]) # Feature matrix (n=3, d=2)
  y = np.array([[1, 0], [0, 1], [1, 0]]) # True labels (n=3, c=2, one-hot encoded)
  W = np.zeros((2, 2)) # Zero weight matrix
  b = np.zeros(2) # Zero bias vector
  z = np.dot(X, W) + b
  y_pred = softmax(z) # Predicted probabilities (uniform distribution)
  expected_cost = -np.sum(y * np.log(y_pred + 1e-10)) / X.shape[0] # Compute expected cost
  assert np.isclose(cost_softmax(X, y, W, b), expected_cost), "Test Case 2 Failed"
  print("All test cases passed!")
# Run the test
test_cost_softmax()

import numpy as np
def compute_gradient_softmax(X, y, W, b):
  """
  Compute the gradients of the cost function with respect to weights and biases.
  Parameters:
  X (numpy.ndarray): Feature matrix of shape (n, d).
  y (numpy.ndarray): True labels (one-hot encoded) of shape (n, c).
  W (numpy.ndarray): Weight matrix of shape (d, c).
  b (numpy.ndarray): Bias vector of shape (c,).
  Returns:
  tuple: Gradients with respect to weights (d, c) and biases (c,).
  """
  n, d = X.shape
  z = np.dot(X, W) + b
  y_pred = softmax(z)
  grad_W = np.dot(X.T, (y_pred - y)) / n
  grad_b = np.sum(y_pred - y, axis=0) / n
  return grad_W, grad_b

# Gradient Descent
def gradient_descent_softmax(X, y, W, b, alpha, n_iter, show_cost=False):

  cost_history = []
  for i in range(n_iter):
    grad_W, grad_b = compute_gradient_softmax(X, y, W, b)
    W -= alpha * grad_W
    b -= alpha * grad_b
    cost = cost_softmax(X, y, W, b)
    cost_history.append(cost)
    if show_cost and (i % 100 == 0 or i == n_iter - 1):
      print(f"Iteration {i}: Cost = {cost:.6f}")
  return W, b, cost_history

def predict_softmax(X, W, b):
  z = np.dot(X, W) + b
  y_pred = softmax(z)
  return np.argmax(y_pred, axis=1)

def test_predict_softmax():
# Generate synthetic data for testing
  np.random.seed(0)
  n, d, c = 10, 5, 3 # 10 samples, 5 features, 3 classes
  X = np.random.rand(n, d)
  W = np.random.rand(d, c)
  b = np.random.rand(c)
  # Compute the predictions using the function
  predictions = predict_softmax(X, W, b)
  # Check the shape of the output
  assert predictions.shape == (n,), f"Shape mismatch: expected {(n,)}, got {predictions.shape}"
  # Verify that all predicted labels are within the range of class indices
  assert np.all(predictions >= 0) and np.all(predictions < c), (
  f"Predictions out of range: expected 0 to {c-1}, got {predictions}"
  )
  # Check that the predicted labels are integers
  assert np.issubdtype(predictions.dtype, np.integer), f"Predictions are not integers: {predictions.dtype}"
  print("All tests passed for predict_softmax!")
# Run the test
test_predict_softmax()

# Evaluation Function
def evaluate_classification(y_true, y_pred):
  """
  Evaluate the classification performance using confusion matrix, precision, recall, and F1-score.
  Parameters:
  y_true (numpy.ndarray): True class labels of shape (n,).
  y_pred (numpy.ndarray): Predicted class labels of shape (n,).
  Returns:
  tuple: Confusion matrix, precision, recall, and F1-score.
  """
  from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
  cm = confusion_matrix(y_true, y_pred)
  precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
  recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
  f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
  return cm, precision, recall, f1

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Convert y to NumPy array before encoding
y_array = y.to_numpy().reshape(-1, 1)  # Ensure y is a 2D array

# One-hot encode y
encoder = OneHotEncoder(sparse_output=False)
y_encoded = encoder.fit_transform(y_array)

class_labels = encoder.categories_[0]  # Get class labels

# Split using the original y (before encoding) for stratification
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_array)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# Assertions to check the shape of X_train_scaled and X_test_scaled
assert X_train_scaled.shape == (X_train.shape[0], X_train.shape[1]), f"X_train_scaled shape mismatch: {X_train_scaled.shape}"
assert X_test_scaled.shape == (X_test.shape[0], X_test.shape[1]), f"X_test_scaled shape mismatch: {X_test_scaled.shape}"
print("Shape assertions passed!")
print("y_train shape:", y_train.shape)

W = np.zeros((X_train_scaled.shape[1], y_train.shape[1]))  # Shape: (n_features, n_classes)
b = 0.0
alpha = 0.1
n_iter = 1000
print("\nTraining Softmax Regression Model:")
W, b, cost_history = gradient_descent_softmax(X_train_scaled, y_train, W, b, alpha, n_iter, show_cost=True)

# Test model
y_train_pred = predict_softmax(X_train_scaled, W, b)
y_test_pred = predict_softmax(X_test_scaled, W, b)
# Evaluate train and test performance
train_cost = cost_softmax(X_train_scaled, y_train, W, b)
test_cost = cost_softmax(X_test_scaled, y_test, W, b)
print(f"\nTrain Loss (Cost): {train_cost:.4f}")
print(f"Test Loss (Cost): {test_cost:.4f}")

# Accuracy on test data
test_accuracy = np.mean(y_test_pred == np.argmax(y_test, axis=1)) * 100

print(f"\nTest Accuracy: {test_accuracy:.2f}%")

# Evaluation
confusion_matrix, precision, recall, f1_score = evaluate_classification(np.argmax(y_test, axis=1), y_test_pred)

print(f"\nConfusion Matrix:\n{confusion_matrix}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1_score:.2f}")

"""Build a primary model"""

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#drop target variable in order to define the feature matrix
X = df.drop(columns=['Air Quality'],axis=1)
#define target variable
y = df['Air Quality']

#split the dataset into train and test (70% test and 30% train)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#initialize the decision tree classifier
clf = DecisionTreeClassifier(random_state = 42)

#fit the classifier into training data
clf.fit(X_train, y_train)

#predict on test data
y_pred = clf.predict(X_test)

#predict on train data
y_train_pred = clf.predict(X_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#calculate accuracy of decision tree classifier on test set
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy is {accuracy*100:.2f}")

#calculate accuracy of decision tree classifier on train set
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Train Accuracy is {train_accuracy*100:.2f}")

#calculate classification report on test set
class_report = classification_report(y_test, y_pred)
print("Test Classification Report \n",class_report)

#calculate confusion matrix on test set
conf_matrix = confusion_matrix(y_test, y_pred)
print("Test Confusion Matrix \n",conf_matrix)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd

# Assuming you have your dataset loaded into a DataFrame called df
# X = df.drop(columns=['target_column'])  # Replace with your feature columns
# y = df['target_column']  # Replace with your target column

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize logistic regression with increased max_iter and a different solver
log_regression = LogisticRegression(max_iter=2000, random_state=42, solver='saga')  # You can also try 'liblinear'

# Fit the logistic regression into the training data
log_regression.fit(X_train_scaled, y_train)

log_regression_y_pred = log_regression.predict(X_test_scaled)

# Prediction on training data using scaled features
log_regression_y_train_pred = log_regression.predict(X_train_scaled)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Calculate accuracy of logistic regression on test set
log_regression_accuracy = accuracy_score(y_test, log_regression_y_pred)
print(f"Test Accuracy is {log_regression_accuracy * 100:.2f}%")

# Calculate accuracy of logistic regression on train set
log_regression_train_accuracy = accuracy_score(y_train, log_regression_y_train_pred)
print(f"Train Accuracy is {log_regression_train_accuracy * 100:.2f}%")

# Calculate classification report on test set
log_regression_class_report = classification_report(y_test, log_regression_y_pred)
print("Test Classification Report:\n", log_regression_class_report)

# Calculate confusion matrix on test set
log_regression_conf_matrix = confusion_matrix(y_test, log_regression_y_pred)
print("Test Confusion Matrix:\n", log_regression_conf_matrix)

"""Decision Tree Classifier performed better in the dataset as the accuracy on test set is 91.2 and the accuracy on train set is 100."""



from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

# Define the parameters for tuning
param_grid_dt = {
    'max_depth': [None, 10, 20, 30, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 5],
    'max_features': ['sqrt', 'log2', None],  # Corrected to valid options
    'criterion': ['gini', 'entropy']
}

# Initialize the decision tree classifier
dt_model = DecisionTreeClassifier(random_state=42)

# Initialize Stratified K-Folds for cross-validation
cv = StratifiedKFold(n_splits=5)

# Initialize RandomizedSearchCV
random_search_dt = RandomizedSearchCV(estimator=dt_model, param_distributions=param_grid_dt,
                                      n_iter=20, cv=cv, scoring='accuracy', random_state=42, n_jobs=-1)

# Fit the RandomizedSearchCV into the training set
random_search_dt.fit(X_train, y_train)

# Get the best hyperparameters
best_params_dt = random_search_dt.best_params_
print("Best Hyperparameters for Decision Tree:", best_params_dt)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
import numpy as np

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Define logistic regression model
lr_model = LogisticRegression()

# Define the parameters for tuning
param_grid_lr = {
    'C': np.logspace(-4, 4, 10),  # Wider range of C values
    'penalty': ['l1', 'l2'],  # Include both 'l1' and 'l2' penalties
    'solver': ['liblinear', 'saga'],  # Include 'saga' for 'l1' penalty
    'max_iter': [1000, 2000]  # Increased iteration limits
}

# Initialize RandomizedSearchCV for Logistic Regression
random_search_lr = RandomizedSearchCV(estimator=lr_model, param_distributions=param_grid_lr,n_iter=20, cv=5, scoring='accuracy', random_state=42, n_jobs=-1)

# Fit the RandomizedSearchCV into the training set
random_search_lr.fit(X_train_scaled, y_train)

# Get the best hyperparameters
best_params_lr = random_search_lr.best_params_
print("Best Hyperparameters for Logistic Regression:", best_params_lr)

from sklearn.feature_selection import SelectFromModel
#initialize the decision tree classifier
clf = DecisionTreeClassifier(random_state=42)

#initialize SFM
sfm_clf = SelectFromModel(clf)

#fit SFM into training data
sfm_clf.fit(X_train, y_train)

#get selected features
selected_feature_indices_clf = np.where(sfm_clf.get_support())[0]
selected_feature_names_clf = X.columns[selected_feature_indices_clf]
print("Selected Features for Decision Tree:", selected_feature_names_clf)

#initialize the logistic regression
log_regression = LogisticRegression(random_state=42)

#initialize SFM
sfm_log_regression = SelectFromModel(log_regression)

#fit SFM into training data
sfm_log_regression.fit(X_train, y_train)

#get selected features
selected_feature_indices_log_regression = np.where(sfm_log_regression.get_support())[0]
selected_feature_names_log_regression = X.columns[selected_feature_indices_log_regression]
print("Selected Features for Logistic Regression:", selected_feature_names_log_regression)

#best hyperparameters for decision tree classifier
best_params_dt = {'min_samples_split': 2, 'min_samples_leaf': 2, 'max_features': None, 'max_depth': 10, 'criterion': 'entropy'}

#initialize the decision tree classifier with the best hyperparameters
final_decision_tree = DecisionTreeClassifier(**best_params_dt)

#selected features for decision tree classifier
selected_features = ['CO', 'Proximity_to_Industrial_Areas']
X_train_selected = X_train.loc[:, selected_features]
X_test_selected = X_test.loc[:, selected_features]

#fit decision tree model on the selected features
final_decision_tree.fit(X_train_selected, y_train)

#calculate the final accuracy
final_decision_tree_accuracy = final_decision_tree.score(X_test_selected, y_test)
print(f"Final Decision Tree Accuracy: {final_decision_tree_accuracy*100:.2f}")

#best hyperparameters for logistic regression
best_params_lr = {'solver': 'saga', 'penalty': 'l1', 'max_iter': 2000, 'C': 166.81005372000558}

#initialize logistic regression with the best hyperparameters
final_logistic_regression = LogisticRegression(**best_params_lr)

#selected features for logistic regression
lr_selected_features = ['SO2', 'Proximity_to_Industrial_Areas']
X_train_selected_lr = X_train.loc[:, lr_selected_features]
X_test_selected_lr = X_test.loc[:, lr_selected_features]

#fit logistic regression model on the selected features
final_logistic_regression.fit(X_train_selected_lr, y_train)

#calculate the final accuracy
final_logistic_regression_accuracy = final_logistic_regression.score(X_test_selected_lr, y_test)
print(f"Final Logistic Regression Accuracy: {final_logistic_regression_accuracy*100:.2f}")

"""Conclusion: <br>
    During the primary model building, the accuracy of decision tree classifier on test set was 91.2. After hyperparameter optimization and feature selection, the accuracy decreased to 90.20.  The accuracy of logistic regression was 84.3 in the primary model and decreased to 76.2 in  final model.
"""