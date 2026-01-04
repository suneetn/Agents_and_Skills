"""
Screen Definitions
Predefined screening criteria for different investment strategies.
"""

SCREEN_DEFINITIONS = {
    "momentum": {
        "name": "Momentum",
        "description": "Stocks with strong upward momentum and positive technical signals",
        "is_growth_screen": False,
        "use_full_rating": False,  # Exclude P/E, P/B from FMP rating
        "criteria": {
            "rsi_min": 50,
            "rsi_max": 70,
            "above_sma_50": True,
            "above_sma_200": True,
            "volume_surge": False,
            "pe_max": 50,  # Not too expensive
            "technical_weight": 0.7,  # Heavily weight technical
        }
    },
    
    "oversold": {
        "name": "Oversold Quality",
        "description": "Quality stocks that are technically oversold - potential bounce candidates",
        "is_growth_screen": False,
        "use_full_rating": False,
        "criteria": {
            "rsi_max": 35,
            "above_sma_200": True,  # Still in long-term uptrend
            "pe_max": 25,
            "roe_min": 0.10,  # 10% ROE minimum
            "technical_weight": 0.6,
        }
    },
    
    "value": {
        "name": "Deep Value",
        "description": "Undervalued stocks with solid fundamentals and dividends",
        "is_growth_screen": False,
        "use_full_rating": True,  # Use full FMP rating including P/E, P/B
        "criteria": {
            "pe_max": 15,
            "pb_max": 2.0,
            "dividend_yield_min": 0.02,  # 2% minimum dividend
            "debt_equity_max": 1.0,
            "roe_min": 0.08,  # 8% ROE minimum
            "technical_weight": 0.3,  # Weight fundamentals more
        }
    },
    
    "quality": {
        "name": "Quality Growth",
        "description": "High-quality companies with strong returns and low debt",
        "is_growth_screen": False,
        "use_full_rating": False,
        "criteria": {
            "roe_min": 0.15,  # 15% ROE minimum
            "debt_equity_max": 0.5,
            "pe_max": 35,
            "above_sma_200": True,
            "technical_weight": 0.4,
        }
    },
    
    "technical_buy": {
        "name": "Technical Buy Setup",
        "description": "Stocks with bullish technical setups near support",
        "is_growth_screen": False,
        "use_full_rating": False,
        "criteria": {
            "rsi_min": 30,
            "rsi_max": 45,
            "above_sma_200": True,
            "below_sma_50": True,  # Pullback to support
            "volume_surge": False,
            "technical_weight": 0.8,  # Almost pure technical
        }
    },
    
    "growth": {
        "name": "High Growth",
        "description": "High-growth companies with strong revenue/earnings growth, regardless of P/E",
        "is_growth_screen": True,
        "use_full_rating": False,  # Exclude P/E, P/B penalties
        "criteria": {
            "revenue_growth_min": 0.15,  # 15% minimum revenue growth
            "eps_growth_min": 0.20,  # 20% minimum EPS growth
            "peg_max": 3.0,  # PEG ratio under 3
            "above_sma_200": True,
            "technical_weight": 0.4,
            "growth_weight": 0.4,  # Weight growth metrics
            "fundamental_weight": 0.2,
        }
    },
    
    "tech_momentum": {
        "name": "Tech Momentum",
        "description": "Technology sector stocks with strong momentum - includes high P/E growth names",
        "is_growth_screen": True,
        "use_full_rating": False,
        "sector": "Technology",  # Filter to tech sector only
        "criteria": {
            "rsi_min": 45,
            "rsi_max": 75,
            "above_sma_50": True,
            "pe_max": 100,  # Allow high P/E for growth tech
            "technical_weight": 0.6,
            "growth_weight": 0.3,
        }
    },
}


def get_screen_criteria(screen_type: str) -> dict:
    """
    Get criteria for a predefined screen.
    
    Args:
        screen_type: Name of the screen (momentum, oversold, value, quality, technical_buy, growth)
    
    Returns:
        Dict of criteria for the screen
    
    Raises:
        ValueError: If screen_type is not recognized
    """
    if screen_type not in SCREEN_DEFINITIONS:
        available = ", ".join(SCREEN_DEFINITIONS.keys())
        raise ValueError(f"Unknown screen type: {screen_type}. Available: {available}")
    
    return SCREEN_DEFINITIONS[screen_type]["criteria"].copy()


def is_growth_screen(screen_type: str) -> bool:
    """Check if the screen is a growth-focused screen."""
    if screen_type not in SCREEN_DEFINITIONS:
        return False
    return SCREEN_DEFINITIONS[screen_type].get("is_growth_screen", False)


def use_full_rating(screen_type: str) -> bool:
    """Check if the screen should use full FMP rating (including P/E, P/B)."""
    if screen_type not in SCREEN_DEFINITIONS:
        return False
    return SCREEN_DEFINITIONS[screen_type].get("use_full_rating", False)


def get_screen_description(screen_type: str) -> str:
    """Get human-readable description of a screen."""
    if screen_type not in SCREEN_DEFINITIONS:
        return "Unknown screen type"
    return SCREEN_DEFINITIONS[screen_type]["description"]


def list_available_screens() -> dict:
    """List all available predefined screens with descriptions."""
    return {
        name: {
            "name": defn["name"],
            "description": defn["description"]
        }
        for name, defn in SCREEN_DEFINITIONS.items()
    }


# Custom criteria builder helpers
def build_custom_criteria(
    rsi_min: float = None,
    rsi_max: float = None,
    pe_max: float = None,
    pb_max: float = None,
    roe_min: float = None,
    debt_equity_max: float = None,
    dividend_yield_min: float = None,
    above_sma_50: bool = None,
    above_sma_200: bool = None,
    below_sma_50: bool = None,
    volume_surge: bool = None,
    technical_weight: float = 0.5
) -> dict:
    """
    Build custom screening criteria.
    
    Args:
        rsi_min: Minimum RSI value
        rsi_max: Maximum RSI value
        pe_max: Maximum P/E ratio
        pb_max: Maximum Price/Book ratio
        roe_min: Minimum Return on Equity (decimal, e.g., 0.15 for 15%)
        debt_equity_max: Maximum Debt/Equity ratio
        dividend_yield_min: Minimum dividend yield (decimal)
        above_sma_50: Require price above 50-day SMA
        above_sma_200: Require price above 200-day SMA
        below_sma_50: Require price below 50-day SMA
        volume_surge: Require volume surge (>1.5x average)
        technical_weight: Weight for technical vs fundamental (0-1)
    
    Returns:
        Dict of criteria
    """
    criteria = {"technical_weight": technical_weight}
    
    if rsi_min is not None:
        criteria["rsi_min"] = rsi_min
    if rsi_max is not None:
        criteria["rsi_max"] = rsi_max
    if pe_max is not None:
        criteria["pe_max"] = pe_max
    if pb_max is not None:
        criteria["pb_max"] = pb_max
    if roe_min is not None:
        criteria["roe_min"] = roe_min
    if debt_equity_max is not None:
        criteria["debt_equity_max"] = debt_equity_max
    if dividend_yield_min is not None:
        criteria["dividend_yield_min"] = dividend_yield_min
    if above_sma_50 is not None:
        criteria["above_sma_50"] = above_sma_50
    if above_sma_200 is not None:
        criteria["above_sma_200"] = above_sma_200
    if below_sma_50 is not None:
        criteria["below_sma_50"] = below_sma_50
    if volume_surge is not None:
        criteria["volume_surge"] = volume_surge
    
    return criteria

