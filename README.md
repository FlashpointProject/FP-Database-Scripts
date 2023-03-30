# Flashpoint Database Scripts

## Usage

### Stripping Database By Tags

Place db at `flashpoint.sqlite`, will output to `stripped.sqlite`

`python ./stripper.py action adventure` - Removes all games that do not have either action or adventure.

### Generating Importable JSONs

Will output to `raw.json`. Can be imported via the Developer tab in the Flashpoint Launcher with `Import Metadata`

`python ./generate_raw.py <database_file>`

You can provide extra data inside `extra_data.json`, this accepts the gameDataSources and tagFilters as they appear in Flashpoint preferences.json. E.G:

```json
{
  "gameDataSources": [
    {
      "type": "raw",
      "name": "Test Project",
      "arguments": [
        "https://example.com/gib-roms/Games/"
      ]
    }
  ]
}```