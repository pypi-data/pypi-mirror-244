# BasketCase
Download images and videos from Instagram.

Notable features:
- Stories can be downloaded without triggering the "seen" flag.
- Downloads a high quality version of a profile picture.

https://www.youtube.com/watch?v=NUTGr5t3MoY ;)

## Installation
Install it from [PyPI](https://pypi.org/project/basketcase/) as a [user install](https://pip.pypa.io/en/stable/user_guide/#user-installs).

```sh
pip install --user basketcase
```

> This should put the executable `basketcase` on your PATH.

Alternatively, you could install it in a virtual environment.
I keep mine at `~/venv`, and I have a shell alias to quickly activate it.

Also, a pre-built executable for Linux is provided with the releases.

## Command-line usage
```sh
basketcase -u "https://instagram.com/p/<post_id>"
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase_downloads`).

To download from multiple URLs, create a text file (e.g. `urls.txt`)
and populate it with resource URLs:

```
https://instagram.com/p/<post_id>
https://instagram.com/reel/<reel_id>
https://instagram.com/<username>
```

```sh
basketcase -f ./urls.txt
```

See `--help` for more info.

### Supported URLs
| Supported URL                                                  | Description                                                                      |
|----------------------------------------------------------------|----------------------------------------------------------------------------------|
| `https://instagram.com/<username>`                             | User profile. Downloads stories from the past 24 hours, and the profile picture. |
| `https://instagram.com/p/<post_id>`                            | Standard publication.                                                            |
| `https://instagram.com/reel/<reel_id>`                         | Reels movie                                                                      |
| `https://www.instagram.com/stories/highlights/<highlight_id>/` | A collection of stories, or "highlights"                                         |
| `https://www.instagram.com/s/<random_characters>`              | A shorter type of URL                                                            |

### Authentication
1. Add a session cookie

```sh
basketcase --cookie <session_cookie_id> --cookie-name "my session"
# Added session id: 1
```

2. Specify its identifier when downloading

```sh
basketcase -s 1
```

> List all available sessions with `basketcase -l`.
> To disable sessions, use `--no-session`.
> If only one exists, it is treated as the default.

## User data
Cookies and other application data are kept in your home directory (i.e. `~/.basketcase`).

## Development setup
See [Packaging Python Projects](https://github.com/pypa/packaging.python.org/blob/5cca66a312ca96ad4d10d2bc806864f63944b870/source/tutorials/packaging-projects.rst).

1. `cd` to the project root and create a virtual environment
in a directory named `venv`, which is conveniently ignored in
version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

3. Install this package in [editable mode](https://github.com/pypa/setuptools/blob/5a3f670457e426b9b6f29700049754327ced3088/docs/userguide/development_mode.rst).

```sh
pip install -e .
```

### Package build and upload
1. Update the requirements list.

```sh
pip freeze --exclude-editable > requirements.txt
```

2. Increment the version on `pyproject.toml`.
3. Build the package.

```sh
python -m build
```

4. Commit and push the changes (and a new version tag) to the git repository.
5. Publish it.
```sh
python -m twine upload dist/*
```

### Build an executable
With the [zipapp](https://docs.python.org/3/library/zipapp.html#creating-standalone-applications-with-zipapp) module
we can build the whole package as an executable file for Linux. The only
runtime requirement is Python 3.

1. `cd` to the project root.
2. Activate the virtual environment.
3. Run `sh zipapp.sh`.

The executable file `basketcase` is in the `dist` folder.
