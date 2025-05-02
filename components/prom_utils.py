from prometheus_api_client import PrometheusConnect
from typing import Dict, List, Any
import pandas as pd

class PrometheusClient:
    def __init__(self, url: str = "http://localhost:9090"):
        self.prom = PrometheusConnect(url=url, disable_ssl=True)
        
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
            
    def query_range(self, promql: str, start_time: str, end_time: str, step: str = "1m") -> pd.DataFrame:
        """Execute a range query and return results as DataFrame."""
        try:
            return self.prom.custom_query_range(
                promql_query=promql,
                start_time=start_time,
                end_time=end_time,
                step=step
            )
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})
            
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
