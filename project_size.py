#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import NamedTuple, Iterable


class File(NamedTuple):
    name: str or Path
    lines: int

    def __str__(self) -> str:
        return f"File: {self.name}\n" \
               f"Size: {self.lines} lines"


class ProjectSize(NamedTuple):
    project_name: str
    lines: int
    files: list[File]

    def __str__(self) -> str:
        files = '\n--------\n'.join(
            f"{file}"
            for file in self.files
        )
        return f"{self.__class__.__name__}(\n" \
               f"Project: {self.project_name},\n" \
               f"lines: {self.lines},\n\n" \
               f"{files})"


def file_size(path: Path) -> int:
    with path.open() as f:
        size = 0
        for num, _ in enumerate(f, 1):
            size = num

    return size
            

def project_size(path: Path,
                 skip: Iterable[str] = None) -> ProjectSize:
    skip = skip or {}
    lines, files = 0, []

    for file in path.rglob('*.py'):
        if any(skip_ in file.parts for skip_ in skip):
            continue
        
        file_size_ = file_size(file)
        file_name = file.relative_to(path)

        files += [File(lines=file_size_, name=file_name)]
        lines += file_size_

    return ProjectSize(files=files, lines=lines, project_name=path.name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check updates of the requirements"
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
        help="These dirs will be skipped",
        default=['venv'],
        dest='skip'
    )
    args = parser.parse_args()
    print(project_size(args.path, args.skip))


if __name__ == '__main__':
    main()
