"""Offline, bounded captured-input analysis. Original implementation, MIT."""
import argparse
import json
import re
import sys
from pathlib import Path

class InputError(ValueError):
    pass

def obj(x,required,optional=()):
    if not isinstance(x,dict) or set(x)-set(required)-set(optional) or set(required)-set(x):
        raise InputError("object keys do not match the documented contract")
    return x

def arr(x,limit=512):
    if not isinstance(x,list) or len(x)>limit:raise InputError("expected a bounded array")
    return x

def text(x):
    if not isinstance(x,str) or not 1<=len(x)<=256:raise InputError("expected a nonempty string <=256 characters")
    return x

def integer(x,maximum=9223372036854775807):
    if type(x) is not int or not 0<=x<=maximum:raise InputError("expected bounded nonnegative integer")
    return x

def unique(xs):
    if len(set(xs))!=len(xs):raise InputError("duplicate identity")
    return xs

def pairs(ps):
    d={}
    for k,v in ps:
        if k in d:raise InputError("duplicate JSON key")
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("snapshot",type=Path);a=p.parse_args()
    try:
        with a.snapshot.open("rb") as f:raw=f.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise InputError("snapshot exceeds2 MiB")
        d=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError("nonfinite JSON")))
        result=analyze(d);print(json.dumps(result,sort_keys=True,ensure_ascii=True));return 1 if result.get("findings") else 0
    except (InputError,ValueError,TypeError,KeyError,OSError,RecursionError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr);return 2

from fractions import Fraction

def dec(x):
    if not isinstance(x,str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,12})?",x):raise InputError("expected plain bounded decimal string")
    return Fraction(x)

def half_up(x):
    sign=-1 if x<0 else 1;n,d=abs(x.numerator),x.denominator;q,r=divmod(n,d)
    return sign*(q+(2*r>=d))

def rational(x):return str(x.numerator)+"/"+str(x.denominator)

def analyze(d):
    obj(d,["currency","digits","lines"])
    if not isinstance(d["currency"],str) or not re.fullmatch("[A-Z]{3}",d["currency"]):raise InputError("expected three-letter currency label")
    scale=10**integer(d["digits"],4);rows=[];groups={};ids=[]
    for line in arr(d["lines"]):
        obj(line,["id","quantity","unit_price","discount","tax_rate"])
        sid=text(line["id"]);ids.append(sid)
        q,u,discount,rate=[dec(line[x]) for x in ("quantity","unit_price","discount","tax_rate")]
        if u<0 or not 0<=discount<=1 or not 0<=rate<=1:raise InputError("price/rate/discount outside contract")
        net=q*u*(1-discount)*scale;tax=net*rate;floor=tax.numerator//tax.denominator
        row={"id":sid,"net":net,"tax":tax,"floor":floor,"fraction":tax-floor,"rate":rate};rows.append(row);groups.setdefault(rate,[]).append(row)
    unique(ids);output=[];group_reports=[]
    for rate,members in sorted(groups.items()):
        exact=sum((x["tax"] for x in members),Fraction());target=half_up(exact)
        extra=target-sum(x["floor"] for x in members)
        ranked=sorted(members,key=lambda x:(-x["fraction"],x["id"]));award={x["id"] for x in ranked[:extra]}
        if not 0<=extra<=len(members):raise InputError("allocation invariant failed")
        for x in members:output.append({"id":x["id"],"net_minor":half_up(x["net"]),"exact_tax_minor":rational(x["tax"]),"line_rounded_tax_minor":half_up(x["tax"]),"allocated_tax_minor":x["floor"]+(x["id"] in award)})
        line_total=sum(half_up(x["tax"]) for x in members)
        group_reports.append({"rate":rational(rate),"invoice_tax_minor":target,"sum_line_rounded_tax_minor":line_total,"difference_minor":target-line_total,"awarded_one_minor_unit":sorted(award)})
    net=sum(half_up(x["net"]) for x in rows);invoice_net=half_up(sum((x["net"] for x in rows),Fraction()));tax=sum(x["invoice_tax_minor"] for x in group_reports)
    return {"currency":d["currency"],"digits":d["digits"],"lines":sorted(output,key=lambda x:x["id"]),"tax_groups":group_reports,"sum_line_net_minor":net,"rounded_invoice_net_minor":invoice_net,"net_rounding_difference_minor":invoice_net-net,"allocated_tax_minor":tax,"payable_using_line_net_minor":net+tax,"rounding":"nearest; ties away from zero; largest fractional remainder per equal rate, id tie-break","findings":[]}

if __name__ == "__main__":
    raise SystemExit(main())
