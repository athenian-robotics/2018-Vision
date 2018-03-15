import cv2
import socket
import sys
import numpy as np
import struct

BUF_LEN = 65540  # Bigger than the max UDP packet size
PACK_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servPort = int(sys.argv[1])
sock.bind(('', servPort))

srcAddr = ""
srcPort = total_pack = width = height = 0

while ";;":
    recv, srcAddr = sock.recvfrom(BUF_LEN)
    try:
        # This is the number of packets that will make the frame
        # Convert recv (# of packets) to a little endian integer
        dat = struct.unpack('<I', recv)[0]
        total_pack = dat & 0xFF

    except:
        # looks like we don't have the "header", keep going until we get one
        print('BORK')
        continue

    buf = []
    for i in range(total_pack):
        recv, _ = sock.recvfrom(BUF_LEN)
        if (len(recv) != PACK_SIZE):
            print("Received unexpected packet size: {}".format(len(recv)), file=sys.stderr)
        # Put each byte as its own element of the buffer
        buf.append(bytearray(recv))

    raw_data = np.array(buf)
    print(len(buf))
    img_np = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)
    if img_np.shape[0] == 0:
        print("empty image")
        continue
    cv2.imshow("IMG", img_np)
    if cv2.waitKey(1) == 27:
        break
