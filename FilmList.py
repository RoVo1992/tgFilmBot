from DBcm import UseDataBase


def film_list(config: dict) -> 'list':
    with UseDataBase(config) as cursor:
        cursor.execute('SELECT * FROM films')
        content = cursor.fetchall()

        return content


def film_list_key(config, list_key) -> 'list':
    with UseDataBase(config) as cursor:
        cursor.execute('SELECT {} FROM films'.format(list_key))
        content = cursor.fetchall()
        return content


def push_content(config: dict, content: list):
    with UseDataBase(config) as cursor:
        _SQL = """insert into films
                (name, director, year, description, genre)
                values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (content[0],
                              content[1],
                              content[2],
                              content[3],
                              content[4],))
