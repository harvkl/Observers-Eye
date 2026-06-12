# Observer's Eye - System Monitoring Tool

A lightweight, cross-platform system monitoring application built with Python and PyQt6 that provides real-time insights into your system's performance, processes, and resource utilization.

![Observer's Eye](media/eye.png)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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

## 🖼️ Screenshots

The application features three main tabs:

1. **Performance Tab** - Real-time monitoring dashboard
2. **Results Tab** - Saved reports and export functionality  
3. **Info Tab** - Detailed system statistics and information

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

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- PyQt6 (GUI framework)
- psutil (system and process utilities)
- discord-webhook (optional webhook notifications)
- requests and related HTTP libraries

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

### Getting Started

1. **Launch the application** - The main window will open with the Performance tab active
2. **Monitor your system** - Watch real-time CPU and RAM usage in the progress bars
3. **View processes** - Browse running processes sorted by CPU usage (descending)
4. **Switch views** - Click "Switch process display mode" to toggle between list and table views
5. **Kill processes** - Select a process and click "Select and kill the process"
   - Check "Terminate all subprocesses?" to kill all instances of a process
6. **Get detailed stats** - Navigate to the Info tab and click "Get stats!" for comprehensive system information
7. **Save reports** - Go to the Results tab and click "Save the results in .txt file?" to export a report

### System Tray

The application runs in the system tray with the following options:
- **Make a sound** - Test system beep
- **Quit app** - Exit the application

### Notes

> ⚠️ **Important**: The percentage shown for the "System Idle Process" represents available resources for other processes, not actual CPU usage.

## 📁 Project Structure

```
Observers-Eye/
├── OE_app/                  # Main application source code
│   ├── main.py             # Application entry point
│   ├── ui_main.py          # User interface implementation
│   └── logic.py            # Core business logic
├── styles/                  # UI styling
│   └── styles.qss          # Qt Style Sheet for custom theming
├── media/                   # Application assets
│   ├── eye.png             # Application icon
│   ├── anchor.png          # Performance tab icon
│   ├── report.png          # Results tab icon
│   └── information.png     # Info tab icon
├── Results/                 # Directory for saved reports
│   └── 1.txt               # Sample report file
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

### Key Files

- **`OE_app/main.py`** - Initializes the QApplication, sets up system tray, loads styles, and launches the main window
- **`OE_app/ui_main.py`** - Contains the `MainWindow` class with three tabs: Performance, Results, and Info
- **`OE_app/logic.py`** - Provides static methods for retrieving process lists and user information using psutil
- **`styles/styles.qss`** - Custom Qt stylesheet defining the dark theme with orange/yellow accents

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.11.0 | GUI framework |
| psutil | 7.2.2 | System and process monitoring |
| requests | 2.32.4 | HTTP library |
| discord-webhook | 1.4.1 | Webhook notifications |
| colorama | 0.4.6 | Cross-platform colored terminal text |
| cryptography | 45.0.4 | Cryptographic recipes and primitives |

See [`requirements.txt`](requirements.txt) for the complete list of dependencies with exact versions.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution

- Bug fixes and improvements
- New monitoring features
- Enhanced UI/UX
- Additional export formats (CSV, JSON, etc.)
- Notification integrations
- Documentation improvements
- Translation support

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain the existing project structure

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[psutil](https://github.com/giampaolo/psutil)** - Cross-platform library for retrieving information on running processes and system utilization
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Python bindings for the Qt application framework
- **haruki** - Original creator and maintainer

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/harvkl/Observers-Eye/issues) page for known problems
2. Create a new issue with detailed information about your problem
3. Include your operating system, Python version, and error messages

---

**Made with ❤️ by haruki**
