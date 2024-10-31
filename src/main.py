import os
import sys
sys.path.append(os.path.abspath('..'))

from waitress import serve

from src import app


def main():
    port = int(os.getenv("PORT"))
    print(port)
    serve(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
