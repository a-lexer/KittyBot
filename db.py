import sqlite3
import os
import hashlib
import logging
import imagehash

def cursor():
    return conn.cursor()

def commit():
    conn.commit()

def start():
    c = cursor()
    c.execute("CREATE TABLE IF NOT EXISTS emoji_counts (user TEXT, emoji TEXT, count INTEGER)")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS emoji_counts_idx ON emoji_counts (user, emoji)")
    c.execute("CREATE TABLE IF NOT EXISTS message_counts (user TEXT, count INTEGER)")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS message_counts_idx ON message_counts (user)")
    c.execute("CREATE TABLE IF NOT EXISTS message_hashes (user TEXT, message_id TEXT, message_hash TEXT, time_sent TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS image_hashes (hash TEXT, message_id TEXT, channel_id TEXT, guild_id TEXT)")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS message_hashes_idx ON message_hashes (message_hash)")
    c.execute("CREATE TABLE IF NOT EXISTS message_deletes (user TEXT, count INTEGER)")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS message_deletes_idx ON message_deletes (user)")
    try:
        c.execute("ALTER TABLE image_hashes ADD hash_color TEXT NOT NULL")
    except Exception as ex:
        logging.info(ex)

    # EmojiCache Table Removed

def md5sum(m):
    return hashlib.md5(m.encode('utf-8')).hexdigest()

def hammingDistance(a, b):
    return imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b)

conn = sqlite3.connect(os.environ.get('KITTY_DB', 'persist.sqlite'))
conn.create_function("md5", 1, md5sum)
conn.create_function("hammingDistance", 2, hammingDistance)
start()