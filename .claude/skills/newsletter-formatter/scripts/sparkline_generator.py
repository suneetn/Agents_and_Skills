#!/usr/bin/env python3
"""
Sparkline Chart Generator for Newsletter
Generates tiny inline charts for stock price history
"""

import io
import base64
from typing import List, Optional, Tuple
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


class SparklineGenerator:
    """Generates sparkline charts for email newsletters"""
    
    def __init__(self, width: int = 100, height: int = 30):
        """
        Initialize sparkline generator
        
        Args:
            width: Chart width in pixels
            height: Chart height in pixels
        """
        self.width = width
        self.height = height
        self.dpi = 100
        
    def generate(
        self, 
        data: List[float], 
        color: str = '#4fd1c5',
        fill_color: Optional[str] = None,
        show_endpoints: bool = True,
        show_trend: bool = True
    ) -> str:
        """
        Generate a sparkline chart as base64 encoded PNG
        
        Args:
            data: List of price values
            color: Line color
            fill_color: Optional fill color under the line
            show_endpoints: Show start/end dots
            show_trend: Color line based on trend (green up, red down)
            
        Returns:
            Base64 encoded PNG image string
        """
        if not data or len(data) < 2:
            return self._generate_placeholder()
        
        # Determine trend color
        if show_trend:
            trend = data[-1] - data[0]
            color = '#38a169' if trend >= 0 else '#e53e3e'
            fill_color = 'rgba(56, 161, 105, 0.1)' if trend >= 0 else 'rgba(229, 62, 62, 0.1)'
        
        # Create figure
        fig_width = self.width / self.dpi
        fig_height = self.height / self.dpi
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=self.dpi)
        
        # Remove all decorations
        ax.axis('off')
        ax.set_xlim(-0.5, len(data) - 0.5)
        
        # Add padding to y-axis
        y_min, y_max = min(data), max(data)
        y_padding = (y_max - y_min) * 0.15 if y_max != y_min else 1
        ax.set_ylim(y_min - y_padding, y_max + y_padding)
        
        # Plot line
        x = np.arange(len(data))
        ax.plot(x, data, color=color, linewidth=1.5, solid_capstyle='round')
        
        # Fill under line
        if fill_color:
            ax.fill_between(x, data, alpha=0.2, color=color)
        
        # Show endpoints
        if show_endpoints:
            ax.scatter([0, len(data)-1], [data[0], data[-1]], 
                      color=color, s=12, zorder=5)
        
        # Remove margins
        plt.tight_layout(pad=0)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Save to base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', transparent=True, 
                   bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return f"data:image/png;base64,{img_base64}"
    
    def _generate_placeholder(self) -> str:
        """Generate a placeholder image for invalid data"""
        fig, ax = plt.subplots(figsize=(self.width/self.dpi, self.height/self.dpi), dpi=self.dpi)
        ax.axis('off')
        ax.text(0.5, 0.5, '—', ha='center', va='center', 
               fontsize=14, color='#a0aec0')
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', transparent=True)
        plt.close(fig)
        
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return f"data:image/png;base64,{img_base64}"
    
    def generate_batch(
        self, 
        data_sets: List[List[float]],
        **kwargs
    ) -> List[str]:
        """
        Generate multiple sparklines
        
        Args:
            data_sets: List of price data lists
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            List of base64 encoded images
        """
        return [self.generate(data, **kwargs) for data in data_sets]


def get_trend_indicator(data: List[float]) -> Tuple[str, str]:
    """
    Get trend indicator emoji and color
    
    Args:
        data: Price data
        
    Returns:
        Tuple of (emoji, color)
    """
    if not data or len(data) < 2:
        return '—', '#a0aec0'
    
    change = (data[-1] - data[0]) / data[0] * 100
    
    if change > 5:
        return '🚀', '#38a169'
    elif change > 2:
        return '📈', '#38a169'
    elif change > 0:
        return '↗️', '#38a169'
    elif change > -2:
        return '↘️', '#e53e3e'
    elif change > -5:
        return '📉', '#e53e3e'
    else:
        return '🔻', '#e53e3e'


if __name__ == '__main__':
    # Test sparkline generation
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate sparkline charts')
    parser.add_argument('--test', action='store_true', help='Run test generation')
    parser.add_argument('--output', type=str, default='sparkline_test.png', 
                       help='Output file path')
    
    args = parser.parse_args()
    
    if args.test:
        # Generate test sparklines
        generator = SparklineGenerator(width=100, height=30)
        
        # Uptrend data
        uptrend = [100, 102, 101, 105, 108, 107, 112, 115]
        up_img = generator.generate(uptrend)
        print(f"Uptrend sparkline: {len(up_img)} chars")
        
        # Downtrend data
        downtrend = [100, 98, 99, 95, 92, 93, 88, 85]
        down_img = generator.generate(downtrend)
        print(f"Downtrend sparkline: {len(down_img)} chars")
        
        # Create HTML test page
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Sparkline Test</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2>Sparkline Test</h2>
            <p>Uptrend: <img src="{up_img}" style="vertical-align: middle;"></p>
            <p>Downtrend: <img src="{down_img}" style="vertical-align: middle;"></p>
        </body>
        </html>
        """
        
        with open('sparkline_test.html', 'w') as f:
            f.write(html)
        
        print("✅ Generated sparkline_test.html")



