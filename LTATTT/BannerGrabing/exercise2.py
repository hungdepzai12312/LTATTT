from scapy.all import *

ip = "192.168.21.1"
ports = [22,53,80] # Danh sách các cổng được giám sát
honeys = [8080,8443] # Danh sách các cổng mồi nhử (honeypot) để phát hiện các kết nối bất thường (HTTP proxy, HTTPS)

blocked = [] # Danh sách các địa chỉ IP bị chặn

def analyzePackets(p):
    print("Gói nhận được!")
    global blocked
    if p.haslayer(IP): # kiểm tra gói tin chứa IP không
        response = Ether(src=p[Ether].dst,dst=p[Ether].src)/\
            IP(src=p[IP].dst,dst=p[IP].src)/\
            TCP(sport=p[TCP].dport,dport=p[TCP].sport,ack=p[TCP].seq+1)
        source = p[IP].src
    else:
        response = Ether(src=p[Ether].dst,dst=p[Ether].src)/\
            IPv6(src=p[IPv6].dst,dst=p[IPv6].src)/\
            TCP(sport=p[TCP].dport,dport=p[TCP].sport,ack=p[TCP].seq+1)
        source = p[IPv6].src
        
    port = p[TCP].dport
    if port in honeys:
        p.show()
    if source in blocked:
        if port in ports:
            response[TCP].flags = "RA"
        elif port in honeys: 
            response[TCP].flags = "SA"
        sendp(response,verbose=False)
    else:
        if source not in ports:
            blocked += source
            if port in honeys:
                response[TCP].flags = "SA"
                sendp(response,verbose=False)

f = "dst host "+ip+" and tcp"
sniff(filter=f,prn=analyzePackets)
#Đoạn mã sẽ bắt đầu giám sát các kết nối TCP đến và đi từ địa chỉ IP mà bạn chỉ định (ip = "192.168.21.1").

#Nếu có kết nối đến các cổng mồi nhử (honeypots) như 8080 hoặc 8443, các gói tin đó sẽ được hiển thị.


#Nếu một địa chỉ IP cố gắng kết nối đến các cổng không mong muốn, địa chỉ đó sẽ bị chặn.
