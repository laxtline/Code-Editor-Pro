import contextlib
import io
import json
import sys

tasks=json.load(sys.stdin)
original_stdin=sys.stdin
count=0
for q in tasks:
    for case in q['testCases']:
        output=io.StringIO()
        try:
            sys.stdin=io.StringIO(case['input']+'\n')
            with contextlib.redirect_stdout(output):
                exec(compile(q['referenceCode']['python'],q['title'],'exec'),{})
        finally:
            sys.stdin=original_stdin
        actual=json.loads(output.getvalue())
        assert actual == json.loads(case['expectedOutput']), (q['title'],case,actual)
        count+=1
print('All Python reference cases passed:',count)
