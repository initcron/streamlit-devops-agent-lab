from prometheus_api_client import PrometheusConnect
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from config import Config
from datetime import datetime
import logging
import requests

class PrometheusClient:
    def __init__(self, url: Optional[str] = None):
        self.base_url = url or Config.PROMETHEUS_BASE_URL
        self.prom = PrometheusConnect(
            url=self.base_url,
            disable_ssl=True
        )
        
    def check_connection(self) -> bool:
        """Check if Prometheus is accessible."""
        try:
            return self.prom.check_prometheus_connection()
        except:
            return False
            
    def query(self, promql: str) -> List[Dict[str, Any]]:
        """Execute a PromQL query."""
        try:
            return self.prom.custom_query(promql_query=promql)
        except Exception as e:
            return [{"error": str(e)}]
            
    def query_range(self, promql: str, start_time: Union[int, str], end_time: Union[int, str], step: str = "1m") -> pd.DataFrame:
        """Execute a range query and return results as DataFrame.
        
        Args:
            promql: The PromQL query string
            start_time: Start time as Unix timestamp (int) or ISO string
            end_time: End time as Unix timestamp (int) or ISO string
            step: Query resolution step width
        """
        try:
            # Construct the query URL
            url = f"{self.base_url}/api/v1/query_range"
            
            # Prepare parameters
            params = {
                'query': promql,
                'start': start_time,
                'end': end_time,
                'step': step
            }
            
            # Make the request
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse the response
            result = response.json()
            
            # Debug logging
            logging.debug(f"Prometheus response: {result}")
            
            # Check if result is valid
            if result['status'] != 'success':
                return pd.DataFrame({"error": [f"Query failed: {result.get('error', 'Unknown error')}"]})
            
            # Get the result data
            if not result.get('data', {}).get('result', []):
                return pd.DataFrame({"error": ["No data returned from Prometheus"]})
            
            # Get the first result
            series = result['data']['result'][0]
            
            if not series.get('values', []):
                return pd.DataFrame({"error": ["No data points in the time series"]})
            
            try:
                # Create DataFrame with timestamp and value columns
                df = pd.DataFrame(series['values'], columns=['timestamp', 'value'])
                
                # Convert timestamp to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'].astype(float), unit='s')
                
                # Convert values to float
                df['value'] = df['value'].astype(float)
                
                return df
            except Exception as e:
                return pd.DataFrame({"error": [f"Error formatting data: {str(e)}"]})
                
        except requests.exceptions.RequestException as e:
            return pd.DataFrame({"error": [f"HTTP request failed: {str(e)}"]})
        except Exception as e:
            return pd.DataFrame({"error": [f"Query failed: {str(e)}"]})
            
    def get_metric_names(self) -> List[str]:
        """Get list of available metric names."""
        try:
            return self.prom.all_metrics()
        except:
            return []
            
    def get_metric_metadata(self, metric_name: str) -> Dict[str, Any]:
        """Get metadata for a specific metric."""
        try:
            return self.prom.get_metric_metadata(metric_name=metric_name)
        except:
            return {}
