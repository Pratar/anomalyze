import numpy as np
from scipy.stats import pearsonr, spearmanr
from statsmodels.tsa.arima.model import ARIMA

class DynamicThreshold:
    def __init__(self, historical_data, context, seasonal_adjustment=False):
        self.historical_data = np.array(historical_data)
        self.context = context
        self.seasonal_adjustment = seasonal_adjustment

    def calculate_threshold(self):
        mean = np.mean(self.historical_data)
        std_dev = np.std(self.historical_data)
        threshold = mean + 2 * std_dev if self.context == 'normal' else mean + 3 * std_dev
        return threshold


class Filter:
    def __init__(self, correlation_threshold=0.8):
        self.correlation_threshold = correlation_threshold

    def filter_anomalies(self, data, correlation_matrix):
        filtered_indices = []
        if correlation_matrix.shape[0] < 2 or correlation_matrix.shape[1] < 2:
            return filtered_indices  # Пропуск фильтрации для матриц 1x1 или 1xN

        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                if correlation_matrix[i, j] >= self.correlation_threshold:
                    filtered_indices.append(i if data[i] < data[j] else j)
        return list(set(filtered_indices))

class CorrelationAnalysis:
    def __init__(self, data_i, data_j):
        self.data_i = np.array(data_i)
        self.data_j = np.array(data_j)

    def pearson_correlation(self):
        correlation, _ = pearsonr(self.data_i, self.data_j)
        return correlation

    def spearman_correlation(self):
        correlation, _ = spearmanr(self.data_i, self.data_j)
        return correlation

    def lagged_correlation(self, lag=1):
        if lag >= len(self.data_j):
            raise ValueError("Lag is greater than the length of the data.")
        lagged_j = np.roll(self.data_j, lag)
        correlation, _ = pearsonr(self.data_i[:-lag], lagged_j[:-lag])
        return correlation


class PredictionModel:
    def __init__(self, data, order=(1, 1, 1)):
        self.data = data
        self.model = ARIMA(data, order=order)

    def fit_model(self):
        self.model_fit = self.model.fit()

    def forecast(self, steps=1):
        return self.model_fit.forecast(steps=steps)


class MetricHierarchy:
    def __init__(self):
        self.metrics = {'critical': [], 'warning': [], 'info': []}

    def add_metric(self, name, level, data):
        if level in self.metrics:
            self.metrics[level].append({'name': name, 'data': data})

    def reclassify_metric(self, name, new_level):
        for level in self.metrics:
            for metric in self.metrics[level]:
                if metric['name'] == name:
                    self.metrics[level].remove(metric)
                    self.metrics[new_level].append(metric)
                    return


class AnomalyDetector:
    def __init__(self, data, context='normal', seasonal_adjustment=False):
        self.data = np.array(data)
        self.context = context
        self.seasonal_adjustment = seasonal_adjustment
        self.threshold_model = DynamicThreshold(self.data, context, seasonal_adjustment)

    def detect_anomalies(self):
        threshold = self.threshold_model.calculate_threshold()
        anomalies = np.where(self.data > threshold)[0]
        return anomalies


class FullAnomalyDetectionSystem:
    def __init__(self, data, metric_hierarchy, order=(1, 1, 1), correlation_threshold=0.8):
        self.data = np.array(data)
        self.metric_hierarchy = metric_hierarchy
        self.prediction_model = PredictionModel(data, order)
        self.filter = Filter(correlation_threshold)

    def process(self):
        # Step 1: Predict future data points
        self.prediction_model.fit_model()
        prediction = self.prediction_model.forecast(steps=1)

        # Step 2: Calculate correlation between metrics
        corr_analysis = []
        for i, metric_data_i in enumerate(self.metric_hierarchy.metrics['critical']):
            for j, metric_data_j in enumerate(self.metric_hierarchy.metrics['warning']):
                correlation = CorrelationAnalysis(metric_data_i['data'], metric_data_j['data']).pearson_correlation()
                corr_analysis.append((metric_data_i['name'], metric_data_j['name'], correlation))

        # Step 3: Filter anomalies based on correlation analysis
        metric_data = [metric['data'] for metric in self.metric_hierarchy.metrics['critical']]
        correlation_matrix = np.corrcoef(metric_data) if len(metric_data) > 1 else np.array([[1.0]])
        filtered_anomalies = self.filter.filter_anomalies(self.data, correlation_matrix)

        # Step 4: Detect anomalies for each metric using dynamic thresholds
        anomaly_detector = AnomalyDetector(self.data, seasonal_adjustment=True)
        anomalies = anomaly_detector.detect_anomalies()

        # Combine predictions, correlations, and anomalies into a result
        result = {
            'prediction': prediction,
            'correlation_analysis': corr_analysis,
            'filtered_anomalies': filtered_anomalies,
            'anomalies': anomalies
        }
        return result
