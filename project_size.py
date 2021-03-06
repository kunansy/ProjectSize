#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import NamedTuple, Iterable


class File(NamedTuple):
    name: Path
    lines: int

    def __str__(self) -> str:
        return f"File: {self.name}\n" \
               f"Size: {self.lines} lines"


class Project(NamedTuple):
    project_name: str
    lines: int
    files: list[File]

    def __str__(self) -> str:
        files = '\n--------\n'.join(
            f"{file}"
            for file in self.files
        )
        return f"Project: {self.project_name}\n" \
               f"lines: {self.lines}\n\n" \
               f"{files}"


def file_size(path: Path) -> int:
    if not path.exists():
        return 0

    with path.open() as f:
        return sum(1 for _ in f)


def project_size(path: Path,
                 extension: str,
                 skip: Iterable[str] = None) -> Project:
    skip = skip or set()
    lines, files = 0, []

    for file in path.rglob(extension):
        if any(skip_ in file.parts for skip_ in skip):
            continue
        
        file_size_ = file_size(file)
        file_name = file.relative_to(path)

        files += [File(lines=file_size_, name=file_name)]
        lines += file_size_

    return Project(files=files, lines=lines, project_name=path.absolute().name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate total amount of lines "
                    "in files with specified extension"
    )
    parser.add_argument(
        '--path',
        type=Path,
        help="Path to the project",
        default=Path('.'),
        dest='path'
    )
    parser.add_argument(
        '--skip',
        type=str,
        nargs='*',
        help="These dirs will be skipped, 'venv' skipped by default",
        default=['venv'],
        dest='skip'
    )
    parser.add_argument(
        '-e', '--extension',
        type=str,
        help="Files with which extension calculate. Example: --ext '*.go'",
        default='*.py',
        dest='ext'
    )

    args = parser.parse_args()
    print(project_size(args.path, args.ext, args.skip,))


if __name__ == '__main__':
    main()
