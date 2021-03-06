import logging
import argparse
import psycopg2


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database='snippets')
logging.debug("Database connection established")


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
    logging.debug("Snippet stored successfully")
    return name, snippet

def catalog():
    """Retrieve list of keywords"""
    logging.info("Select keyword list")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword")
        return cursor.fetchall()
        
def search(search_string):
    "Search for a snippet based on wildcard"
    logging.info("search snippet database")
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where keyword like %s", (search_string,))
        return cursor.fetchall()
    
def get(name):
    """Retrieve the snippet with a given name."""
    logging.info("Retrieve snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    if not row:
        # No snippet was found with that name.
        return "404: Snippet Not Found"
    return row[0]
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparse for the put command
    logging.debug("Constructing the subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    # Subparse for the get command
    logging.debug("Constructing the subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of the snippet")
    
    # Subparse for the catalog command
    logging.debug("Constructing the subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve keywords")
    
    # Subparse for the search command
    logging.debug("Constructing the subparser")
    search_parser = subparsers.add_parser("search", help="Wildcard search")
    search_parser.add_argument("search_string", help="Search word")
    
    arguments = parser.parse_args()
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        keyword = catalog(**arguments)
        print("Retrieved keyword: {!r}".format(keyword))
    elif command == "search":
        search_string = search(**arguments)
        print("Search results: {!r}".format(search_string))

if __name__ == "__main__":
    main()
    
