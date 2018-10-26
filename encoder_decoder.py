import json
import io
import PIL.Image as I
import base64
import zlib

class EncoderDecoder:
    def __init__(self):
        pass

    def encode(self, x):
        return x

    def decode(self, x):
        return x


class ImageEncoderDecoder(EncoderDecoder):
    def __init__(self, image_format="jpeg"):
        super(ImageEncoderDecoder).__init__()
        self.image_format = image_format

    def encode(self, x):
        if isinstance(x, str):
            x = zlib.compress(open(x, 'rb').read())
            x = base64.b64encode(x)
        elif isinstance(x, I.Image):
            img_bytes = io.BytesIO()
            x.save(img_bytes, format=self.image_format)
            img_bytes.seek(0)
            x = zlib.compress(img_bytes.read())
            x = base64.b64encode(x)
        return x

    def decode(self, x):
        if isinstance(x, str):
            x = x.encode()
        return I.open(io.BytesIO(zlib.decompress(base64.b64decode(x))),)

class CSVEncoderDecoder(EncoderDecoder):
    def __init__(self, ):
        super(CSVEncoderDecoder).__init__()

    def encode(self, x):
        if isinstance(x, pd.DataFrame):
            x = zlib.compress(x.to_csv().encode())

        elif isinstance(x, str):
            x = zlib.compress(x.encode())
        x = base64.b64encode(x)
        return x

    def decode(self, x):
        if isinstance(x, str):
            x = x.encode()
        x = zlib.decompress(base64.b64decode(x)).decode()
        x = pd.read_csv(io.StringIO(x),index_col=0)
        return x

class PickleEncoderDecoder(EncoderDecoder):
    def __init__(self, ):
        super(PickleEncoderDecoder).__init__()

    def encode(self, x):
        f = io.BytesIO()
        file = pickle.dump(x, f)
        f.seek(0)
        x = zlib.compress(f.read())
        x = base64.b64encode(x)
        return x

    def decode(self, x):
        x = zlib.decompress(base64.b64decode(x))#.decode()
        f = io.BytesIO(x)
        x = pickle.load(f)
        return x


