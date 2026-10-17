"""Original CodeLab teaching notes. Source links verify concepts, not copied text."""
COURSES=[]
SOURCES={
 'w3html':('W3Schools HTML topic reference','https://www.w3schools.com/html/'),
 'w3css':('W3Schools CSS topic reference','https://www.w3schools.com/css/'),
 'jsinfo':('JavaScript.info tutorial','https://javascript.info/'),
 'odin':('The Odin Project learning paths','https://www.theodinproject.com/paths'),
 'freecodecamp':('freeCodeCamp curriculum','https://www.freecodecamp.org/learn/'),
 'python':('Python tutorial','https://docs.python.org/3/tutorial/'),
 'mdn':('MDN web development','https://developer.mozilla.org/en-US/docs/Learn_web_development'),
 'react':('React Learn','https://react.dev/learn'),
 'next':('Next.js App Router','https://nextjs.org/docs/app/getting-started'),
 'node':('Node.js Learn','https://nodejs.org/en/learn/getting-started/introduction-to-nodejs'),
 'express':('Express routing','https://expressjs.com/en/guide/routing/'),
 'fastapi':('FastAPI tutorial','https://fastapi.tiangolo.com/tutorial/'),
 'postgres':('PostgreSQL documentation','https://www.postgresql.org/docs/current/'),
 'os':('Operating Systems Three Easy Pieces','https://pages.cs.wisc.edu/~remzi/OSTEP/'),
 'network':('MDN HTTP guides','https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides'),
 'git':('Pro Git book','https://git-scm.com/book/en/v2'),
 'docker':('Docker Get started','https://docs.docker.com/get-started/'),
 'owasp':('OWASP Cheat Sheet Series','https://cheatsheetseries.owasp.org/'),
 'claude':('Claude API and prompt design','https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview'),
 'sklearn':('scikit-learn user guide','https://scikit-learn.org/stable/user_guide.html'),
 'flutter':('Learn Flutter','https://docs.flutter.dev/learn'),
 'android':('Android Basics with Compose','https://developer.android.com/courses/android-basics-compose/course'),
 'rn':('React Native introduction','https://reactnative.dev/docs/getting-started'),
 'swift':('Swift language guide','https://docs.swift.org/swift-book/documentation/the-swift-programming-language/'),
 'electron':('Electron tutorial','https://www.electronjs.org/docs/latest/tutorial/tutorial-prerequisites'),
 'dotnet':('Microsoft Learn C#','https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/'),
 'java':('Dev.java learning guides','https://dev.java/learn/'),
 'c':('GNU C introduction and reference','https://www.gnu.org/software/c-intro-and-ref/manual/'),
 'cpp':('Standard C++ learning resources','https://isocpp.org/get-started'),
 'dsa':('MIT introduction to algorithms','https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-notes/'),
 'numpy':('NumPy fundamentals','https://numpy.org/doc/stable/user/basics.html'),
 'pandas':('Pandas getting started','https://pandas.pydata.org/docs/getting_started/index.html'),
 'typescript':('TypeScript handbook','https://www.typescriptlang.org/docs/handbook/intro.html'),
 'mongo':('MongoDB data modelling','https://www.mongodb.com/docs/manual/data-modeling/'),
 'rag':('pgvector project documentation','https://github.com/pgvector/pgvector'),
 'mcp':('Model Context Protocol introduction','https://modelcontextprotocol.io/docs/getting-started/intro'),
 'payment':('Razorpay webhook validation','https://razorpay.com/docs/webhooks/validate-test/'),
}

def course(id,title,group,summary,duration,project,sources,prerequisites=''):
    result=dict(id=id,title=title,group=group,summary=summary,duration=duration,project=project,
                sources=[dict(title=SOURCES[s][0],url=SOURCES[s][1]) for s in sources],prerequisites=prerequisites,lessons=[])
    COURSES.append(result)
    return result

def lesson(c,id,title,body,exercise,interviews,quiz,example=None,skills=(),minutes=15):
    question,options,answer,explanation=quiz
    item=dict(id=id,title=title,body=body.strip(),exercise=exercise.strip(),interviews=[dict(q=q,a=a) for q,a in interviews],
              quiz=dict(question=question,options=options,answer=answer,explanation=explanation),skills=list(skills),minutes=minutes)
    if example:item['example']=dict(lang=example[0],code=example[1].strip(),expected=example[2],stdin=example[3] if len(example)>3 else '')
    c['lessons'].append(item)
    return item
