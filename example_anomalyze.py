import numpy as np

# Инициализация данных
data = np.random.random(100) * 50
metric_hierarchy = MetricHierarchy()
metric_hierarchy.add_metric('cpu_usage', 'critical', data)

# Запуск системы детекции
full_system = FullAnomalyDetectionSystem(data, metric_hierarchy)
results = full_system.process()

print("Прогнозирование:", results['prediction'])
print("Корреляционный анализ:", results['correlation_analysis'])
print("Отфильтрованные аномалии:", results['filtered_anomalies'])
print("Обнаруженные аномалии:", results['anomalies'])
