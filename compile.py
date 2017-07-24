import sys
from pathlib import Path
from stackvm.image import Image
from assembler.assembler import Assembler

input_file = Path(sys.argv[1])
output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix(".svmb")

with open(input_file) as f:
    lines = f.read().split("\n")

data, code = Assembler().assemble(lines)

img = Image.from_sections(data, code)
img.write(output_file)
