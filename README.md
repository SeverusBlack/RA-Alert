# RA Alert

RA Alert is a Python application designed for monitoring real-time mechanical or structural testing processes. It reads data from an external GUI-based measurement software, evaluates the data against predefined thresholds, and triggers alerts when errors or critical conditions are detected.

## 🚀 Features

- 🖥️ GUI-based configuration via `Tkinter`
- 📋 Real-time clipboard data scraping using `pyautogui` and `pyperclip`
- ⚙️ Concurrent data processing using Python `multiprocessing`
- 📈 Monitors stroke, load, and deflection values
- 🔔 Automatic phone call alerts via Twilio when:
  - Device stops unexpectedly
  - Errors exceed user-defined limits
  - Values exceed safety thresholds
- 📁 Automatic CSV logging of monitored data
- 🧪 Designed for use in lab or industrial testing environments

## 🛠️ Technologies Used

- Python 3.x
- Tkinter
- pyautogui
- pyperclip
- pandas
- pynput
- Twilio API
- pytesseract (optional for OCR-based use cases)

## 🧑‍💻 How It Works

1. **User Interface**: Configure threshold limits for stroke, load, and deflection via a pop-up window.
2. **Data Capture**: The program reads clipboard content scraped from external GUI (assumes user clicks on external software to copy data).
3. **Validation**: The software checks each value for validity and range violations.
4. **Logging**: Valid readings are saved periodically to CSV logs.
5. **Alerting**: If critical conditions occur (e.g. device stalling, excessive errors), the software triggers a Twilio call to notify users.
