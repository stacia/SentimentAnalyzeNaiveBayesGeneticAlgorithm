import tweepy, sqlite3
from myTwitterAPI import consumer_key, consumer_secret, access_token, access_token_secret

# Membuat database
def createDB():
    try:
        c.execute("""CREATE TABLE jokowiNewNormal(
                [primary_key] INTEGER PRIMARY KEY NOT NULL,
                [dateTime] TEXT, 
                [id] TEXT, 
                [originalTweet] TEXT,
                [preprocessResultTweet] TEXT,
                [sentimentType] TEXT
                )""")
        print('new (Database/Table created)')

    # Jika udah ada database atau table nya
    except:
        print('pass (Database already exist)')
        pass

# Fungsi untuk memasukkan value ke database
def insertValue2dB(date, id, text):
    execute = ("""INSERT INTO 
                jokowiNewNormal(
                    dateTime, 
                    id, 
                    originalTweet)
                values(
                    '{}',
                    '{}',
                    '''{}''')""").format(date, id, text) # waktu, id status, teks full
    # print(execute)
    c.execute(execute)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True) # Autentikasi API

# buat database dengan  sqlite3
dbPATH = 'jokowidanNewNormal.db'   # PATH
conn = sqlite3.connect(dbPATH)  # konek ke databasenya, kalau belum ada filenya nanti buat sendiri
c = conn.cursor()   # kursor untuk edit database
createDB() # buat database

user_name = "@jokowi"
# user_name = '@aniesbaswedan'
morekeyword = 'new normal'

# Mengambil tweet dari balasan orang
replies = tweepy.Cursor(api.search, q='to:{} AND {}'.format(user_name, morekeyword),
                                tweet_mode='extended',
                                ).items(1000)
# Iterasi untuk database
num = 0
for r in replies:
    text = r.full_text.replace("'", '''"''')
    print()
    print(num, r.created_at, r.id, text)
    num+=1
    insertValue2dB(r.created_at, r.id, text)
    conn.commit()

c.close() # tutup koneksi database