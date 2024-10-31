The theoretical foundation and justification for the model are provided in the document **anomalies-eng.pdf**. This document includes detailed explanations of the principles and methodologies underlying the anomaly detection system, offering a comprehensive understanding of its structural and functional components.

# Anomalyze

Anomalyze is a comprehensive anomaly detection system designed for real-time data analysis. Anomalyze provides dynamic thresholding, adaptive filtering, correlation analysis, time series forecasting, and metric hierarchy management to identify and analyze anomalies in complex data streams.

## Features
- **Dynamic Thresholding**: Set adaptive thresholds based on historical data and context.
- **Adaptive Filtering**: Minimize false positives with customizable filtering rules.
- **Correlation Analysis**: Identify relationships between metrics using Pearson, Spearman, and lagged correlation coefficients.
- **Time Series Forecasting**: Predict future data points to preemptively identify anomalies.
- **Metric Hierarchy Management**: Organize metrics by criticality (e.g., critical, warning, info) with dynamic reclassification.

## Comparison with seasonal-esd-anomaly-detection (SESD)

This section provides a comparison between **Anomalyze** and **seasonal-esd-anomaly-detection** (SESD) in terms of anomaly detection approach, data processing flexibility, threshold settings, and anomaly detection accuracy. Both libraries offer time series analysis capabilities, but they differ significantly in methodology and feature sets.

### 1. **Anomaly Detection Method**

| Feature                                | This Anomalyze                                     | seasonal-esd-anomaly-detection (SESD)           |
|----------------------------------------|--------------------------------------------------|-------------------------------------------------|
| **Anomaly Detection**                  | Dynamic thresholds based on history and context  | Seasonal Hybrid ESD with fixed thresholds       |
| **Correlation Analysis Support**       | Yes                                              | No                                              |
| **Forecasting Capabilities**           | Yes, using ARIMA model                           | No                                              |
| **False Positive Filtering**           | Yes, via dynamic thresholds                      | No, thresholds are fixed                        |
| **Metric Hierarchy**                   | Supported with critical, warning, and info levels| Not available                                   |

### 2. **Analysis Approach and Configuration Flexibility**

- **Anomalyze** uses dynamic thresholds that adapt based on the context (e.g., normal or emergency conditions). This helps detect anomalies while accounting for the current state of the system, minimizing false positives.
- **SESD** relies on the **Seasonal Hybrid ESD** method for identifying anomalies in data with seasonal components. This approach focuses on detecting anomalies within predictable patterns (e.g., seasonal peaks or troughs) using fixed thresholds.

### 3. **Configuration Flexibility and Adaptability**

- **Anomalyze** offers flexible settings for thresholds, contextual parameters (e.g., time of day, day of the week), and a metric hierarchy to prioritize metrics based on importance. This configuration provides greater flexibility in responding to various types of anomalies.
- **SESD** is oriented towards scenarios where data has clear seasonal patterns with minimal threshold adjustment requirements. However, this approach limits adaptability under changing conditions.

### 4. **Forecasting Support**

- **Anomalyze** includes prediction capabilities using **ARIMA** time series models, which allows forecasting metric values and identifying potential anomalies before they occur. This approach enables proactive anomaly detection.
- **SESD** does not support forecasting, which makes it less suited for anomaly prevention and more for retrospective detection.

### 5. **False Positive Filtering**

- **Anomalyze** supports false positive filtering through correlation analysis and dynamic threshold adjustment, reducing redundant alerts and ensuring the detection of meaningful anomalies.
- **SESD** lacks built-in mechanisms for filtering false positives, which can result in numerous redundant alerts, especially when seasonal patterns are unstable.

### Summary Evaluation

- **Anomalyze** provides a comprehensive approach to anomaly detection, focusing on adaptability and configuration flexibility. It is better suited for systems with changing conditions where reducing false positives and forecasting are crucial.
- **seasonal-esd-anomaly-detection (SESD)** is a more specialized tool suitable for data with stable seasonal patterns. It can be effective for straightforward scenarios where system and seasonal patterns are stable and do not require dynamic adjustments.

### Recommendations

- For applications requiring precise threshold settings, forecasting, and correlation analysis, this Anomalyze is preferable.
- For analyzing stable seasonal data with minimal configuration needs, **SESD** may be beneficial, especially if simplicity and ease of setup are essential.

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
