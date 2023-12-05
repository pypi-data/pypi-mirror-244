import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import scipy.stats as stats
from pandas import DataFrame
import pandas as pd
from sklearn import preprocessing
import statsmodels.api as sm

##########################################################################################
####################################### SOME VALUES ######################################
##########################################################################################

def calculate_pvalue(residuals):
    """
    Calculate the p-value for the residuals.
    :param residuals: the residuals (list)
    :return: the p-value (float)

    :Example:
    >>> residuals = list of residuals
    >>> p_value = calculate_pvalue(residuals)
    """
    t_dist = abs(np.mean(residuals)) / (np.std(residuals, ddof=1) / np.sqrt(len(residuals)))
    p_value = (1 - t.cdf(t_dist, len(residuals) - 1, loc=0, scale=1)) * 2
    
    return p_value


##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
###################################### ERROR METRICS #####################################
##########################################################################################

def make_length_equal_to_compare(realVals, forecastVals):
    """
    Make the length of the real and forecast values equal.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the real and forecast values with equal length (list, list)    

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> realVals, forecastVals = make_length_equal_to_compare(data, forecasts)
    """
    no_None = forecastVals.count(None)

    realVals = list(np.array(realVals)[no_None:])
    forecastVals = list((np.array(forecastVals)[no_None:])[:len(realVals)])

    return realVals, forecastVals



def MSE(realVals, forecastVals):
    """
    Compute the mean squared error between the real and forecast values.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the mean squared error (float)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> error = MSE(data, forecasts)
    """
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)

    return np.mean((np.array(realVals) - np.array(forecastVals))**2)



def RMSE(realVals, forecastVals):
    """
    Compute the root mean squared error between the real and forecast values.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the root mean squared error (float)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> error = RMSE(data, forecasts)
    """ 
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)

    return np.sqrt(MSE(realVals, forecastVals))



def MAE(realVals, forecastVals):
    """
    Compute the mean absolute error between the real and forecast values.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the mean absolute error (float)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> error = MAE(data, forecasts)
    """
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)

    return np.mean(np.abs(np.array(realVals) - np.array(forecastVals)))



def MAPE(realVals, forecastVals):
    """
    Compute the mean absolute percentage error between the real and forecast values.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the mean absolute percentage error (float)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> error = MAPE(data, forecasts)
    """
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)

    return np.mean(np.abs((np.array(realVals) - np.array(forecastVals))) / np.array(realVals)) * 100



def calculate_Error(error_method, realVals, forecastVals):
    """
    Compute the error between the real and forecast values.
    :param error_method: the error method to use (function)
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the error (float)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> error = calculate_Error(MSE, data, forecasts)
    """
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)
    
    return error_method(realVals, forecastVals)



def get_all_residuals(realVals, forecastVals):
    """
    Get the errors for the forecasts.
    :param realVals: the real values (list)
    :param forecastVals: the forecast values (list)
    :return: the errors (list)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> residuals = get_all_residuals(data, forecasts)
    """
    realVals, forecastVals = make_length_equal_to_compare(realVals, forecastVals)

    return list(np.array(realVals) - np.array(forecastVals))



def print_error_summary(data, forecasts, **error_method):
    """
    Print the error summary for the forecasts.
    :param data: the time series
    :param forecasts: the forecasts
    :param error_method: the error methods to use (function)

    :Example:
    >>> data = list of data values
    >>> forecasts = list of forecasts
    >>> print_error_summary(data, forecasts, MSE=MSE, RMSE=RMSE, MAE=MAE, MAPE=MAPE)
    """

    print('Error Summary')
    print('-------------')
    for method, error in error_method.items():
        print(f'{method}: {error(data, forecasts):.4f}')



def print_resids_summary(residuals):
    """
    Print the summary of the residuals.
    :param residuals: the residuals (list)
    """
    residuals_mean = np.mean(residuals)
    residuals_sd = np.std(residuals, ddof=1)
    no_residuals = len(residuals)

    p_value = calculate_pvalue(residuals)
    width = (residuals_sd / np.sqrt(no_residuals)) * t.ppf(0.975, no_residuals - 1, loc=0, scale=1)
    
    print(f'Mean of Residual:   {residuals_mean:.4f}')
    print(f'S.D. of Residual:   {residuals_sd:.4f}')
    print(f'Half Width :        {width:.4f}   (degree of freedom = {no_residuals - 1}, Confidence Level = 0.95)')
    print(f'p-value :           {p_value:.4f}')



##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
################################ PLOTTING RESIDUALS (ERRORS) #############################
##########################################################################################


def plot_resids(residuals, figsize=(8, 4), x_label='Time', y_label='Residuals', title='Residuals for the Forecast'):
    """
    Plot the residuals.
    :param residuals: the residuals (list)
    """

    residuals_mean = np.mean(residuals)
    no_residuals = len(residuals)
    mean_array = [residuals_mean] * no_residuals

    plt.figure(figsize=figsize)
    plt.plot(residuals, label='Residual', color='b')
    plt.plot(mean_array, label='Mean', linestyle='--', color='r')
    plt.title(title, loc = 'center')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()



def plot_normalized_resids(residuals, figsize=(6, 4)):
    """
    Plot the normalized residuals.
    :param residuals: the residuals (list)
    """

    residual_array = np.array(residuals)

    mean = residual_array.mean()
    std = residual_array.std()

    normalized_resids = DataFrame((residual_array - np.array(mean)) / std)

    plt.figure(figsize=figsize)
    plt.plot(normalized_resids, label='Normalized Residual', color='b')
    plt.title("Normalized Residuals for the Forecast", loc = 'center')
    plt.xlabel("Time")
    plt.ylabel("Normalized Residuals")
    plt.legend()
    plt.show()



def plot_histogram_of_normalized_resids(residuals, figsize=(6, 4)):
    """
    Plot the histogram of the normalized residuals.
    :param residuals: the residuals (list)
    """

    residual_array = np.array(residuals)
    
    mean = residual_array.mean()
    std = residual_array.std()

    normalized_resids = DataFrame((residual_array - np.array(mean)) / std)

    fig = plt.figure(figsize=figsize)
    normalized_resids.plot(kind='hist', density=True, color='b', ec='w', ax=fig.gca(), legend=False)
    normalized_resids.plot(kind='kde', color='r', ax=fig.gca(), legend=False)
    plt.title("Histogram Plus Estimated Density", loc = 'center')
    plt.ylabel("Density")
    plt.xlabel("Residuals")
    plt.show()



def plot_normal_of_normalized_resids(residuals, figsize=(6, 4)):
    """
    Plot the normal Q-Q plot of the normalized residuals.
    :param residuals: the residuals (list)
    """

    residual_array = np.array(residuals)

    rng = (0, 1)
    scaler = preprocessing.MinMaxScaler(feature_range=(rng[0], rng[1]))
    normed = scaler.fit_transform(residual_array.reshape(-1, 1)) 
    residuals_norm = [round(i[0], 2) for i in normed]

    plt.figure(figsize=figsize)
    stats.probplot(residuals_norm, dist="norm", plot=plt)
    plt.ylabel("Residuals")
    plt.title("Normal Q-Q plot", loc='center')
    plt.show()



def show_all_normalized_resids_plots(residuals):
    """
    Show all the normalized residuals plots.
    :param residuals: the residuals (list)
    """

    # creating dataframe and then standardizing and normalizing
    residual_array = np.array(residuals)

    mean = residual_array.mean()
    std = residual_array.std()

    normalized_resids = DataFrame((residual_array - np.array(mean)) / std)

    rng = (0, 1)
    scaler = preprocessing.MinMaxScaler(feature_range=(rng[0], rng[1]))
    normed = scaler.fit_transform(residual_array.reshape(-1, 1))
    residuals_norm = [round(i[0], 2) for i in normed]

    
    # designing a 2 by 2 plot 
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.set_figheight(11)
    fig.set_figwidth(15)

    # top left subplot
    ax1.plot(normalized_resids, color='b')
    ax1.set_title("Normalized Residuals", loc = 'center')
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Residuals")

    # top right subplot
    ax2.set_xlim(-4, 4)
    ax2.set_title("Histogram Plus Estimated Density", loc='center')
    normalized_resids.plot(kind='hist', density=True, color='b', ec='w', ax=ax2)
    normalized_resids.plot(kind='kde', ax=ax2, color='r') 
    ax2.set_xlabel("Residuals")
    ax2.get_legend().remove()
    
    # bottom left subplot
    stats.probplot(residuals_norm, dist="norm", plot=ax3)
    ax3.set_title("Normal Q-Q plot", loc='center')
    ax3.set_ylabel("Residuals")
    
    
    # bottom right subplot
    max_lag = len(residuals)
    if max_lag > 30:
        max_lag = 31

    sm.graphics.tsa.plot_acf(normalized_resids, color='b', ax=ax4, lags=np.arange(1, max_lag))
    ax4.set_title("Autocorrelation", loc='center')
    ax4.set_ylabel("Correlations")
    ax4.set_xlabel("Lags")

    plt.show()


##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
##################################### FORECAST METHODS ###################################
##########################################################################################

def naive_forecast(data):
    """
    Forecast the next value in the time series using the naive method.
    :param data: time series (list)
    :return: naive forecast (float or integer or None)

    :Example:
    >>> naive_forecast([1, 2, 3, 4, 5])
    """
    if len(data) == 0:
        return None
    
    return data[-1]



def seasonal_forecast(data, k):
    """
    Forecast the next value in the time series using the single value seasonal method.
    :param data: time series (list)
    :param k: length of the season (integer)
    :return: single value seasonal forecast (float or integer or None)

    :Example:
    >>> seasonal_forecast([1, 2, 3, 4, 5], 3)
    >>> seasonal_forecast([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    """
    if len(data) < k:
        return None
    
    return data[-k]



def MA_forecast(data, N, step_ahead=1):
    """
    Forecast the next value in a time series using a moving average.
    :param data: the time series (list)
    :param n: the number of previous values to use in the moving average (integer)
    :param step_ahead: the number of steps ahead to forecast (integer)
    :return: the forecast (float or integer or None)

    :Example:
    >>> MA_forecast([1, 2, 3, 4, 5], 3)
    >>> MA_forecast([1, 2, 3, 4, 5], 3, 2)
    """

    if step_ahead < 1:
        raise Exception('step_ahead must be greater than 1')
    
    elif (type(step_ahead) != int):
        raise Exception('step_ahead must be an integer')

    elif len(data) < N + (step_ahead - 1):
        return None

    elif step_ahead != 1: 
        return np.mean((data[:-(step_ahead - 1)])[-(N):])

    else:
        return np.mean(data[-(N):])



def ES_forecast(data, alpha, step_ahead=1):
    """
    Forecast the next value in a time series using an exponential smoothing.
    :param data: the time series (list)
    :param alpha: the smoothing parameter (float)
    :param step_ahead: the number of steps ahead to forecast (integer)
    :return: the forecast (float or integer or None)

    :Example:
    >>> ES_forecast([1, 2, 3, 4, 5], 0.5, 1)
    >>> ES_forecast([1, 2, 3, 4, 5], 0.5, 2)
    """

    if (step_ahead < 1):
        raise Exception('step_ahead must be greater than 1')
    
    elif (type(step_ahead) != int):
        raise Exception('step_ahead must be an integer')

    elif len(data) == 0:
        raise ValueError('data must not be empty')
    
    elif len(data) < step_ahead:
        return None

    elif len(data) == step_ahead:
        return data[-step_ahead]

    return alpha * data[-step_ahead] + (1 - alpha) * ES_forecast(data[:-1], alpha, step_ahead)



def ES_forecast_for_all_data(data, alpha, h=1):

    """
    This function generates an exponential smoothing forecast for all data,
    calling itself recursively with the h steps ahead.
    :param data: data (list)
    :param alpha: smoothing parameter (float)
    :param h: number of steps ahead (int)
    :return: ES forecast (list)

    :Example:
    >>> data = list of data values
    >>> ES_forecast_for_all_data(data, 0.5, recursive_step)
    """

    y_hat = [0] * len(data)

    y_hat[0:h] = data[0:h]

    for i in range(h, len(data)):
        y_hat[i] = alpha * data[i - h] + (1 - alpha) * y_hat[i - h]

    y_hat[0:h] = [None] * (h)

    return y_hat



def make_forecast(data, forecast_method, **kwargs):
    """
    Create a forecast for the next value in the time series.
    :param data: the time series (list)
    :param forecast_method: the forecasting method to use (function)
    :param kwargs: the keyword arguments for the forecasting method (parameters for the forecasting method)
    :return: the forecast (float or integer or None)

    :Example:
    >>> data = list of data values
    >>> forecast = make_forecast(data, naive_forecast)
    >>> forecast = make_forecast(data, seasonal_forecast, k=4)
    >>> forecast = make_forecast(data, MA_forecast, N=4)
    >>> forecast = make_forecast(data, ES_forecast, alpha=0.5)
    """

    try :
        return forecast_method(data, **kwargs)
    except:
        raise Exception('Forecast method failed')
    


def make_forecast_for_all_data(data, forecast_method, **kwargs):
    """
    Create a forecast for each value in the time series.
    :param data: the time series (list)
    :param forecast_method: the forecasting method to use (function)
    :param kwargs: the keyword arguments for the forecasting method (parameters for the forecasting method)
    :return: the forecast list (list)

    :Example:
    >>> data = list of data values
    >>> forecasts = make_forecast_for_all_data(data, naive_forecast)
    >>> forecasts = make_forecast_for_all_data(data, seasonal_forecast, k=4)
    >>> forecasts = make_forecast_for_all_data(data, MA_forecast, N=4)
    """
    forecasts = [None]
    
    for i in range(len(data)):
        forecasts.append(make_forecast(data[:i+1], forecast_method, **kwargs))

    return list(forecasts)


def compare_forecasts(data, forecasts, **error_metrics):
    """
    This function takes in a list of data, a dictionary of forecasts, and
    a dictionary of error metrics. It returns a dataframe with the error
    metrics for each forecast.
    :param data: list of data values (list)
    :param forecasts: dictionary of forecasts (dictionary)
    :param error_metrics: dictionary of error metrics (dictionary)
    :return: dataframe of error metrics (pandas dataframe)

    :Example:
    >>> data = list of data values
    >>> forecasts = {
    ...     'naive': naive_forecast(data),
    ...     'seasonal': seasonal_forecast(data, k),
    ...     'MA': MA_forecast(data, N),
    ...     'ES': ES_forecast(data, alpha)
    ... }
    >>> compare_forecasts(data, forecasts, MAE=mean_absolute_error, RMSE=root_mean_squared_error)
    """

    if len(forecasts) == 0:
        raise ValueError("No forecast methods were passed to the function.")
        
    if len(error_metrics) == 0:
        raise ValueError("No error metrics were passed to the function.")
    

    results = {}

    for error_name, error_metric in error_metrics.items():
        results[error_name] = []
        for forecast in forecasts.values():
            error = error_metric(data, forecast)
            results[error_name].append(error)

    pd.options.display.float_format = '{:.2f}'.format

    df_results = pd.DataFrame(results, index=forecasts.keys())
    df_results
    
    return df_results



##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
#################################### FORECAST PLOTTING ###################################
##########################################################################################



def plot_forecasts(data, horizon, forecasts, time_step=1,
                    figsize=(12, 5), title='Forecast and Data', xlabel=None, ylabel=None):
    """
    Plot the forecasts for the time series.
    :param data: the time series (list)
    :param horizon: the time horizon (list)
    :param forecasts: the forecasts (list)
    :param time_step: the step size for the time axis (integer)

    :Example:
    >>> data = list of data values
    >>> horizon = list of time values
    >>> forecasts = list of forecast values
    >>> plot_forecasts(data, horizon, forecasts)
    >>> plot_forecasts(data, horizon, forecasts, time_step=2)
    """
    
    number_of_dots = len(horizon)

    plt.figure(figsize=figsize)
    plt.xticks(np.arange(min(horizon), max(horizon)+1, time_step))
    plt.grid()
    plt.plot(horizon, data[:number_of_dots], label='data')
    plt.plot(horizon, forecasts[:number_of_dots], label='forecast')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()



def plot_forecasts_predictIntervals(data, horizon, forecasts, error_value, percent=0.90, time_step=1, 
                                    figsize=(12, 5), title='Forecast and Data with Prediction Intervals', xlabel=None, ylabel=None):
    """
    Plot the forecasts for the time series.
    :param data: the time series (list)
    :param horizon: the time horizon (list)
    :param forecasts: the forecasts (list)
    :param error_function: the error function to calculate the error of the forecasts (function)
    :param percent: the percentage of the prediction interval (float)
    :param time_step: the step size for the time axis (integer)

    :Example:
    >>> data = list of data values
    >>> horizon = list of time values
    >>> forecasts = list of forecast values
    >>> error_value = the error value for the forecasts (float)
    >>> percent = the percentage of the interval (0.90, 0.95, 0.99)
    >>> time_step = the step size for the time axis (1, 2, 3, 4, 5, 6, 12)
    >>> plot_forecasts(data, horizon, forecasts, error_function, percent, time_step)
    """
    
    no_values = len(horizon)

    a = (1 - percent) / 2
    zval = abs(stats.norm.ppf(a))
    forecasts_upper_bounds = forecasts + zval * error_value
    forecasts_lower_bounds = forecasts - zval * error_value

    plt.figure(figsize=figsize)
    plt.xticks(np.arange(min(horizon), max(horizon)+1, time_step))
    plt.grid()
    plt.plot(horizon, data[:no_values], label='data')
    plt.plot(horizon, forecasts[:no_values], label='forecast')
    plt.fill_between(horizon, forecasts_lower_bounds[:no_values], forecasts_upper_bounds[:no_values], color='b', alpha=.1, label='confidence interval')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()



def plot_autocorrelation(values, no_lags=30, figsize=(6, 4)):
    """
    Plot the autocorrelation of the values.
    :param values: the values (list)
    :param no_lags: the number of lags to plot (int)

    :Example:
    >>> data = list of data values
    >>> plot_autocorrelation(data , no_lags=10)
    >>> residuals = list of residuals
    >>> plot_autocorrelation(residuals)
    """
    
    values_array = np.array(values)
    normalized_values = values_array - np.array(values_array.mean()) / values_array.std()

    max_lag = len(values)
    if max_lag > 30:
        max_lag = 31

    if no_lags < max_lag:
        max_lag = no_lags + 1

    plt.figure(figsize=figsize)
    sm.graphics.tsa.plot_acf(normalized_values, color='b', ax=plt.gca(), lags=np.arange(1, max_lag))
    plt.title("Autocorrelation", loc='center')
    plt.ylabel("Correlations")
    plt.xlabel("Lags")
    plt.show()



def plot_partial_autocorrelation(values, no_lags=30, figsize=(6, 4)):
    """
    Plot the autocorrelation of the values.
    :param values: the values to plot (list)
    :param no_lags: the number of lags to plot (int)

    :Example:
    >>> data = list of data values
    >>> plot_autocorrelation(data , no_lags=10)
    >>> residuals = list of residuals
    >>> plot_autocorrelation(residuals)
    """
    
    values_array = np.array(values)
    normalized_values = values_array - np.array(values_array.mean()) / values_array.std()

    max_lag = len(values)
    if max_lag > 10:
        max_lag = 11

    if no_lags < max_lag:
        max_lag = no_lags + 1

    plt.figure(figsize=figsize)
    sm.graphics.tsa.plot_pacf(normalized_values, color='b', ax=plt.gca(), lags=np.arange(1, max_lag), method='ywm')
    plt.title("Partial-Autocorrelation", loc='center')
    plt.ylabel("Correlations")
    plt.xlabel("Lags")
    plt.show()



def plot_PACF_ACF_together(values, no_lags=30, figsize=(13, 4)):
    """
    Plot the autocorrelation and partial autocorrelation of the values.
    :param values: the values to plot (list)
    :param no_lags: the number of lags to plot (int)

    :Example:
    >>> data = list of data values
    >>> plot_autocorrelation(data , no_lags=10)
    >>> residuals = list of residuals
    >>> plot_autocorrelation(residuals)
    """
    
    values_array = np.array(values)
    normalized_values = values_array - np.array(values_array.mean()) / values_array.std()

    max_lag = len(values)
    if max_lag > 30:
        max_lag = 31

    if no_lags < max_lag:
        max_lag = no_lags + 1

    plt.figure(figsize=figsize) 
    plt.subplot(1, 2, 1)
    sm.graphics.tsa.plot_acf(normalized_values, color='b', ax=plt.gca(), lags=np.arange(1, max_lag))
    plt.title("Autocorrelation", loc='center')
    plt.ylabel("Correlations")
    plt.xlabel("Lags")

    plt.subplot(1, 2, 2)
    sm.graphics.tsa.plot_pacf(normalized_values, color='b', ax=plt.gca(), lags=np.arange(1, max_lag), method='ywm')
    plt.title("Partial-Autocorrelation", loc='center')
    plt.ylabel("Correlations")
    plt.xlabel("Lags")
    plt.show()
    


##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
################################### DATA TRANSFORMATIONS #################################
##########################################################################################


def take_log_of_series(series):
    """
    This function takes the log transform of a series and returns the log transformed series.
    :param series: series (list)
    :return: log transformed series (list)

    :Example:
    >>> take_log_of_series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    """

    series_array = np.array(series)

    log_series = np.log(series_array)

    return list(log_series)



def take_diff_of_series(series):
    """
    This function takes the difference of a series and returns the difference series.
    :param series: series (list)
    :return: series that is the difference of the input series (list)

    :Example:
    >>> take_diff_of_series([1, 2, 3, 4, 5])
    """

    series_array = np.array(series)

    diff_series = np.diff(series_array)

    return list(diff_series)



def deseasonalize_series(series, season_length):
    """
    This function takes the seaonal difference of a series and returns the deseasonalized series.
    :param series: series (list)
    :param season_length: length of the season (int)
    :return: deseasonalized series (list)

    :Example:
    >>> deseasonalize_series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
    """

    deseasonalized_series = []

    for i in range(len(series)):
        if i < season_length:
            deseasonalized_series.append(None)
        else:
            deseasonalized_series.append(series[i] - series[i - season_length])

    return deseasonalized_series



##########################################################################################
##########################################################################################
##########################################################################################


##########################################################################################
###################################### GENERATE SERIES ###################################
##########################################################################################

def generate_AR_process(c, phi, errors, length_of_series, init_values=None):
    """
    Generate an AR(p) time series with coefficients c and phi, and errors e.

    Parameters:
    c (float): The constant term in the autoregressive model equation.
    phi (list): The list of p autoregressive coefficients.
    errors (list): The list of errors, assumed to be white noise with mean 0 and constant variance.
    length_of_series (int): The desired length of the time series.
    init_values (list): The list of initial values for the time series. If None, the first p values will be set to 0.

    Returns:
    list: A list of length length_of_series containing the generated time series.
    """

    p = len(phi)

    # Set initial values of the time series
    if init_values is None:
        init_values = [0] * p
    else:
        assert len(init_values) == p, "Number of initial values must match the order of the autoregressive model."

    # Generate the time series
    AR_process = init_values.copy()
    
    for i in range(p, length_of_series + p):
        y = c
        for j in range(p):
            y += phi[j] * AR_process[i-j-1]
        
        y += errors[i-p]
        
        AR_process.append(y)

    return AR_process[p:]


def generate_MA_process(c, theta, errors, length_of_series, init_errors=None):
    """
    Generate an MA(q) time series with mean C, coefficients theta, and errors e.

    Parameters:
    mu (float): The mean of the time series.
    theta (list): The list of q moving average coefficients.
    errors (list): The list of errors, assumed to be white noise with mean 0 and constant variance.
    length_of_series (int): The desired length of the time series.
    init_errors (list): The list of initial errors for the time series. If None, the first q values will be set to 0.

    Returns:
    list: A list of length length_of_series containing the generated time series.
    """

    q = len(theta)

    # Set initial values of the time series
    if init_errors is None:
        init_errors = [0] * q
    else:
        assert len(init_errors) == q, "Number of initial errors must match the order of the moving average model."

    # Generate the time series
    MA_process = []
    
    errors = init_errors + errors
    
    for i in range(q, length_of_series + q):
        y = c
        for j in range(q):
            y += theta[j] * errors[i-j-1]

        y += errors[i]
        MA_process.append(y)
        
    return MA_process

def generate_ARMA_process(c, phi, theta, errors, length_of_series, init_values=None, init_errors=None):
    """
    Generate an ARMA(p,q) time series with mean C, autoregressive coefficients phi, moving average coefficients theta,
    and errors e.

    Parameters:
    c (float): The mean of the time series.
    phi (list): The list of p autoregressive coefficients.
    theta (list): The list of q moving average coefficients.
    errors (list): The list of errors, assumed to be white noise with mean 0 and constant variance.
    length_of_series (int): The desired length of the time series.
    init_values (list): The list of initial values for the time series. If None, the first p values will be set to 0.
    init_errors (list): The list of initial errors for the time series. If None, the first q values will be set to 0.

    Returns:
    list: A list of length length_of_series containing the generated time series.
    """

    p = len(phi)
    q = len(theta)

    # Set initial values of the time series and errors
    if init_values is None:
        init_values = [0] * p
    else:
        assert len(init_values) == p, "Number of initial values must match the order of the autoregressive model."
        
    if init_errors is None:
        init_errors = [0] * q
    else:
        assert len(init_errors) == q, "Number of initial errors must match the order of the moving average model."

    # Generate the time series
    ARMA_process = init_values.copy()

    errors = init_errors + errors

    for i in range(p, length_of_series + p):
        y = c
        for j in range(p):
            y += phi[j] * ARMA_process[i-j-1]

        for j in range(q):
            y += theta[j] * errors[i-j-1]

        y += errors[i]

        ARMA_process.append(y)

    return ARMA_process[p:]

