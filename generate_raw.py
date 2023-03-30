import json
import sqlite3
import sys

def generate_categories():
    conn = sqlite3.connect(sys.argv[1])
    conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
    c = conn.cursor()
        
    query = """
        SELECT *
        FROM tag_category t
    """

    rows = c.execute(query)
    cats = combine_cols_and_rows(c, "tag_category", rows)

    return cats

def generate_games():
    conn = sqlite3.connect(sys.argv[1])
    conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
    c = conn.cursor()
        
    query = """
        SELECT *
        FROM game g
    """

    rows = c.execute(query)
    games = combine_cols_and_rows(c, "game", rows)

    query = f"""
        SELECT *
        FROM game_data gd
        WHERE gd.gameId = ?
    """

    for row in games:
      rows = c.execute(query, (row["id"],))
      game_data = combine_cols_and_rows(c, "game_data", rows)
      row["gameData"] = game_data

    query = f"""
        SELECT *
        FROM additional_app aa
        WHERE aa.parentGameId = ?
    """

    for row in games:
      rows = c.execute(query, (row["id"],))
      add_apps = combine_cols_and_rows(c, "additional_app", rows)
      row["addApps"] = add_apps

    query = f"""
        SELECT gtg.tagId
        FROM game_tags_tag gtg
        WHERE gtg.gameId = ?
    """
    for game in games:
      rows = c.execute(query, (game["id"],))
      game["tags"] = []
      for row in rows:
          game["tags"].append(row[0])

    query = f"""
        SELECT gtg.platformId
        FROM game_platforms_platform gtg
        WHERE gtg.gameId = ?
    """
    for game in games:
      rows = c.execute(query, (game["id"],))
      game["platforms"] = []
      for row in rows:
          game["platforms"].append(row[0])


    conn.close()

    return games

def generate_tags():
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()

    query = """
        SELECT *
        FROM tag t
    """

    rows = c.execute(query)
    tags = combine_cols_and_rows(c, "tag", rows)

    query = f"""
        SELECT *
        FROM tag_alias ta
        WHERE ta.tagId = ?
    """
    for row in tags:
        rows = c.execute(query, (row["id"],))
        tag_aliases = combine_cols_and_rows(c, "tag_alias", rows)
        row["tagAliases"] = tag_aliases

    conn.close()
    return tags

def generate_platforms():
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()

    query = """
        SELECT *
        FROM platform p
    """

    rows = c.execute(query)
    platforms = combine_cols_and_rows(c, "platform", rows)

    query = f"""
        SELECT *
        FROM platform_alias pa
        WHERE pa.platformId = ?
    """
    for row in platforms:
        rows = c.execute(query, (row["id"],))
        platform_aliases = combine_cols_and_rows(c, "platform_alias", rows)
        row["platformAliases"] = platform_aliases

    conn.close()
    return platforms
    
def combine_cols_and_rows(c, table_name, rows):
    rows_saved = []
    for row in rows:
        rows_saved.append(row)
    # Execute the PRAGMA statement to retrieve column information for the specified table
    c.execute(f"PRAGMA table_info({table_name})")

    # Fetch all the columns returned by the PRAGMA statement
    columns = c.fetchall()

    # Extract the column names from the result set
    column_names = [column[1] for column in columns]

    row_dicts = []
    for row in rows_saved:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        row_dicts.append(row_dict)
    return row_dicts

def saveAll():
    games = generate_games()
    tags = generate_tags()
    platforms = generate_platforms()
    cats = generate_categories()
    data = {
      "games": games,
      "tags": tags,
      "platforms": platforms,
      "categories": cats
    }
    try:
      with open('extra_data.json') as f:
        extraData = json.load(f)
        data.update(extraData)
    except:
      pass
    with open("raw.json", "w", encoding="utf-8") as outfile:
      # write the dictionary to the file as a JSON object
      json.dump(data, outfile)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('provide database name')
    else:
        saveAll()

