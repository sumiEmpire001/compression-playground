"""Explore lossless run-length encoding for binary files."""
import argparse
import json
from pathlib import Path


def encode(data):
    if not isinstance(data,bytes):
        raise TypeError("input must be bytes")
    output=bytearray(b"RLE1")
    for index in range(0,len(data)):
        if index and data[index]==data[index-1]:
            continue
        value=data[index]
        count=1
        while index+count<len(data) and data[index+count]==value and count<255:
            count+=1
        # Each run is encoded by a count and byte value.
        output.extend((count,value))
    return bytes(output)


def encode_runs(data):
    if not isinstance(data,bytes):
        raise TypeError("input must be bytes")
    output=bytearray(b"RLE1")
    position=0
    while position<len(data):
        value=data[position]
        count=1
        while position+count<len(data) and data[position+count]==value and count<255:
            count+=1
        output.extend((count,value))
        position+=count
    return bytes(output)


def decode(data,max_output=100_000_000):
    if not isinstance(data,bytes) or not data.startswith(b"RLE1") or (len(data)-4)%2:
        raise ValueError("invalid RLE data")
    output=bytearray()
    for index in range(4,len(data),2):
        count,value=data[index],data[index+1]
        if count==0:
            raise ValueError("zero-length run")
        if len(output)+count>max_output:
            raise ValueError("decoded size limit exceeded")
        output.extend(bytes([value])*count)
    return bytes(output)


def main():
    parser=argparse.ArgumentParser(description="Lossless run-length encoding demo")
    sub=parser.add_subparsers(dest="action",required=True)
    for action in ("compress","decompress"):
        command=sub.add_parser(action)
        command.add_argument("source")
        command.add_argument("target")
    args=parser.parse_args()
    source=Path(args.source).read_bytes()
    result=encode_runs(source) if args.action=="compress" else decode(source)
    Path(args.target).write_bytes(result)
    print(json.dumps({"input_bytes":len(source),"output_bytes":len(result),"ratio":round(len(result)/len(source),3) if source else None}))


if __name__=="__main__":
    main()
