#!/usr/bin/env python3
"""Creates servers.dat so your server shows up in the multiplayer list.
Usage: python make_servers_dat.py "My Server" play.example.com
"""
import struct, sys

def tag_string(name, value):
    n, v = name.encode(), value.encode()
    return b"\x08" + struct.pack(">H", len(n)) + n + struct.pack(">H", len(v)) + v

def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    display, address = sys.argv[1], sys.argv[2]
    server = tag_string("name", display) + tag_string("ip", address) + b"\x00"
    servers_list = b"\x09" + struct.pack(">H", 7) + b"servers" + b"\x0a" + struct.pack(">i", 1) + server
    root = b"\x0a" + struct.pack(">H", 0) + servers_list + b"\x00"
    with open("servers.dat", "wb") as f:
        f.write(root)
    print(f"servers.dat created for {display} ({address})")

if __name__ == "__main__":
    main()
