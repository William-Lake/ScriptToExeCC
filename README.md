# ScriptToEXECC

Uses the incredibly helpful [cookiecutter](https://github.com/cookiecutter/cookiecutter) library to generate a bare-bones Python project for personal use.

The generated project includes a [github action](https://github.com/features/actions) which uses [pyinstaller](https://www.pyinstaller.org/) via [Pyinstaller Windows](https://github.com/marketplace/actions/pyinstaller-windows) to generate an .exe and add it in a newly generated release.

The action is triggered when a new tag matching the syntax v#.#.# (E.g. v1.0.0) is created/pushed.

## Why?

I have a lot of Python utility scripts at work. I like to have them available as .exes so I can run them from a computer without Python installed, or provide them to someone who doesn't have/doesn't want to have Python installed.

This project reduces the time it takes to meet those needs.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- cookiecutter

## Usage

`cookiecutter https://github.com/William-Lake/ScriptToExeCC.git`
