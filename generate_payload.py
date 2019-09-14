import sys
import os
import json
import argparse

# print(data)
def generate_payload(data,host):
    for listener in data:
        for payload in listener['payloads']:
            print('generating payload:',payload['name'],'....')
            cmd=payload['generate'].replace('<host>',host).replace('<port>',str(listener['port']))
            print(cmd)
            os.system(cmd)

def generate_special_usage(data):
    with open('special_usage.txt','w') as f:
        for listener in data:
            for payload in listener['payloads']:
                try:
                    f.write(payload['name']+':\n\t'+payload['usage']+'\n')
                except KeyError:
                    pass
                

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='setup your meterpreter payloads')
    parser.add_argument('host',help='ip of your host')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    # print(sys.argv)
    # args = parser.parse_args()
    args = parser.parse_args(['1.1.1.1'])
    # print(args.host)

    with open('all_payload.json','r') as f:
        json_data = f.read()

    data = json.loads(json_data)
    # print(data)
    generate_payload(data,args.host)
    generate_special_usage(data)