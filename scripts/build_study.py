"""Build and validate original offline lessons from committed curriculum sources."""
import argparse
import importlib
import json
from pathlib import Path
from curriculum.common import COURSES

ROOT=Path(__file__).resolve().parents[1]
MODULES=['python_notes','web_notes','frontend_notes','backend_notes','systems_notes','ai_notes','career_notes']

PATHS=[
 dict(title='Frontend Developer',level='Start with the browser',description='Build the pages, interactions and accessible interfaces users see.',courses=['html','css','javascript','git','typescript','react','next'],project='Build an accessible portfolio, a weather dashboard and a tested storefront interface.'),
 dict(title='Backend Developer',level='Choose Python or Node first',description='Design APIs, model data, validate input and enforce permissions on the server.',courses=['python','node','python-backend','databases','networks','security','devops'],project='Build a task API with login, object-level permissions, transactions and deployment.'),
 dict(title='Full-Stack Developer',level='Connect both halves',description='Take a product from a form in the browser through an API to a database and a reliable release.',courses=['html','css','javascript','git','react','node','databases','security','projects','devops'],project='Build a client portal or commerce application with tests and a documented failure strategy.'),
 dict(title='App Developer',level='Pick one mobile path',description='Learn shared programming concepts, then specialise in Flutter, Kotlin, React Native or Swift.',courses=['mobile-flutter','mobile-kotlin','mobile-react-native','mobile-swift','networks','security'],project='Build an offline-capable task app with navigation, local storage and a release checklist.'),
 dict(title='Desktop App Developer',level='Pick a desktop toolkit',description='Create useful Windows, macOS or Linux applications with native file and window workflows.',courses=['desktop-electron','desktop-python','desktop-dotnet','git','security'],project='Build a local notes application with import/export, a database and an installer.'),
 dict(title='Python Developer',level='Language to applied work',description='Use Python for automation, APIs, data processing and measured AI features.',courses=['python','dsa','data-science','python-backend','ai-foundations','rag','agents'],project='Build a tested report pipeline that validates data, measures model quality and works through provider failures.'),
 dict(title='Placement & CS Foundations',level='Study alongside projects',description='Practise DSA, SQL, operating systems, networks and concise interview explanations.',courses=['dsa','databases','os','networks','placement'],project='Follow a topic sheet, complete judged drills and explain one project trade-off every day.'),
]

def build(partial=False):
    for module in MODULES:
        path=ROOT/'scripts/curriculum'/f'{module}.py'
        if path.exists():importlib.import_module('curriculum.'+module).build()
        elif not partial:raise ValueError('Missing curriculum module: '+module)
    lessons=[l for c in COURSES for l in c['lessons']]
    assert lessons and len({l['id'] for l in lessons})==len(lessons),'Duplicate lesson IDs'
    assert len({c['id'] for c in COURSES})==len(COURSES),'Duplicate course IDs'
    for l in lessons:
        assert len(l['body'].split())>=100,(l['id'],'lesson needs a real explanation')
        assert len(l['interviews'])>=2 and all(len(i['a'])>=80 for i in l['interviews']),(l['id'],'interview answers need reasoning')
        q=l['quiz'];assert len(set(q['options']))==4 and 0<=q['answer']<4 and len(q['explanation'])>=35,l['id']
        assert len(l['exercise'])>=40,l['id']
    mapped={}
    for l in lessons:
        for number in l['skills']:
            assert number not in mapped,('Skill mapped twice',number)
            mapped[number]=l['id']
    syllabus=json.loads((ROOT/'data/study-syllabus.json').read_text(encoding='utf-8'))
    if not partial:assert set(mapped)==set(range(1,277)),('Unmapped PDF skills',sorted(set(range(1,277))-set(mapped)))
    skills=[{**row,'lesson':mapped[row['number']]} for row in syllabus['skills'] if row['number'] in mapped]
    course_ids={c['id'] for c in COURSES}
    paths=[{**p,'courses':[id for id in p['courses'] if id in course_ids]} for p in PATHS]
    data=dict(checked='17-18 October 2026',edition='development' if partial else '3.0',courses=COURSES,paths=paths,skills=skills,stages=syllabus['stages'],sources=syllabus['sources'])
    (ROOT/'assets/study-data.js').write_text('window.CODELAB_STUDY='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    print(f'Built {len(COURSES)} courses, {len(lessons)} original lessons, {sum(len(l["interviews"]) for l in lessons)} interview answers; {len(skills)}/276 PDF skill mappings.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--partial',action='store_true',help='Development preview only: allow missing course modules/skill mappings.')
    build(parser.parse_args().partial)
