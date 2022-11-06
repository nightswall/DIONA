#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time, random, sys, json

params: dict = {}

def on_publish():
    global params
    while 1:
        with open(params['rwfile']) as p:
            output: dict = json.load(p)
            p.close()
        output['id'] = params['id']
        for board in params['board']:
            client.publish(board, json.dumps(output))
        time.sleep(output['delay'])

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for board in params['board']:
        client.subscribe(board)

def on_message(client, userdata, msg):
    decoded_msg = msg.payload.decode()
    payload = json.loads(decoded_msg)
    with open(params['rwfile'], 'w') as s:
        json.dump(payload, s)
        s.close()
    for k,v in payload.items():
        print(f'{k}:{v}', end=" ")
    print()
    
"""
    client_config.json
    {
        'id': <int>,
        'host': <str> (ipv4),
        'port': <int>,
        'ttl': <int> (secs),
        'mode': <int> (0:=Subs, 1:=Pubs),
        'rwfile': <str> (realpath),
        'board': <str> (subs_or_pubs_path)
    }
"""
if __name__ == "__main__":
    for arg in sys.argv[1:]:
        k, v = arg.split(':')
        if k == 'board':
            params[k] = v.split(';')
        else:
            params[k] = int(v) if k in ('mode', 'port', 'ttl', 'id') else v

    client: mqtt.Client = mqtt.Client()
    client.connect(params['host'], params['port'], params['ttl'])
    try:
        if params['mode'] == 0:
            client.on_connect = on_connect
            client.on_message = on_message
            client.loop_forever()
        elif params['mode'] == 1:
            on_publish()

    except Exception as e:
        print(e)


    
