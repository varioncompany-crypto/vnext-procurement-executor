#!/usr/bin/env python3
"""Retrieve current policy-aware workflow; explicit no-fixed-TTL logistics only.
Private source payloads remain outside Git; approval and quote guards are unchanged.
"""
import base64,json,subprocess,sys,tempfile,argparse,os
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-bundle',type=Path,default=os.environ.get('PROCUREMENT_SOURCE_BUNDLE_PATH'));parser.add_argument('--tracking-source',type=Path);parser.add_argument('--read-only',action='store_true');group=parser.add_mutually_exclusive_group();group.add_argument('--logistics-source',type=Path);group.add_argument('--prepare-with-logistics',type=Path);group.add_argument('--proforma-source',type=Path);group.add_argument('--account-source',type=Path);group.add_argument('--portal-account-read',action='store_true');group.add_argument('--logistics-read',action='store_true');group.add_argument('--logistics-refresh',action='store_true');parser.add_argument('--scan-request-id');args=parser.parse_args()
    if args.read_only and any((args.logistics_source,args.prepare_with_logistics,args.proforma_source)):
        parser.error('--read-only cannot be combined with order actions')
    if (args.account_source or args.portal_account_read) and not args.read_only:
        parser.error('account readers require --read-only')
    if args.portal_account_read:parser.error('portal/password execution disabled by current User instruction; use API/original events')
    if args.logistics_read and not args.read_only:parser.error('--logistics-read requires --read-only')
    with tempfile.TemporaryDirectory(prefix='varion-procurement-') as scratch:
        root=Path(scratch)
        # Current execution contract and policy are mandatory, never an archived checkout.
        for path in ('tools/PROCUREMENT-APP-CONTRACT.md','architecture/procurement-workflow.v1.json'):
            r=subprocess.run(['gh','api','repos/varioncompany-crypto/vnext-ceo/contents/'+path+'?ref=main'],capture_output=True,text=True)
            if r.returncode: raise RuntimeError('current_procurement_contract_fetch_failed')
            (root/Path(path).name).write_bytes(base64.b64decode(json.loads(r.stdout)['content']))
        for name in ('procurement_workflow.py','procurement_historical.py','procurement_delivery_status.py','procurement_planning.py','procurement_order_handoff.py','procurement_logistics_refresh.py','procurement_scan.py','procurement_tracking.py','procurement_supplier_account.py','shared_tasks.py'):
            r=subprocess.run(['gh','api','repos/varioncompany-crypto/vnext-ceo/contents/tools/'+name+'?ref=main'],capture_output=True,text=True)
            if r.returncode: raise RuntimeError('private_workflow_fetch_failed')
            x=json.loads(r.stdout);(root/name).write_bytes(base64.b64decode(x['content']))
        if args.account_source or args.portal_account_read:
            selected=['--source',str(args.account_source.resolve())] if args.account_source else ['--portal-read']
            subprocess.run([sys.executable,'-B',str(root/'procurement_supplier_account.py'),*selected,'--private-output',str(root/'private'/'account-source.json')],check=True)
            return
        selected=next(((flag,value) for flag,value in [('--logistics-source',args.logistics_source),('--prepare-with-logistics',args.prepare_with_logistics),('--proforma-source',args.proforma_source)] if value),None)
        extra=[selected[0],str(selected[1].resolve()),'--publish'] if selected else (['--read-only'] if args.read_only else ['--supplier-preflight','--publish'])+(['--source-bundle',str(args.source_bundle.resolve())] if args.source_bundle else [])
        if args.logistics_refresh:extra=['--read-only','--logistics-refresh']
        if args.logistics_read:extra+=['--logistics-read']
        if args.tracking_source:extra+=['--tracking-source',str(args.tracking_source.resolve())]
        subprocess.run([sys.executable,'-B',str(root/'procurement_workflow.py'),'--private-output',str(root/'private')]+(['--scan-request-id',args.scan_request_id] if args.scan_request_id else [])+extra,check=True)
if __name__=='__main__':main()
