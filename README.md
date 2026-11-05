# Compression Playground

A Python standard-library educational implementation of **lossless run-length encoding (RLE)** for binary files. Compress repeated byte runs into `(count, byte)` pairs, decode them exactly, and display input/output size ratios.

## Usage

```bash
python compression.py compress examples/sample.txt sample.rle
python compression.py decompress sample.rle restored.txt
```

The binary format begins with `RLE1`, followed by pairs of one-byte run length (1–255) and byte value. The decoder rejects invalid headers, zero-length runs, malformed payloads, and outputs over 100 MB by default.

## Tests

```bash
python -m unittest discover -s tests -v
```

Nine tests run through GitHub Actions on Python 3.10, 3.12 and 3.13.

## Limitations

RLE is efficient for repeated bytes but **often increases file size** for varied or already-compressed content. This is an educational codec, not a replacement for gzip, zstd, or production archive formats. It does not store file names or checksums.
