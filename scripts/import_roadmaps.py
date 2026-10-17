"""Read the three supplied PDF roadmaps into app data. Requires pypdf only for this import."""
import argparse
import json
from pathlib import Path
import re
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SPECS=[('service','DSA_Study_Steps','Service-company foundations',140),
       ('finance','Product_Finance_DSA_Steps','Product & finance technology',200),
       ('tech','Top_Tech_Python_DSA_Steps','Top technology companies',240)]

def build(pdf_root):
    tracks=[]
    for key,name,label,target in SPECS:
        reader=PdfReader(pdf_root/(name+'.pdf'))
        text='\n'.join(page.extract_text() or '' for page in reader.pages)
        pattern=r'STEP (\d+)\s*\n(.+?)\n\s*(\d+) QUESTIONS\s*\n(.*?)\n# COMPANY FOCUS:\s*\n([^\n]+)'
        steps=[]
        for match in re.finditer(pattern,text,re.S):
            n=int(match[1]);first,last=(3,7) if key=='service' else (4,8)
            stage=1 if n<=first else 2 if n<=last else 3
            steps.append(dict(number=n,title=match[2].strip(),target=int(match[3]),
                topics=re.sub(r'\s+',' ',match[4]).strip(),companies=[s.strip() for s in match[5].split('|')],stage=stage))
        if len(steps)!=(10 if key=='service' else 12) or sum(s['target'] for s in steps)!=target:
            raise ValueError(f'{name}: extracted steps/targets do not match the supplied roadmap; inspect the PDF before replacing data.')
        tracks.append(dict(id=key,label=label,source=name+'.pdf',target=target,steps=steps))
    (ROOT/'data/roadmaps.json').write_text(json.dumps(tracks,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Imported 34 steps. Source PDFs were not modified.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf-root',type=Path,default=Path.home()/'Desktop')
    build(parser.parse_args().pdf_root)
