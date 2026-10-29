# EPK3 Emoji Pack

A compact image-resource format, offline Python optimizer and Android Java reader
for 64×64 emoji. The reader reconstructs a complete ARGB bitmap while keeping
palette maps, mask records and bounded root-map caches internal.

## Standalone, reproducible demo

Python 3.11+, a WebP-enabled Pillow build and JDK 17+:

```sh
python -m pip install -r requirements.txt
python make_demo.py --output demo
python build_emoji_pack.py --reference demo/reference.pack --textures demo/textures.zip --output demo/emoji.pack --workers 1 --lossless
python verify_emoji_pack.py demo/emoji.pack --reference demo/reference.pack --textures demo/textures.zip
python test_java_loader.py demo/emoji.pack
```

The demo generates eight original geometric images, including alpha masks; no
third-party emoji artwork or Telegram installation is needed. The independent
Python verifier and JVM test check reconstruction against the reference pixels.
JVM graphics stubs use predecoded fixtures: they do **not** test Android native
WebP performance, premultiplication or memory behavior.

## Components

- `base_builder.py`: general v2 optimizer, with optional fitted/lossy candidates.
- `build_emoji_pack.py`: v2 optimization followed by lossless v3 palette compaction.
- `verify_emoji_pack.py`: independent v2/v3 reader and quality gates.
- `EmojiPack.java`: Android decoder, now independent of Telegram's ApplicationLoader.
- [FORMAT.md](FORMAT.md): binary layout, palette encoding and predictors.

Use `new EmojiPack(context)` with an **uncompressed** asset named `emoji.pack`,
then `getEmoji(x,y)`. Copy the Java class into its declared package and configure
the Android build to avoid compressing `.pack` assets (`androidResources.noCompress`).
The descriptor constructor supports custom asset loading.

## Research scope

The format reader supports the v3 split predictors documented in FORMAT.md.
This public builder performs general palette compaction; it does not reproduce
the missing dataset-specific historical C++ split-search experiment.
Original fixed-dataset statistics are retained under `docs/historical/` as historical
measurements, not promises of compression ratios for arbitrary images. Format and
decode checks are distinct from benchmark claims.

Only use trusted input/cache files: optional optimizer caches use Python pickle.
The format is intended for trusted application assets, not hostile downloaded packs.
See NOTICE.md and LICENSE for GPL-2.0 provenance; artwork has its own separate terms.

Русский: формат компактного хранения emoji, Python-оптимизатор и Android-декодер.
Демонстрация полностью воспроизводится на сгенерированных геометрических изображениях.
