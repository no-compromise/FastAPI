from fastapi import FastAPI
import psycopg

try:
    conn = psycopg.connect(
        host="localhost", dbname="fastapi", user="postgres", password="kokotko123"
    )
    cursor = conn.cursor()
    print("Connection to DB OK!")
except Exception as error:
    print(error)


app = FastAPI()


@app.get("/")
def root_get():
    return {"data": "root page"}
