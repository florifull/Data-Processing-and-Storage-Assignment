"""
This module implements an in-memory key-value database with transaction support.
"""

class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.temp_changes = {}
        self.transaction_in_progress = False

    def begin_transaction(self):
        if self.transaction_in_progress:
            raise Exception("A transaction is already in progress")
        self.transaction_in_progress = True
        self.temp_changes = {}

    def put(self, key, val):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        self.temp_changes[key] = val

    def get(self, key):
        if key in self.temp_changes:
            return self.temp_changes[key]
        return self.data.get(key)

    def commit(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction to commit")
        self.data.update(self.temp_changes)
        self.temp_changes.clear()
        self.transaction_in_progress = False

    def rollback(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction to rollback")
        self.temp_changes.clear()
        self.transaction_in_progress = False

def main():
    db = InMemoryDB()

    # Test case 1: Get non-existent key
    print(db.get("A"))  # Should print None

    # Test case 2: Put without transaction
    try:
        db.put("A", 5)
    except Exception as e:
        print(f"Error: {e}")  # Should print error

    # Test case 3: Begin transaction and put
    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))  # Should print None (not committed yet)

    # Test case 4: Update within transaction
    db.put("A", 6)
    db.commit()
    print(db.get("A"))  # Should print 6

    # Test case 5: Commit without transaction
    try:
        db.commit()
    except Exception as e:
        print(f"Error: {e}")  # Should print error

    # Test case 6: Rollback without transaction
    try:
        db.rollback()
    except Exception as e:
        print(f"Error: {e}")  # Should print error

    # Test case 7: Transaction with rollback
    print(db.get("B"))  # Should print None
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))  # Should print None

if __name__ == "__main__":
    main()