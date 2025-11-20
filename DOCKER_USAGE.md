# Network Tester Container Image

This container image is based on Amazon Linux 2023 and includes the network_tester.py tool along with all necessary network utilities.

## Building the Image

```bash
docker build -t network-tester:latest .
```

## Running the Container

### Basic Usage

Test a host with default settings (ports 80, 443):
```bash
docker run --rm network-tester:latest google.com
```

### Custom Ports

Test specific ports:
```bash
docker run --rm network-tester:latest google.com -p 80 443 8080
```

### Custom Ping Count

Specify number of ping packets:
```bash
docker run --rm network-tester:latest google.com -c 10
```

### Save Results to Host

Mount a volume to save results to your host machine:
```bash
docker run --rm -v $(pwd)/results:/app/output network-tester:latest google.com
```

On Windows (PowerShell):
```powershell
docker run --rm -v ${PWD}/results:/app/output network-tester:latest google.com
```

On Windows (CMD):
```cmd
docker run --rm -v %cd%/results:/app/output network-tester:latest google.com
```

### Interactive Shell

Access the container shell for manual testing:
```bash
docker run --rm -it --entrypoint /bin/bash network-tester:latest
```

### Run as Static Container (Long-Running)

Run the container in the background and exec into it for manual network testing:

```bash
# Start the container in detached mode with sleep to keep it running
docker run -d --name network-tester-static --entrypoint sleep network-tester:latest infinity

# Exec into the running container
docker exec -it network-tester-static /bin/bash

# When done, stop and remove the container
docker stop network-tester-static
docker rm network-tester-static
```

Once inside the container, you can run any network commands:
```bash
# Run the network tester manually
python3 /app/network_tester.py google.com -p 80 443

# Or use any of the included network tools
ping -c 4 google.com
traceroute google.com
dig google.com
nslookup google.com
curl -I https://google.com
nc -zv google.com 443
```

## Included Network Tools

The container includes the following network utilities:
- `ping` - ICMP echo requests
- `traceroute` - Trace network path
- `nslookup` / `dig` - DNS lookup tools
- `netstat` - Network statistics
- `ip` - IP configuration
- `tcpdump` - Packet analyzer
- `nc` (ncat) - Network connections
- `telnet` - Telnet client
- `wget` / `curl` - HTTP clients

## Examples

### Test multiple hosts
```bash
docker run --rm network-tester:latest example.com -p 80 443
docker run --rm network-tester:latest 8.8.8.8 -p 53
```

### Test with custom output filename
```bash
docker run --rm -v $(pwd)/results:/app/output network-tester:latest google.com -o custom_test.txt
```

### Run in Kubernetes
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-tester
spec:
  containers:
  - name: network-tester
    image: network-tester:latest
    command: ["python3", "/app/network_tester.py"]
    args: ["google.com", "-p", "80", "443"]
```

## Pushing to a Registry

### Amazon ECR
```bash
# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag the image
docker tag network-tester:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/network-tester:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/network-tester:latest
```

### Docker Hub
```bash
docker tag network-tester:latest <username>/network-tester:latest
docker push <username>/network-tester:latest
```
