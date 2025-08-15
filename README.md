# 🌍 TMD Earthquake MCP Server v1.0

Model Context Protocol (MCP) server สำหรับเข้าถึงข้อมูลแผ่นดินไหวจากกรมอุตุนิยมวิทยา (TMD) แบบ real-time

## 📋 สารบัญ
- [คุณสมบัติ](#-คุณสมบัติ)
- [ความต้องการของระบบ](#-ความต้องการของระบบ)
- [การติดตั้ง](#-การติดตั้ง)
- [การตั้งค่า Claude Desktop](#-การตั้งค่า-claude-desktop)
- [วิธีใช้งาน](#-วิธีใช้งาน)
- [ตัวอย่างคำสั่ง](#-ตัวอย่างคำสั่ง)
- [API Reference](#-api-reference)
- [การแก้ปัญหา](#-การแก้ปัญหา)

## ✨ คุณสมบัติ

### 🛠️ Tools (เครื่องมือ)
Server นี้มี tools สำหรับค้นหาและวิเคราะห์ข้อมูลแผ่นดินไหว:

| Tool | คำอธิบาย | Parameters |
|------|----------|------------|
| `get_earthquakes` | ดึงข้อมูลแผ่นดินไหวล่าสุด | `limit` (จำนวนรายการ, default: 10) |
| `get_earthquakes_by_magnitude` | กรองแผ่นดินไหวตามขนาด | `min_magnitude` (ขนาดขั้นต่ำ, default: 3.0) |
| `get_earthquakes_by_location` | ค้นหาตามสถานที่/ประเทศ | `location` (ชื่อสถานที่ภาษาไทย/อังกฤษ) |
| `get_earthquake_summary` | สรุปสถิติแผ่นดินไหว | - |
| `get_large_earthquakes` | หาแผ่นดินไหวขนาดใหญ่ที่อันตราย | `magnitude_threshold` (default: 5.0) |

### 📚 Resources (ทรัพยากร)
| Resource | คำอธิบาย |
|----------|----------|
| `earthquake://latest` | ข้อมูลแผ่นดินไหวล่าสุด 1 รายการ |
| `earthquake://today` | แผ่นดินไหวทั้งหมดในวันนี้ (เวลาไทย) |

### 📊 ข้อมูลที่ได้รับ
- 📅 วันที่และเวลา (ทั้ง UTC และเวลาไทย)
- 📍 พิกัดที่ตั้ง (Latitude, Longitude)
- 🎯 ความลึกของจุดศูนย์กลาง (กิโลเมตร)
- 📊 ขนาดแผ่นดินไหว (Magnitude)
- 🌏 สถานที่เกิดเหตุ (ภาษาไทย)
- 💬 รายละเอียดเพิ่มเติม

## 💻 ความต้องการของระบบ

- **Python** 3.10 หรือสูงกว่า
- **pip** (Python package manager)
- **Internet** สำหรับเชื่อมต่อ TMD API
- **Claude Desktop** (สำหรับใช้งานกับ Claude)

## 🚀 การติดตั้ง

### วิธีที่ 1: ใช้ Script อัตโนมัติ (แนะนำ)

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

### วิธีที่ 2: ติดตั้งด้วยตนเอง

1. **เปิด Command Prompt/Terminal**

2. **ไปยัง directory ของ server:**
```bash
cd C:\Users\Asus\2025-Aug-APT_LLMs-for-Telecom\tmd-earthquake-server-1.0
```

3. **สร้าง virtual environment (optional แต่แนะนำ):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **ติดตั้ง dependencies:**
```bash
pip install -r requirements.txt
```

หรือติดตั้งแยก:
```bash
pip install "mcp[cli]" httpx
```

## ⚙️ การตั้งค่า Claude Desktop

### 1. หาไฟล์ Configuration

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```
หรือ
```
C:\Users\[ชื่อผู้ใช้]\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 2. เพิ่ม Server Configuration

เปิดไฟล์ `claude_desktop_config.json` ด้วย text editor แล้วเพิ่ม:

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

**หมายเหตุ:** 
- ใช้ `\\` (double backslash) สำหรับ Windows paths
- ถ้ามี server อื่นอยู่แล้ว ให้เพิ่มหลัง server ที่มีอยู่ (อย่าลืม comma)

### 3. Restart Claude Desktop

1. ปิด Claude Desktop ทั้งหมด (รวมถึงใน system tray)
2. เปิด Claude Desktop ใหม่
3. ตรวจสอบว่ามีไอคอน 🔌 แสดงว่า MCP server เชื่อมต่อแล้ว

## 📖 วิธีใช้งาน

### ทดสอบ Server โดยตรง

```bash
# ทดสอบว่า server ทำงานได้
python server.py

# ใช้ MCP Inspector (ต้องติดตั้ง Node.js)
npx @modelcontextprotocol/inspector python server.py
```

### ใช้งานใน Claude Desktop

เมื่อตั้งค่าเสร็จแล้ว สามารถใช้คำสั่งภาษาธรรมชาติกับ Claude:

## 💬 ตัวอย่างคำสั่ง

### ภาษาไทย
- "แสดงข้อมูลแผ่นดินไหวล่าสุด"
- "หาแผ่นดินไหวที่มีขนาดมากกว่า 4 ริกเตอร์"
- "มีแผ่นดินไหวที่ประเทศเมียนมาบ้างไหม"
- "สรุปสถิติแผ่นดินไหวให้หน่อย"
- "แผ่นดินไหววันนี้มีกี่ครั้ง"
- "หาแผ่นดินไหวขนาดใหญ่ที่อาจเป็นอันตราย"

### English
- "Show me recent earthquakes"
- "Find earthquakes with magnitude 4 or higher"
- "Are there any earthquakes in Myanmar?"
- "Give me a summary of earthquake activity"
- "Show today's earthquakes"
- "Find large earthquakes that might be dangerous"

## 📊 API Reference

### Tools

#### `get_earthquakes(limit: int = 10)`
ดึงข้อมูลแผ่นดินไหวล่าสุด
- **limit**: จำนวนรายการสูงสุดที่ต้องการ (default: 10)
- **Returns**: รายการแผ่นดินไหวพร้อมรายละเอียด

#### `get_earthquakes_by_magnitude(min_magnitude: float = 3.0)`
กรองแผ่นดินไหวตามขนาด magnitude
- **min_magnitude**: ขนาด magnitude ขั้นต่ำ (default: 3.0)
- **Returns**: แผ่นดินไหวที่มีขนาดตามที่กำหนด

#### `get_earthquakes_by_location(location: str)`
ค้นหาแผ่นดินไหวตามสถานที่
- **location**: ชื่อสถานที่/ประเทศ (ภาษาไทยหรืออังกฤษ)
- **Returns**: แผ่นดินไหวในพื้นที่ที่ระบุ

#### `get_earthquake_summary()`
สรุปสถิติแผ่นดินไหว
- **Returns**: สถิติรวม, ขนาดเฉลี่ย, การกระจายตามพื้นที่

#### `get_large_earthquakes(magnitude_threshold: float = 5.0)`
หาแผ่นดินไหวขนาดใหญ่
- **magnitude_threshold**: เกณฑ์ขนาดแผ่นดินไหว (default: 5.0)
- **Returns**: แผ่นดินไหวที่มีขนาดเกินเกณฑ์

### Resources

#### `earthquake://latest`
- **Returns**: ข้อมูลแผ่นดินไหวล่าสุด 1 รายการ

#### `earthquake://today`
- **Returns**: แผ่นดินไหวทั้งหมดในวันนี้ (เวลาไทย)

## 🔧 การแก้ปัญหา

### Server ไม่ปรากฏใน Claude Desktop

1. **ตรวจสอบ Python:**
```bash
python --version
# ต้องเป็น Python 3.10 หรือสูงกว่า
```

2. **ตรวจสอบ dependencies:**
```bash
pip list | findstr mcp
# ต้องมี mcp package
```

3. **ดู logs:**
```bash
# Windows
type %APPDATA%\Claude\logs\mcp*.log

# หรือเปิดด้วย notepad
notepad %APPDATA%\Claude\logs\mcp-server-tmd-earthquake.log
```

4. **ทดสอบ server โดยตรง:**
```bash
cd C:\Users\Asus\2025-Aug-APT_LLMs-for-Telecom\tmd-earthquake-server-1.0
python server.py
```

### Error Messages ที่พบบ่อย

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| `ModuleNotFoundError: No module named 'mcp'` | ยังไม่ได้ติดตั้ง MCP | รัน `pip install "mcp[cli]"` |
| `ModuleNotFoundError: No module named 'httpx'` | ยังไม่ได้ติดตั้ง httpx | รัน `pip install httpx` |
| `Connection timeout` | ไม่สามารถเชื่อมต่อ TMD API | ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต |
| `Server not responding` | Path ใน config ไม่ถูกต้อง | ตรวจสอบ path ใน claude_desktop_config.json |

### วิธีตรวจสอบว่า Server ทำงาน

1. ใน Claude Desktop ต้องมีไอคอน 🔌 หรือ ⚡
2. พิมพ์ "Show MCP tools" ใน Claude
3. ต้องเห็น tools ของ tmd-earthquake server

## 📊 แหล่งข้อมูล

- **API Provider**: กรมอุตุนิยมวิทยา (Thai Meteorological Department)
- **API Endpoint**: https://data.tmd.go.th/api/DailySeismicEvent/v1/
- **Update Frequency**: Real-time
- **Coverage**: ภูมิภาคและทั่วโลก

## 📄 License

This server is for educational and informational purposes. The earthquake data is provided by TMD.

## 🤝 Contributing

หากพบปัญหาหรือต้องการเพิ่ม features สามารถ:
1. สร้าง Issue
2. Submit Pull Request
3. ติดต่อผู้พัฒนา

## 📞 Support

หากต้องการความช่วยเหลือ:
- ตรวจสอบ [การแก้ปัญหา](#-การแก้ปัญหา) ก่อน
- ดู logs ใน `%APPDATA%\Claude\logs\`
- ทดสอบ server โดยตรงด้วย `python server.py`

---

**Version**: 1.0.0  
**Last Updated**: 2025-08-15  
**Developed for**: TMD Earthquake Data Access via MCP
