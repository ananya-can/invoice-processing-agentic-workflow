import sqlite3


def create_inventory_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            item TEXT PRIMARY KEY,
            stock INTEGER
        )
    """)

    # Reset data (so it doesn't duplicate every run)
    cursor.execute("DELETE FROM inventory")

    # Insert sample inventory
    cursor.executemany("""
        INSERT INTO inventory (item, stock) VALUES (?, ?)
    """, [
        ("WidgetA", 15),
        ("WidgetB", 10),
        ("GadgetX", 5),
        ("FakeItem", 0)
    ])

    conn.commit()
    conn.close()

    print("inventory.db created successfully with sample data.")


if __name__ == "__main__":
    create_inventory_db()