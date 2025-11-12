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
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def cache_to_csv(df, name):
    
    if not name.endswith(".csv"): #if the file doesnt end with csv, add it to the end
        name = name + ".csv"
    
    path = os.path.join(DATA_DIR, name) #adds the file into data folder
    
    df.to_csv(path, index=False) #creates csv in path
    
    return os.path.abspath(path) ## converts to absolute path


def _as_date(x):
   return pd.to_datetime(x).date() # removes time to just YYYY-MM-DD
    

def _clean_text(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()