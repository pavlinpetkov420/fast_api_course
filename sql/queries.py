INSERT_INTO_RETURNING_STAR: str = """
INSERT INTO {table} ({column_names}) 
VALUES(
%s, %s, %s
) RETURNING *
"""

FILTER_POST_BY_ID: str = """
SELECT *
FROM {table}
WHERE id = %s;
"""

DELETE_POST_BY_ID: str = """
DELETE
FROM {table}
WHERE id = %s RETURNING *
"""

UPDATE_POST_BY_ID: str = """
UPDATE {table}
SET title = %s
, content = %s
, published = %s
WHERE {column} = %s
RETURNING *
"""