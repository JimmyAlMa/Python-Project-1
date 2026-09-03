from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime

import google as genai
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv()