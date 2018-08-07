
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "Wee6fqwfWRZaTsNm2lNdeZemB"
csecret = "4k5VQ9rS9ivJHBmAGKBFy29vWu2oBCnzMA9xxq5kSlK1bGmuGk"
atoken = "767136071817826304-aOjltLigv68ywKrYnHOszlsaNuHBCAU"
asecret = "JPnKD9Ss20vCFyCOpoTYZn3haDC4repX9B7GzVZHWTi2N"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado" + "=> " + dictTweet["_id"])
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
    db = server.create('restaurantes')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['restaurantes']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["Osteria Francescana","Celler de Can Roca", "Mirazur", "Eleven Madison Park", "Gaggan","Central", "Maido", "Arpège", "Mugaritz", "Asador Etxebarri", "American Bar", "Dandelyan Bar",
                            "Nomad Bar", "Connaught Bar", "The Clumsies", "Manhattan", "Attaboy", "Bar Termini", "Speak Low", "Green Valley",
                            "Ushuaïa", "Zouk", "Echostage", "Hï"])
