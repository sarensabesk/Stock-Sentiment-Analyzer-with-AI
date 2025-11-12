from __future__ import annotations

import os
import re
import time
import datetime as dt
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf
import feedparser


#All Downloaded CSV go here
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

