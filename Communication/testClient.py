import client
import json

if __name__ =="__main__":
	client.run()

	data = {
    'ID' : 101,
    'X'  : 100.0,
    'Y'  : 200.0,
    'Z'  : 300.0,
    'speed' : 15.0,
    'pitch' : 16.0,
    'roll'  : 17.0,
    'azimuth' : 18.0
    }
    data = json.dumps(data)
    client.send(data)
