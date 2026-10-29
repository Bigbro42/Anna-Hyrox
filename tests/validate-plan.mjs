import fs from 'node:fs';
import assert from 'node:assert/strict';
const plan=JSON.parse(fs.readFileSync(new URL('../plan.json',import.meta.url),'utf8'));
assert.equal(plan.weeks.length,13);
assert.equal(plan.sessions.filter(x=>x.week<=13).length,52);
assert.equal(plan.sessions.filter(x=>x.week===14).length,3);
assert.equal(plan.partnerStrategy.length,8);
assert.equal(plan.metadata.sourceRaceDate,'2027-01-19');
assert.equal(plan.sessions.find(x=>x.id==='w02-A').status,'done');
for(let i=1;i<=13;i++){
 const ws=plan.sessions.filter(x=>x.week===i);
 assert.deepEqual(new Set(ws.map(x=>x.slot)),new Set(['A','B','C','D']));
 assert(ws.every(x=>x.exercises.length>=2));
 for(const s of ws){assert.match(s.date,/^\d{4}-\d{2}-\d{2}$/);assert(s.description.length>8);assert(s.exercises.every(e=>e.name.length>0));}
}
console.log('PASS: 13 weeks, 52 detailed workouts, 3 race days, 8 stations, source dates and status.');
