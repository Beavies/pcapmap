# pcapmap
Graphic conversations of wireshark (pcap file) with graphviz

## Trafic_map.py
Python script with 2 parameters:
 - param 1 = Export Wireshark conversations to CSV file (with ';' as separator)
 - param 2 = dictionary to print names and not IP. Format: <Name>;<IP> per line

It generates a dot file to use with graphviz

## Linux_parse_pcap.sh
Bash script with 2 parameters
 - param 1 = pcap file that tcpdump can read
 - param 2 = output file
 
It creates a dot file with simple traffic relations

## Parse_tcpdump_2_ip_mac.sh
Bash script to read pcap file and output IP and MAC addresses
