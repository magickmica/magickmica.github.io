# incoming/

Drop your export files here to update the whole site:

- `get-notes-magickmica-YYYY-MM-DD.json` (from GET NOTES!)
- `get-articles-magickmica.substack.com-YYYY-MM-DD.json` (from GET ARTICLES!)
- `get-articles-magickmicaart.substack.com-YYYY-MM-DD.json` (from GET ARTICLES!)

Uploading them starts the "Update site from exports" job (Actions tab). It merges
them into `_data/`, rebuilds every page, commits the result, and removes the export
files from this folder. Keep your own copies: GET NOTES! and GET ARTICLES! use them
next time to fetch only what's new.
