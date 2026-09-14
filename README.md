# Automation Financial Tracker Bot

An automated financial tracking system built with two dedicated Telegram bots — an **Income Tracker** and an **Expense Tracker** — designed to help users log their finances effortlessly through simple chat messages, with all data automatically recorded into the user's personal Google Sheets.

## Overview

Manually recording daily income and expenses is often tedious and easy to forget. This project solves that problem by allowing users to simply send a message via Telegram, which is then automatically processed and saved into a Google Sheets spreadsheet — no manual spreadsheet editing required.

The system consists of two separate bots, each handling a specific responsibility:

- **Income Tracker Bot** — records incoming income entries.
- **Expense Tracker Bot** — records outgoing expense entries.

Separating the two bots keeps each one focused on a single task, making the system simpler to maintain, test, and extend in the future.

## How It Works

The data flow follows a simple and consistent pattern:

1. **User sends a message via Telegram**
   The user chats with either the Income Tracker Bot or the Expense Tracker Bot, providing transaction details (e.g., amount, category, or notes).

2. **Bot processes and records the data to Google Sheets**
   The bot parses the incoming message and automatically writes the transaction data into the user's connected Google Sheets.

3. **Bot sends a confirmation message back to the user**
   Once the data has been successfully saved, the bot replies via Telegram with a confirmation message, such as:
   > "Tercatat! Rp50.000 untuk Makan Siang telah disimpan ke catatan pengeluaranmu."

```
Telegram Chat → Bot → Google Sheets → Confirmation Message → Telegram Chat
```

## Features

- 📥 **Income Tracker Bot** — logs all income transactions sent via Telegram.
- 📤 **Expense Tracker Bot** — logs all expense transactions sent via Telegram.
- 📊 **Automatic Google Sheets Integration** — every recorded transaction is instantly saved to the user's own spreadsheet.
- ✅ **Instant Confirmation** — users receive a reply message confirming that their data has been successfully recorded.
- 🔄 **Simple, Chat-Based Workflow** — no manual input into spreadsheets; everything is handled through natural conversation.

## Tech Stack

- **Telegram Bot API** — for handling chat-based interactions.
- **Google Sheets API** — for automated data recording and storage.
- **Python** — backend language for bot logic and data processing.
- **Render** — hosting and deployment platform.

## Setup & Installation

1. Clone this repository.
2. Install the required dependencies for both bots.
3. Create a Telegram bot for each service (Income and Expense) via [BotFather](https://t.me/BotFather) and obtain the bot tokens.
4. Set up a Google Cloud project, enable the Google Sheets API, and generate the necessary credentials.
5. Configure environment variables (bot tokens, Google Sheets credentials, spreadsheet ID, etc.) in a `.env` file.
6. Run both bots.

## Usage

1. Start a chat with the Income Tracker Bot or Expense Tracker Bot on Telegram.
2. Send a message containing your transaction details.
3. The bot will automatically record the data into your connected Google Sheets.
4. You will receive a confirmation message once the data has been successfully saved.