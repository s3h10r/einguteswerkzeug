Tip
===

processing filterchains feels a bit like in the 90s of the last century, means
it can get time-consuming. By setting the size to 200*200 pixels
(`--size-inner 200`) and not using any frame (`--noframe`) the runtime
shortens a lot. This is ideal for getting a preview while experimenting with
different settings until a combination produces interesting results which
can then be rendered in high-res:

```console
  $ egw --generator psychedelic --filter pixelsort,mosaic,oil2
        --params-filter '{"algo":10}{"block_size":16}{"brush_size":8, "roughness" : 80}'
        -o /tmp/3.png -s 200 --noframe && feh /tmp/3.png
```
