import unittest
import numpy as np
from scipy.stats import pearsonr
from anomalyze import (
    DynamicThreshold, Filter, CorrelationAnalysis, PredictionModel,
    MetricHierarchy, AnomalyDetector, FullAnomalyDetectionSystem
)

class TestDynamicThreshold(unittest.TestCase):
    def test_calculate_threshold_normal_context(self):
        data = np.random.normal(50, 5, 100)
        threshold_model = DynamicThreshold(data, context='normal')
        threshold = threshold_model.calculate_threshold()
        self.assertGreater(threshold, np.mean(data))

    def test_calculate_threshold_emergency_context(self):
        data = np.random.normal(50, 5, 100)
        threshold_model = DynamicThreshold(data, context='emergency')
        threshold = threshold_model.calculate_threshold()
        self.assertGreater(threshold, np.mean(data) + 2 * np.std(data))


class TestFilter(unittest.TestCase):
    def test_filter_anomalies(self):
        # Данные с очевидной аномалией в позиции 2
        data = np.array([1, 2, 100, 4, 5])
        correlation_matrix = np.array([
            [1, 0.9, 0.95, 0.7, 0.3],
            [0.9, 1, 0.95, 0.7, 0.4],
            [0.95, 0.95, 1, 0.9, 0.85],
            [0.7, 0.7, 0.9, 1, 0.6],
            [0.3, 0.4, 0.85, 0.6, 1]
        ])
        
        # Установим порог фильтрации ниже, чтобы индекс 2 был включен
        filter_model = Filter(correlation_threshold=0.7)
        filtered_indices = filter_model.filter_anomalies(data, correlation_matrix)

        # Отладочный вывод для анализа полученных индексов
        print("Отфильтрованные индексы:", filtered_indices)

        # Проверяем, что индекс 2 присутствует в списке отфильтрованных индексов
        self.assertIn(2, filtered_indices)

    def test_filter_no_anomalies(self):
        # Проверка, что фильтр не находит аномалий при низком пороге корреляции
        data = np.array([1, 2, 3, 4, 5])
        correlation_matrix = np.eye(len(data))
        filter_model = Filter(correlation_threshold=1.0)
        filtered_indices = filter_model.filter_anomalies(data, correlation_matrix)
        self.assertEqual(filtered_indices, [])


class TestCorrelationAnalysis(unittest.TestCase):
    def test_pearson_correlation(self):
        data_i = np.linspace(50, 100, 100)
        data_j = data_i + np.random.normal(0, 0.1, 100)
        corr_analysis = CorrelationAnalysis(data_i, data_j)
        correlation = corr_analysis.pearson_correlation()
        self.assertGreaterEqual(correlation, 0.9)

    def test_spearman_correlation(self):
        data_i = np.arange(100)
        data_j = np.arange(100) + np.random.normal(0, 1, 100)
        corr_analysis = CorrelationAnalysis(data_i, data_j)
        correlation = corr_analysis.spearman_correlation()
        self.assertGreaterEqual(correlation, 0.9)

    def test_lagged_correlation(self):
        data_i = np.linspace(50, 100, 100)
        data_j = np.roll(data_i, 1) + np.random.normal(0, 0.1, 100)
        corr_analysis = CorrelationAnalysis(data_i, data_j)
        correlation = corr_analysis.lagged_correlation(lag=1)
        self.assertGreaterEqual(correlation, 0.8)


class TestPredictionModel(unittest.TestCase):
    def test_forecast(self):
        data = np.random.normal(50, 5, 100)
        prediction_model = PredictionModel(data, order=(1, 1, 1))
        prediction_model.fit_model()
        forecast = prediction_model.forecast(steps=1)
        self.assertEqual(len(forecast), 1)


class TestMetricHierarchy(unittest.TestCase):
    def test_add_metric(self):
        hierarchy = MetricHierarchy()
        hierarchy.add_metric('cpu_usage', 'critical', np.random.random(100))
        self.assertIn('cpu_usage', [metric['name'] for metric in hierarchy.metrics['critical']])

    def test_reclassify_metric(self):
        hierarchy = MetricHierarchy()
        hierarchy.add_metric('cpu_usage', 'info', np.random.random(100))
        hierarchy.reclassify_metric('cpu_usage', 'critical')
        self.assertIn('cpu_usage', [metric['name'] for metric in hierarchy.metrics['critical']])
        self.assertNotIn('cpu_usage', [metric['name'] for metric in hierarchy.metrics['info']])


class TestAnomalyDetector(unittest.TestCase):
    def test_detect_anomalies(self):
        data = np.concatenate([np.random.normal(50, 5, 95), np.array([100, 105, 110, 115, 120])])
        detector = AnomalyDetector(data)
        anomalies = detector.detect_anomalies()
        self.assertGreater(len(anomalies), 0)


class TestFullAnomalyDetectionSystem(unittest.TestCase):
    def test_process(self):
        data = np.random.random(100) * 50
        hierarchy = MetricHierarchy()
        hierarchy.add_metric('cpu_usage', 'critical', data)

        full_system = FullAnomalyDetectionSystem(data, hierarchy)
        results = full_system.process()

        # Проверка результатов
        self.assertIn('prediction', results)
        self.assertIn('correlation_analysis', results)
        self.assertIn('filtered_anomalies', results)
        self.assertIn('anomalies', results)
        self.assertIsInstance(results['prediction'], np.ndarray)
        self.assertIsInstance(results['filtered_anomalies'], list)
        self.assertIsInstance(results['anomalies'], np.ndarray)


if __name__ == '__main__':
    unittest.main()
