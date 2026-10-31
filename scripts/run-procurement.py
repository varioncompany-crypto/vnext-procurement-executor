#!/usr/bin/env python3
"""Retrieve the current authorized private workflow; retain no private source payloads."""
import base64,json,subprocess,sys,tempfile
from pathlib import Path

def main():
    with tempfile.TemporaryDirectory(prefix='varion-procurement-') as scratch:
        root=Path(scratch)
        for name in ('procurement_workflow.py','shared_tasks.py'):
            r=subprocess.run(['gh','api','repos/varioncompany-crypto/vnext-ceo/contents/tools/'+name+'?ref=main'],capture_output=True,text=True)
            if r.returncode: raise RuntimeError('private_workflow_fetch_failed')
            x=json.loads(r.stdout);(root/name).write_bytes(base64.b64decode(x['content']))
        subprocess.run([sys.executable,'-B',str(root/'procurement_workflow.py'),'--private-output',str(root/'private'),'--supplier-preflight','--publish'],check=True)
if __name__=='__main__':main()
