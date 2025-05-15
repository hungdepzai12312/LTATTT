import os
import socket
 
# host to listen on
HOST = '192.168.56.1'
def main():
    # create raw socket, bin to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
 
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    # include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
 
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
 
    # read one packet
    print(sniffer.recvfrom(65565))
 
    # if we're on Windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
 
if __name__ == '__main__':
    main()
#Đoạn mã trên tạo một packet sniffer (máy bắt gói tin) sử dụng raw socket để nghe và ghi lại các gói tin mạng.
#Cụ thể, nó sẽ lắng nghe trên giao diện mạng của máy tính với một địa chỉ IP xác định (ở đây là 192.168.56.1).