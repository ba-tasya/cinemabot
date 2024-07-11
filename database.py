import sqlite3


class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('cinema_bot.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_movie (
            user_id INTEGER,
            movie_name TEXT
        )
        ''')
        self.conn.commit()

    def add_movie(self, user_id: int, movie_name: str) -> None:
        """
        Добавляет информацию о фильме в базу данных.
        """
        self.cursor.execute('''INSERT INTO user_movie (user_id, movie_name) VALUES (?, ?) ''', (user_id, movie_name))
        self.conn.commit()

    def get_history(self, user_id: int) -> str:
        self.cursor.execute('''SELECT movie_name
                            FROM user_movie
                            WHERE user_id = ?''', (user_id,))
        history = self.cursor.fetchall()

        # return history

        if not history:
            return "История поиска пуста."

        result = "История поиска:\n"
        for idx, (movie_name, ) in enumerate(reversed(history), 1):
            result += f"{idx}. {movie_name}\n"

        return result

    def get_stats(self, user_id: int) -> str:
        self.cursor.execute('''SELECT movie_name, COUNT(*) as count
                            FROM user_movie
                            WHERE user_id = ?
                            GROUP BY movie_name
                            ORDER BY count DESC''', (user_id,))
        stats = self.cursor.fetchall()

        # return stats

        if not stats:
            return "Статистика пуста."

        result = "Статистика по просмотрам:\n"
        for idx, (movie_name, count) in enumerate(stats, 1):
            result += f"{idx}. {movie_name}\n   Просмотрено раз: {count}\n\n"

        return result

    def __del__(self) -> None:
        self.conn.close()
