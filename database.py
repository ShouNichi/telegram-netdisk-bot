import sqlite3


def execute(db_file, query, values):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # query_log = "QUERY => "+query
    # logger.info(query_log % values)
    cur.execute(query, values)
    conn.commit()


def create_db(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE info(
        current_folder           INT      NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE files(
        file_id           INTEGER      PRIMARY KEY,
        user_id           INT          NOT NULL,
        chat_id           INT          NOT NULL,
        full_name         TEXT,
        username          TEXT,
        created_at        TIMESTAMP    NOT NULL,
        file_name         TEXT         NOT NULL,
        file_hash         TEXT         NOT NULL,
        folder_id         INT
    );
    """)

    cursor.execute("""
    CREATE TABLE folders(
        folder_id         INTEGER      PRIMARY KEY,
        folder_name       TEXT         NOT NULL,
        parent            INT,
        created_at        TIMESTAMP    NOT NULL
    );
    """)

    cursor.execute("""INSERT INTO folders (folder_name, parent, created_at ) 
        VALUES ('Home', NULL, CURRENT_TIMESTAMP)""")
    cursor.execute("INSERT INTO info (current_folder) VALUES (1)")

    connection.commit()


def get_current_directory(db_file):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT * FROM info').fetchall()[0][0]


def change_current_directory(db_file, id):
    execute(db_file, """UPDATE info
                        SET current_folder = ?""", (int(id),))


def register_file(db_file, user_id, chat_id, full_name, username, file_name, file_hash, folder_id):
    execute(db_file, """INSERT INTO files (user_id, chat_id, full_name, username, file_name, file_hash, folder_id, created_at) 
    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (user_id, chat_id, full_name, username, file_name, file_hash, folder_id))


def get_all_files_by_user(db_file, user_id):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT file_id, file_name FROM files WHERE user_id = ?', (user_id,)).fetchall()


def get_files_by_folder(db_file, folder_id):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT file_id, file_name FROM files WHERE folder_id = ?', (folder_id,)).fetchall()


def create_folder(db_file, folder_name, current_folder_id):
    print(folder_name)
    print(current_folder_id)
    execute(db_file, """INSERT INTO folders (folder_name, parent, created_at) 
    VALUES (?, ?, CURRENT_TIMESTAMP)""",
            (folder_name, current_folder_id,))


def move_file(db_file, file_id, destination_folder_id):
    execute(db_file, """UPDATE files
                        SET folder_id = ?
                        WHERE file_id = ?;""", (destination_folder_id, file_id))


def move_folder(db_file, folder_id, destination_folder_id):
    execute(db_file, """UPDATE folders
                        SET parent = ?
                        WHERE folder_id = ?;""", (destination_folder_id, folder_id))


def get_file_hash(db_file, file_id):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT file_hash FROM files WHERE file_id = ?', (file_id,)).fetchall()


def get_sub_folders(db_file, current_folder_id):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT folder_id, folder_name FROM folders WHERE parent = ?',
                              (current_folder_id,)).fetchall()


def get_directory_info(db_file, folder_id):
    connection = sqlite3.connect(db_file)
    return connection.execute('SELECT folder_name, parent FROM folders WHERE folder_id = ?',
                              (folder_id,)).fetchall()



if __name__ == '__main__':
    pass
