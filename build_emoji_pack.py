#!/usr/bin/env python3
"""Build EPK3 v3 from a PNG reference pack and its original texture ZIP."""
import argparse
import json
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path
from verify_emoji_pack import Pack, validate

ROOT = Path(__file__).resolve().parent

def compact_palettes(source, output):
    pack = Pack(source)
    entries, chunks = [], []
    offset = 32 + 20 * pack.n
    try:
        for original in pack.entries:
            entry = list(original)
            blob = bytes(pack.data[entry[2]:entry[2]+entry[3]])
            length = pack.palette_length(entry)
            if length and not (entry[9] & 128):
                compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
                zipped = compressor.compress(blob[:length]) + compressor.flush()
                if len(zipped) + 2 < length:
                    blob = struct.pack('<H', len(zipped)) + zipped + blob[length:]
                    entry[9] |= 128
            entry[2], entry[3] = offset, len(blob)
            if len(blob) > 65535:
                raise ValueError('Record exceeds the format payload limit')
            entries.append(struct.pack('<HHIHHHHBBBB', *entry))
            chunks.append(blob)
            offset += len(blob)
        header = struct.pack('<4sHHIIIIII', b'EPK3', 3, 20, 64, 64, pack.n, pack.ne, offset, 0)
        Path(output).write_bytes(header + b''.join(entries) + b''.join(chunks))
    finally:
        pack.close()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',required=True)
    parser.add_argument('--textures',required=True)
    parser.add_argument('--output',default='emoji.pack')
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--lossless',action='store_true',help='Disable fitted palettes and lossy WebP candidates')
    args=parser.parse_args()
    if args.workers < 1: parser.error('--workers must be positive')
    output=Path(args.output).resolve()
    if output in {Path(args.reference).resolve(), Path(args.textures).resolve()}:
        parser.error('Output must not overwrite an input')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='epk3-build-') as work:
        base=Path(work)/'base.pack'
        command=[sys.executable,str(ROOT/'base_builder.py'),'--reference',str(Path(args.reference).resolve()),
                 '--textures',str(Path(args.textures).resolve()),'--output',str(base),'--workers',str(args.workers)]
        if args.lossless: command.append('--lossless')
        subprocess.run(command,check=True)
        compact_palettes(base,output)
    result=validate(output,args.reference,args.textures)
    output.with_suffix('.verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
