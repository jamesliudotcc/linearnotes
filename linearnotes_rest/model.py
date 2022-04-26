from __future__ import annotations
import aiosqlite

DB_PATH = "example.db"

# TODO: Do this in a literate programming style. Describe how to create an FT5
# table, have a way to create a new DB and create the table. Don't assume it
# exists. Also, encapsulate this into a class to encapsulate setup/teardown

class Model():
    """The model is meant to be extremely simple, to the point of being naive.
    
    I don't anticipate supporting more than a sinle user. This is not meant for a
    multiuser application. You clone or fork this and deploy it on your own computer,
    your own network, or your own free hosting provider. It's for you.
    
    The one interesting-ish thing is the full text search 
    
    Maybe don't do a class. Just use the module as a singleton. Do the setup at import
    time and that's it.
    
    """

async def save_note(note: str) -> None:
    """Save a note

    TODO: Create a git style sha and save with, also time created.
    TODO: Allow creation of a note related to an ealier note"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT INTO notes(note) VALUES(?)""", [note])
        await db.commit()

async def search_notes(terms: str) -> list[str]:
    """Search the notes using full text search.
    If an empty string is passed, do the expected thing and return all results.
    TODO: Add limit, skip logic"""
    async with aiosqlite.connect(DB_PATH) as db:
        if not terms:
            query = """SELECT * FROM notes"""
            cursor = await db.execute(query)
        else:
            query = """SELECT * FROM notes WHERE note MATCH ?"""
            cursor = await db.execute(query, [terms])
        rows = await cursor.fetchall()
        await cursor.close()


    # row is a tuple with one item TODO also add date and sha
    return [row[0] for row in rows]
