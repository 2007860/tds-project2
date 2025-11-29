"""Visualization utilities."""
import logging
import base64
import io
from typing import Optional

logger = logging.getLogger(__name__)

# Optional imports
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("matplotlib/seaborn not available - visualization disabled")


class Visualizer:
    """Create visualizations and encode them as base64."""
    
    @staticmethod
    def create_bar_chart(
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "Bar Chart"
    ) -> Optional[str]:
        """
        Create a bar chart and return as base64.
        
        Args:
            data: Input DataFrame
            x_col: Column for x-axis
            y_col: Column for y-axis
            title: Chart title
            
        Returns:
            Base64-encoded image or None
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(data[x_col], data[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(title)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return Visualizer._encode_plot()
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return None
    
    @staticmethod
    def create_line_chart(
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "Line Chart"
    ) -> Optional[str]:
        """
        Create a line chart and return as base64.
        
        Args:
            data: Input DataFrame
            x_col: Column for x-axis
            y_col: Column for y-axis
            title: Chart title
            
        Returns:
            Base64-encoded image or None
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(data[x_col], data[y_col], marker='o')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(title)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return Visualizer._encode_plot()
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return None
    
    @staticmethod
    def create_pie_chart(
        data: pd.DataFrame,
        labels_col: str,
        values_col: str,
        title: str = "Pie Chart"
    ) -> Optional[str]:
        """
        Create a pie chart and return as base64.
        
        Args:
            data: Input DataFrame
            labels_col: Column for labels
            values_col: Column for values
            title: Chart title
            
        Returns:
            Base64-encoded image or None
        """
        try:
            plt.figure(figsize=(10, 8))
            plt.pie(data[values_col], labels=data[labels_col], autopct='%1.1f%%')
            plt.title(title)
            plt.tight_layout()
            
            return Visualizer._encode_plot()
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            return None
    
    @staticmethod
    def create_scatter_plot(
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "Scatter Plot"
    ) -> Optional[str]:
        """
        Create a scatter plot and return as base64.
        
        Args:
            data: Input DataFrame
            x_col: Column for x-axis
            y_col: Column for y-axis
            title: Chart title
            
        Returns:
            Base64-encoded image or None
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(data[x_col], data[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(title)
            plt.tight_layout()
            
            return Visualizer._encode_plot()
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return None
    
    @staticmethod
    def _encode_plot() -> str:
        """
        Encode the current matplotlib plot as base64.
        
        Returns:
            Base64-encoded string with data URI prefix
        """
        try:
            # Save plot to bytes buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            # Close the plot
            plt.close()
            
            # Return with data URI prefix
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"Error encoding plot: {e}")
            plt.close()
            return ""
