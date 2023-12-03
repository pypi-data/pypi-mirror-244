import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.signal import savgol_coeffs
import matplotlib.pyplot as plt

def savitzky_golay(y, window_size, degree, x):
    half_size = window_size // 2
    order_range = range(-half_size, half_size + 1)
    coeffs = savgol_coeffs(window_size, degree, deriv=0, delta=1.0)

    smoothed = np.zeros(len(y))
    for i in range(len(y)):
        valid_indices = [(i + k) for k in order_range if 0 <= (i + k) < len(y)]
        valid_coeffs = [coeffs[k + half_size] for k in order_range if 0 <= (i + k) < len(y)]
        smoothed[i] = np.sum(valid_coeffs * y[valid_indices])

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='Noisy Data')
    plt.plot(x, smoothed, label='Filtered Data', color='red', linewidth=2)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.title('Savitzky-Golay Filtering')
    plt.grid(True)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

def listwise_deletion(data):
    cleaned_data = data[~np.isnan(data)]
    return cleaned_data

def linear_interpolation(data):
    for i in range(len(data)):
        if np.isnan(data[i]):
            left, right = i - 1, i + 1
            while np.isnan(data[left]) and left >= 0:
                left -= 1
            while np.isnan(data[right]) and right < len(data):
                right += 1
            data[i] = data[left] + (data[right] - data[left]) / (right - left) * (i - left)
    return data

def forward_fill(data):
    for i in range(len(data)):
        if np.isnan(data[i]):
            j = i + 1
            while np.isnan(data[j]) and j < len(data):
                j += 1
            if not np.isnan(data[j]):
                data[i] = data[j]
    return data

def backward_fill(data):
    for i in range(len(data) - 1, -1, -1):
        if np.isnan(data[i]):
            j = i - 1
            while np.isnan(data[j]) and j >= 0:
                j -= 1
            if not np.isnan(data[j]):
                data[i] = data[j]
    return data

def handle_missing_values(data, method='listwise_deletion'):
    if method == 'listwise_deletion':
        return listwise_deletion(data)
    elif method == 'linear_interpolation':
        return linear_interpolation(data)
    elif method == 'forward_fill':
        return forward_fill(data)
    elif method == 'backward_fill':
        return backward_fill(data)
    else:
        raise ValueError("Invalid method. Please choose from 'listwise_deletion', 'linear_interpolation', 'forward_fill', or 'backward_fill'.")

def missing_data_imputation(data):
    methods = ['listwise_deletion', 'linear_interpolation', 'forward_fill', 'backward_fill']
    plt.figure(figsize=(8, 6))

    # Plotting original data
    plt.plot(np.arange(len(data)), data, label='Original', color='black')

    # Plotting cleaned data for each method
    colors = plt.cm.rainbow(np.linspace(0, 1, len(methods)))
    for index, method in enumerate(methods):
        cleaned_data = handle_missing_values(data.copy(), method=method)
        plt.scatter(np.arange(len(cleaned_data)), cleaned_data, label=method.replace('_', ' ').capitalize(), alpha=0.6)
        plt.plot(np.arange(len(cleaned_data)), cleaned_data, linestyle='-', color=colors[index])  # Line connecting points

    plt.xlabel('Index')
    plt.ylabel('Data Value')
    plt.legend()
    plt.title('Missing Data Imputation')
    plt.show()

def summary_statistics(X):
    # Convert the list to a NumPy array
    X_array = np.array(X)
    
    # Calculate mean
    mean = np.mean(X_array)
    
    # Calculate standard deviation
    std_dev = np.std(X_array)
    
    # Calculate minimum and maximum
    min_val = np.min(X_array)
    max_val = np.max(X_array)
    
    # Get array details
    array_details = {
        'Shape': X_array.shape,
        'Data Type': X_array.dtype,
        'Sum': np.sum(X_array),
        'Median': np.median(X_array),
        'Variance': np.var(X_array)
    }
    
    # Print the summary statistics and array details
    print("Summary Statistics:")
    print("===================")
    print(f"Mean: {mean:.4f}")
    print(f"Standard Deviation: {std_dev:.4f}")
    print(f"Minimum: {min_val}")
    print(f"Maximum: {max_val}")
    
    print("\nArray Details:")
    print("===================")
    for key, value in array_details.items():
        print(f"{key}: {value}")

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def plots(x, y, plot_types):
    num_plots = len(plot_types)
    plt.figure(figsize=(5*num_plots, 4))

    for i, plot_type in enumerate(plot_types, start=1):
        plt.subplot(1, num_plots, i)
        
        if plot_type == 'scatter':
            plt.scatter(x, y)
            plt.title('Scatter Plot')
            plt.xlabel('X values')
            plt.ylabel('Y values')
        elif plot_type == 'histogram':
            sns.histplot(y, kde=True)
            plt.title('Histogram')
            plt.xlabel('Y values')
            plt.ylabel('Frequency')
        elif plot_type == 'qqplot':
            stats.probplot(y, dist="norm", plot=plt)
            plt.title('Q-Q Plot')
            plt.xlabel('Theoretical Quantiles')
            plt.ylabel('Ordered Values')
        elif plot_type == 'bar':
            plt.bar(x, y)
            plt.title('Bar Plot')
            plt.xlabel('X values')
            plt.ylabel('Y values')
        elif plot_type == 'line':
            plt.plot(x, y)
            plt.title('Line Plot')
            plt.xlabel('X values')
            plt.ylabel('Y values')
        # Add more conditions for other plot types if needed
        
    plt.tight_layout()
    plt.show()

import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import pandas as pd

# Define regression functions...
def sinusoidal(x, a, b, c, d):
    return a * np.sin(b * x + c) + d

def logarithmic(x, a, b):
    return a * np.log(b * x)

# Define additional regression functions...
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b):
    return a * np.exp(b * x)

def cubic(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def inverse(x, a, b):
    return a / (x + b)

def gaussian(x, a, b, c):
    return a * np.exp(-((x - b)**2) / (2 * c**2))

def power(x, a, b):
    return a * x**b

def s_curve(x, a, b, c):
    return a / (1 + np.exp(-b * (x - c)))

# Add more regression models...

def regression(x, y):
    models = [
        ('Linear Regression', sm.OLS),
        ('Polynomial Regression', PolynomialFeatures),
        ('Sinusoidal Regression', sinusoidal),
        ('Logarithmic Regression', logarithmic),
        ('Quadratic Regression', quadratic),
        ('Exponential Regression', exponential),
        ('Cubic Regression', cubic),
        ('Inverse Regression', inverse),
        ('Gaussian Regression', gaussian),
        ('Power Regression', power),
        ('S-Curve Regression', s_curve),
        ('Logistic Regression (Lasso)', Lasso),
        # Add more regression models here
    ]

    results = []

    for model_name, model_method in models:
        stats = {}
        if model_name == 'Linear Regression':
            X = sm.add_constant(x)  # Adding a constant for intercept
            model = sm.OLS(y, X).fit()
            y_pred = model.predict(X)
            stats['R-squared'] = r2_score(y, y_pred)
        elif model_name == 'Polynomial Regression':
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(x.reshape(-1, 1))
            model = sm.OLS(y, X_poly).fit()
            y_pred = model.predict(X_poly)
            stats['R-squared'] = r2_score(y, y_pred)
        # Add conditions for other regression types...
        
        elif model_name == 'Power Regression':
            popt, _ = curve_fit(power, x, y)
            y_pred = power(x, *popt)
            stats['R-squared'] = r2_score(y, y_pred)
        elif model_name == 'S-Curve Regression':
            popt, _ = curve_fit(s_curve, x, y)
            y_pred = s_curve(x, *popt)
            stats['R-squared'] = r2_score(y, y_pred)
        # Add conditions for other regression types...

        results.append(stats)

    results_df = pd.DataFrame(results, index=[model[0] for model in models])
    print(results_df)

    plt.figure(figsize=(15, 10))

    for i, (model_name, model_method) in enumerate(models, start=1):
        plt.subplot(3, 4, i)
        plt.scatter(x, y, label='Data')
        
        if model_name == 'Linear Regression':
            X = sm.add_constant(x)  # Adding a constant for intercept
            model = sm.OLS(y, X).fit()
            y_pred = model.predict(X)
            plt.plot(x, y_pred, color='red', label='Linear Fit')
        elif model_name == 'Polynomial Regression':
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(x.reshape(-1, 1))
            model = sm.OLS(y, X_poly).fit()
            y_pred = model.predict(X_poly)
            plt.plot(x, y_pred, color='green', label='Polynomial Fit')
        elif model_name == 'Sinusoidal Regression':
            popt, _ = curve_fit(sinusoidal, x, y)
            y_pred = sinusoidal(x, *popt)
            plt.plot(x, y_pred, color='blue', label='Sinusoidal Fit')
        elif model_name == 'Logarithmic Regression':
            popt, _ = curve_fit(logarithmic, x, y)
            y_pred = logarithmic(x, *popt)
            plt.plot(x, y_pred, color='orange', label='Logarithmic Fit')
        elif model_name == 'Quadratic Regression':
            popt, _ = curve_fit(quadratic, x, y)
            y_pred = quadratic(x, *popt)
            plt.plot(x, y_pred, color='purple', label='Quadratic Fit')
        elif model_name == 'Exponential Regression':
            popt, _ = curve_fit(exponential, x, y)
            y_pred = exponential(x, *popt)
            plt.plot(x, y_pred, color='brown', label='Exponential Fit')
        elif model_name == 'Cubic Regression':
            popt, _ = curve_fit(cubic, x, y)
            y_pred = cubic(x, *popt)
            plt.plot(x, y_pred, color='pink', label='Cubic Fit')
        elif model_name == 'Inverse Regression':
            popt, _ = curve_fit(inverse, x, y)
            y_pred = inverse(x, *popt)
            plt.plot(x, y_pred, color='gray', label='Inverse Fit')
        elif model_name == 'Gaussian Regression':
            popt, _ = curve_fit(gaussian, x, y)
            y_pred = gaussian(x, *popt)
            plt.plot(x, y_pred, color='cyan', label='Gaussian Fit')
        elif model_name == 'Power Regression':
            popt, _ = curve_fit(power, x, y)
            y_pred = power(x, *popt)
            plt.plot(x, y_pred, color='magenta', label='Power Fit')
        elif model_name == 'S-Curve Regression':
            popt, _ = curve_fit(s_curve, x, y)
            y_pred = s_curve(x, *popt)
            plt.plot(x, y_pred, color='lime', label='S-Curve Fit')
        elif model_name == 'Logistic Regression (Lasso)':
            lasso_model = Lasso()
            lasso_model.fit(x.reshape(-1, 1), y)
            y_pred = lasso_model.predict(x.reshape(-1, 1))
            plt.plot(x, y_pred, color='black', label='Lasso Fit')
            # Additional metrics can be displayed here
        # Add conditions for other regression types...
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(model_name)
        plt.legend()

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np

def residual_analysis(observed, predicted=None, predictor_variable=None):
    if predicted is not None and predictor_variable is not None:
        residuals = observed - predicted
        plt.scatter(predictor_variable, residuals)
        plt.xlabel('Predictor Variable')
        plt.ylabel('Residuals')
        plt.title('Residual Analysis')
        plt.axhline(y=0, color='r', linestyle='-')  # Adding a horizontal line at y=0 for reference
        plt.show()
    else:
        print("Predicted values or predictor variable not provided. Skipping residual analysis.")

def r_squared(observed, predicted):
    ss_res = np.sum((observed - predicted) ** 2)
    ss_tot = np.sum((observed - np.mean(observed)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return r2

def adjusted_r_squared(observed, predicted, n, k):
    r2 = r_squared(observed, predicted)
    adj_r2 = 1 - ((1 - r2) * (n - 1) / (n - k - 1))
    return adj_r2

def mean_squared_error(observed, predicted):
    mse = np.mean((observed - predicted) ** 2)
    return mse

def aic(n, mse, k):
    aic_value = 2 * k - 2 * np.log(mse) * n
    return aic_value

def bic(n, mse, k):
    bic_value = -2 * np.log(mse) * n + k * np.log(n)
    return bic_value

def model_analysis(observed, predicted=None, predictor_variable=None, n=None, k=None, plot_predicted=True):
    eval_metrics = {}
    
    if predicted is not None and plot_predicted and predictor_variable is not None:
        plt.scatter(observed, predicted)
        plt.xlabel('Observed')
        plt.ylabel('Predicted')
        plt.title('Predicted vs. Observed')
        plt.show()
    
    if predicted is not None and predictor_variable is not None:
        residual_analysis(observed, predicted, predictor_variable)
        eval_metrics['R-squared'] = r_squared(observed, predicted)
        eval_metrics['Adjusted R-squared'] = adjusted_r_squared(observed, predicted, n, k) if n is not None and k is not None else None
        eval_metrics['Mean Squared Error'] = mean_squared_error(observed, predicted)
    
    if n is not None and k is not None and predicted is not None:
        mse = mean_squared_error(observed, predicted)
        eval_metrics['Akaike Information Criterion'] = aic(n, mse, k)
        eval_metrics['Bayesian Information Criterion'] = bic(n, mse, k)
    
    return eval_metrics

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, stats

def optimize(func, x_data, y_data, guess_params):
    def ask_user_input(prompt, default=None):
        if default is not None:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        value = input(prompt)
        if value == '':
            return default
        if value == "-inf":
            return -np.inf
        if value == "inf":
            return np.inf
        return eval(value)

    lower_bounds_input = ask_user_input("Enter the lower bounds (optional): ", default=None)
    upper_bounds_input = ask_user_input("Enter the upper bounds (optional): ", default=None)
    maxfev = ask_user_input("Enter the number of function evaluations (optional): ", default=10000)

    lower_bounds = lower_bounds_input if lower_bounds_input is not None else -np.inf
    upper_bounds = upper_bounds_input if upper_bounds_input is not None else np.inf
    maxfev = int(maxfev) if maxfev is not None else 10000

    fitted_params, _ = optimize.curve_fit(func, x_data, y_data, guess_params, bounds=(lower_bounds, upper_bounds), maxfev=maxfev)
    y_pred = func(x_data, *fitted_params)

    residuals = y_data - y_pred
    sse = np.sum(residuals ** 2)
    rmse = np.sqrt(sse / len(x_data))
    r_squared = 1 - (sse / np.sum((y_data - np.mean(y_data)) ** 2))
    chi_square = np.sum((residuals / y_pred) ** 2)

    ks_statistic, ks_pvalue = stats.kstest(residuals, 'norm')
    ad_statistic, ad_critical_values, ad_significance_levels = stats.anderson(residuals, 'norm')

    print("Fitting results:")
    print("Parameters:", fitted_params)
    print("Number of data points:", len(x_data))
    print("Number of parameters:", len(fitted_params))
    print("SSE:", sse)
    print("RMSE:", rmse)
    print("R-squared:", r_squared)
    print("Chi-square:", chi_square)
    print("KS Test - Statistic:", ks_statistic)
    print("KS Test - p-value:", ks_pvalue)
    print("AD Test - Statistic:", ad_statistic)
    print("AD Test - Critical Values:", ad_critical_values)
    print("AD Test - Significance Levels:", ad_significance_levels)

    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label='Data')
    plt.plot(x_data, y_pred, label='Fit')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Data and Fitted Function')
    plt.show()

    return fitted_params