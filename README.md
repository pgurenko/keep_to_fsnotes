# keep_to_fsnotes

Converting [Google Keep](https://keep.google.com) notes to the [FSNotes](https://fsnot.es/).

What should currently work:
- actual notes
- images
- lists

Needs:

```
pip install marshmallow
```

Usage:

- download `keep` notes via `Google Takeout`
- put them to the `keep` folder
- run `keep_to_fsnotes.py`
- `fsnotes` in markdown + images should be in the `fsnotes` folder
