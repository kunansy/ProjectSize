#!/usr/bin/env python3
from pathlib import Path
from typing import NamedTuple


class FileSize(NamedTuple):
    name: str or Path
    lines: int

    def __str__(self) -> str:
        return f"File name: {self.name}\n" \
               f"Size: {self.lines} lines"


class ProjectSize(NamedTuple):
    project_name: str
    lines: int
    files: list[FileSize]

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
                 skip: set[str] = None) -> ProjectSize:
    skip = skip or {}
    lines, files = 0, []

    for file in path.rglob('*.py'):
        if any(skip_ in file.parts for skip_ in skip):
            continue
        
        file_size_ = file_size(file)
        file_name = file.relative_to(path)

        files += [FileSize(lines=file_size_, name=file_name)]
        lines += file_size_

    return ProjectSize(files=files, lines=lines, project_name=path.name)


if __name__ == '__main__':
    project_path = Path('/home/kirill/ReadingTracker/')
    print(project_size(project_path, {'venv'}))

