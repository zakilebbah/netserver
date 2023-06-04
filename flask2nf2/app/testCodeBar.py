from barcode import Code128
from barcode.writer import ImageWriter

# print to a file-like object:
# rv = BytesIO()
# EAN13(str("21d16000"), writer=ImageWriter()).write(rv)

# or sure, to an actual file:
with open('barCode.jpeg', 'wb') as f:
    Code128('100000011111', writer=ImageWriter()).write(f)