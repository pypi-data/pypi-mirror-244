class FugueSQLHelper:
    @staticmethod
    def run_sql(table__4__sql, sql: str):
        # noinspection PyUnresolvedReferences
        from fugue.api import fugue_sql
        _ = table__4__sql
        return fugue_sql(sql, fsql_ignore_case=True)
