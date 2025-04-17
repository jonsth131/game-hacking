#!/usr/bin/env python3
import argparse
import os

"""
Types:
    0x00 - Code?
    0x01 - Image
    0x02 - ?
    0x03 - Font
    0x04 - ?
    0x05 - ?
    0x06 - ?
"""

RETAL00IDX = [
    0x01000000,
    0x01001be2,
    0x01006ef6,
    0x0300b79c,
    0x0100c42a,
    0x0101279f,
    0x0101737e,
    0x0101bb43,
    0x01023285,
    0x0102ac8d,
    0x0102ccab,
    0x0202f46c,
    0x03031479,
    0x04031f35,
    0x050357c8,
    0x00038ab7,
    0x0003a660,
]

RETAL01IDX = [
    0x06000000,
    0x0600442c,
    0x06009c39,
    0x0600f87f,
    0x01015403,
    0x0101cc91,
    0x010236fc,
    0x01028d8f,
    0x0002f771,
    0x00032b08,
    0x0003c7a4,
    0x000418dd,
    0x00044bd8,
    0x00045a57,
    0x000463a5,
    0x00047538,
    0x01048aef,
    0x0104de58,
    0x01052826,
    0x01057b04,
]


def decode(data):
    decoded = bytearray()
    checkbyte = 0x26
    bh = 0x00
    i = 0

    while i < len(data):
        current_byte = data[i]

        if current_byte == checkbyte:
            next_byte = data[i + 1] if i + 1 < len(data) else None
            i += 1
            if next_byte is None:
                break
            if next_byte == 0x00:
                decoded.append(current_byte)
                i += 1
                continue
            elif next_byte & 0x80 == 0x00:
                third_byte = data[i + 1] if i + 1 < len(data) else None
                i += 1
                if third_byte is None:
                    break
                bh = third_byte

            times = next_byte & 0x7f
            for _ in range(times + 2):
                decoded.append(bh)

        else:
            decoded.append(current_byte)

        i += 1

    return decoded


def extract_file(file_path, idx_arr, output_dir):
    with open(file_path, "rb") as f:
        data = f.read()

    file_name = os.path.basename(file_path)

    for i in range(len(idx_arr)-1):
        start = idx_arr[i] & 0x00FFFFFF
        end = idx_arr[i + 1] & 0x00FFFFFF
        chunk = data[start:end]
        decoded_chunk = decode(chunk)

        out_file = os.path.join(output_dir, f"{file_name}extracted_{i}.bin")

        with open(out_file, "wb") as out_file:
            out_file.write(decoded_chunk)
            print(f"Extracted chunk {i} to {out_file.name}")


def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    retal00_path = os.path.join(input_dir, "RETAL.00")
    retal01_path = os.path.join(input_dir, "RETAL.01")

    extract_file(retal00_path, RETAL00IDX, output_dir)
    extract_file(retal01_path, RETAL01IDX, output_dir)


if __name__ == "__main__":
    argsparse = argparse.ArgumentParser(
        description="Extract and decode files.")

    argsparse.add_argument("input", type=str,
                           help="Directory containing RETAL.00 and RETAL.01 files")
    argsparse.add_argument("output", type=str,
                           help="Directory to save the extracted files")

    args = argsparse.parse_args()

    input_dir = args.input
    output_dir = args.output

    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        exit(1)

    if not os.path.isdir(input_dir):
        print(f"Input path '{input_dir}' is not a directory.")
        exit(1)

    main(input_dir, output_dir)
