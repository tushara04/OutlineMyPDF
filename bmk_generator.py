#!/usr/bin/env python3
import sys
import re

if len(sys.argv) < 3:
    print("Usage: python bmk_generator.py content.txt offset_value > content.bmk")
    sys.exit(1)

bmk_file = sys.argv[1]
offset = int(sys.argv[2])

page_pattern = re.compile(r'(\d+)\s*$')  # match last number at line end

with open(bmk_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        match = page_pattern.search(line)
        if match:
            page_num = int(match.group(1)) + offset
            # replace old page number with new
            line = page_pattern.sub(str(page_num), line)
        print(line)
