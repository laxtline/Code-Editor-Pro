"""Read the user-supplied documents; store only technical syllabus metadata, never edit originals."""
import argparse
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--folder',default=r'd:\SURYA\Coding');args=parser.parse_args()
    source=Path(args.folder)/'AI_Full_Stack_Engineer_Path.pdf';reader=PdfReader(source)
    rows=[];stages=[];stage=0
    for page_no,page in enumerate(reader.pages,1):
        lines=(page.extract_text() or '').splitlines()
        for i,line in enumerate(lines):
            if line.startswith('STAGE ') and ' OF 11' in line:
                stage=int(line.split()[1]);stages.append(dict(id=stage,title=f'{stage:02} - '+lines[i+1]))
            if line.strip()==chr(0x2610):
                parts=[]
                for part in lines[i+1:]:
                    if part.strip() in ['HAVE','CORE','DEPTH']:break
                    parts.append(part)
                rows.append(dict(number=len(rows)+1,stage=stage,page=page_no,text=' '.join(parts)))
    assert len(rows)==276 and len(stages)==11,(len(rows),len(stages))
    sources=[]
    for name in ['AI_Full_Stack_Engineer_Path.pdf','Tech_Stack_ClientHub_and_Ramachandra_Traders.docx']:
        p=Path(args.folder)/name;sources.append(dict(name=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    data=dict(stages=stages,skills=rows,sources=sources)
    (ROOT/'data/study-syllabus.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Imported 276 technical skill rows across 11 stages; original documents unchanged.')
if __name__=='__main__':main()
