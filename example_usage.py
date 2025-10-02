#!/usr/bin/env python3
"""
Example usage of the NetworkTester class
"""

from network_tester import NetworkTester

def main():
    # Test Google's DNS server
    print("Testing connectivity to Google DNS (8.8.8.8)...")
    tester = NetworkTester("8.8.8.8", "google_dns_test.txt")
    tester.run_full_test(tcp_ports=[53], ping_count=5)
    tester.save_results()
    
    print("\n" + "="*50 + "\n")
    
    # Test a website
    print("Testing connectivity to google.com...")
    tester2 = NetworkTester("google.com", "google_web_test.txt")
    tester2.run_full_test(tcp_ports=[80, 443], ping_count=4)
    tester2.save_results()

if __name__ == "__main__":
    main()