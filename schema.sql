DROP TABLE IF EXISTS lists;
DROP TABLE IF EXISTS items;

CREATE TABLE lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL, --identify which list this belongs to
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES lists (id) --lists is parent table.  List can have multiple items. Items belong to a single list
);

-- lists 1----M items