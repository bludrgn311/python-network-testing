# Network Testing Tool

A Python program that tests network connectivity and latency to any host or IP address. The tool performs comprehensive network diagnostics and outputs results to a text file.

## Features

- **DNS Resolution Testing**: Verifies hostname resolution with error reporting and response time measurement
- **Ping Testing**: Tests ICMP connectivity with detailed statistics including:
  - Successful and failed packet counts
  - Packet loss percentage
  - Min/Max/Average latency
  - Partial failure detection
- **TCP Connection Testing**: Tests specific port connectivity with:
  - Response times
  - HTTP/HTTPS status code detection (ports 80, 443, 8080, 8443)
  - SSL/TLS support for HTTPS connections
- **Security Hardened**: Input validation to prevent command injection and path traversal attacks
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Detailed Reporting**: Saves comprehensive results to timestamped text files in the `output/` folder
- **Container Ready**: Includes Dockerfile for containerized network testing

## Usage

### Command Line Interface

```bash
# Basic usage - test a website
python network_tester.py google.com

# Test with custom output filename (automatically timestamped, saved to output/ folder)
python network_tester.py google.com -o my_test_results.txt

# Test specific ports
python network_tester.py example.com -p 80 443 8080

# Send more ping packets
python network_tester.py 8.8.8.8 -c 10

# Combine options (results saved to output/github_test_YYYYMMDD_HHMMSS.txt)
python network_tester.py github.com -o github_test.txt -p 22 80 443 -c 5
```

### Programmatic Usage

```python
from network_tester import NetworkTester

# Create tester instance (results will be saved to output/results_YYYYMMDD_HHMMSS.txt)
tester = NetworkTester("example.com", "results.txt")

# Run comprehensive test
tester.run_full_test(tcp_ports=[80, 443, 22], ping_count=5)

# Save results
tester.save_results()
```

## Command Line Arguments

- `host`: Target hostname or IP address (required, validated for security)
- `-o, --output`: Output filename for results (automatically timestamped and saved to output/ folder, default: network_test_results.txt)
- `-p, --ports`: TCP ports to test (default: 80 443, valid range: 1-65535)
- `-c, --count`: Number of ping packets to send (default: 4, valid range: 1-1000)

## Output File Naming

All output files are automatically timestamped to prevent overwrites and maintain a history of tests:
- Format: `filename_YYYYMMDD_HHMMSS.ext`
- Example: `network_test_results_20241015_143025.txt`
- Files are saved in the `output/` directory

## Example Output

The tool generates detailed text reports like this:

```
============================================================
NETWORK TEST RESULTS FOR GOOGLE.COM
============================================================
Test completed at: 2024-01-15 14:30:25

Test 1: DNS Resolution
----------------------------------------
Timestamp: 2024-01-15 14:30:20
Status: PASS
Hostname: google.com
Resolved IP: 142.250.191.14
Response Time: 15.23ms

Test 2: Ping Test
----------------------------------------
Timestamp: 2024-01-15 14:30:21
Status: PASS
Packets Sent: 4
Packets Received: 4
Packets Successful: 4
Packets Failed: 0
Packet Loss: 0.0%
Min Latency: 12.1ms
Max Latency: 18.7ms
Avg Latency: 14.8ms

Test 3: TCP Connection
----------------------------------------
Timestamp: 2024-01-15 14:30:23
Status: PASS
Port: 443
Response Time: 45.67ms
HTTP Status Code: 200
```

### Console Output

The tool also provides real-time console output:

```
Starting network tests for google.com...
Testing DNS resolution...
DNS resolved to: 142.250.191.14
Running ping test (4 packets)...
Ping results - Successful: 4, Failed: 0, Packet loss: 0.0%
Latency - Avg: 14.8ms, Min: 12.1ms, Max: 18.7ms
Status: All 4 pings successful
Testing TCP connection on port 443...
TCP connection to port 443 successful - Response time: 45.67ms, HTTP Status: 200
Results saved to: output/network_test_results_20241015_143025.txt
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Running the Examples

```bash
# Run the example script
python example_usage.py
```

This will test both Google's DNS server and google.com, creating separate result files for each test.

## Docker Container

The tool is available as a container image based on Amazon Linux 2023. See [DOCKER_USAGE.md](DOCKER_USAGE.md) for detailed instructions.

### Quick Start with Docker

```bash
# Build the container
docker build -t network-tester:latest .

# Run a test
docker run --rm network-tester:latest google.com

# Save results to host
docker run --rm -v $(pwd)/results:/app/output network-tester:latest google.com
```

## Security Features

- **Input Validation**: Hostnames are validated to prevent command injection attacks
- **Path Traversal Protection**: Output filenames are sanitized to prevent directory traversal
- **Resource Limits**: Ping count and port numbers are validated to prevent resource exhaustion
- **SSL/TLS Verification**: HTTPS connections verify certificates by default
- **Safe Error Handling**: Specific exception handling prevents information leakage

## Troubleshooting

### Ping Test Timeouts

If you experience timeouts with large ping counts, the tool automatically adjusts the timeout based on the number of pings (2 seconds per ping + 10 second buffer).

### SSL Certificate Errors

For HTTPS connections, the tool verifies SSL certificates. Self-signed certificates will cause the HTTP status code to be unavailable, but the TCP connection test will still succeed.

### DNS Resolution Failures

DNS errors are captured and reported in both console and file output with detailed error messages.