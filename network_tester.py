#!/usr/bin/env python3
"""
Network Testing Tool
A simple tool to test connectivity and latency to remote hosts.
"""

import socket
import subprocess
import time
import argparse
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class NetworkTester:
    def __init__(self, target_host: str, output_file: str = "network_test_results.txt"):
        self.target_host = target_host
        # Ensure output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Add timestamp to filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename, ext = os.path.splitext(output_file)
        timestamped_filename = f"{filename}_{timestamp}{ext}"
        
        # Set output file path to output folder with timestamp
        self.output_file = os.path.join(output_dir, timestamped_filename)
        self.results = []
        
    def resolve_hostname(self) -> Optional[str]:
        """Resolve hostname to IP address."""
        try:
            ip_address = socket.gethostbyname(self.target_host)
            return ip_address
        except socket.gaierror as e:
            return None
    
    def test_tcp_connection(self, port: int = 80, timeout: int = 5) -> Dict:
        """Test TCP connection to target host."""
        result = {
            'test_type': 'TCP Connection',
            'port': port,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'success': False,
            'response_time': None,
            'error': None
        }
        
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            connection_result = sock.connect_ex((self.target_host, port))
            end_time = time.time()
            
            if connection_result == 0:
                result['success'] = True
                result['response_time'] = round((end_time - start_time) * 1000, 2)  # ms
            else:
                result['error'] = f"Connection failed (error code: {connection_result})"
                
            sock.close()
            
        except Exception as e:
            result['error'] = str(e)
            
        return result 
   
    def ping_test(self, count: int = 4) -> Dict:
        """Perform ping test to target host."""
        result = {
            'test_type': 'Ping Test',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'packets_sent': count,
            'packets_received': 0,
            'packet_loss': 0,
            'min_latency': None,
            'max_latency': None,
            'avg_latency': None,
            'success': False,
            'error': None
        }
        
        try:
            # Windows ping command
            if sys.platform.startswith('win'):
                cmd = ['ping', '-n', str(count), self.target_host]
            else:
                # Linux/Mac ping command
                cmd = ['ping', '-c', str(count), self.target_host]
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if process.returncode == 0:
                output = process.stdout
                result['success'] = True
                
                # Parse ping results (basic parsing)
                lines = output.split('\n')
                latencies = []
                
                for line in lines:
                    if 'time=' in line or 'time<' in line:
                        try:
                            # Extract time value
                            if 'time=' in line:
                                time_part = line.split('time=')[1].split('ms')[0]
                            else:  # time<
                                time_part = line.split('time<')[1].split('ms')[0]
                            latencies.append(float(time_part))
                        except (IndexError, ValueError):
                            continue
                
                if latencies:
                    result['packets_received'] = len(latencies)
                    result['packet_loss'] = round(((count - len(latencies)) / count) * 100, 1)
                    result['min_latency'] = round(min(latencies), 2)
                    result['max_latency'] = round(max(latencies), 2)
                    result['avg_latency'] = round(sum(latencies) / len(latencies), 2)
                    
            else:
                result['error'] = f"Ping failed: {process.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            result['error'] = "Ping test timed out"
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    def test_dns_resolution(self) -> Dict:
        """Test DNS resolution for the target host."""
        result = {
            'test_type': 'DNS Resolution',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hostname': self.target_host,
            'resolved_ip': None,
            'success': False,
            'response_time': None,
            'error': None
        }
        
        try:
            start_time = time.time()
            ip_address = socket.gethostbyname(self.target_host)
            end_time = time.time()
            
            result['success'] = True
            result['resolved_ip'] = ip_address
            result['response_time'] = round((end_time - start_time) * 1000, 2)  # ms
            
        except socket.gaierror as e:
            result['error'] = f"DNS resolution failed: {str(e)}"
        except Exception as e:
            result['error'] = str(e)
            
        return result    

    def run_full_test(self, tcp_ports: List[int] = None, ping_count: int = 4) -> List[Dict]:
        """Run a comprehensive network test."""
        if tcp_ports is None:
            tcp_ports = [80, 443]  # Default HTTP and HTTPS ports
            
        print(f"Starting network tests for {self.target_host}...")
        
        # DNS Resolution Test
        print("Testing DNS resolution...")
        dns_result = self.test_dns_resolution()
        self.results.append(dns_result)
        
        if not dns_result['success']:
            print(f"DNS resolution failed: {dns_result['error']}")
            return self.results
        
        print(f"DNS resolved to: {dns_result['resolved_ip']}")
        
        # Ping Test
        print(f"Running ping test ({ping_count} packets)...")
        ping_result = self.ping_test(ping_count)
        self.results.append(ping_result)
        
        if ping_result['success']:
            print(f"Ping successful - Avg latency: {ping_result['avg_latency']}ms, "
                  f"Packet loss: {ping_result['packet_loss']}%")
        else:
            print(f"Ping failed: {ping_result['error']}")
        
        # TCP Connection Tests
        for port in tcp_ports:
            print(f"Testing TCP connection on port {port}...")
            tcp_result = self.test_tcp_connection(port)
            self.results.append(tcp_result)
            
            if tcp_result['success']:
                print(f"TCP connection to port {port} successful - "
                      f"Response time: {tcp_result['response_time']}ms")
            else:
                print(f"TCP connection to port {port} failed: {tcp_result['error']}")
        
        return self.results
    
    def save_results(self) -> None:
        """Save test results to output file."""
        try:
            with open(self.output_file, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write(f"NETWORK TEST RESULTS FOR {self.target_host.upper()}\n")
                f.write("=" * 60 + "\n")
                f.write(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for i, result in enumerate(self.results, 1):
                    f.write(f"Test {i}: {result['test_type']}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Timestamp: {result['timestamp']}\n")
                    f.write(f"Status: {'PASS' if result['success'] else 'FAIL'}\n")
                    
                    if result['test_type'] == 'DNS Resolution':
                        if result['success']:
                            f.write(f"Hostname: {result['hostname']}\n")
                            f.write(f"Resolved IP: {result['resolved_ip']}\n")
                            f.write(f"Response Time: {result['response_time']}ms\n")
                        else:
                            f.write(f"Error: {result['error']}\n")
                    
                    elif result['test_type'] == 'Ping Test':
                        if result['success']:
                            f.write(f"Packets Sent: {result['packets_sent']}\n")
                            f.write(f"Packets Received: {result['packets_received']}\n")
                            f.write(f"Packet Loss: {result['packet_loss']}%\n")
                            f.write(f"Min Latency: {result['min_latency']}ms\n")
                            f.write(f"Max Latency: {result['max_latency']}ms\n")
                            f.write(f"Avg Latency: {result['avg_latency']}ms\n")
                        else:
                            f.write(f"Error: {result['error']}\n")
                    
                    elif result['test_type'] == 'TCP Connection':
                        f.write(f"Port: {result['port']}\n")
                        if result['success']:
                            f.write(f"Response Time: {result['response_time']}ms\n")
                        else:
                            f.write(f"Error: {result['error']}\n")
                    
                    f.write("\n")
                
            print(f"Results saved to: {self.output_file}")
            
        except Exception as e:
            print(f"Error saving results: {e}")


def main():
    parser = argparse.ArgumentParser(description='Network connectivity and latency tester')
    parser.add_argument('host', help='Target hostname or IP address')
    parser.add_argument('-o', '--output', default='network_test_results.txt',
                       help='Output filename for results (saved to output/ folder, default: network_test_results.txt)')
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[80, 443],
                       help='TCP ports to test (default: 80 443)')
    parser.add_argument('-c', '--count', type=int, default=4,
                       help='Number of ping packets to send (default: 4)')
    
    args = parser.parse_args()
    
    # Create and run network tester
    tester = NetworkTester(args.host, args.output)
    tester.run_full_test(tcp_ports=args.ports, ping_count=args.count)
    tester.save_results()


if __name__ == "__main__":
    main()