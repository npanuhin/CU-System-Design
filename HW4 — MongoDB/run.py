import pymongo
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://root:example@localhost:27017/"
DB_NAME = "hw4"
COLLECTION_NAME = "books"

def main():
    client = None
    try:
        print("Connecting to MongoDB...")
        client = pymongo.MongoClient(MONGO_URI)
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")

        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        print("\n--- Writing data ---")
        new_book = {
            "title": "Master and Margarita",
            "author": "Mikhail Bulgakov",
            "year": 1967,
            "genre": "Novel"
        }

        if collection.count_documents({"title": new_book["title"]}) == 0:
            result = collection.insert_one(new_book)
            print(f"Added new book with ID: {result.inserted_id}")
        else:
            print(f"Book '{new_book['title']}' already exists in the database.")

        print("\n--- Reading data ---")
        print("All books in the collection:")

        all_books = collection.find()

        if collection.count_documents({}) > 0:
            for book in all_books:
                print(f"- '{book['title']}' by {book['author']}, {book['year']}, genre: {book['genre']}")
        else:
            print("No books found in the collection.")

    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("\nMongoDB connection closed.")

if __name__ == "__main__":
    main()

