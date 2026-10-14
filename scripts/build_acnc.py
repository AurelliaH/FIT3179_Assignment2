"""Section-5 treemap data: volunteers by charitable purpose.

Joins the ACNC 2024 Annual Information Statement (volunteer counts) to the
ACNC Charity Register (charitable purposes) on ABN.

The Register records up to 12 charitable purposes per charity, so a charity can
tick several. To keep the treemap a true partition with no double counting:
  - exactly one purpose ticked  -> that purpose
  - more than one               -> "More than one purpose"
  - none ticked                 -> "Purpose not stated"
Registered charities only, and only those reporting at least one volunteer.
No reported value is altered; the largest charities in each purpose are named
so outliers are visible rather than hidden.
"""
import csv, collections, re

REG="/mnt/user-data/uploads/Downloads/datadotgov_main.csv"
AIS="/mnt/user-data/uploads/datadotgov_ais24.csv"
OUT="/home/claude/story/data/acnc_volunteers_2024.csv"
OUT2="/home/claude/story/data/acnc_purposes_2024.csv"
OUT3="/home/claude/story/data/acnc_purpose_split_2024.csv"
TOPN=1
GUT=0.45                    # gutter inside each purpose block, in layout units
KEEP=9                      # purposes shown on their own; the rest merge
W,H=100.0,50.0
PX_W,PX_H=1100.0,550.0   # the fixed chart box the layout is tuned for

PURPOSE={
 "Advancing_social_or_public_welfare":"Social welfare",
 "Advancing_Religion":"Religion",
 "Advancing_Education":"Education",
 "Advancing_Health":"Health",
 "Advancing_Culture":"Culture and recreation",
 "Advancing_natual_environment":"Environment",
 "Preventing_or_relieving_suffering_of_animals":"Animals",
 "Promoting_or_protecting_human_rights":"Human rights",
 "Advancing_security_or_safety_of_Australia_or_Australian_public":"Safety and emergency",
 "Promoting_reconciliation__mutual_respect_and_tolerance":"Reconciliation",
 "Promote_or_oppose_a_change_to_law__government_poll_or_prac":"Law and advocacy",
 "Purposes_beneficial_to_ther_general_public_and_other_analogous":"Other public benefit",
}
def abn(v): return re.sub(r"\D","", v or "")
def iv(r,k):
    v=(r.get(k) or "").strip().replace(",","")
    try: return int(float(v))
    except: return 0

def worst(row, short):
    s=sum(row); mn,mx=min(row),max(row)
    if s<=0 or short<=0 or mn<=0: return float('inf')
    return max((short*short*mx)/(s*s), (s*s)/(short*short*mn))

def squarify(values, x, y, w, h):
    out=[None]*len(values)
    order=sorted(range(len(values)), key=lambda i:-values[i])
    total=sum(values)
    if total<=0 or w<=0 or h<=0: return [(x,y,x,y)]*len(values)
    scaled=[values[i]*(w*h)/total for i in order]
    pos=0
    while pos<len(scaled):
        short=min(w,h)
        row=[scaled[pos]]; best=worst(row,short); k=pos+1
        while k<len(scaled):
            t=worst(row+[scaled[k]], short)
            if t>best: break
            row=row+[scaled[k]]; best=t; k+=1
        rs=sum(row)
        if w>=h:
            rw=rs/h if h else 0; oy=y
            for j,v in enumerate(row):
                rh=(v/rs*h) if rs else 0
                out[order[pos+j]]=(x,oy,x+rw,oy+rh); oy+=rh
            x+=rw; w-=rw
        else:
            rh=rs/w if w else 0; ox=x
            for j,v in enumerate(row):
                rw=(v/rs*w) if rs else 0
                out[order[pos+j]]=(ox,y,ox+rw,y+rh); ox+=rw
            y+=rh; h-=rh
        pos=k
    return out

sector={}
for r in csv.DictReader(open(REG, encoding="utf-8-sig", errors="replace")):
    f=[lbl for k,lbl in PURPOSE.items() if (r.get(k) or "").strip().lower() in ("y","yes","true","1")]
    a=abn(r.get("ABN"))
    if a:
        sector[a]= f[0] if len(f)==1 else ("More than one purpose" if f else "Purpose not stated")

groups=collections.defaultdict(list); unmatched=0
for r in csv.DictReader(open(AIS, encoding="utf-8-sig", errors="replace")):
    if (r.get("registration status") or "").strip()!="Registered": continue
    v=iv(r,"staff - volunteers")
    if v<=0: continue
    a=abn(r.get("abn"))
    if a not in sector: unmatched+=1; continue
    groups[sector[a]].append(((r.get("charity name") or "").strip(), v))

tot=sum(v for g in groups.values() for _,v in g)
ranked=sorted(groups, key=lambda k:-sum(v for _,v in groups[k]))
keep, merge = ranked[:KEEP], ranked[KEEP:]
if merge:
    groups["Other purposes"]=[x for k in merge for x in groups[k]]
    for k in merge: del groups[k]
    keep=keep+["Other purposes"]

gvals=[sum(v for _,v in groups[g]) for g in keep]
grects=squarify(gvals, 0, 0, W, H)
out=[]
for g,(gx0,gy0,gx1,gy1) in zip(keep, grects):
    # inset the block so the purpose blocks read as separate cards with gutters
    gx0,gy0,gx1,gy1 = gx0+GUT, gy0+GUT, gx1-GUT, gy1-GUT
    items=sorted(groups[g], key=lambda t:-t[1])
    named=items[:TOPN]; rest=sum(v for _,v in items[TOPN:])
    cells=list(named)+([("%d other charities" % (len(items)-TOPN), rest)] if len(items)>TOPN else [])
    rects=squarify([v for _,v in cells], gx0, gy0, gx1-gx0, gy1-gy0)
    for (name,v),(x0,y0,x1,y1) in zip(cells, rects):
        cell_px=(x1-x0)/W*PX_W
        maxc=int((cell_px-26)/7.35)
        disp=name[4:] if name.startswith("The ") else name
        if len(disp)<=maxc:
            short=disp
        else:                                   # trim on a word boundary, never mid-word
            cut=disp[:max(0,maxc-1)].rsplit(" ",1)[0]
            short=(cut+"\u2026") if cut else ""
        if maxc<6: short=""
        out.append({"sector":g,"charity":name,"label":short,"volunteers":v,
                    "share_pct":round(v/tot*100,2),
                    "x0":round(x0,3),"y0":round(y0,3),"x1":round(x1,3),"y1":round(y1,3),
                    "cell_w":round(x1-x0,3),"cell_h":round(y1-y0,3),
                    "named":"yes" if (name,v) in named else "no"})

def wrap(name, px):
    """Break a purpose name over two lines when one line will not fit the block."""
    if len(name)*7.15+18 <= px or " " not in name:
        return name, len(name), 1
    words=name.split(); best=None
    for i in range(1,len(words)):
        a=" ".join(words[:i]); b=" ".join(words[i:])
        m=max(len(a),len(b))
        if best is None or m<best[1]: best=(a+"\n"+b, m)
    return best[0], best[1], 2

blocks=[]
for g,(gx0,gy0,gx1,gy1),gt in zip(keep, grects, gvals):
    pw=(gx1-gx0-2*GUT)/W*PX_W; ph=(gy1-gy0-2*GUT)/H*PX_H
    wrapped,longest,lines=wrap(g,pw)
    pct_long="%.1f%% of all roles" % (gt/tot*100)
    pct_short="%.1f%%" % (gt/tot*100)
    blocks.append({"sector":g,"volunteers":gt,"share_pct":round(gt/tot*100,1),
                   "charities":len(groups[g]),
                   "x0":round(gx0+GUT,3),"y0":round(gy0+GUT,3),
                   "x1":round(gx1-GUT,3),"y1":round(gy1-GUT,3),
                   "block_w":round(gx1-gx0,3),"block_h":round(gy1-gy0,3),
                   "px_w":round(pw,1),"px_h":round(ph,1),
                   "name":wrapped,"name_lines":lines,
                   "show_name":"yes" if (longest*7.15+18<=pw and ph>=30) else "no",
                   "pct_text":pct_long if len(pct_long)*6.7+20<=pw else pct_short,
                   "show_pct":"yes" if (longest*7.15+18<=pw and ph>=30+lines*19
                                        and len(pct_short)*6.7+20<=pw) else "no"})

# Section-5 bar chart: each purpose split into its single largest charity and the rest,
# because in two purposes one organisation is most of the total.
split=[]
for i,(g,gt) in enumerate(sorted(zip(keep,gvals), key=lambda t:-t[1])):
    items=sorted(groups[g], key=lambda t:-t[1])
    top_name, top_v = items[0]
    rest_v = sum(v for _,v in items[1:])
    disp = top_name[4:] if top_name.startswith("The ") else top_name
    split.append({"sector":g,"order":i,"segment":"Largest single charity",
                  "charity":disp,"volunteers":top_v,
                  "share_pct":round(top_v/tot*100,2),
                  "seg_share_of_purpose":round(top_v/gt*100,1),
                  "purpose_total":gt,"purpose_share":round(gt/tot*100,1),
                  "charities":len(items)})
    split.append({"sector":g,"order":i,"segment":"All other charities",
                  "charity":"%d other charities" % (len(items)-1),"volunteers":rest_v,
                  "share_pct":round(rest_v/tot*100,2),
                  "seg_share_of_purpose":round(rest_v/gt*100,1),
                  "purpose_total":gt,"purpose_share":round(gt/tot*100,1),
                  "charities":len(items)})
with open(OUT3,"w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(split[0])); w.writeheader(); w.writerows(split)
print("wrote %s  (%d rows)" % (OUT3, len(split)))

with open(OUT2,"w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(blocks[0])); w.writeheader(); w.writerows(blocks)
print("wrote %s  (%d blocks)" % (OUT2, len(blocks)))

with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("wrote %s  (%d cells)" % (OUT, len(out)))
print("volunteers %s across %s charities; %d AIS charities had no Register match"
      % (f"{tot:,}", f"{sum(len(v) for v in groups.values()):,}", unmatched))
for g,gt in sorted(zip(keep,gvals), key=lambda t:-t[1]):
    print("   %-24s %12s  %5.1f%%" % (g, f"{gt:,}", gt/tot*100))
