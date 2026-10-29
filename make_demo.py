"""Generate original geometric images, a PNG reference pack and matching ZIP."""
import argparse
import io
import struct
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image

def create(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    yy,xx=np.indices((64,64));records=[];originals=[]
    mask=np.where((xx-32)**2+(yy-32)**2<28**2,255,0).astype(np.uint8)
    def png(image):
        stream=io.BytesIO();image.save(stream,format='PNG');return stream.getvalue()
    for i in range(8):
        index=((xx//(3+i)+yy//(4+i))%3).astype(np.uint8)
        colors=np.array([[20+i*9,40,80],[100,180-i*7,220],[240,130,40+i*8]],dtype=np.uint8)
        rgb=colors[index];image=Image.fromarray(rgb)
        mid=1 if i%2 else 65535
        rgba=np.dstack([rgb,mask if mid==1 else np.full((64,64),255,np.uint8)])
        records.append((i,mid,png(image)));originals.append(png(Image.fromarray(rgba)))
    mb=png(Image.fromarray(mask))
    offset=4+12*len(records)+4+10
    table=[];chunks=[]
    for key,mid,data in records:
        table.append(struct.pack('<HHII',key,mid,offset,len(data)));chunks.append(data);offset+=len(data)
    masks=struct.pack('<HII',1,offset,len(mb))
    reference=struct.pack('<I',12*len(records))+b''.join(table)+struct.pack('<I',10)+masks+b''.join(chunks)+mb
    (output/'reference.pack').write_bytes(reference)
    with zipfile.ZipFile(output/'textures.zip','w') as archive:
        for i,data in enumerate(originals):archive.writestr(f'0_{i}.png',data)
    print('Created eight original geometric fixtures in',output)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default='demo')
    create(parser.parse_args().output)
