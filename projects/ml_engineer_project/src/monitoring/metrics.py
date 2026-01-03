"""
Model Monitoring Module
Tracks model performance and data drift
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
from datetime import datetime
from scipy.stats import ks_2samp
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelMonitor:
    """
    Monitors model performance and data drift
    """
    
    def __init__(self, reference_data: pd.DataFrame = None):
        """
        Initialize monitor
        
        Args:
            reference_data: Training data used as reference
        """
        self.reference_data = reference_data
        self.performance_log = []
        self.drift_log = []
        
    def log_prediction(self, prediction: Dict[str, Any]):
        """
        Log a prediction for monitoring
        
        Args:
            prediction: Prediction details
        """
        prediction['timestamp'] = datetime.now().isoformat()
        self.performance_log.append(prediction)
        
    def calculate_drift(self, current_data: pd.DataFrame,
                       feature: str,
                       method: str = 'ks') -> float:
        """
        Calculate data drift for a specific feature
        
        Args:
            current_data: Current production data
            feature: Feature name to check
            method: Drift detection method ('ks', 'psi')
            
        Returns:
            Drift score
        """
        if self.reference_data is None:
            logger.warning("No reference data available")
            return 0.0
        
        if feature not in self.reference_data.columns or feature not in current_data.columns:
            logger.warning(f"Feature {feature} not found")
            return 0.0
        
        reference_values = self.reference_data[feature].dropna()
        current_values = current_data[feature].dropna()
        
        if method == 'ks':
            # Kolmogorov-Smirnov test
            statistic, p_value = ks_2samp(reference_values, current_values)
            drift_score = statistic
            
            logger.info(f"KS test for {feature}: statistic={statistic:.4f}, p-value={p_value:.4f}")
            
        elif method == 'psi':
            # Population Stability Index
            drift_score = self.calculate_psi(reference_values, current_values)
            logger.info(f"PSI for {feature}: {drift_score:.4f}")
        
        return drift_score
        
    def calculate_psi(self, expected: pd.Series, actual: pd.Series, 
                     bins: int = 10) -> float:
        """
        Calculate Population Stability Index
        
        Args:
            expected: Expected (reference) distribution
            actual: Actual (current) distribution
            bins: Number of bins for discretization
            
        Returns:
            PSI value
        """
        # Create bins
        breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        # Calculate percentages
        expected_percents = pd.cut(expected, bins=breakpoints, 
                                  include_lowest=True).value_counts(normalize=True).sort_index()
        actual_percents = pd.cut(actual, bins=breakpoints, 
                                include_lowest=True).value_counts(normalize=True).sort_index()
        
        # Calculate PSI
        psi_values = (actual_percents - expected_percents) * np.log(actual_percents / expected_percents)
        psi = psi_values.sum()
        
        return psi
        
    def check_all_features_drift(self, current_data: pd.DataFrame,
                                 numerical_features: list,
                                 threshold: float = 0.3) -> Dict[str, Any]:
        """
        Check drift for all numerical features
        
        Args:
            current_data: Current production data
            numerical_features: List of numerical features
            threshold: Drift threshold for alerting
            
        Returns:
            Dictionary with drift results
        """
        drift_results = {
            'timestamp': datetime.now().isoformat(),
            'features': {},
            'drifted_features': [],
            'drift_detected': False
        }
        
        for feature in numerical_features:
            if feature in current_data.columns:
                drift_score = self.calculate_drift(current_data, feature, method='ks')
                drift_results['features'][feature] = drift_score
                
                if drift_score > threshold:
                    drift_results['drifted_features'].append(feature)
                    drift_results['drift_detected'] = True
        
        # Log results
        self.drift_log.append(drift_results)
        
        if drift_results['drift_detected']:
            logger.warning(f"Data drift detected in features: {drift_results['drifted_features']}")
        else:
            logger.info("No significant data drift detected")
        
        return drift_results
        
    def calculate_model_metrics(self, y_true: np.ndarray, 
                               y_pred: np.ndarray,
                               y_pred_proba: np.ndarray = None) -> Dict[str, float]:
        """
        Calculate model performance metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Prediction probabilities
            
        Returns:
            Dictionary of metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred)
        }
        
        if y_pred_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
        
        # Log metrics
        logger.info(f"Model metrics: {metrics}")
        
        return metrics
        
    def check_performance_degradation(self, current_metrics: Dict[str, float],
                                     baseline_metrics: Dict[str, float],
                                     threshold: float = 0.05) -> Dict[str, Any]:
        """
        Check if model performance has degraded
        
        Args:
            current_metrics: Current model metrics
            baseline_metrics: Baseline metrics from training
            threshold: Acceptable degradation threshold
            
        Returns:
            Degradation analysis
        """
        degradation_report = {
            'timestamp': datetime.now().isoformat(),
            'degraded': False,
            'degraded_metrics': []
        }
        
        for metric, baseline_value in baseline_metrics.items():
            if metric in current_metrics:
                current_value = current_metrics[metric]
                degradation = baseline_value - current_value
                
                if degradation > threshold:
                    degradation_report['degraded'] = True
                    degradation_report['degraded_metrics'].append({
                        'metric': metric,
                        'baseline': baseline_value,
                        'current': current_value,
                        'degradation': degradation
                    })
        
        if degradation_report['degraded']:
            logger.warning(f"Performance degradation detected: {degradation_report['degraded_metrics']}")
        
        return degradation_report
        
    def should_retrain(self, drift_detected: bool,
                      performance_degraded: bool,
                      days_since_training: int,
                      max_days: int = 30) -> Dict[str, Any]:
        """
        Determine if model should be retrained
        
        Args:
            drift_detected: Whether data drift was detected
            performance_degraded: Whether performance degraded
            days_since_training: Days since last training
            max_days: Maximum days between retraining
            
        Returns:
            Retraining recommendation
        """
        should_retrain = False
        reasons = []
        
        if drift_detected:
            should_retrain = True
            reasons.append("Data drift detected")
        
        if performance_degraded:
            should_retrain = True
            reasons.append("Performance degradation detected")
        
        if days_since_training >= max_days:
            should_retrain = True
            reasons.append(f"Scheduled retraining (>{max_days} days)")
        
        recommendation = {
            'timestamp': datetime.now().isoformat(),
            'should_retrain': should_retrain,
            'reasons': reasons,
            'priority': 'high' if performance_degraded else 'medium'
        }
        
        if should_retrain:
            logger.info(f"Retraining recommended: {reasons}")
        
        return recommendation
        
    def export_monitoring_report(self, filepath: str):
        """
        Export monitoring report to JSON
        
        Args:
            filepath: Path to save report
        """
        report = {
            'performance_log': self.performance_log,
            'drift_log': self.drift_log,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Monitoring report exported to {filepath}")


if __name__ == "__main__":
    # Example usage
    # Create sample reference data
    reference_data = pd.DataFrame({
        'tenure': np.random.randint(1, 72, 1000),
        'monthly_charges': np.random.uniform(20, 120, 1000)
    })
    
    # Create current data (slightly different distribution)
    current_data = pd.DataFrame({
        'tenure': np.random.randint(1, 60, 500),  # Different range
        'monthly_charges': np.random.uniform(30, 140, 500)  # Shifted distribution
    })
    
    # Initialize monitor
    monitor = ModelMonitor(reference_data=reference_data)
    
    # Check drift
    drift_results = monitor.check_all_features_drift(
        current_data,
        numerical_features=['tenure', 'monthly_charges'],
        threshold=0.3
    )
    
    print("\nDrift Results:")
    print(f"Drift detected: {drift_results['drift_detected']}")
    print(f"Drifted features: {drift_results['drifted_features']}")
    print(f"Drift scores: {drift_results['features']}")
