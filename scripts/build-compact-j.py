#!/usr/bin/env python3
"""Build the Compact J family from the edited UFO masters."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]


def rename_variable_family(path):
    """Keep the variable family and its named instances distinct from static fonts."""
    font = TTFont(path)
    for record in font['name'].names:
        value = record.toUnicode()
        renamed = value.replace('Jost Compact J', 'Jost Compact J Variable')
        renamed = renamed.replace('JostCompactJ-', 'JostCompactJVariable-')
        if renamed != value:
            record.string = renamed.encode(record.getEncoding())
    font['name'].setName('JostCompactJVariable', 25, 3, 1, 0x409)
    font.save(path)


def build():
    with tempfile.TemporaryDirectory(prefix='jost-compact-j-') as directory:
        temp = Path(directory)
        shutil.copytree(ROOT / 'sources' / 'UFO', temp / 'sources' / 'UFO')
        shutil.copytree(ROOT / 'sources' / 'designspace', temp / 'sources' / 'designspace')
        designspace = temp / 'sources' / 'designspace' / 'jost.designspace'
        output = temp / 'fonts'
        variable = output / 'JostCompactJ-VF.ttf'
        output.mkdir()
        subprocess.run([
            sys.executable, '-m', 'fontmake', '-m', str(designspace),
            '-o', 'variable', '--output-path', str(variable),
        ], check=True, cwd=temp)
        rename_variable_family(variable)
        for extension in ('ttf', 'otf'):
            folder = output / extension
            subprocess.run([
                sys.executable, '-m', 'fontmake', '-m', str(designspace),
                '-i', '-o', extension, '--output-dir', str(folder),
            ], check=True, cwd=temp)
            for path in list(folder.glob('*.' + extension)):
                font = TTFont(path)
                weight = font['OS/2'].usWeightClass
                name = font['name'].getDebugName(6)
                style = name.removeprefix('JostCompactJ-')
                path.rename(folder / f'JostCompactJ-{weight}-{style}.{extension}')
        web = output / 'woff2'
        web.mkdir()
        for path in [variable, *sorted((output / 'ttf').glob('*.ttf'))]:
            font = TTFont(path)
            font.flavor = 'woff2'
            font.save(web / (path.stem + '.woff2'))
        # Publish only after every format has built successfully.
        for folder in ('ttf', 'otf', 'woff2'):
            target = ROOT / 'fonts' / folder
            target.mkdir(parents=True, exist_ok=True)
            for path in target.glob('Jost*.' + folder):
                path.unlink()
            for path in (output / folder).iterdir():
                shutil.copy2(path, target / path.name)
        shutil.copy2(variable, ROOT / 'fonts' / variable.name)
        upstream_variable = ROOT / 'fonts' / 'Jost-VF.ttf'
        upstream_variable.unlink(missing_ok=True)


if __name__ == '__main__':
    build()
