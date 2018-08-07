
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "a3EFsN0kUu04QtdUJlFdSBrHH"
csecret = "uXXkD81WVnhLk0M8tdNb8jDXAsQhIGzKSFcUQRlDShWFl9Wzg3"
atoken = "2593813213-Fi5yWsk71uKcGmDconMaY8obRVV4A5QXmP9TVQU"
asecret = "4nXx4BNOE9QK5MMW1TxXAxz3U69hBdB1Y1caXp2rJ0Nz0"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('hobbies1')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['hobbies1']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweet
twitterStream.filter(track=["futbol",
                            "soccer",
                            "basket",
                            "boli",
                            "ajedrez",
                            "billar",
                            "boliche",
                            "crucigrama",
                            "baile",
                            "dibujo",
                            "cartas",
                            "pesca",
                            "pintura",
                            "fotografía",
                            "lectura"])


