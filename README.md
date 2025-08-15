# 🌍 TMD Earthquake MCP Server v1.0

Model Context Protocol (MCP) server for real-time earthquake data access from Thai Meteorological Department (TMD)

## 📋 Table of Contents
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Claude Desktop Configuration](#-claude-desktop-configuration)
- [Usage](#-usage)
- [Example Commands](#-example-commands)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

### 🛠️ Tools
This server provides tools for searching and analyzing earthquake data:

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_earthquakes` | Fetch recent earthquake data | `limit` (number of items, default: 10) |
| `get_earthquakes_by_magnitude` | Filter earthquakes by magnitude | `min_magnitude` (minimum magnitude, default: 3.0) |
| `get_earthquakes_by_location` | Search by location/country | `location` (location name in Thai/English) |
| `get_earthquake_summary` | Get earthquake statistics summary | - |
| `get_large_earthquakes` | Find large dangerous earthquakes | `magnitude_threshold` (default: 5.0) |

### 📚 Resources
| Resource | Description |
|----------|-------------|
| `earthquake://latest` | Latest earthquake data (1 item) |
| `earthquake://today` | All earthquakes today (Thai timezone) |

### 📊 Data Provided
- 📅 Date and time (both UTC and Thai time)
- 📍 Location coordinates (Latitude, Longitude)
- 🎯 Epicenter depth (kilometers)
- 📊 Earthquake magnitude
- 🌏 Event location (in Thai)
- 💬 Additional details

## 💻 System Requirements

- **Python** 3.10 or higher
- **pip** (Python package manager)
- **Internet** connection for TMD API access
- **Claude Desktop** (for Claude integration)

## 🚀 Installation

### Method 1: Automatic Script (Recommended)

#### Windows:
```batch
cd C:\Users\Asus\2025-Aug-APT_LLMs-for-Telecom\tmd-earthquake-server-1.0
install.bat
```

#### Linux/Mac:
```bash
cd /path/to/tmd-earthquake-server-1.0
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation

1. **Open Command Prompt/Terminal**

2. **Navigate to server directory:**
```bash
cd C:\Users\Asus\2025-Aug-APT_LLMs-for-Telecom\tmd-earthquake-server-1.0
```

3. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Or install separately:
```bash
pip install "mcp[cli]" httpx
```

## ⚙️ Claude Desktop Configuration

### 1. Locate Configuration File

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```
or
```
C:\Users\[Username]\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 2. Add Server Configuration

Open `claude_desktop_config.json` with a text editor and add:

```json
{
  "mcpServers": {
    "tmd-earthquake": {
      "command": "python",
      "args": ["C:\\Users\\Asus\\2025-Aug-APT_LLMs-for-Telecom\\tmd-earthquake-server-1.0\\server.py"]
    }
  }
}
```

**Note:** 
- Use `\\` (double backslash) for Windows paths
- If other servers exist, add after existing servers (don't forget the comma)

### 3. Restart Claude Desktop

1. Close Claude Desktop completely (including system tray)
2. Reopen Claude Desktop
3. Check for 🔌 icon indicating MCP server connection

## 📖 Usage

### Direct Server Testing

```bash
# Test if server works
python server.py

# Use MCP Inspector (requires Node.js)
npx @modelcontextprotocol/inspector python server.py
```

### Using in Claude Desktop

Once configured, use natural language commands with Claude:

## 💬 Example Commands

### English
- "Show me recent earthquakes"
- "Find earthquakes with magnitude 4 or higher"
- "Are there any earthquakes in Myanmar?"
- "Give me a summary of earthquake activity"
- "Show today's earthquakes"
- "Find large earthquakes that might be dangerous"

### Thai
- "แสดงข้อมูลแผ่นดินไหวล่าสุด"
- "หาแผ่นดินไหวที่มีขนาดมากกว่า 4 ริกเตอร์"
- "มีแผ่นดินไหวที่ประเทศเมียนมาบ้างไหม"
- "สรุปสถิติแผ่นดินไหวให้หน่อย"
- "แผ่นดินไหววันนี้มีกี่ครั้ง"
- "หาแผ่นดินไหวขนาดใหญ่ที่อาจเป็นอันตราย"

## 📊 API Reference

### Tools

#### `get_earthquakes(limit: int = 10)`
Fetch recent earthquake data
- **limit**: Maximum number of items to retrieve (default: 10)
- **Returns**: List of earthquakes with details

#### `get_earthquakes_by_magnitude(min_magnitude: float = 3.0)`
Filter earthquakes by magnitude
- **min_magnitude**: Minimum magnitude threshold (default: 3.0)
- **Returns**: Earthquakes matching the magnitude criteria

#### `get_earthquakes_by_location(location: str)`
Search earthquakes by location
- **location**: Location/country name (Thai or English)
- **Returns**: Earthquakes in specified area

#### `get_earthquake_summary()`
Get earthquake statistics summary
- **Returns**: Total statistics, average magnitude, distribution by area

#### `get_large_earthquakes(magnitude_threshold: float = 5.0)`
Find large earthquakes
- **magnitude_threshold**: Magnitude threshold (default: 5.0)
- **Returns**: Earthquakes exceeding the threshold

### Resources

#### `earthquake://latest`
- **Returns**: Latest earthquake data (1 item)

#### `earthquake://today`
- **Returns**: All earthquakes today (Thai timezone)

## 🔧 Troubleshooting

### Server Not Appearing in Claude Desktop

1. **Check Python:**
```bash
python --version
# Must be Python 3.10 or higher
```

2. **Check dependencies:**
```bash
pip list | findstr mcp
# Must have mcp package
```

3. **View logs:**
```bash
# Windows
type %APPDATA%\Claude\logs\mcp*.log

# Or open with notepad
notepad %APPDATA%\Claude\logs\mcp-server-tmd-earthquake.log
```

4. **Test server directly:**
```bash
cd C:\Users\Asus\2025-Aug-APT_LLMs-for-Telecom\tmd-earthquake-server-1.0
python server.py
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | MCP not installed | Run `pip install "mcp[cli]"` |
| `ModuleNotFoundError: No module named 'httpx'` | httpx not installed | Run `pip install httpx` |
| `Connection timeout` | Cannot connect to TMD API | Check internet connection |
| `Server not responding` | Incorrect path in config | Check path in claude_desktop_config.json |

### How to Verify Server is Working

1. Claude Desktop should show 🔌 or ⚡ icon
2. Type "Show MCP tools" in Claude
3. Should see tmd-earthquake server tools

## 📊 Data Source

- **API Provider**: Thai Meteorological Department (TMD)
- **API Endpoint**: https://data.tmd.go.th/api/DailySeismicEvent/v1/
- **Update Frequency**: Real-time
- **Coverage**: Regional and global

## 📄 License

This server is for educational and informational purposes. The earthquake data is provided by TMD.

## 🤝 Contributing

If you find issues or want to add features:
1. Create an Issue
2. Submit Pull Request
3. Contact the developer

## 📞 Support

If you need help:
- Check [Troubleshooting](#-troubleshooting) first
- Review logs in `%APPDATA%\Claude\logs\`
- Test server directly with `python server.py`

---

**Version**: 1.0.0  
**Last Updated**: 2025-08-15  
**Developed for**: TMD Earthquake Data Access via MCP
