"""Reviewed explanations and explicit corrections for the frozen original MCQ bank.

No answer is accepted merely because it was the old answer key. Numeric families
are recalculated; remaining entries have an explicit reviewed answer below.
"""
from copy import deepcopy
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]

# ordinal: (topic, correct answer, worked explanation). These refer to the frozen snapshot.
REVIEW={
19:('trains','36 km/h','The train travels its own 100 m length in 10 s: 100/10=10 m/s. Multiply by 18/5 to obtain 36 km/h.'),
20:('speed','60 km/h','Average speed=distance/time=180/3=60 km/h.'),
21:('speed','4 hours','Time=distance/speed=20/5=4 hours.'),
22:('speed','2 hours','Opposite-direction separation increases at 40+60=100 km/h. Time=200/100=2 hours.'),
23:('boats','12 km/h','The stated downstream distance and time directly give downstream speed=24/2=12 km/h. No stream correction is needed.'),
24:('speed','15 km/h','Speed=90 km/6 h=15 km/h.'),
25:('trains','20 m/s','To clear the platform the train travels 150+350=500 m. Speed=500/25=20 m/s.'),
26:('speed','5 km','50 minutes=50/60 hour. Distance=6×50/60=5 km.'),
27:('speed','75 km/h','The fixed distance is 60×5=300 km. To cover it in 4 h requires 300/4=75 km/h.'),
28:('speed','10 m/s','Convert km/h to m/s by multiplying by 5/18: 36×5/18=10 m/s.'),
29:('work','6 days','Combined daily rate=1/10+1/15=1/6 job. The reciprocal is 6 days.'),
30:('work','9 days','The job requires 6×12=72 person-days at equal productivity. Eight workers need 72/8=9 days.'),
31:('work','3/4','In 5 days A completes 5/20=1/4 of the job; the remaining fraction is 1−1/4=3/4.'),
32:('work','16','Total work=12×8=96 worker-days. Finishing in 6 days needs 96/6=16 workers.'),
33:('work','15 days','B’s daily rate=1/6−1/10=1/15 job. Thus B alone takes 15 days.'),
34:('work','3 days','Five men finish 1/12 job per day, so ten men finish 1/6. Similarly sixteen women finish 1/6. Combined rate=1/3 job/day, giving 3 days.'),
35:('pipes','15 hours','Net filling rate=1/6−1/10=1/15 tank per hour, so an initially empty tank fills in 15 hours.'),
36:('work','6 days','Y completes 10/15=2/3 of the job, leaving 1/3. X requires 18×1/3=6 days for that remainder.'),
37:('profit','20%','Profit=600−500=100. Profit percentage uses cost as the base: 100/500×100=20%.'),
38:('profit','₹360','At a 10% loss the selling price is 90% of cost: 400×0.9=360 rupees.'),
39:('profit','₹600','A 20% profit means SP=1.2×CP. Therefore CP=720/1.2=600 rupees.'),
40:('profit','20%','Set cost to 100. Marked price=150; after a 20% discount, selling price=150×0.8=120. Profit is 20% of cost.'),
41:('profit','₹340','The selling-price increase spans a 15% loss to a 10% profit, or 25% of cost. Thus 0.25×CP=85 and CP=340.'),
42:('profit','No profit no loss','The items have equal costs. Selling prices are 400×1.1=440 and 400×0.9=360. Total selling price 800 equals total cost 800.'),
43:('profit','20%','Let unit cost be c and unit selling price s. 12c=10s, so s=1.2c: profit is 20% of cost.'),
44:('ratio','₹420','Total ratio units=5+7=12. B receives 7/12 of 720=420 rupees.'),
45:('ratio','48','The sum of ratio units is 7. One unit is 84/7=12; the larger number is 4×12=48.'),
46:('ratio','8:12:15','Make b equal in both ratios: a:b=8:12 and b:c=12:15. Thus a:b:c=8:12:15.'),
47:('average','23.89','Original sum=10×25=250. Removing 35 leaves sum 215 and count 9. Average=215/9=23.888…, which rounds to 23.89.'),
48:('average','12.9','The 30 students total 30×12=360 years. Including the 40-year-old teacher gives 400/31=12.903… years, or 12.9 to one decimal place.'),
49:('average','10.5','For natural numbers 1 through 20, pair the first and last. Their mean is (1+20)/2=10.5.'),
50:('average','₹2750','Both groups contain six months. The monthly mean for the full year is (6×2500+6×3000)/12=2750 rupees.'),
52:('hcf-lcm','48','8=2³, 12=2²×3 and 16=2⁴. The LCM uses the largest prime powers: 2⁴×3=48.'),
53:('progression','120','The sum 1+…+15 is 15×16/2=120.'),
54:('algebra','2 and 3','Factor x²−5x+6 as (x−2)(x−3). Setting either factor to zero gives x=2 or x=3.'),
55:('simplification','24','Evaluate multiplication/division left to right: 6×4÷2=12. Then 15+12−3=24.'),
56:('indices','42','42²=(40+2)²=1600+160+4=1764. The principal square root is 42.'),
57:('algebra','32','Let the numbers be x,x+2,x+4. Their sum 3x+6=90 gives x=28. The largest is 32.'),
58:('indices','48','2⁵=32 and 3²=9. Their product is 288; 288/6=48.'),
59:('algebra','5','Subtract 7 from both sides: 3x=15. Dividing by 3 gives x=5.'),
60:('number-system','53','48,50 and52 are even; 49=7² and51=3×17. The next integer 53 has no divisor 2,3,5 or7, so it is prime.'),
61:('probability','1/3','Total balls=3+4+5=12, with 4 green outcomes. Probability=4/12=1/3.'),
62:('permutation','120','There are 5 choices for the first seat, then 4,3,2,1: 5!=120 arrangements.'),
63:('permutation','24','Order matters and letters cannot repeat: 4P3=4×3×2=24 strings.'),
64:('probability','3/4','For a fair coin the equally likely sequences are HH,HT,TH,TT. Three contain at least one head, giving 3/4.'),
65:('probability','1/13','A standard deck has four kings among 52 cards. Probability=4/52=1/13.'),
66:('permutation','12','BOOK has 4 letters with O repeated twice. Distinct arrangements=4!/2!=12.'),
67:('series','96','The intended rule doubles each term: 3,6,12,24,48,96.'),
68:('series','95','Each term is twice the previous term plus one: 47×2+1=95.'),
69:('series','216','These are consecutive cubes 2³,3³,4³,5³. The next is 6³=216.'),
70:('series','MN','The first letters advance A,D,G,J,M by three alphabet positions; each group has two consecutive letters.'),
71:('coding','XPSE','The stated encoding shifts every letter forward by one: W→X,O→P,R→S,D→E.'),
72:('relations','Mother','The speaker is the only daughter of her own mother. Therefore “his mother” is the speaker herself, making her the man’s mother.'),
73:('direction','South-East','Both mappings rotate direction labels 135° anticlockwise. Applying the same rotation to West yields South-East.'),
74:('analogy','Speed','Square, circle, triangle and pentagon are geometric shapes; speed is a rate rather than a shape.'),
75:('analogy','Snake','The dog, cat, lion and tiger are mammals. The snake is a reptile, making it the odd one under that classification.'),
76:('syllogism','Cannot be determined','The rich educated people need not include any doctor. The premises permit doctors to be rich or not rich, so the conclusion is not forced.'),
77:('inequality','D','The statements give D>C>A>B, so D is tallest.'),
78:('ranking','19','After swapping, A occupies B’s original position, which is 11th from the left and 9th from the right. Total=11+9−1=19.'),
79:('calendar','Thursday','The 25th is 24 days after the 1st. Since 24 mod 7=3, move three days from Monday to Thursday.'),
80:('series','37','Terms follow n²+1 for n=1,2,3,4,5. Next is 6²+1=37; equivalently the gaps are 3,5,7,9,11.'),
81:('analogy','School','The relationship is profession to usual workplace: a doctor works in a hospital, a teacher in a school.'),
82:('analogy','Cut','The relationship is instrument to action: a pen is used to write and a knife to cut.'),
83:('simplification','19.25','Replace the operator symbols first: 10×2−3÷4. Under standard precedence this is 20−0.75=19.25.'),
84:('series','R','The letters move two positions backwards: Z,X,V,T,R.'),
85:('coding','MJPOT','Shift each letter forward one: L→M,I→J,O→P,N→O,S→T.'),
86:('seating','Cannot be determined','The constraints imply R<P<Q<S, but T is unrestricted. R,P,Q,S,T places Q in the middle; T,R,P,Q,S places P there. A unique middle person cannot be inferred.'),
87:('syllogism','Cats','Subset inclusion is transitive: Lions⊆Tigers and Tigers⊆Cats imply Lions⊆Cats.'),
88:('clock','7.5°','At 3:15 the minute hand is at 90°. The hour hand has moved to 90+15×0.5=97.5°. The difference is 7.5°.'),
89:('analogy','(6,35)','The second value should be the square of the first. 6²=36, not35; the other three pairs fit.'),
90:('calendar','53','366=52×7+2. Starting on Sunday, the extra days are Sunday and Monday, so Sunday occurs 53 times.'),
91:('series','Heptagon','The polygon side counts increase 3,4,5,6. Seven sides give a heptagon.'),
92:('seating','Cannot be determined','Even with everyone facing the centre and B immediately right of A, the seat immediately left of D is not fixed by these constraints. Unspecified people can occupy it.'),
93:('relations','Father','Q and R share the same parents. Since P is Q’s father, P is also R’s father.'),
94:('cubes','Back to original position','Four successive quarter-turns make 4×90°=360°, restoring the original orientation.'),
95:('series','18','Reading row by row gives consecutive even integers 2,4,6,…,16,18.'),
96:('relations','Uncle','A and C are distinct full siblings. C is D’s father and A is male, so A is D’s paternal uncle.'),
97:('coding','UBCMF','Shift each capital one place forward: T→U,A→B,B→C,L→M,E→F.'),
98:('coding','3-1-20','Under A=1,…,Z=26, C=3,A=1,T=20; preserve the letter order.'),
99:('coding','6715','Use the explicitly supplied letter mapping S=6,O=7,A=1,P=5. Concatenating in SOAP order gives6715.'),
100:('relations','Sister','The paternal grandfather’s only son is Rohan’s father. His daughter, distinct from Rohan, is Rohan’s sister.'),
101:('relations','Grandfather','C and D are parents of B and A’s father. Thus D is the father of A’s father, or A’s paternal grandfather.'),
112:('spelling','Necessary','Necessary has one c and two s letters. The other options alter that standard spelling.'),
113:('prepositions','since','Since introduces a starting point such as2015; for introduces a duration.'),
114:('prepositions','to','The conventional adjective–preposition combination is allergic to something.'),
115:('prepositions','to','The expression is look forward to. Here to is a preposition followed by the gerund hearing.'),
116:('prepositions','on','Congratulate someone on an achievement is the standard construction.'),
117:('agreement',"She doesn't like coffee.",'A third-person singular subject uses does not, followed by the base verb like, not likes.'),
118:('voice','A letter is written by her.','The active simple present writes becomes passive is written; the object a letter becomes the subject.'),
119:('word-classes','Adverb','Quickly modifies the action runs, explaining how the action happens, so it functions as an adverb.'),
120:('word-classes','Bibliophile','A bibliophile is a lover of books; a bibliographer compiles or studies bibliographies.'),
121:('word-classes','Democracy','Democracy denotes government by the people, directly or through representatives.'),
122:('word-classes','Incomprehensible','Incomprehensible means impossible to understand. Illegible concerns reading handwriting, inaudible hearing, and indelible removal.'),
123:('idioms','Reveal a secret','Spill the beans means disclose information that was supposed to remain secret.'),
124:('idioms','Very rarely','Once in a blue moon describes something happening very infrequently.'),
125:('idioms','Something easy','A piece of cake describes a task as easy, regardless of the task’s size.'),
126:('idioms','Avoid the main topic','Beat around the bush means speak indirectly rather than address the central issue.'),
127:('word-classes','Phenomena','The conventional plural of the Greek-derived singular phenomenon is phenomena.'),
128:('word-classes','Analyses','Analysis forms the plural analyses. Analyzes is a verb form, not the noun plural.'),
129:('agreement','have should be has','Each is the singular grammatical head, so have changes to has. Singular their can refer to each person and need not be replaced.'),
130:('agreement','student should be students','One of selects a member of a plural group: one of the best students. The main subject he correctly takes is.'),
136:('agreement','is','The revised stem treats the committee as one unit, so singular is is appropriate. Notional plural agreement can occur in other contexts, especially British English.'),
137:('tense','when','The paired construction is hardly…when. No sooner…than is a different construction.'),
138:('reading','Reduced atmospheric pressure','The passage explicitly attributes the lower boiling temperature to lower atmospheric pressure; the other causes are not stated.'),
139:('reading','No direct emissions','The passage names absence of direct emissions. It makes no guarantee about cost, reliability or installation speed.'),
140:('reading','Mechanization','The passage states that mechanization transformed manufacturing. None of the alternative mechanisms is identified.'),
141:('complexity','Queue','A queue removes the oldest enqueued item first: first in, first out.'),
142:('complexity','Stack','A stack pops the most recently pushed item first: last in, first out.'),
143:('complexity','O(log n)','Binary search halves a sorted search interval at each step, requiring logarithmically many comparisons in the worst case.'),
144:('complexity','O(n²)','Worst-case bubble sort makes a quadratic number of comparisons/swaps across its passes.'),
145:('web-foundations','PUT','PUT requests create or replace the target resource’s state using the enclosed representation. The revised question distinguishes this from a partial update.'),
146:('web-foundations','404','HTTP404 is Not Found. 200 is OK,301 is a permanent redirect and500 is a server error.'),
147:('database','TRUNCATE','TRUNCATE TABLE performs table truncation while retaining the table definition. DELETE can also remove all rows, which is why the original broader wording was ambiguous.'),
148:('web-foundations','Cascading Style Sheets','CSS expands to Cascading Style Sheets, the language used to specify presentation of web documents.'),
149:('web-foundations','80','The default TCP port for an http URL without an explicit port is80; HTTPS conventionally uses443.'),
150:('database','MySQL','MySQL is a relational database system. MongoDB, Redis and Cassandra are commonly classified as NoSQL systems.'),
151:('web-foundations','Representational State Transfer','REST expands to Representational State Transfer, an architectural style for distributed systems.'),
152:('complexity','Quick Sort / Merge Sort O(n log n)','For arbitrary input among these comparison sorts, merge sort and average-case quicksort are O(n log n); bubble, selection and insertion sorts have quadratic average behaviour. Quicksort’s worst case can be quadratic.'),
153:('web-foundations','git branch <name>','git branch <name> creates a branch reference without switching the current checkout. git switch -c is another creation-and-switch command, but is not an option here.'),
154:('web-foundations','CSS','CSS controls layout, typography and other presentation rules. HTML describes document structure; JSON and XML represent data/markup.'),
155:('database','Structured Query Language','SQL expands to Structured Query Language.'),
156:('python-state','int','Java int is a primitive type. String, arrays and ArrayList are reference types.'),
157:('database','Speed up data retrieval','An index stores an access structure that can avoid scanning every row for suitable queries. Maintaining indexes can add write and storage costs.'),
158:('python-state','const','const declares a block-scoped binding that cannot be reassigned. It does not make the contents of an object deeply immutable.'),
159:('web-foundations','Application Programming Interface','An API is an Application Programming Interface: an agreed way for software components to interact.'),
160:('web-foundations','Git','Git tracks versions of source content and branching history. Docker/Kubernetes manage containers; Jenkins automates workflows.'),
211:('series','24','The terms increase by4, so20+4=24.'),
212:('series','36','The terms are1²,2²,3²,4²,5². The next is6²=36.'),
213:('series','64','Each term doubles. The next is32×2=64.'),
214:('series','243','Multiply each term by3:81×3=243.'),
215:('series','160','Each term doubles, giving80×2=160.'),
216:('series','21','The gaps are2,3,4,5. The next gap is6, yielding15+6=21.'),
217:('series','50','The gaps3,5,7,9,11 increase by2. Next add13 to37, yielding50.'),
218:('series','42','These are consecutive positive multiples of7, so35+7=42.'),
219:('series','66','Subtract10,9,8, then7:73−7=66.'),
220:('series','22','The differences are1,2,3,4,5. Next add6 to16, producing22.'),
221:('series','81','Differences are5,10,15,20. The next difference is25, so56+25=81.'),
222:('series','80','The gaps10,15,20 rise by5. The next gap is25, giving55+25=80.'),
228:('python-output','512','Exponentiation associates right to left in Python: 2 ** (3 ** 2)=2 **9=512, not (2 **3) **2.'),
229:('python-state',"'number'",'NaN is a special numeric value in JavaScript, so typeof NaN returns the string number.'),
230:('python-state',"'11'",'With a string operand, JavaScript + performs string concatenation here: numeric1 becomes the string1, producing11.'),
231:('python-state',"'1,2,34,5,6'",'Each array converts to its comma-joined string:1,2,3 and4,5,6. Adding the strings concatenates them without an extra comma.'),
232:('python-output','3','The outer list has three elements:1,2,and the nested list[3,4]. len does not recursively count nested contents.'),
233:('python-output',"'55'",'Both operands are strings. Python + concatenates them, so the printed string is55 rather than numeric10.'),
234:('python-state','true','Loose equality converts the string0 to numeric0 in this comparison, so0 == "0" is true.'),
235:('python-state','false','Strict equality does not perform that conversion. A number and a string are different types, so the comparison is false.'),
236:('python-state','false','Java boolean instance fields receive the default value false. Local variables, by contrast, require definite assignment before use.'),
237:('complexity','O(1)','Under ordinary hashing assumptions, average/expected lookup is constant time. The statement is not a universal worst-case guarantee.'),
238:('database','HAVING','WHERE filters source rows before grouping; HAVING filters the resulting groups and can use aggregate expressions.'),
239:('python-state','int arr[10];','The C declaration uses the element type, identifier and bracketed array bound. This declares an array of ten ints.'),
240:('python-state','obj, the call’s receiver','For an ordinary unbound function called as obj.method(), this is the receiver obj. Detaching the function or using bind/call/apply can change the receiver.'),
241:('python-output','3','Python // performs floor division. For positive7/2=3.5 the floor is3.'),
242:('python-output','False','Numeric zero is false in Python truth-value testing, so bool(0) is False.'),
243:('database','FULL OUTER JOIN','A full outer join retains matched pairs plus unmatched rows from both sides, filling the missing side with NULL.'),
244:('database','find()','MongoDB collection.find() retrieves matching documents as a cursor. Other listed method names are not the standard query method.'),
245:('python-state',"'undefined'",'The typeof operator returns a string. Applied to undefined, it produces the string undefined, shown with quotes in the option.'),
246:('python-state','final','A Java class declared final cannot be subclassed. final on a method or variable has different related restrictions.'),
247:('complexity','Efficient sorting algorithms like Merge/Quick Sort','Merge sort takes O(n log n) comparisons and quicksort has that average order. Quicksort’s worst case can still be O(n²).'),
248:('direction','3 km','The5 km north and5 km south movements cancel. The two right turns leave a3 km east displacement, so the distance is3 km.'),
249:('direction','10 m East','North and south cancel; the remaining displacement is10 m to the east.'),
250:('calendar','Saturday','17 days is two complete weeks plus3 days. Wednesday+3 days=Saturday.'),
251:('analogy','200','121=11²,144=12²,169=13² and225=15². 200 is not an integer square.'),
252:('syllogism',"Valid based on the statements given, though factually penguins can't fly",'The conclusion follows from the supplied universal premise and membership statement. Logical validity concerns this implication; the real-world universal premise is false.'),
253:('seating','D, A, B, C, E','The constraints form D>A>B>C, with E below all others. Thus the order is D,A,B,C,E.'),
254:('relations','Son','The revised question states full siblings. Brother identifies X as male; since Y is Z’s child and shares both parents with X, X is Z’s son.'),
255:('clock','150°','The stated movement is30° each hour. In5 hours the hour hand travels5×30=150°.'),
256:('ranking','24','Total students=rank from top+rank from bottom−1=7+18−1=24.'),
257:('series','25','Each pair maps x to x². Therefore5 maps to25.'),
262:('word-classes','Ornithology','Ornithology is the study of birds. Entomology concerns insects, botany plants, and zoology animals more broadly.'),
263:('word-classes','Illegible','Illegible describes writing that cannot be read; incomprehensible describes meaning that cannot be understood.'),
264:('idioms','Work late into the night','Burn the midnight oil means study or work late into the night.'),
265:('idioms','Say exactly the right thing','Hit the nail on the head means identify or express the point exactly.'),
266:('prepositions','to','The standard expression is married to a person, not married with that person.'),
267:('prepositions','for','Apologise/apologize for introduces the action or fault for which someone is sorry.'),
268:('spelling','Occurrence','Occurrence has double c and double r. The alternative spellings omit or alter these letters.'),
269:('voice','This house was built in 1990.','Simple past built becomes the passive was built; the date remains a past-time marker.'),
270:('ages','12 years','Let the son’s age be x, so the father’s is3x. After12 years,3x+12=2(x+12), giving x=12.'),
271:('ages','20 years','The two conditions give A−5=3(B−5), hence A=3B−10, and A+10=2(B+10), hence A=2B+10. Equating gives B=20.'),
272:('boats','12.5 km/h','Downstream speed=30/2=15 and upstream speed=30/3=10 km/h. Still-water speed=(15+10)/2=12.5 km/h.'),
273:('mixture','15 litres','Initially milk=5x, water=x. Then5x/(x+6)=5/3, so3x=x+6 and x=3. Milk=5×3=15 litres.'),
274:('database','A non-null column that uniquely identifies each row','For the revised single-column case, a primary key enforces both uniqueness and non-nullability. A primary key may instead contain multiple columns.'),
275:('database','Organizing data to reduce redundancy','Normalization decomposes relations according to dependencies to reduce redundancy and update anomalies while preserving useful relationships.'),
276:('database','2NF','Second normal form requires1NF and removes partial dependency of non-prime attributes on a proper subset of a candidate key.'),
277:('database','A column or column set referencing a candidate key in a referenced table','A foreign key establishes a referential constraint. The referenced key need not be the primary key, and a table may reference itself.'),
278:('database','INSERT','INSERT adds new rows. UPDATE changes existing rows and CREATE defines an object.'),
279:('database','ORDER BY','ORDER BY requests a particular ordering. GROUP BY forms groups and does not by itself guarantee result order.'),
280:('database','Atomicity, Consistency, Isolation, Durability','These are the transaction properties: all-or-nothing atomicity, preserved constraints/consistency, concurrent-execution isolation and committed-data durability.'),
281:('database','INNER JOIN','An inner join retains only combinations satisfying the join condition; unmatched rows are excluded.'),
282:('database','To group rows sharing a common value for aggregation','GROUP BY partitions rows by grouping expressions, allowing aggregate calculations for each group.'),
283:('database','Document','A MongoDB document is analogous to a relational row, although it can have a richer nested structure.'),
284:('database','Collection','A collection groups MongoDB documents, playing a role analogous to a relational table.'),
285:('database','insertOne()','insertOne explicitly names the operation for one document. Older generic insert methods could also insert one, so the revised stem asks for the explicit single-document method.'),
286:('database','BSON (Binary JSON)','MongoDB stores documents as BSON, a binary representation with additional data types beyond plain JSON.'),
287:('database','DISTINCT','SELECT DISTINCT eliminates duplicate projected rows in the result set; it does not delete source-table rows.'),
288:('database','A cycle of transactions waiting on one another’s held resources','A deadlock is a circular wait involving two or more transactions/resources. The original two-transaction example was narrower than the full concept.'),
289:('database','DROP TABLE','DROP TABLE removes the table object, subject to permissions and dependencies. DELETE and TRUNCATE primarily remove rows.'),
290:('database','DELETE can use WHERE; TRUNCATE removes all rows without WHERE; logging and rollback details depend on the database','DELETE can selectively remove rows. TRUNCATE has no row predicate. It is incorrect to claim universally that TRUNCATE is unlogged or cannot roll back; PostgreSQL documents transactional rollback support.'),
291:('database','COUNT()','COUNT(*) counts rows. COUNT(expression) counts non-NULL values of that expression, so these forms can differ.'),
292:('database','Speeding up data retrieval operations','Suitable indexes provide faster access paths for predicates/orderings. Their benefit depends on query and data distribution; writes and storage may cost more.'),
293:('database','$gt','MongoDB $gt selects values greater than the supplied comparison value. $gte includes equality.'),
294:('para-order','1-3-4-5-2 (The sun rises every morning)','Place subject the sun first(1,3), then verb rises(4), followed by the time expression every morning(5,2).'),
295:('tense','went','The added marker yesterday establishes a finished past event, requiring the simple past went. Without a time context, goes could also be grammatical.'),
296:('parallelism','Although it was raining, we went out.','An introductory although-clause is followed by a comma before the independent clause. A semicolon does not join a subordinate clause to its main clause this way.'),
297:('agreement','is','The grammatical head is the singular number in the number of students; it takes is. A number of students would normally take a plural verb.'),
298:('agreement','were','Under the conventional proximity rule for neither…nor, the verb agrees with the nearer plural subject employees, giving were in this past-time context.'),
303:('word-classes','Aviary','An aviary houses birds. An apiary houses bees and an aquarium aquatic organisms; sanctuary is a broader term.'),
304:('calendar','Monday','If the day before yesterday was Friday, yesterday was Saturday and today is Sunday. Tomorrow is Monday.'),
305:('ages','10 years','Let B=x and A=2x. Five years ago2x−5=3(x−5), giving2x−5=3x−15 and x=10.'),
306:('analogy','Sun','Mercury,Venus,Earth andMars are planets; the Sun is a star.'),
307:('analogy','Music','The revised stem asks for the general created medium: an author creates a book and a composer creates music. A song is one example, so it is removed as an overlapping alternative.'),
308:('syllogism','Parallelograms','By transitivity of the stated class inclusions, square⊆rectangle⊆parallelogram. The conclusion follows without introducing other shape definitions.')}

VOCAB={
'ELOQUENT':('Articulate','speaking or writing fluently and expressively'),
'ARDUOUS':('Difficult','requiring considerable effort'),
'TENACIOUS':('Persistent','holding firmly to a purpose'),
'AUSTERE':('Strict','severe or plain; strict is the closest option in this context'),
'CANDOR':('Honesty','frankness and openness'),
'GENEROUS':('Stingy','willing to give, whose opposite here is stingy'),
'OPTIMISTIC':('Pessimistic','hopeful about outcomes, opposed to pessimistic'),
'ANCIENT':('Modern','belonging to the distant past, opposed to modern'),
'VERBOSE':('Concise','using more words than needed, opposed to concise'),
'HUMBLE':('Arrogant','modest rather than self-important or arrogant'),
'BENEVOLENT':('Kind','well-meaning and kindly'),
'METICULOUS':('Careful','showing great attention to detail'),
'GREGARIOUS':('Sociable','enjoying the company of others'),
'TRANSPARENT':('Opaque','allowing light through, opposed in the material sense to opaque'),
'DILIGENT':('Lazy','showing careful effort, opposed here to lazy'),
'FRUGAL':('Extravagant','economical with resources, opposed to extravagant'),
'COHERENT':('Confusing','logically connected and clear, opposed here to confusing'),
'PRUDENT':('Wise','showing careful practical judgement'),
'ZEALOUS':('Enthusiastic','showing strong enthusiasm'),
'UBIQUITOUS':('Omnipresent','present or found everywhere'),
'PRAGMATIC':('Practical','concerned with workable practical results'),
'MUNDANE':('Extraordinary','ordinary or commonplace, opposed to extraordinary'),
'CONCISE':('Verbose','briefly expressed without unnecessary words, opposed to verbose')}

PATCHES={
34:dict(options=['3 days','5 days','4 days','8 days']),
47:dict(q='The average of 10 numbers is 25. If the number 35 is removed, find the new average rounded to two decimal places.',options=['23.89','24','22.5','23']),
48:dict(q='The average age of 30 students is 12 years. Including a 40-year-old teacher, find the new average rounded to one decimal place.'),
64:dict(q='A fair coin is tossed independently twice. What is the probability of getting at least one head?'),
83:dict(q="If '+' means '×', '×' means '−', '−' means '÷' and '÷' means '+', evaluate 10 + 2 × 3 − 4 after replacing the operators, using standard arithmetic precedence.",options=['19.25','18','16','22']),
86:dict(options=['Q','R','S','Cannot be determined']),
92:dict(q='Six people A,B,C,D,E,F sit around a circular table facing the centre. A is opposite D and B is immediately right of A. Who is immediately left of D?'),
93:dict(q='P is Q’s father. Q and R are full siblings sharing both parents. How is P related to R?'),
96:dict(q='A is B’s son. A and C are distinct full siblings, and C is D’s father. How is A related to D?'),
99:dict(q='A letter code explicitly maps G→5, S→6, O→7, A→1 and P→5. Concatenate the digit codes to encode SOAP.'),
100:dict(q='Pointing to a girl, Rohan says: “She is the daughter of my paternal grandfather’s only son.” Assuming the usual stated biological relationships, how is the girl related to Rohan?'),
101:dict(q='C and D are the mother and father of B and his brother. A is the child of B’s brother. How is D related to A?'),
134:dict(q="In the sense of a material transmitting light, choose the antonym of 'TRANSPARENT':"),
136:dict(q='Treating the committee as a single unit, fill the blank: The committee ___ yet to decide.'),
143:dict(q='What is the worst-case comparison count order of binary search on a sorted random-access array of n elements?'),
145:dict(q='Which listed HTTP method requests creation or complete replacement of a target resource’s state using the supplied representation?'),
147:dict(q='Which SQL keyword specifically performs table truncation while retaining the table definition?'),
152:dict(q='Among the listed comparison-sorting choices on arbitrary unsorted input, which has the best average time-complexity order?'),
158:dict(q='Which ES6 keyword declares a block-scoped binding that cannot be reassigned?'),
240:dict(q='When a regular unbound JavaScript method is called as obj.method() (without call, apply, bind or a proxy), what is this inside that invocation?',options=['obj, the call’s receiver','Always the global window','The parent function','Always undefined']),
254:dict(q='X is Y’s brother. X and Y are full siblings sharing both parents, and Y is Z’s daughter. How is X related to Z?',options=['Son','Father','Brother','Cannot be determined']),
274:dict(q='Which description correctly identifies a single-column primary key?',options=['A non-null column that uniquely identifies each row','A column that can have duplicates','A column used only for sorting','A backup field']),
277:dict(options=['A column or column set referencing a candidate key in a referenced table','An encryption key','An unrelated unique key','A backup key']),
285:dict(q='Which explicitly named modern MongoDB method inserts exactly one document?'),
288:dict(options=['A cycle of transactions waiting on one another’s held resources','A failed commit only','A database backup type','A corrupted index']),
290:dict(q='Which DELETE/TRUNCATE comparison avoids incorrect database-independent claims about logging and rollback?',options=['DELETE can use WHERE; TRUNCATE removes all rows without WHERE; logging and rollback details depend on the database','They are identical in every database','TRUNCATE can use WHERE but DELETE cannot','DELETE removes the table definition']),
294:dict(options=['1-3-4-5-2 (The sun rises every morning)','1-2-3-4-5','5-1-2-3-4','2-3-4-1-5']),
295:dict(q='Complete the past-time sentence: “Yesterday, despite the rain, the match ___ on schedule.”'),
298:dict(q='Complete the past-time sentence using the conventional proximity agreement rule: “Yesterday, neither the manager nor the employees ___ aware of the change.”'),
307:dict(q='Complete the creator-to-general-medium analogy: Author : Book :: Composer : ?',options=['Music','Orchestra','Instrument','Conductor']),
308:dict(q='Using only these premises — all squares are rectangles; all rectangles are parallelograms — all squares are definitely members of which stated class?',options=['Parallelograms','Circles','Triangles','None of the stated classes'])}

def number(value):
    f=Fraction(value)
    return str(f.numerator) if f.denominator==1 else str(float(f)).rstrip('0').rstrip('.')

def computed(q):
    text=q['q']
    if m:=re.fullmatch(r'What is (\d+)% of (\d+)\?',text):
        p,n=map(int,m.groups());answer=number(Fraction(p*n,100))
        return 'percent',answer,f'Use the whole quantity {n} as the base. {p}% of {n} = {p}×{n}/100 = {answer}.'
    if m:=re.search(r'simple interest on ₹(\d+) at (\d+)% per annum for (\d+) year',text):
        p,r,t=map(int,m.groups());answer=number(Fraction(p*r*t,100))
        return 'simple-interest',answer,f'Simple interest = PRT/100 = {p}×{r}×{t}/100 = {answer} rupees. The interest uses the original principal throughout.'
    if m:=re.fullmatch(r'Find the (HCF|LCM) of (\d+) and (\d+)\.',text):
        kind,a,b=m.groups();a,b=int(a),int(b);g=gcd(a,b);value=g if kind=='HCF' else lcm(a,b)
        return 'hcf-lcm',str(value),f'gcd({a},{b})={g}. '+(f'This is the greatest common factor: {value}.' if kind=='HCF' else f'LCM = {a}×{b}/{g}={value}.')
    if m:=re.fullmatch(r'A car travels (\d+) km at a speed of (\d+) km/h\. How long does it take\?',text):
        d,v=map(int,m.groups());answer=number(Fraction(d,v))
        return 'speed',answer+' hours',f'Time = distance/speed = {d}/{v} = {answer} hours. The kilometre units cancel.'
    if m:=re.fullmatch(r'A man buys an article for ₹(\d+) and sells it at a profit of (\d+)%\. Find the selling price\.',text):
        cost,p=map(int,m.groups());answer=number(Fraction(cost*(100+p),100))
        return 'profit',answer,f'Selling price = cost × (1+profit%/100) = {cost}×{100+p}/100={answer} rupees.'
    if text.startswith('Find the average of: '):
        a=list(map(int,text.split(': ',1)[1].split(', ')));answer=number(Fraction(sum(a),len(a)))
        return 'average',answer,f'Add the {len(a)} values to get {sum(a)}. Divide by their count: {sum(a)}/{len(a)}={answer}.'
    for word,(answer,meaning) in VOCAB.items():
        if f"'{word}'" in text:
            return 'vocabulary',answer,f'{word.title()} means {meaning}. The requested '+('opposite' if 'Antonym' in text else 'closest synonym')+f' among the options is {answer.lower()}.'
    return None

def review_bank(topics):
    raw=(ROOT/'data/legacy-bank.snapshot.json').read_bytes();bank=json.loads(raw)
    assert len(bank)==308
    meta={t['id']:t for t in topics};reviewed=[];changes=[]
    for i,original in enumerate(bank,1):
        check=computed(original) or REVIEW.get(i)
        if check is None:raise ValueError(f'Unreviewed classic question {i}: {original["q"]}')
        topic,answer,explanation=check
        if topic=='python-state':topic='programming-semantics'
        entry=deepcopy(original);entry.update(PATCHES.get(i,{}))
        if answer not in entry['options']:raise ValueError((i,answer,entry['options']))
        entry['answer']=entry['options'].index(answer)
        assert len(set(entry['options']))==4
        changed={k:dict(before=original[k],after=entry[k]) for k in ('q','options','answer') if original[k]!=entry[k]}
        if changed:changes.append(dict(ordinal=i,changes=changed,reason=explanation))
        entry.update(id=f'legacy-{i:03}',topic=topic,explanation=explanation,formula=meta[topic]['formula'],
            trick=meta[topic]['trick'],difficulty='Easy' if original['section']!='Logical' else 'Medium',
            origin='StudyLab classic bank · reviewed',sources=meta[topic]['sources'],legacyOriginal=original['q'],legacyOrdinal=i)
        reviewed.append(entry)
    report=dict(snapshotSha256=hashlib.sha256(raw).hexdigest(),reviewed=len(reviewed),changed=len(changes),changes=changes)
    (ROOT/'data/legacy-audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return reviewed,report

APT_REVIEW=[
('trains','8 s','54 km/h=15 m/s. To cross a pole the train travels its120 m length, requiring120/15=8 seconds.'),
('work','10','The fixed job requires5×18=90 worker-days. Nine equally productive workers need90/9=10 days.'),
('average','20','Five consecutive even numbers are symmetric around their middle number, which equals their average16. They are12,14,16,18,20.'),
('simple-interest','12.5%','Doubling requires interest equal to principal. P×r×8/100=P, so r=100/8=12.5% per year.'),
('percent','320','Let the number be x. Since0.25x=80, x=80/0.25=320.'),
('ratio','40','There are3+5=8 ratio units. Each unit is64/8=8; the larger part is5×8=40.'),
('profit','5%','Set cost to100. After40% markup, marked price=140. A25% discount gives140×0.75=105, a5% profit.'),
('hcf-lcm','60','Prime factorizations are12=2²×3,15=3×5 and20=2²×5. Their LCM is2²×3×5=60.'),
('speed','80 km/h','The distance remains240 km. Covering it in3 hours requires240/3=80 km/h.'),
('compound-interest','210','With annual compounding, amount=1000×1.1²=1210. Subtract principal1000 to obtain interest210.'),
('algebra','7','Square the given expression: (x+1/x)²=x²+2+1/x²=9. Subtract2 to obtain7.'),
('probability','2/5','A uniform draw has4 red outcomes among10 balls. Probability=4/10=2/5.'),
('series','42','Terms follow n(n+1):1×2,2×3,3×4,4×5,5×6; next6×7=42.'),
('coding','32','Using the explicitly stated sum-of-alphabet-positions rule, PIG=16+9+7=32.'),
('analogy','14','The other listed numbers are prime. Fourteen is composite because14=2×7.'),
('relations','Brother','A is male because he is B’s brother. With the revised explicit full-sibling assumption, A and C share parents, so A is C’s brother.'),
('coding','DW','The first letters advance A,B,C,D while the second letters retreat Z,Y,X,W.'),
('coding','GSJEBZ','The stated shift is +1 per letter: F→G,R→S,I→J,D→E,A→B,Y→Z.'),
('relations','His sister','The speaker is a man, so he is not his mother’s only daughter. That daughter is his sister.'),
('series','36','The series contains squares1²,2²,3²,4²,5², so the next is6²=36.'),
('series','112','Each term doubles:56×2=112.'),
('analogy','Carrot','In the ordinary food classification intended here, apple,mango andbanana are fruits while carrot is an edible root.'),
('simplification','-5','Replace the operators before calculating:6÷2−4×2=3−8=−5 under standard precedence.'),
('syllogism','Does not follow','Pens form a subset of books, but the red books might all be outside that subset. Some pens being red is possible, not forced.'),
('vocabulary','Plentiful','Abundant means present in a large quantity, so plentiful is the closest synonym.'),
('vocabulary','Cruel','Benevolent means kindly or well-meaning; cruel is the contrasting option.'),
('spelling','Accommodate','Accommodate has double c and double m. The alternative spellings omit one or both doubled letters.'),
('prepositions','at','The conventional construction is good at a subject or activity.'),
('tense','He has been working for 5 years','For introduces a duration such as five years. Since requires a starting point such as2021.'),
('word-classes','Omnivore','An omnivore eats both plant and animal material. This does not literally mean it can eat every substance.'),
('vocabulary','Frank','Candid means frank, open and straightforward; sly, rude and secret do not preserve that meaning.'),
('vocabulary','Opaque','For transmission of light, transparent and opaque are opposites.'),
('word-classes','Crises','The conventional plural changes the ending of crisis to crises.'),
('idioms','Endure a hardship','Bite the bullet means accept or endure a difficult or unpleasant situation with resolve.'),
('agreement','nor','Neither pairs with nor. In this sentence the nearer singular subject coach agrees with was.'),
('vocabulary','Careful','Meticulous means very attentive to detail, making careful the closest option.')]

def review_aptitude(topics):
    bank=json.loads((ROOT/'data/aptitude-bank.snapshot.json').read_text(encoding='utf-8'))
    assert len(bank)==len(APT_REVIEW)==36
    meta={t['id']:t for t in topics};results=[];changed=[]
    for i,(original,(topic,answer,why)) in enumerate(zip(bank,APT_REVIEW),1):
        entry=deepcopy(original)
        if i==10:entry['q']='With annual compounding, find compound interest on1000 at10% per year for2 years.'
        if i==14:entry['q']='A word’s code is the sum of its letters’ positions(A=1,…,Z=26). CAT=24 and DOG=26. What is PIG’s code?'
        if i==16:entry['q']='A,B and C are distinct full siblings sharing both parents. A is B’s brother and B is C’s sister. How is A related to C?'
        if i==23:entry['q']='Replace the coded operators first, then use standard precedence: if "+" means ÷, "÷" means − and "−" means ×, evaluate6 + 2 ÷ 4 − 2.'
        if i==27:entry['q']='Choose the standard spelling of the verb meaning to provide lodging or make room for someone.'
        if i==30:entry['q']='Which term describes an animal whose diet includes both plant and animal material?'
        if i==32:entry['q']='For a material transmitting light, choose the antonym of "TRANSPARENT".'
        entry['answer']=entry['options'].index(answer)
        if any(entry[k]!=original[k] for k in ('q','options','answer')):changed.append(i)
        entry.update(id=f'aptitude-{i:03}',topic=topic,explanation=why,formula=meta[topic]['formula'],
            trick=meta[topic]['trick'],difficulty='Easy',origin='StudyLab sectional bank · reviewed',
            sources=meta[topic]['sources'],legacyOriginal=original['q'],legacyOrdinal=i)
        results.append(entry)
    return results,dict(reviewed=36,clarified=changed)
