#! /bin/python3 ./lapine-secreter.py
import sys
import secrets
import typing
from typing import List
import os
import shutil

output_file: typing.TextIO  = None

def usage():
    print("usage:\tlapine-secrets [mode] /path/to/input")
    print("\tmodes:\tgenerate-env revert")

def open_output_file():
    global output_file
    output_file = open("./.env", "w")

def close_and_flush_outputfile():
    global output_file
    output_file.flush()
    output_file.close()

def open_and_read_request_file(file: str) -> List[str]:
    returnValue = []
    requestFile = open(file)
    returnValue = requestFile.readlines()
    requestFile.close()
    return returnValue

def write_literal_value(key:str, value: str) -> str:
    global output_file
    output_file.write(f"{key}={value}\n")
    return value

def write_hex_value(key:str,length: int) -> str:
    global output_file
    value = secrets.token_hex(length)
    output_file.write(f"{key}={value}\n")
    return value

def write_urlsafe_value(key:str, length: int) -> str:
    global output_file
    value = secrets.token_urlsafe(length)
    output_file.write(f"{key}={value}\n")
    return value

def process_line_to_dot_env(line: str) -> bool:
    key_value_pair = line.strip().split(":")
    key: str = key_value_pair[0]
    print(key_value_pair)
    format_argument_pair = key_value_pair[1].strip().split(" ")
    print(format_argument_pair)
    tokenValue: str = ""
    match format_argument_pair[0]:
        case "literal":
            value = format_argument_pair[1]
            tokenValue = write_literal_value(key, value)
        case "lit":
            value = format_argument_pair[1]
            tokenValue = write_literal_value(key, value)
        case "hex":
            value = 32
            if len(format_argument_pair) == 2:
                value = format_argument_pair[1]
            length = int(format_argument_pair[1])
            tokenValue = write_hex_value(key, length)
        case "urlsafe":
            value = 32
            if len(format_argument_pair) == 2:
                value = format_argument_pair[1]
            write_literal_value(key, value)
            length = int(format_argument_pair[1])
            tokenValue = write_urlsafe_value(key, length)

    if len(format_argument_pair) > 2 and format_argument_pair[2] == "overwrites":
        for file in format_argument_pair[3:]:
            if os.path.exists(file):
                shutil.copy2(file, file + ".bak")
                fd = open(file, "r")
                lines = fd.readlines()
                fd.close
                fd = open(file, "w")
                for line in lines:
                    line = line.replace(key, tokenValue)
                    fd.write(line)
                fd.flush()
                fd.close()
                
    return True

def revert_overwrite(line: str):
    lineParameters = line.strip().split(" ")
    if len(lineParameters) <= 3:
        return
    
    overwriteFiles = [file + ".bak" for file in lineParameters[4:]]
    for file in overwriteFiles:
        if os.path.exists(file):
            os.rename(file, file[:-4])

            



def main():
    if len(sys.argv) != 4:
        usage()
        exit(1)
    
    mode = sys.argv[2]
    lines = open_and_read_request_file(sys.argv[3])
    match mode:
        case "generate-env":
            open_output_file()
            for line in lines:
                process_line_to_dot_env(line)
            close_and_flush_outputfile()
        case "revert":
            for line in lines:
                revert_overwrite(line)

if __name__ == "__main__":
    main()