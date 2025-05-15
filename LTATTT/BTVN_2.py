from scapy.all import *
import socket
import ssl
import time
from concurrent.futures import ThreadPoolExecutor
from prettytable import PrettyTable

# Danh sách cổng cần quét
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389,8080]

# Danh sách dịch vụ phổ biến
SERVICE_DICT = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    135: "msrpc",
    139: "netbios-ssn",
    143: "imap",
    443: "ssl/http",
    445: "microsoft-ds",
    3306: "mysql",
    3389: "ms-wbt-server",
    8080: "http"
}

def scan_port(target_ip, port):
    """Thử nhiều cách quét (SYN Scan + TCP Connect Scan)"""
    try:
        # 🛠 SYN Scan (Gửi SYN, chờ SYN-ACK)
        syn_packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
        response = sr1(syn_packet, timeout=1, verbose=False)

        if response is None:
            return "Filtered"
        elif response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK (Cổng mở)
                sr(IP(dst=target_ip) / TCP(dport=port, flags="R"), timeout=1, verbose=False)  # Gửi RST để đóng kết nối
                return "Open"
            elif response[TCP].flags == 0x14:  # RST-ACK (Cổng đóng)
                return "Closed"
        
        # 🔥 Nếu SYN scan không thành công => Dùng TCP Connect
        with socket.create_connection((target_ip, port), timeout=2) as s:
            return "Open"
    except:
        return "Filtered"

def grab_banner(target_ip, port):
    """Banner Grabbing bằng nhiều cách"""
    try:
        with socket.create_connection((target_ip, port), timeout=2) as s:
            if port == 443:
                s = ssl.wrap_socket(s)

            # Gửi nhiều kiểu request để lấy banner
            if port in [21, 22, 25, 110, 143]:  
                time.sleep(0.5)  # Chờ server gửi banner trước
                banner = s.recv(1024).decode(errors="ignore").strip()
            elif port in [80, 443]:  
                s.sendall(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
            else:  
                s.sendall(b"\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()

            return banner if len(banner) <= 50 else banner[:47] + "..."
    except:
        return "N/A"

def scan_worker(target_ip, port):
    """Dùng trong ThreadPool để quét nhanh hơn"""
    state = scan_port(target_ip, port)
    banner = grab_banner(target_ip, port) if state == "Open" else "N/A"
    service_name = SERVICE_DICT.get(port, "Unknown")
    return [port, state, service_name, banner]

def main():
    target_ip = input("Nhập địa chỉ IP cần quét: ")

    table = PrettyTable()
    table.field_names = ["Port", "State", "Service", "Banner"]
    table.align["Port"] = "c"
    table.align["State"] = "l"
    table.align["Service"] = "l"
    table.align["Banner"] = "l"

    # 🔥 Dùng ThreadPool để quét nhanh hơn
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda p: scan_worker(target_ip, p), PORTS_TO_SCAN))

    for row in results:
        table.add_row(row)
    
    print(table)

if __name__ == "__main__":
    main()
#quét cổng mạng và lấy thông tin banner của các dịch vụ phổ biến trên các cổng cụ thể
