import fs from 'fs';
import { feature } from 'topojson-client';

const topo = JSON.parse(fs.readFileSync('data/au_sa4_2021.topo.json','utf8'));
const fc = feature(topo, topo.objects.sa4);

// volunteer counts per SA4
const rows = fs.readFileSync('data/volunteer_sa4_2021.csv','utf8').trim().split('\n');
const head = rows[0].split(',');
const recs = rows.slice(1).map(l => {
  // simple CSV split is unsafe for quoted commas -> use a small parser
  const out=[]; let cur='', q=false;
  for (const ch of l){ if(ch==='"') q=!q; else if(ch===',' && !q){out.push(cur);cur='';} else cur+=ch; }
  out.push(cur);
  return Object.fromEntries(head.map((h,i)=>[h,out[i]]));
});
const info = {};
for (const r of recs) if (r.region_type !== 'Other Territories') info[r.sa4_code] = r;

const PER = Number(process.env.PER || 4000);

// --- geometry helpers (lon/lat plane; fine at this scale for placement) ---
function ringsOf(geom){
  if (geom.type === 'Polygon') return [geom.coordinates];
  if (geom.type === 'MultiPolygon') return geom.coordinates;
  return [];
}
function inRing(x,y,ring){
  let inside=false;
  for(let i=0,j=ring.length-1;i<ring.length;j=i++){
    const xi=ring[i][0], yi=ring[i][1], xj=ring[j][0], yj=ring[j][1];
    if (((yi>y)!==(yj>y)) && (x < (xj-xi)*(y-yi)/(yj-yi)+xi)) inside=!inside;
  }
  return inside;
}
function inPoly(x,y,poly){                 // poly = [outer, hole, hole...]
  if(!inRing(x,y,poly[0])) return false;
  for(let k=1;k<poly.length;k++) if(inRing(x,y,poly[k])) return false;
  return true;
}
function ringArea(ring){                   // signed planar area, lat-corrected
  let a=0;
  for(let i=0,j=ring.length-1;i<ring.length;j=i++){
    const latm=(ring[i][1]+ring[j][1])/2, k=Math.cos(latm*Math.PI/180);
    a += (ring[j][0]*k*ring[i][1] - ring[i][0]*k*ring[j][1]);
  }
  return Math.abs(a/2);
}

// deterministic PRNG so the map is identical on every build
let seed = 20211001;
function rnd(){ seed = (seed*1664525 + 1013904223) % 4294967296; return seed/4294967296; }

const dots=[]; let missing=[];
for (const f of fc.features){
  const code = String(f.properties.sa4_code);
  const rec = info[code];
  if (!rec) continue;
  const n = Math.round(Number(rec.volunteers)/PER);
  if (n < 1) continue;
  const polys = ringsOf(f.geometry);
  const areas = polys.map(p=>ringArea(p[0]));
  const total = areas.reduce((a,b)=>a+b,0);
  // bounding boxes per part
  const bb = polys.map(p=>{
    let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    for(const [x,y] of p[0]){ if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; }
    return [x0,y0,x1,y1];
  });
  let placed=0, guard=0;
  while (placed<n && guard<n*4000){
    guard++;
    // pick a part in proportion to its area
    let t=rnd()*total, pi=0;
    while(pi<areas.length-1 && t>areas[pi]){ t-=areas[pi]; pi++; }
    const [x0,y0,x1,y1]=bb[pi];
    const x=x0+rnd()*(x1-x0), y=y0+rnd()*(y1-y0);
    if (inPoly(x,y,polys[pi])){
      dots.push({lon:+x.toFixed(4), lat:+y.toFixed(4), sa4_code:code,
                 sa4_name:rec.sa4_name, state_abbr:rec.state_abbr,
                 region_type:rec.region_type, volunteers:rec.volunteers,
                 rate_pop15plus:rec.rate_pop15plus});
      placed++;
    }
  }
  if (placed<n) missing.push(rec.sa4_name+' '+placed+'/'+n);
}
const cols=['lon','lat','sa4_code','sa4_name','state_abbr','region_type','volunteers','rate_pop15plus'];
const esc=v=>/[",]/.test(v)?'"'+String(v).replace(/"/g,'""')+'"':v;
fs.writeFileSync('data/dotdensity_sa4_2021.csv',
  cols.join(',')+'\n'+dots.map(d=>cols.map(c=>esc(d[c])).join(',')).join('\n')+'\n');
const tot = recs.filter(r=>r.region_type!=='Other Territories').reduce((a,r)=>a+Number(r.volunteers),0);
console.log('one dot =', PER, 'volunteers');
console.log('dots placed:', dots.length, '| expected ~', Math.round(tot/PER));
console.log('regions short of their quota:', missing.length ? missing.join('; ') : 'none');
