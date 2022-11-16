#!/usr/bin/env python3

import json,sys,toml,subprocess,tempfile

def main():
    args=sys.argv
    args[0]='jq'
    with tempfile.SpooledTemporaryFile(mode='wt+') as tfp:
        json.dump(toml.loads(sys.stdin.read()),tfp)
        tfp.seek(0)
        return subprocess.run(args,stdin=tfp,text=True).returncode

if __name__ == '__main__':
    sys.exit(main())
