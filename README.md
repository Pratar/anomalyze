The theoretical foundation and justification for the model are provided in the document **anomalies-eng.pdf**. This document includes detailed explanations of the principles and methodologies underlying the anomaly detection system, offering a comprehensive understanding of its structural and functional components.

# Anomalyze

Anomalyze is a comprehensive anomaly detection system designed for real-time data analysis. This library provides dynamic thresholding, adaptive filtering, correlation analysis, time series forecasting, and metric hierarchy management to identify and analyze anomalies in complex data streams.

## Features
- **Dynamic Thresholding**: Set adaptive thresholds based on historical data and context.
- **Adaptive Filtering**: Minimize false positives with customizable filtering rules.
- **Correlation Analysis**: Identify relationships between metrics using Pearson, Spearman, and lagged correlation coefficients.
- **Time Series Forecasting**: Predict future data points to preemptively identify anomalies.
- **Metric Hierarchy Management**: Organize metrics by criticality (e.g., critical, warning, info) with dynamic reclassification.

## Installation

Install the package using `pip`:
```bash
pip install git+https://github.com/Pratar/anomalyze.git
```

Or install from a local clone:
```bash
git clone https://github.com/Pratar/anomalyze.git
cd anomalyze
pip install .
```

Usage:
```python
import numpy as np
from anomalyze import FullAnomalyDetectionSystem, MetricHierarchy

# Generate sample data
data = np.random.random(100) * 50

# Create a metric hierarchy and add a critical metric
hierarchy = MetricHierarchy()
hierarchy.add_metric('cpu_usage', 'critical', data)

# Initialize the full anomaly detection system
full_system = FullAnomalyDetectionSystem(data, hierarchy)

# Process the data
results = full_system.process()

# Display results
print("Prediction:", results['prediction'])
print("Correlation Analysis:", results['correlation_analysis'])
print("Filtered Anomalies:", results['filtered_anomalies'])
print("Detected Anomalies:", results['anomalies'])
```

Components

1. DynamicThreshold

Calculates adaptive thresholds based on historical data and context, useful for monitoring metrics in changing conditions.

2. Filter

Minimizes false positives by filtering anomalies based on correlation thresholds and other customizable rules.

3. CorrelationAnalysis

Performs linear and nonlinear correlation analysis, including lagged correlation, to identify metric dependencies.

4. PredictionModel

Uses ARIMA to forecast future data points for predictive anomaly detection.

5. MetricHierarchy

Manages metrics by criticality, with support for dynamic reclassification based on changing conditions.

6. FullAnomalyDetectionSystem

Combines all components to provide a complete anomaly detection system that identifies, filters, and predicts anomalies.

Tests

To run the test suite, use the following command:
```bash
python -m unittest discover tests
```

Requirements

	•	numpy>=1.18.2
	•	scipy>=1.5.2
	•	statsmodels>=0.12.2

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contributing

Contributions are welcome! Please open an issue or submit a pull request.

Contact

	•	Author: Mikhail Nazarenko
	•	Email:  mikhail.nazarenko@gmail.com
	•	GitHub: Pratar
