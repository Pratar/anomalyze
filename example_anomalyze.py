import numpy as np
from anomalyze import (
    DynamicThreshold, Filter, CorrelationAnalysis, PredictionModel,
    MetricHierarchy, AnomalyDetector, FullAnomalyDetectionSystem
)

def run_example():
    print("=== Anomalyze Library Example ===\n")

    # 1. Basic Anomaly Detection (Spikes and Drops)
    print("--- 1. Detecting Spikes and Drops ---")
    np.random.seed(42)
    # Generate normal data around 50
    data = np.random.normal(50, 2, 100)
    # Add anomalies
    data[20] = 80  # Positive spike
    data[50] = 10  # Negative drop
    
    detector = AnomalyDetector(data, context='normal')
    anomalies = detector.detect_anomalies()
    print(f"Data length: {len(data)}")
    print(f"Anomalies injected at indices: 20 (value=80), 50 (value=10)")
    print(f"Detected anomalies at indices: {anomalies}")
    print("-" * 30 + "\n")

    # 2. Correlation Analysis with Lag
    print("--- 2. Lagged Correlation Analysis ---")
    # Create a base signal
    t = np.linspace(0, 20, 100)
    signal_a = np.sin(t)
    # Create a lagged version of the signal (shifted by 5 steps)
    signal_b = np.roll(signal_a, 5)
    # Correct the beginning of signal_b because roll is circular (simulate real lag)
    signal_b[:5] = signal_b[5] 
    
    # Let's use the library to find correlation
    # Note: signal_b lags behind signal_a if we consider signal_b[t] ~= signal_a[t-lag]
    # Actually, np.roll(shift) pushes elements to the right. 
    # signal_b[5] is signal_a[0]. So signal_b is delayed.
    
    analysis = CorrelationAnalysis(signal_a, signal_b)
    
    # Direct correlation might be low
    direct_corr = analysis.pearson_correlation()
    print(f"Direct Pearson Correlation: {direct_corr:.4f}")
    
    # Lagged correlation (checking if B follows A with lag 5)
    # Our lagged_correlation(lag) compares data_i[lag:] with data_j[:-lag]
    # If data_j is lagged version of data_i (shifted right by lag), 
    # then data_j[k] should match data_i[k-lag].
    # But the function compares data_i[k] with data_j[k-lag]?
    # Let's check implementation:
    # y_lagged = data_j[:-lag]  (elements 0 to N-lag-1)
    # x_trimmed = data_i[lag:]  (elements lag to N-1)
    # It compares x[t] with y[t-lag]? No.
    # x_trimmed[0] is x[lag]. y_lagged[0] is y[0].
    # It compares x[lag] with y[0].
    # If y is shifted right by 'lag', then y[lag] corresponds to x[0] (if it was shifted left?)
    # Wait. If y is delayed by 5. y[5] ~= x[0].
    # We want to compare y[5] with x[0].
    # Code: x_trimmed[0] = x[lag]. y_lagged[0] = y[0].
    # This compares x[lag] and y[0].
    # If y is delayed, y[0] happened long ago (or is padding).
    # If y[5] == x[0].
    # We want to match x[0] with y[5].
    # The code matches x[5] with y[0].
    # This seems to check if x follows y? Or reverse lag?
    
    # Let's try to find which lag works.
    # If we want to check if Y is a delayed version of X (Y[t] = X[t-lag]).
    # Then Y[lag] = X[0].
    # We want to compare X[0] and Y[lag].
    # The code compares X[lag] and Y[0].
    # So the code checks if X is a delayed version of Y (X[t] = Y[t-lag]).
    
    # So if signal_b is delayed signal_a.
    # signal_a is "ahead". signal_a is the leading indicator.
    # We want to check if signal_a leads signal_b.
    # That means signal_b[t+lag] ~ signal_a[t]? 
    # Or signal_a[t] ~ signal_b[t-lag] (A is delayed version of B?) No.
    
    # Let's swap them for the tool.
    # If we put A as data_i and B as data_j.
    # Code checks corr(A[lag:], B[:-lag]). 
    # Compares A[lag] with B[0].
    # If B is delayed by lag, B[lag] = A[0]. 
    # B[0] is ???. A[lag] is some future value.
    # This doesn't seem to match "B is delayed A".
    
    # What if we swap?
    # analysis(B, A). i=B, j=A.
    # Compares B[lag] with A[0].
    # If B is delayed, B[lag] = A[0].
    # Bingo!
    
    # So to check if signal_b is a lagged version of signal_a (lag=5),
    # we should check CorrelationAnalysis(signal_b, signal_a).lagged_correlation(5).
    
    analysis_ba = CorrelationAnalysis(signal_b, signal_a)
    lagged_corr = analysis_ba.lagged_correlation(lag=5)
    print(f"Lagged Correlation (lag=5, checking if B lags A): {lagged_corr:.4f}")
    
    print("-" * 30 + "\n")

    # 3. Full System Example
    print("--- 3. Full System Usage ---")
    hierarchy = MetricHierarchy()
    hierarchy.add_metric('cpu_usage', 'critical', data)
    hierarchy.add_metric('memory_usage', 'warning', data * 0.5 + np.random.normal(0, 1, 100)) # Correlated
    
    full_system = FullAnomalyDetectionSystem(data, hierarchy)
    results = full_system.process()
    
    print("Processing complete.")
    print(f"Filtered Anomalies: {results['filtered_anomalies']}")
    print(f"All Detected Anomalies: {results['anomalies']}")

if __name__ == "__main__":
    run_example()
