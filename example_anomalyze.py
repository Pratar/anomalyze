import numpy as np
from anomalyze import (
    DynamicThreshold, Filter, CorrelationAnalysis, PredictionModel,
    MetricHierarchy, AnomalyDetector, FullAnomalyDetectionSystem
)

# Инициализация данных для различных метрик
np.random.seed(42)  # Для воспроизводимости
cpu_usage_data = np.random.normal(60, 10, 1000)  # CPU usage в процентах
memory_usage_data = np.random.normal(70, 15, 1000)  # Memory usage в процентах
disk_io_data = np.random.normal(100, 20, 1000)  # Данные о скорости ввода-вывода диска
network_traffic_data = np.random.normal(300, 50, 1000)  # Данные о сетевом трафике
latency_data = np.random.normal(200, 30, 1000)  # Задержка отклика в миллисекундах
delay_data = np.random.normal(50, 10, 1000)  # Общая задержка в миллисекундах

# Инициализация иерархии метрик
metric_hierarchy = MetricHierarchy()
metric_hierarchy.add_metric('cpu_usage', 'critical', cpu_usage_data)
metric_hierarchy.add_metric('memory_usage', 'warning', memory_usage_data)
metric_hierarchy.add_metric('disk_io', 'info', disk_io_data)
metric_hierarchy.add_metric('network_traffic', 'warning', network_traffic_data)
metric_hierarchy.add_metric('latency', 'critical', latency_data)
metric_hierarchy.add_metric('delay', 'warning', delay_data)

# Запуск системы детекции аномалий
full_system = FullAnomalyDetectionSystem(latency_data, metric_hierarchy)
results = full_system.process()

# Вывод результатов
print("=== Результаты анализа ===")
print("\nПрогнозирование:")
print("Следующее прогнозируемое значение метрики Latency:", results['prediction'])

print("\nКорреляционный анализ:")
for analysis in results['correlation_analysis']:
    metric_i, metric_j, correlation = analysis
    print(f"Корреляция между {metric_i} и {metric_j}: {correlation:.2f}")

print("\nОтфильтрованные аномалии:")
if results['filtered_anomalies']:
    print("Индексы отфильтрованных аномалий:", results['filtered_anomalies'])
else:
    print("Отфильтрованных аномалий не обнаружено.")

print("\nОбнаруженные аномалии:")
if results['anomalies'].size > 0:
    print("Индексы обнаруженных аномалий:", results['anomalies'])
else:
    print("Аномалий не обнаружено.")
