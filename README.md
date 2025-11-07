# Bitburner Savefile Editor

A Python application to edit your Bitburner save file and apply exploits.

> [!WARNING]
> The source code contains spoilers.  I would not recommend running this
> application early on in your Bitburner game.

## Running

1. Install [uv](https://docs.astral.sh/uv/)
2. Clone this repo
3. Run the application

```shell
uv run bitburner-save-file-editor --directory <path to your game exports>
```

> [!CAUTION]
> You don't want to edit your normal save game folder.  Manually export your
> save, then run this application on that file.

This application will read your save game `.json.gz` file, and write a new file
to the same folder as `bitburnerSave-modified.json.gz`.  Import that file to load
your cheats.
