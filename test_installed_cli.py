"""Verify actual installed console entry point outside the source checkout."""
import json,os,subprocess,sys,tempfile
from pathlib import Path

def main():
    py=Path(sys.argv[1]).absolute();root=Path(__file__).resolve().parent
    executable=py.parent/('invoice-rounding-ledger.exe' if os.name=='nt' else 'invoice-rounding-ledger')
    with tempfile.TemporaryDirectory() as td:
        wd=Path(td);example=json.loads((root/'example.json').read_text());snapshot=wd/'input.json';snapshot.write_text(json.dumps(example))
        def run():return subprocess.run([str(executable),str(snapshot)],cwd=wd,capture_output=True,text=True,timeout=15)
        result=run();assert result.returncode==0,(result.stdout,result.stderr);report=json.loads(result.stdout)
        if 'invoice-rounding-ledger'=='backup-chain-audit':assert report['needed_bytes']==120 and report['eligible_delete']==['obsolete']
        if 'invoice-rounding-ledger'=='kafka-offset-audit':assert report['partitions'][0]['offset_distance_to_end']==7
        if 'invoice-rounding-ledger'=='invoice-rounding-ledger':assert report['allocated_tax_minor']==2 and sum(x['allocated_tax_minor'] for x in report['lines'])==2
        if 'invoice-rounding-ledger'=='otel-span-witness':assert report['spans'][0]['clipped_direct_child_union_ns']==70
        if 'invoice-rounding-ledger'=='matrix-include-trace':assert report['job_count']==4
        snapshot.write_text('{"duplicate":1,"duplicate":2}');assert run().returncode==2
        snapshot.write_text('{');assert run().returncode==2
        snapshot.write_bytes(b' '* (2*1024*1024+1));assert run().returncode==2
        snapshot.write_text(json.dumps(example));example['unknown']=True;snapshot.write_text(json.dumps(example));assert run().returncode==2
        example.pop('unknown')
        if 'invoice-rounding-ledger'=='backup-chain-audit':example['delete']=['base'];expected=1
        elif 'invoice-rounding-ledger'=='kafka-offset-audit':example['partitions'][0]['committed']=3;expected=1
        elif 'invoice-rounding-ledger'=='otel-span-witness':example['spans']=example['spans'][1:];expected=1
        elif 'invoice-rounding-ledger'=='invoice-rounding-ledger':example['lines'][0]['unit_price']=0.1;expected=2
        else:example['axes']={'x':['${{ inputs.x }}']};expected=2
        snapshot.write_text(json.dumps(example));assert run().returncode==expected
    print('Installed console example, malformed/duplicate/oversized/unknown input and meaningful failure checks passed.')

if __name__=='__main__':main()
