from src.args import args
from src.cmd import run_cmd
import os, sys

def load_keys():
    print("[*] Loading public key")
    if not (os.path.isfile("keys/HOST") and os.path.isfile("keys/HOST.pub")):
        gen_HOST_keys()

    with open("keys/HOST") as f:
        host_priv = f.read(1024)
        if(args.verbose > 0):
            print("|=> Private Host Key :\n" + host_priv)
        host_priv = host_priv.replace("\n", "\\n")
    
    with open("keys/HOST.pub") as f:
        host_pub = f.read(1024)
        host_pub = " ".join(host_pub.split(" ")[:2]) + " ROGUE@SERV"
        if(args.verbose > 0):
            print("|=> Public Host Key  :\n" + host_pub)
    
    if args.public_key:
        print("[*] CLIENT public_key supplied... skipping generating new CLIENT key pair")
        run_cmd("rm keys/CLIENT{,.pub}")
        check_type(args.public_key)
        cli_pub = args.public_key
    else:
        if not (os.path.isfile("keys/CLIENT") and os.path.isfile("keys/CLIENT.pub")) and not args.public_key:
            gen_CLIENT_keys()
        with open("keys/CLIENT.pub") as f:
            cli_pub = f.read(1024)
            cli_pub = " ".join(cli_pub.split(" ")[:2]) + " ROGUE@ROGUE"

    if(args.verbose > 0):
        print("|=> Public Client Key :\n" + cli_pub)

    return host_priv, host_pub, cli_pub


def gen_HOST_keys():
    print("[*] HOST Keys generation...")
    run_cmd("rm -rf keys/; mkdir keys/")
    run_cmd("ssh-keygen -b 4096 -f keys/HOST -t ed25519 -N ''")

def gen_CLIENT_keys():
    print("[*] CLIENT Keys generation...")
    run_cmd("ssh-keygen -b 4096 -f keys/CLIENT -t ed25519 -N ''")

def check_type(key):
    print("[*] Checking key type...",end='')
    c =  key.split()[0] != "ssh-ed25519"
    if c:    
        print("key type might not be supported... please provide an ed25519 key")
        sys.exit(-1)
    else:
        print("key type good")
        return c


