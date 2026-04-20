# 🌐 Webserv - HTTP/1.1 Server Implementation

<div align="center">

![C++](https://img.shields.io/badge/C++-98-blue.svg?style=flat&logo=c%2B%2B)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![42 School](https://img.shields.io/badge/42-Project-black.svg)

**A robust, non-blocking HTTP/1.1 server built in C++98 for the 42 curriculum**

[Features](#-features) •
[Installation](#-installation) •
[Configuration](#-configuration) •
[Testing](#-testing) •
[Documentation](#-documentation)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Overview

**Webserv** is a custom HTTP/1.1 server implementation written in C++98, developed as part of the 42 School curriculum. It demonstrates deep understanding of network programming, HTTP protocol, and system-level programming in C++.

### Why Webserv?

- 🚀 **High Performance**: Non-blocking I/O using `poll()` for efficient handling of multiple connections
- 🔒 **Secure**: Proper request validation, timeout handling, and resource limits
- 🎨 **Flexible**: NGINX-style configuration for easy customization
- 📦 **Complete**: Full HTTP/1.1 support including GET, POST, DELETE, CGI, file uploads, and more
- 🧪 **Well-Tested**: Comprehensive test suite with 100% coverage of core functionality

### Quick Start

```bash
# Clone and compile
git clone https://github.com/yourusername/webserv.git
cd webserv
make

# Run server
./webserv webserv.conf

# Test
./complete_test.py
```

---

## ✨ Features

### HTTP Protocol Support

<table>
<tr>
<td width="50%">

#### Core Features
- ✅ HTTP/1.0 and HTTP/1.1
- ✅ Keep-alive connections
- ✅ Chunked transfer encoding
- ✅ Multiple simultaneous connections
- ✅ Request timeout handling (60s default)
- ✅ URL decoding
- ✅ Query string parsing

</td>
<td width="50%">

#### HTTP Methods
- ✅ **GET** - Retrieve resources
- ✅ **POST** - Submit data / Upload files
- ✅ **DELETE** - Remove resources
- ❌ **PUT** - Not implemented
- ❌ **PATCH** - Not implemented
- ✅ Error responses for unsupported methods (405)

</td>
</tr>
</table>

### Advanced Capabilities

<table>
<tr>
<td width="33%">

#### 📁 File Serving
- Static file delivery
- MIME type detection (20+ types)
- Directory index files
- Custom error pages
- Autoindex (directory listing)

</td>
<td width="33%">

#### 📤 File Upload
- Multipart form data
- Configurable size limits
- Upload path customization
- Content-Length validation
- 413 error on oversized uploads

</td>
<td width="33%">

#### ⚙️ CGI Support
- Python CGI execution
- PHP CGI execution
- Environment variables
- POST data handling
- Timeout protection (60s)

</td>
</tr>
</table>

### Server Configuration

- 🔧 **Multiple Server Blocks**: Run multiple virtual servers on different ports
- 🛣️ **Location Routing**: Flexible URL-based routing with longest-prefix matching
- 📏 **Request Size Limits**: Configurable `client_max_body_size`
- 🔄 **HTTP Redirects**: Support for 301/302 redirects
- 📂 **Directory Listing**: Automatic index generation (autoindex on/off)
- 🚫 **Method Restrictions**: Per-location HTTP method control
- 📄 **Custom Error Pages**: Configurable error pages for all HTTP status codes

### Error Handling

Comprehensive error page support for:
- **3xx Redirects**: 301 (Moved Permanently), 302 (Found)
- **4xx Client Errors**: 400 (Bad Request), 403 (Forbidden), 404 (Not Found), 405 (Method Not Allowed), 411 (Length Required), 413 (Payload Too Large)
- **5xx Server Errors**: 500 (Internal Server Error), 501 (Not Implemented)

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                         Webserv                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Config    │  │    Server    │  │   Request    │      │
│  │   Parser    │──│   Manager    │──│   Handler    │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│                           │                 │               │
│                    ┌──────┴─────┐    ┌─────┴──────┐       │
│                    │   poll()   │    │  Response  │       │
│                    │   Loop     │    │  Builder   │       │
│                    └────────────┘    └────────────┘       │
│                           │                 │               │
│         ┌─────────────────┼─────────────────┤              │
│         │                 │                 │               │
│    ┌────▼────┐     ┌─────▼──────┐    ┌────▼─────┐        │
│    │  File   │     │    CGI     │    │  Upload  │        │
│    │ Handler │     │  Executor  │    │  Handler │        │
│    └─────────┘     └────────────┘    └──────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Description | File |
|-----------|-------------|------|
| **Config** | Parses NGINX-style configuration | `Config.cpp` |
| **Server** | Manages server sockets and binding | `Server.cpp` |
| **Request** | HTTP request parser with validation | `Request.cpp` |
| **Response** | HTTP response builder | `Response.cpp` |
| **Route** | URL routing and matching | `Route.cpp` |
| **Client** | Client connection state management | `Client.cpp` |
| **CGI** | CGI script execution handler | `CGI.cpp` |
| **Main** | Event loop with poll() | `main.cpp` |

### Request Flow

```
1. Client connects → Socket accepted
2. Request received → Parse HTTP headers
3. Route matching → Find location block
4. Method validation → Check allowed methods
5. Resource handling:
   ├─ Static file → Serve from filesystem
   ├─ CGI script → Execute and capture output
   ├─ Upload → Save to configured path
   └─ Redirect → Send 301/302 response
6. Response built → Send to client
7. Connection → Keep-alive or close
```

---

## 🚀 Installation

### Prerequisites

- **C++ Compiler**: g++ or clang++ with C++98 support
- **Make**: GNU Make 3.81 or higher
- **Operating System**: Linux or macOS
- **Python 3**: For CGI support (optional)
- **PHP**: For PHP CGI support (optional)

### Build from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/webserv.git
cd webserv

# Compile
make

# Run
./webserv webserv.conf
```

### Compilation Options

```bash
make              # Build with default settings
make clean        # Remove object files
make fclean       # Remove all build artifacts
make re           # Rebuild from scratch
```

### Build Flags

The project compiles with strict flags for code quality:
```makefile
CXXFLAGS = -Wall -Wextra -Werror -std=c++98
```

---

## ⚙️ Configuration

### Configuration File Format

Webserv uses an NGINX-inspired configuration syntax:

```nginx
server {
    listen 8080;                          # Port to bind
    server_name localhost;                # Server name
    client_max_body_size 10M;            # Max request body size
    
    # Custom error pages
    error_page 404 www/errors/404.html;
    error_page 500 www/errors/500.html;
    
    # Root location
    location / {
        methods GET POST;                 # Allowed HTTP methods
        root www;                         # Document root
        index index.html;                 # Default index file
        autoindex off;                    # Directory listing
    }
    
    # File uploads
    location /uploads {
        methods GET POST;
        root www;
        upload_path www/uploads;          # Upload destination
    }
    
    # CGI scripts
    location /cgi-bin {
        methods GET POST;
        root cgi-bin;
        cgi .py /usr/bin/python3;        # Python CGI
        cgi .php /usr/bin/php-cgi;       # PHP CGI
    }
    
    # Redirect
    location /redirect {
        redirect https://example.com;
    }
    
    # Autoindex (directory listing)
    location /files {
        methods GET;
        root www;
        autoindex on;                     # Enable directory listing
    }
}
```

### Configuration Directives

#### Server Block Directives

| Directive | Description | Example |
|-----------|-------------|---------|
| `listen` | Port number to bind | `listen 8080;` |
| `server_name` | Virtual host name | `server_name example.com;` |
| `client_max_body_size` | Max request body size | `client_max_body_size 10M;` |
| `error_page` | Custom error page | `error_page 404 /404.html;` |

#### Location Block Directives

| Directive | Description | Example |
|-----------|-------------|---------|
| `methods` | Allowed HTTP methods | `methods GET POST DELETE;` |
| `root` | Document root directory | `root /var/www;` |
| `index` | Default index file | `index index.html;` |
| `autoindex` | Enable directory listing | `autoindex on;` |
| `upload_path` | File upload destination | `upload_path /uploads;` |
| `cgi` | CGI handler mapping | `cgi .py /usr/bin/python3;` |
| `redirect` | HTTP redirect URL | `redirect https://example.com;` |

---

## 🎮 Usage

### Starting the Server

```bash
# Basic usage
./webserv webserv.conf

# Custom configuration
./webserv path/to/custom.conf
```

### Server Output

```
Config file: webserv.conf
Parsed 2 server block(s)
Server 'localhost' listening on 0.0.0.0:8080
Server 'test' listening on 0.0.0.0:9090
Server initialized with 2 listening socket(s)
Server running... Press Ctrl+C to stop
```

### Making Requests

```bash
# GET request
curl http://localhost:8080/

# GET with query string
curl http://localhost:8080/page?id=123&name=test

# POST request
curl -X POST -d "key=value" http://localhost:8080/upload

# File upload
curl -F "file=@document.pdf" http://localhost:8080/uploads

# DELETE request
curl -X DELETE http://localhost:8080/files/test.txt

# Directory listing (autoindex)
curl http://localhost:8080/files/

# CGI script
curl http://localhost:8080/cgi-bin/test.py

# CGI with query
curl "http://localhost:8080/cgi-bin/test.py?name=John&age=25"

# Test redirect
curl -L http://localhost:8080/redirect

# Headers inspection
curl -I http://localhost:8080/

# Verbose output
curl -v http://localhost:8080/
```

### Browser Testing

Open your browser and navigate to:

- **Homepage**: `http://localhost:8080/`
- **Directory listing**: `http://localhost:8080/autoindex_test/`
- **CGI script**: `http://localhost:8080/cgi-bin/test.py`
- **Error page**: `http://localhost:8080/nonexistent`
- **Redirect**: `http://localhost:8080/redirect`

---

## 🧪 Testing

### Automated Test Suite

The project includes a comprehensive test suite covering all functionality:

```bash
# Verify setup first
./verify_setup.sh

# Run all tests
./complete_test.py
```

### Test Coverage

The test suite includes **30+ automated tests** across 6 sections:

#### ✅ Section 1: Basic HTTP Operations (13 tests)
- GET requests (root, files, directories)  
- POST requests (with/without Content-Length)  
- DELETE requests (existing/non-existing files)  
- Error responses (404, 405, 411, 413)  
- Multiple server ports  
- File size limits  

#### ✅ Section 2: CGI Functionality (4 tests)
- Python CGI execution (10s delay test)
- Query string handling  
- Environment variables  
- Timeout protection (infinite loop test)

#### ✅ Section 3: Autoindex (Directory Listing)
- Autoindex enabled locations
- File listing display
- Directory navigation

#### ✅ Section 4: Redirects
- 301/302 HTTP redirects
- Internal redirects
- External redirects

#### ✅ Section 5: Error Pages
- 3xx redirects (301, 302)
- 4xx client errors (400, 403, 404, 405, 411, 413)
- 5xx server errors (500, 501)

#### ✅ Section 6: Performance (Siege tests)
- Concurrent connection handling  
- Load testing

### Manual Testing Examples

<details>
<summary><b>Autoindex Testing</b></summary>

```bash
# Test directory listing
curl http://127.0.0.1:8080/autoindex_test/

# Expected output: HTML with file listing
# - file1.html
# - file2.txt
# - data.json

# In browser
# Navigate to: http://localhost:8080/autoindex_test/
# Should see clickable file list
```
</details>

<details>
<summary><b>Redirect Testing</b></summary>

```bash
# Test external redirect
curl -I http://127.0.0.1:8080/redirect
# Expected: HTTP/1.1 301 Moved Permanently
# Location: https://github.com/42

# Test with follow redirects
curl -L http://127.0.0.1:8080/redirect

# Test internal redirect
curl -I http://127.0.0.1:8080/redirect-local
# Expected: Redirects to http://127.0.0.1:8080/
```
</details>

<details>
<summary><b>CGI Testing</b></summary>

```bash
# Python CGI (waits 10s)
time curl http://127.0.0.1:8080/cgi-bin/test.py
# Expected: "CGI worked" after ~10 seconds

# CGI with query string
curl "http://127.0.0.1:8080/cgi-bin/q.py?v=1&x=2"
# Expected: Display query string, script name, method

# CGI timeout test (infinite loop)
curl --max-time 65 http://127.0.0.1:8080/cgi-bin/loop.py
# Expected: Timeout after 60-65 seconds

# Non-executable file in CGI dir
curl -I http://127.0.0.1:8080/cgi-bin/hello.txt
# Expected: HTTP/1.1 403 Forbidden
```
</details>

<details>
<summary><b>Error Page Testing</b></summary>

```bash
# 404 Not Found
curl -I http://127.0.0.1:8080/does-not-exist
# Expected: HTTP/1.1 404 Not Found
# + Custom 404 error page

# 403 Forbidden
curl -I http://127.0.0.1:8080/cgi-bin/hello.txt
# Expected: HTTP/1.1 403 Forbidden
# + Custom 403 error page

# 405 Method Not Allowed
curl -I -X POST http://127.0.0.1:8080/files/test.txt
# Expected: HTTP/1.1 405 Method Not Allowed

# 411 Length Required
curl -X POST http://127.0.0.1:8080/upload
# Expected: HTTP/1.1 411 Length Required

# 413 Payload Too Large
dd if=/dev/zero of=2mb.bin bs=1M count=2
curl -F "file=@2mb.bin" http://127.0.0.1:9090/
# Expected: HTTP/1.1 413 Payload Too Large
# (port 9090 has 1M limit)
```
</details>

### Expected Test Results

```
======================================================================
TEST SUMMARY
======================================================================
✓ Passed:  30+
✗ Failed:   0
  Total:   30+

Success Rate: 100.0%

🎉 PERFECT SCORE! ALL TESTS PASSED! 🎉
```

---

## ⚡ Performance

### Key Features

- **Non-blocking I/O**: Single `poll()` loop handles all connections
- **Connection Pooling**: Reuse connections with keep-alive
- **Efficient Parsing**: Fast HTTP request parsing
- **Timeout Management**: 60s timeout prevents resource exhaustion
- **Configurable Limits**: Control memory and CPU usage

### Stress Test with Siege

```bash
# Install siege
sudo apt-get install siege  # Ubuntu
brew install siege           # macOS

# Moderate load test
siege -b -c 25 -r 200 http://127.0.0.1:8080/
# 25 concurrent users, 200 requests each = 5,000 total

# Heavy load test
siege -b -c 20 -r 1000 http://127.0.0.1:8080/
# 20 concurrent users, 1,000 requests each = 20,000 total

# Expected results:
# - Availability: > 99%
# - Response time: < 100ms
# - No failed transactions
```

---

## 🔧 Troubleshooting

### Common Issues

<details>
<summary><b>Server won't start - Port already in use</b></summary>

```bash
# Check what's using the port
lsof -i :8080

# Kill the process
kill -9 $(lsof -t -i:8080)

# Or use a different port
# Edit webserv.conf: listen 9090;
```
</details>

<details>
<summary><b>403 Forbidden on valid files</b></summary>

```bash
# Check file exists
ls -la www/files/test.txt

# Check permissions (should be readable)
chmod 644 www/files/test.txt

# Check directory permissions
chmod 755 www/files/

# Verify path in config
# Ensure root path matches actual directory
```
</details>

<details>
<summary><b>CGI scripts not working</b></summary>

```bash
# Make scripts executable
chmod +x cgi-bin/*.py

# Check shebang
head -n1 cgi-bin/test.py
# Must be: #!/usr/bin/python3

# Verify Python installation
which python3
/usr/bin/python3 --version

# Test script manually
./cgi-bin/test.py

# Check config has CGI mapping
# cgi .py /usr/bin/python3;
```
</details>

<details>
<summary><b>Autoindex not showing files</b></summary>

```bash
# Check autoindex is enabled in config
# location /files {
#     autoindex on;
# }

# Check directory has files
ls -la www/autoindex_test/

# Try in browser
# http://localhost:8080/autoindex_test/

# Check response
curl http://localhost:8080/autoindex_test/
```
</details>

<details>
<summary><b>Redirects not working</b></summary>

```bash
# Check redirect configuration
# location /redirect {
#     redirect https://example.com;
# }

# Test with curl (see headers)
curl -I http://localhost:8080/redirect

# Expected:
# HTTP/1.1 301 Moved Permanently
# Location: https://example.com

# Follow redirects
curl -L http://localhost:8080/redirect
```
</details>

### Debug Commands

```bash
# Check server is running
ps aux | grep webserv

# Monitor connections
lsof -i :8080

# Check config parsing
./webserv webserv.conf
# Should show: "Parsed 2 server block(s)"

# Test with minimal config
cat > test.conf << EOF
server {
    listen 8080;
    location / {
        methods GET;
        root www;
    }
}
EOF
./webserv test.conf
```

---

## 📄 License

This project is part of the 42 School curriculum.

---

## 🙏 Acknowledgments

- **42 School** - Project specifications
- **NGINX** - Configuration syntax inspiration
- **RFC 7230-7235** - HTTP/1.1 specification

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ for 42 School

</div>
