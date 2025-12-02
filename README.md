# Network Testing Tool

A Python program that tests network connectivity and latency to any host or IP address. The tool performs comprehensive network diagnostics and outputs results to a text file.

## Features

- **DNS Resolution Testing**: Verifies hostname resolution and measures response time
- **Ping Testing**: Tests ICMP connectivity with packet loss and latency statistics
- **TCP Connection Testing**: Tests specific port connectivity with response times
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Detailed Reporting**: Saves comprehensive results to timestamped text files in the ```output/``` folder

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

- `host`: Target hostname or IP address (required)
- `-o, --output`: Output filename for results (automatically timestamped and saved to output/ folder, default: network_test_results.txt)
- `-p, --ports`: TCP ports to test (default: 80 443)
- `-c, --count`: Number of ping packets to send (default: 4)

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
Packet Loss: 0.0%
Min Latency: 12.1ms
Max Latency: 18.7ms
Avg Latency: 14.8ms

Test 3: TCP Connection
----------------------------------------
Timestamp: 2024-01-15 14:30:23
Status: PASS
Port: 80
Response Time: 45.67ms
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