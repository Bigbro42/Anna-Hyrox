from playwright.sync_api import sync_playwright
from pathlib import Path
import shutil
import json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text().replace('<link rel="stylesheet" href="./styles.css">', '<style>'+(root/'styles.css').read_text()+'</style>').replace('<script type="module" src="./app.js"></script>','')
js=(root/'app.js').read_text()
plan=json.loads((root/'plan.json').read_text())

def boot(page,saved=None):
 page.set_content(html)
 page.evaluate('''({plan,saved})=>{window.__mockPlan=plan;window.__local=saved||{};window.fetch=async()=>({ok:true,json:async()=>JSON.parse(JSON.stringify(window.__mockPlan))});Object.defineProperty(window,'indexedDB',{configurable:true,value:undefined});Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window.__local[k]||null,setItem:(k,v)=>window.__local[k]=v}});window.scrollTo=()=>{}}''',dict(plan=plan,saved=saved))
 page.add_script_tag(content=js)
 page.wait_for_function("document.querySelector('h1')?.textContent.includes('Heute')",timeout=8000)

with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,accept_downloads=True)
 page=ctx.new_page();errors=[];page.on('pageerror',lambda x:errors.append(str(x)))
 page.on('dialog',lambda d: d.accept('RESET') if d.type=='prompt' and 'RESET' in d.message else d.accept())
 boot(page)
 assert page.locator('h1').first.inner_text().startswith('Heute')
 assert page.locator('.metric b').first.inner_text()=='1'
 for route,heading in [('calendar','Kalender'),('training','Trainingsplan'),('partner','Partnerstrategie'),('progress','Fortschritt')]:
  page.locator(f'button[data-route="{route}"]').last.click()
  assert heading.split()[0].lower() in page.locator('h1').first.inner_text().lower(),(route,page.locator('h1').first.inner_text())
  assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'overflow {route}'
  print('PASS route',route)
 page.locator('button[data-route="training"]').last.click()
 page.locator('button[data-week="1"]').click()
 assert page.locator('.workout').count()==4
 page.locator('button[data-open="w01-B"]').click()
 assert page.locator('.exercise').count()>=7
 title_before=page.locator('input[data-field="title"]').input_value()
 page.locator('input[data-field="title"]').fill('Kraft Test angepasst');page.locator('input[data-field="title"]').press('Tab')
 page.locator('input[data-exercise="0|actual"]').fill('15 Min.');page.locator('input[data-exercise="0|actual"]').press('Tab')
 page.locator('input[data-exercise-done="0"]').check()
 page.locator('button[data-status="done"]').click()
 saved=page.evaluate('window.__local')
 assert next(x for x in json.loads(saved['anna-hyrox2-local-backup-v1'])['sessions'] if x['id']=='w01-B')['title']=='Kraft Test angepasst'
 print('PASS edit, completion, local backup')
 # start a fresh page: mock storage survives via the saved snapshot
 page.close()
 page=ctx.new_page()
 page.on('pageerror',lambda x:errors.append(str(x)))
 page.on('dialog',lambda d: d.accept('RESET') if d.type=='prompt' and 'RESET' in d.message else d.accept())
 boot(page,saved)
 page.locator('button[data-route="progress"]').last.click()
 assert page.locator('.metric b').first.inner_text()=='2'
 page.locator('button[data-route="partner"]').last.click()
 first=page.locator('input[data-partner="0|share"]');first.fill('425 m');first.press('Tab')
 assert page.locator('input[data-partner="0|share"]').input_value()=='425 m'
 print('PASS rehydration, score, partner')
 page.locator('button[data-route="settings"]').first.click()
 with page.expect_download() as dl:page.locator('button[data-export]').click()
 f=dl.value
 backup=json.loads(f.path().read_text())
 assert backup['app']=='anna-hyrox2'
 assert len(backup['data']['sessions'])==55
 with page.expect_download() as dc:page.locator('button[data-csv]').click()
 data=dc.value.path().read_text()
 assert 'Kraft Test angepasst' in data
 print('PASS JSON and CSV export')
 page.locator('#planStart').fill('2026-10-26')
 page.locator('#raceDate').fill('2027-01-26')
 page.locator('button[data-settings-save]').click()
 state=json.loads(page.evaluate('window.__local')["anna-hyrox2-local-backup-v1"])
 assert state['startDate']=='2026-10-26'
 assert state['raceDate']=='2027-01-26'
 assert next(x for x in state['sessions'] if x['id']=='w01-B')['date']=='2026-10-28'
 assert next(x for x in state['sessions'] if x['id']=='race-2')['date']=='2027-01-26'
 print('PASS moving overall plan and race date')
 page.locator('button[data-route="calendar"]').last.click()
 assert page.locator('.day').count()>=28
 page.locator('button[data-route="training"]').last.click()
 page.locator('button[data-week="1"]').click()
 assert page.locator('.workout').count()==4
 print('PASS calendar and 13 week plan')
 # verify no unexpected errors
 assert not errors,errors
 print('ALL CHECKS PASS',len(errors))
 b.close()
