import sqlite3
import sys
import shutil

def filter_games_by_tags(tags):
    l = tuple(tags)
    conn = sqlite3.connect("stripped.sqlite")
    c = conn.cursor()
    query = '''DELETE FROM game WHERE id NOT IN (
                SELECT gameId FROM game_tags_tag
                WHERE tagId IN (
                    SELECT id FROM tag_alias
                    WHERE name IN {}
                )
                );'''.format(l) if len(tags) > 1 else '''DELETE FROM game WHERE id NOT IN (
                        SELECT gameId FROM game_tags_tag
                        WHERE tagId IN (
                            SELECT id FROM tag_alias
                            WHERE name = "{}"
                        )
                        );'''.format(tags[0])
    c.execute(query)

    c.execute('''
        DELETE FROM game_data 
        WHERE gameId NOT IN (SELECT id FROM game)
    ''')
    c.execute('''
        DELETE FROM additional_app 
        WHERE parentGameId NOT IN (SELECT id FROM game)
    ''')
    c.execute('''
        DELETE FROM game_tags_tag 
        WHERE gameId NOT IN (SELECT id FROM game)
    ''')
    c.execute('''
        DELETE FROM game_platforms_platform 
        WHERE gameId NOT IN (SELECT id FROM game)
    ''')

    c.execute('''
        DELETE FROM tag 
        WHERE id NOT IN (SELECT tagId FROM game_tags_tag)
    ''')
    c.execute('''
        DELETE FROM platform 
        WHERE id NOT IN (SELECT platformId FROM game_platforms_platform)
    ''')

    c.execute('''
        DELETE FROM tag_alias 
        WHERE tagId NOT IN (SELECT id FROM tag)
    ''')
    c.execute('''
        DELETE FROM platform_alias 
        WHERE platformId NOT IN (SELECT id FROM platform)
    ''')


    conn.commit()

    c.execute('VACUUM')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    tags = sys.argv[1:]
    print(tags)

    # Copy file first
    shutil.copyfile("flashpoint.sqlite", "stripped.sqlite")

    filter_games_by_tags(tags)
