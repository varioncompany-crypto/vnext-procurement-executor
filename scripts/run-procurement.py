#!/usr/bin/env python3
"""Retrieve the current authorized private workflow; retain no private source payloads."""
import base64,json,subprocess,sys,tempfile,argparse,os
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-bundle',type=Path,default=os.environ.get('PROCUREMENT_SOURCE_BUNDLE_PATH'));args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='varion-procurement-') as scratch:
        root=Path(scratch)
        for name in ('procurement_workflow.py','procurement_planning.py','procurement_order_handoff.py','shared_tasks.py'):
            r=subprocess.run(['gh','api','repos/varioncompany-crypto/vnext-ceo/contents/tools/'+name+'?ref=main'],capture_output=True,text=True)
            if r.returncode: raise RuntimeError('private_workflow_fetch_failed')
            x=json.loads(r.stdout);(root/name).write_bytes(base64.b64decode(x['content']))
        extra=['--source-bundle',str(args.source_bundle.resolve())] if args.source_bundle else []
        subprocess.run([sys.executable,'-B',str(root/'procurement_workflow.py'),'--private-output',str(root/'private'),'--supplier-preflight','--publish']+extra,check=True)
if __name__=='__main__':main()
