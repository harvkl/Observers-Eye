# ![Observer's Eye](media/eye.png) Observer's Eye - System Monitoring Tool

A lightweight, cross-platform system monitoring application built with Python and PyQt6 that provides real-time insights into your system's performance, processes, and resource utilization.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#️-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dependencies](#-dependencies)
- [License](#-license)

## ✨ Features

- **Real-time Performance Monitoring**: Track CPU and RAM usage with visual progress bars and instant updates every 3 seconds
- **Process Management**: View detailed information about running processes including PID, name, CPU%, and RAM%
- **Dual Display Modes**: Toggle between list view and table view for process information
- **Process Termination**: Select and kill individual processes or terminate all subprocesses
- **High Usage Alerts**: Automatic warnings when CPU exceeds 90% or RAM exceeds 80%
- **System Statistics**: Detailed CPU stats including context switches, interrupts, system calls, load averages, and CPU frequency
- **Report Generation**: Save comprehensive system reports to text files with timestamps
- **System Tray Integration**: Minimize to system tray with quick access menu
- **Custom Styling**: Modern dark theme with orange accents using Qt Style Sheets (QSS)
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.10 or later)
- **pip** (Python package installer)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/harvkl/Observers-Eye.git
cd Observers-Eye
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- PyQt6 (GUI framework)
- psutil (system and process utilities)

## 🚀 Usage

### Running the Application

```bash
cd OE_app
python main.py
```

Or from the root directory:

```bash
python OE_app/main.py
```

### Notes

> ⚠️ **Important**: The percentage shown for the "System Idle Process" represents available resources for other processes, not actual CPU usage.

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.11.0 | GUI framework |
| psutil | 7.2.2 | System and process monitoring |

See [`requirements.txt`](requirements.txt) for the complete list of dependencies with exact versions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
