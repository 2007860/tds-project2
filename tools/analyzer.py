"""Data analysis utilities."""
import logging
from typing import Any, Optional, List

logger = logging.getLogger(__name__)

# Optional imports
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.warning("pandas/numpy not available - analysis features limited")


class DataAnalyzer:
    """Analyze and transform data."""
    
    @staticmethod
    def filter_data(df: pd.DataFrame, conditions: dict) -> pd.DataFrame:
        """
        Filter DataFrame based on conditions.
        
        Args:
            df: Input DataFrame
            conditions: Dict of column: value conditions
            
        Returns:
            Filtered DataFrame
        """
        try:
            result = df.copy()
            for col, value in conditions.items():
                if col in result.columns:
                    result = result[result[col] == value]
            logger.info(f"Filtered to {len(result)} rows")
            return result
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return df
    
    @staticmethod
    def aggregate(df: pd.DataFrame, group_by: str, agg_func: str, agg_col: str) -> Any:
        """
        Aggregate data.
        
        Args:
            df: Input DataFrame
            group_by: Column to group by
            agg_func: Aggregation function (sum, mean, count, etc.)
            agg_col: Column to aggregate
            
        Returns:
            Aggregated result
        """
        try:
            if group_by in df.columns:
                grouped = df.groupby(group_by)[agg_col]
                
                if agg_func == 'sum':
                    result = grouped.sum()
                elif agg_func == 'mean':
                    result = grouped.mean()
                elif agg_func == 'count':
                    result = grouped.count()
                elif agg_func == 'max':
                    result = grouped.max()
                elif agg_func == 'min':
                    result = grouped.min()
                else:
                    result = grouped.agg(agg_func)
                
                logger.info(f"Aggregated {agg_col} by {group_by} using {agg_func}")
                return result
        except Exception as e:
            logger.error(f"Error aggregating data: {e}")
            return None
    
    @staticmethod
    def calculate_sum(df: pd.DataFrame, column: str) -> Optional[float]:
        """
        Calculate sum of a column.
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            Sum or None
        """
        try:
            if column in df.columns:
                result = df[column].sum()
                logger.info(f"Sum of {column}: {result}")
                return result
        except Exception as e:
            logger.error(f"Error calculating sum: {e}")
            return None
    
    @staticmethod
    def calculate_mean(df: pd.DataFrame, column: str) -> Optional[float]:
        """
        Calculate mean of a column.
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            Mean or None
        """
        try:
            if column in df.columns:
                result = df[column].mean()
                logger.info(f"Mean of {column}: {result}")
                return result
        except Exception as e:
            logger.error(f"Error calculating mean: {e}")
            return None
    
    @staticmethod
    def sort_data(df: pd.DataFrame, by: str, ascending: bool = True) -> pd.DataFrame:
        """
        Sort DataFrame.
        
        Args:
            df: Input DataFrame
            by: Column to sort by
            ascending: Sort order
            
        Returns:
            Sorted DataFrame
        """
        try:
            if by in df.columns:
                result = df.sort_values(by=by, ascending=ascending)
                logger.info(f"Sorted by {by}")
                return result
        except Exception as e:
            logger.error(f"Error sorting data: {e}")
            return df
    
    @staticmethod
    def get_statistics(df: pd.DataFrame, column: str) -> Optional[dict]:
        """
        Get basic statistics for a column.
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            Dict with statistics
        """
        try:
            if column in df.columns:
                stats = {
                    'count': df[column].count(),
                    'mean': df[column].mean(),
                    'std': df[column].std(),
                    'min': df[column].min(),
                    'max': df[column].max(),
                    'median': df[column].median()
                }
                logger.info(f"Statistics for {column}: {stats}")
                return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return None
    
    @staticmethod
    def find_value(df: pd.DataFrame, search_col: str, search_value: Any, return_col: str) -> Any:
        """
        Find a value in DataFrame.
        
        Args:
            df: Input DataFrame
            search_col: Column to search in
            search_value: Value to search for
            return_col: Column to return value from
            
        Returns:
            Found value or None
        """
        try:
            matches = df[df[search_col] == search_value]
            if len(matches) > 0:
                result = matches[return_col].iloc[0]
                logger.info(f"Found {result} for {search_value}")
                return result
        except Exception as e:
            logger.error(f"Error finding value: {e}")
            return None
