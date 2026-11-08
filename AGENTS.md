# Working on Jost Compact J

## Scope and source of truth

This fork gives Jost a compact capital J with corrected spacing. Keep changes
focused on the requested font or build behavior. Preserve the SIL Open Font
License, upstream copyright notices, and author credits.

The editable build inputs are the six masters under `sources/UFO/` and the
files under `sources/designspace/`. `sources/FontForge/` and the upstream shell
scripts are historical material. Use `scripts/build-compact-j.py` for this fork.

Change the UFO sources when editing glyphs. Keep generated files reproducible
through the build script. Avoid unrelated glyph, kerning, metadata, or source
formatting changes.

## Approved J design and spacing

The changes below are already applied to the masters. Treat them as design
constraints and do not apply the offsets a second time.

- The hook is raised 210 font units relative to upstream Jost.
- The glyph is shifted right 155 units and its advance width is increased by
  155 units, providing room before the raised hook while retaining spacing
  after J.
- Italic masters at the maximum italic axis value also shift the raised hook
  72 units right to follow the stem's slant. Intermediate italics interpolate.
- The Book J outline bounds are `(44, -10, 315, 700)` with advance width 395.
  Preserve optical overshoot in the other weights and glyphs.
- Check J in the middle of text, especially `IJK` and `GHIJKLM`. Initial-only
  specimens missed an I–J collision in an earlier version.

## Family names

Static fonts use `Jost Compact J`. The variable font uses
`Jost Compact J Variable` so both can be installed together. Preserve distinct
PostScript names for the variable font and its named instances, including the
variable PostScript name prefix. The build script applies the variable rename
after compilation and before WOFF2 conversion.

## Building

From the repository root, use Python 3.10 or newer.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-compact-j.txt
.venv/bin/python scripts/build-compact-j.py
```

Reuse a suitable existing environment when available. Keep local environments
and temporary build files out of commits. Use the pinned dependency versions
unless dependency changes are part of the task.

The build generates 18 TTFs in `fonts/ttf/`, 18 OTFs in `fonts/otf/`, the
variable TTF at `fonts/JostCompactJ-VF.ttf`, and 19 WOFF2 files in `fonts/woff2/`.
Generated fonts are tracked. Include the corresponding outputs when changing
the sources or font metadata. The build replaces the Jost font outputs in
these locations, so inspect the working tree before running it.

## Verification

For changes affecting fonts, rebuild and check the relevant outputs with
fontTools. Confirm the expected file counts, family names, named instances,
outline bounds, and advance widths. For variable changes, sample both axes,
including intermediate values, and check the WOFF2 round trip. For metadata-only
changes, confirm glyph outlines, metrics, and variation data are preserved.

Render and visually inspect spacing when changing glyphs or metrics. Include
upright and italic examples and representative light and heavy weights. Update
`documentation/compact-j-specimen.png` when a visible design change makes the
README specimen outdated.

Before finishing, run `git diff --check` and review the changed files. Report
what was verified and any limitations. Commit and push when requested by the
user. Use `apastuszak <apastuszak@gmail.com>` as the author and committer for
requested commits, with command-local Git settings rather than changing the
global Git identity.
