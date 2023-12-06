import sqlite3


class SimpleSQLite:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        Crée une nouvelle table dans la base de données.
        Args:
            table_name (str): Nom de la table.
            columns (list): Liste de tuples contenant le nom de la colonne et son type de données (ex: [('id', 'INTEGER PRIMARY KEY'), ('name', 'TEXT'), ('age', 'INTEGER')]).

        Returns:
            None
        """
        columns_str = ', '.join([f'{col} {data_type}' for col, data_type in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        """
        Insère des données dans une table.
        Args:
            table_name (str): Nom de la table.
            data (dict): Dictionnaire contenant les valeurs à insérer (ex: {'name': 'John', 'age': 30}).

        Returns:
            None
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def fetch_data(self, table_name):
        """
        Récupère toutes les données de la table.
        Args:
            table_name (str): Nom de la table.

        Returns:
            list: Liste de tuples représentant les lignes de données.
        """
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name, data, condition):
        """
        Met à jour des données dans une table.
        Args:
            table_name (str): Nom de la table.
            data (dict): Dictionnaire contenant les valeurs à mettre à jour (ex: {'name': 'John', 'age': 35}).
            condition (str): Clause WHERE pour spécifier les enregistrements à mettre à jour (ex: "id = 1").

        Returns:
            None
        """
        columns = ', '.join([f"{col} = ?" for col in data.keys()])
        values = tuple(data.values())
        query = f"UPDATE {table_name} SET {columns} WHERE {condition}"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        """
        Supprime des données d'une table.
        Args:
            table_name (str): Nom de la table.
            condition (str): Clause WHERE pour spécifier les enregistrements à supprimer (ex: "age < 30").

        Returns:
            None
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def display_all_data(self, table_name):
        """
        Affiche toutes les données d'une table.
        Args:
            table_name (str): Nom de la table à afficher.

        Returns:
            None
        """
        results = self.fetch_data(table_name)
        for row in results:
            print(row)

    def close_connection(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()
