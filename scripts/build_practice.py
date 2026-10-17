"""Build original, explained practice items; source sites inform coverage, not copied banks."""
from fractions import Fraction as F
from math import comb, factorial, gcd
from pathlib import Path
import datetime
import json
import random

ROOT = Path(__file__).resolve().parents[1]
TOPICS, QUESTIONS = [], []


def fmt(x):
    if isinstance(x, F):
        return str(x.numerator) if x.denominator == 1 else str(x)
    if isinstance(x, float):
        return str(round(x, 4)).rstrip('0').rstrip('.') if x != int(x) else str(int(x))
    return str(x)


def topic(key, section, title, formula, notes, trick, trap):
    TOPICS.append(dict(id=key, section=section, title=title, formula=formula, notes=notes,
                       trick=trick, trap=trap, sources=['coverage'] if section != 'Coding' else ['algorithms']))
    return key


def add(key, prompt, correct, explanation, distractors=None, difficulty='Medium'):
    meta = next(t for t in TOPICS if t['id'] == key)
    right = fmt(correct)
    if distractors is None:
        value = F(correct)
        distractors = [value + 1, value - 1, value + 2, value * 2, value / 2]
    options = [right]
    for d in distractors:
        if fmt(d) not in options:
            options.append(fmt(d))
        if len(options) == 4:
            break
    if len(options) != 4:
        raise ValueError((key, prompt, options))
    i = len(QUESTIONS)
    random.Random(1027 + i).shuffle(options)
    QUESTIONS.append(dict(id=f'prep-{key}-{sum(q["topic"]==key for q in QUESTIONS)+1:02}',
        section=meta['section'], topic=key, q=prompt, options=options, answer=options.index(right),
        explanation=explanation, formula=meta['formula'], trick=meta['trick'], difficulty=difficulty,
        origin='CodeLab original practice', sources=meta['sources']))


def numeric_topics():
    topic('percent','Quant','Percentages','Percentage = part / whole × 100; new value = old × (1 ± r/100).',
          'Choose the reference whole before calculating. Successive changes multiply their factors; they do not simply add.',
          'Convert 12.5% to 1/8 and 16⅔% to 1/6 when useful.','A percentage increase and an equal percentage decrease do not cancel.')
    topic('profit','Quant','Profit, loss & marked price','Profit% = (SP − CP)/CP × 100; SP = MP × (1 − discount/100).',
          'Cost price is the base for profit/loss; marked price is the base for discount.', 'Set CP to 100 for percentage-only questions.','Never divide profit by selling price unless a margin is explicitly requested.')
    topic('discount','Quant','Successive discounts','Equivalent discount = a + b − ab/100.',
          'Apply each discount to the price remaining after the previous one.', 'Use remaining-price multipliers.','Two 20% discounts produce 36%, not 40%.')
    topic('simple-interest','Quant','Simple interest','SI = PRT/100; amount = P + SI.',
          'Use consistent time units. Under simple interest, interest is always computed on the original principal.', 'Find interest for one year, then scale.','Convert months to years before using an annual rate.')
    topic('compound-interest','Quant','Compound interest','A = P(1+r/100)^n; CI = A−P.',
          'For half-yearly compounding, halve the annual rate and double the number of years.', 'For two years, CI−SI = P(r/100)².','Distinguish compound amount from compound interest.')
    topic('ratio','Quant','Ratio & proportion','Share = total × corresponding ratio / sum of ratio terms.',
          'Ratios compare quantities in the same units; multiply both terms by the same factor.', 'Work in ratio units before substituting the total.','The denominator for a part of the total is a+b, not the other part.')
    topic('average','Quant','Averages & weighted means','Average = sum/count; combined mean = (n₁m₁+n₂m₂)/(n₁+n₂).',
          'Treat group size as the weight. Averages of unequal-sized groups cannot be averaged directly.', 'Track the change in the total when a value is replaced.','A new member changes both sum and count.')
    topic('mixture','Quant','Mixtures & alligation','Quantity at concentration c₁ / quantity at c₂ = (c₂−c)/(c−c₁).',
          'The target concentration must lie between the two input concentrations for a positive mixture.', 'Cross differences give the quantity ratio.','Apply the ratio in the correct low-to-high order.')
    topic('partnership','Quant','Partnership','Profit share ∝ capital × time invested.',
          'Split an investment into intervals when capital changes, then add capital-months.', 'Reduce weighted investments by their GCD.','Equal investments for unequal durations do not get equal profits.')
    topic('ages','Quant','Problems on ages','Present ages x,y become x+t,y+t after t years.',
          'Age differences are constant; ratios change with time.', 'Use ratio units and solve one linear equation.','Do not add a year count to the ratio terms themselves.')
    topic('work','Quant','Time & work','Combined work rate = 1/a + 1/b; time = 1/rate.',
          'Choose one completed job as the unit of work. Rates add, completion times do not.', 'Use the LCM of completion times as total work units.','An outlet or undoing worker contributes a negative rate.')
    topic('pipes','Quant','Pipes & cisterns','Net rate = filling rates − draining rates.',
          'Assume a constant flow only when stated. An empty tank cannot lose water below zero.', 'Use tank capacity equal to the LCM of the times.','A net rate of zero or less cannot fill an initially empty tank.')
    topic('speed','Quant','Time, speed & distance','d=vt; km/h→m/s multiply by 5/18; equal-distance mean speed=2uv/(u+v).',
          'Use relative speeds for two moving objects and align distance/time units.', 'For equal distances use the harmonic mean.','The arithmetic mean applies to equal travel times, not equal distances.')
    topic('trains','Quant','Trains & relative motion','Time to cross = total length to clear / relative speed.',
          'For a pole use train length; for a platform add platform length.', 'Opposite directions add speeds; same direction subtract.','Convert km/h to m/s when lengths are in metres.')
    topic('boats','Quant','Boats & streams','Downstream = b+s; upstream = b−s.',
          'The still-water speed must exceed the stream speed for upstream travel.', 'b=(down+up)/2; s=(down−up)/2.','Do not use downstream speed for a return upstream trip.')
    topic('number-system','Quant','Divisibility, factors & remainders','a = dq+r with 0≤r<d; divisibility by 9 uses digit sum.',
          'Use modular arithmetic for powers and last digits. Factor counts come from prime exponents.', 'Reduce residues at each multiplication.','A remainder is relative to the given divisor, not a digit by default.')
    topic('hcf-lcm','Quant','HCF & LCM','For two positive integers: gcd(a,b) × lcm(a,b) = ab.',
          'The identity applies to two numbers. Euclid repeatedly replaces (a,b) by (b,a mod b).','Divide before multiplying to reduce overflow.','For three numbers use pairwise LCM; do not multiply all numbers and divide by one GCD.')
    topic('simplification','Quant','Fractions & simplification','Apply brackets, powers, multiplication/division, addition/subtraction.',
          'Operations of equal precedence proceed left to right. Convert mixed numbers carefully.', 'Cancel common factors before multiplication.','Multiplication does not always precede division; they have equal precedence.')
    topic('indices','Quant','Surds, indices & logarithms','a^m a^n=a^(m+n); logₐ(a^k)=k for a>0,a≠1.',
          'Exponent laws require compatible bases; logarithms require positive arguments.', 'Rewrite all terms using a common base.','(a+b)² includes the cross term 2ab.')
    topic('progression','Quant','Arithmetic & geometric progressions','AP: aₙ=a+(n−1)d; Sₙ=n(2a+(n−1)d)/2.',
          'First differences identify an AP; constant ratios identify a GP.', 'For an AP, average of first and last terms times count gives the sum.','The nth term uses n−1 steps from the first term.')
    topic('permutation','Quant','Permutations','nPr = n!/(n−r)!; repeated letters: n!/(p!q!…).',
          'Order matters for arrangements; identical objects do not create new permutations.', 'Fill constrained positions first.','Treating identical objects as distinct overcounts.')
    topic('combination','Quant','Combinations','nCr = n!/[r!(n−r)!]; nCr=nC(n−r).',
          'Choose without ordering when a committee or subset is requested.', 'Use the smaller of r and n−r.','Do not use permutations for an unordered team.')
    topic('probability','Quant','Probability','P(E)=favourable/equally likely outcomes; P(not E)=1−P(E).',
          'State replacement and independence assumptions. Without replacement the sample changes.', 'Use the complement for at-least-one questions.','Mutually exclusive events are generally not independent.')
    topic('area','Quant','Area, perimeter & geometry','Rectangle A=lw; triangle A=bh/2; circle A=πr²; circumference=2πr.',
          'Keep length, square units and volume units separate. Similar-area ratios are squares of length ratios.', 'Use π=22/7 only when the question specifies it.','Area and perimeter do not scale by the same factor.')
    topic('volume','Quant','Volume & surface area','Cuboid V=lwh; cylinder V=πr²h; cone V=πr²h/3.',
          'Convert all dimensions before multiplying. One litre is 1000 cubic centimetres.', 'Use dimensional analysis to check cubic units.','A cone with the same base and height has one third of the cylinder volume.')
    topic('trigonometry','Quant','Heights & distances','tan θ = opposite/adjacent; sin²θ+cos²θ=1.',
          'Draw the right triangle and identify the angle of elevation before applying a ratio.', 'At 45°, vertical height above eye level equals horizontal distance.','Add eye height to the triangle height when the observer is above ground.')
    topic('clock','Quant','Clocks','Angle = |30h−5.5m| degrees, then use the smaller of θ and 360−θ.',
          'The hour hand moves continuously at 0.5° per minute.', 'At a whole hour use 30° times the hour difference.','The hour hand is not fixed at the hour numeral between whole hours.')
    topic('calendar','Quant','Calendars','Ordinary year shifts weekdays by 1; leap year by 2; Gregorian leap: divisible by 4 except centuries unless divisible by 400.',
          'Use the Gregorian calendar unless another calendar is stated.', 'Count complete weeks first and keep only the remainder modulo 7.','1900 is not a leap year; 2000 is.')
    for i in range(12):
        base=(i+5)*80; rate=[5,10,15,20,25,30][i%6]
        add('percent',f'A training centre has {base} learners. {rate}% choose Python. How many choose Python?',F(base*rate,100),f'Use the full learner count as the base: {base} × {rate}/100 = {fmt(F(base*rate,100))}.',difficulty='Easy')
        cp=400+100*i; p=10+5*(i%5)
        add('profit',f'A keyboard costs Rs {cp} and is sold at a {p}% profit on cost. Find its selling price in rupees.',F(cp*(100+p),100),f'Profit = {cp}×{p}/100. Add it to cost: {cp}×{100+p}/100 = {fmt(F(cp*(100+p),100))}.')
        a=5+5*(i%4); b=10+5*(i//4)
        add('discount',f'A store applies discounts of {a}% and then {b}%. What is the equivalent single discount percentage?',F(100*(a+b)-a*b,100),f'The remaining-price factor is {(100-a)}/100 × {(100-b)}/100. Discount = {a}+{b}−({a}×{b}/100) = {fmt(F(100*(a+b)-a*b,100))}%.')
        principal=1000+500*i; r=4+i%7; years=2+i%3
        add('simple-interest',f'Find simple interest in rupees on Rs {principal} at {r}% per year for {years} years.',F(principal*r*years,100),f'SI = PRT/100 = {principal}×{r}×{years}/100 = {fmt(F(principal*r*years,100))}.')
        principal=10000+1000*i; rate=10
        ci=F(principal*121,100)-principal
        add('compound-interest',f'Rs {principal} earns 10% per year compounded annually for 2 years. Find the compound interest in rupees.',ci,f'Amount = {principal}×1.1² = {fmt(ci+principal)}. Subtract principal: CI = {fmt(ci)}.')
        a=i%5+2;b=i%3+4; unit=30+5*i
        add('ratio',f'A and B divide Rs {(a+b)*unit} in the ratio {a}:{b}. How many rupees does A get?',a*unit,f'Total ratio units = {a+b}. One unit = {(a+b)*unit}/{a+b} = {unit}. A receives {a}×{unit}={a*unit}.')
        n=8+i; mean=20+i; newcomer=mean+2*(n+1)
        add('average',f'The average of {n} values is {mean}. A new value {newcomer} is added. Find the new average.',mean+2,f'Old sum={n*mean}. New sum={n*mean+newcomer}; count={n+1}. Average={mean+2}.')
        low=10+i; high=50+i; target=30+i
        add('mixture',f'A {low}% solution and a {high}% solution are mixed to get a {target}% solution. Find the ratio of low-concentration to high-concentration quantities.','1:1',f'Alligation gives ({high}−{target}):({target}−{low}) = 20:20 = 1:1.',['1:2','2:1','3:1'])
        x=2+i%4;y=3+i%5; total=(x+y)*1000
        add('partnership',f'A invests Rs {x*1000} for 12 months; B invests Rs {y*2000} for 6 months. A total profit of Rs {total} is shared by capital-time. Find A\'s share.',x*1000,f'Weighted capitals are {x*12000} and {y*12000}, giving ratio {x}:{y}. A gets {total}×{x}/{x+y} = {x*1000}.')
        younger=12+3*i; diff=6
        add('ages',f'A is {diff} years older than B. Their present ages total {2*younger+diff} years. Find B\'s age.',younger,f'Let B=x, A=x+{diff}. Then 2x+{diff}={2*younger+diff}, so x={younger}.',difficulty='Easy')
        a=10+2*i;b=2*a
        add('work',f'A completes a job in {a} days; B completes it in {b} days. Working together at constant rates, how many days are needed?',F(a*b,a+b),f'Combined daily rate = 1/{a}+1/{b} = {fmt(F(a+b,a*b))}. Time is its reciprocal = {fmt(F(a*b,a+b))} days.')
        fill=6+i; drain=2*fill
        add('pipes',f'A pipe fills a tank in {fill} hours. A drain empties it in {drain} hours. With both open, how many hours fill the initially empty tank?',2*fill,f'Net hourly rate = 1/{fill}−1/{drain}=1/{2*fill}. Time={2*fill} hours.')
        u=30+3*i;v=2*u
        add('speed',f'A car travels the same distance at {u} km/h outward and {v} km/h returning. What is its average speed in km/h?',F(2*u*v,u+v),f'For equal distances use 2uv/(u+v) = 2×{u}×{v}/{u+v} = {fmt(F(2*u*v,u+v))}.')
        length=100+10*i; platform=length; speed=36
        add('trains',f'A {length} m train moving at {speed} km/h crosses a {platform} m platform. Find the time in seconds.',F(2*length,10),f'36 km/h = 10 m/s. Distance to clear = {length}+{platform}={2*length} m. Time={2*length}/10={fmt(F(2*length,10))} s.')
        b=12+i;s=2+i%3
        add('boats',f'A boat moves at {b} km/h in still water. The stream is {s} km/h. How long in hours does it take to travel {(b-s)*3} km upstream?',3,f'Upstream speed={b}−{s}={b-s} km/h. Time={(b-s)*3}/{b-s}=3 hours.')
        n=10+i;d=7
        add('number-system',f'What is the non-negative remainder when {n}² is divided by {d}?',n*n%d,f'{n}²={n*n}; {n*n}={d}×{n*n//d}+{n*n%d}. The remainder is {n*n%d}.',distractors=[(n*n+1)%7,(n*n+2)%7,(n*n+3)%7],difficulty='Easy')
        a=12+6*i;b=18+6*i;ans=a*b//gcd(a,b)
        add('hcf-lcm',f'Find the least common multiple of {a} and {b}.',ans,f'gcd({a},{b})={gcd(a,b)}. lcm={a}×{b}/{gcd(a,b)}={ans}.')
        a=i+2;b=i+5
        add('simplification',f'Evaluate ({a} + {b}) × 3 − 12 ÷ 4.',(a+b)*3-3,f'Brackets give {a+b}; multiply to get {(a+b)*3}; 12÷4=3. Result={(a+b)*3-3}.',difficulty='Easy')
        e=i+2
        add('indices',f'Evaluate log₂(2^{e}) + 2³.',e+8,f'log₂(2^{e})={e}; 2³=8. Sum={e+8}.')
        a=3+i;d=2+i%4;n=8+i
        add('progression',f'An arithmetic progression starts at {a} with common difference {d}. Find its {n}th term.',a+(n-1)*d,f'aₙ=a+(n−1)d={a}+({n}−1)×{d}={a+(n-1)*d}.')
        n=5+i%7;r=2+i//7
        add('permutation',f'From {n} distinct runners, in how many ways can ordered first {r} places be assigned?',factorial(n)//factorial(n-r),f'Positions are distinct, so use nPr={n}!/{n-r}!={factorial(n)//factorial(n-r)}.')
        n=6+i;r=3
        add('combination',f'A committee of 3 is chosen from {n} people. How many different committees exist?',comb(n,r),f'Order does not matter: C({n},3)={n}×{n-1}×{n-2}/6={comb(n,3)}.')
        red=3+i;blue=5+i%5
        add('probability',f'A bag contains {red} red and {blue} blue balls. One ball is drawn uniformly at random. What is the probability it is red?',F(red,red+blue),f'Total balls={red+blue}; favourable={red}. Probability={fmt(F(red,red+blue))}.',distractors=[F(blue,red+blue),F(red,red+blue+1),F(red,red+blue-1),F(1,red+blue)])
        l=10+i;w=4+i%4
        add('area',f'A rectangle is {l} cm long and {w} cm wide. Find its area in cm².',l*w,f'Area=length×width={l}×{w}={l*w} cm².',difficulty='Easy')
        r=7;h=3+i
        add('volume',f'Using π=22/7, find the volume in cm³ of a cylinder of radius 7 cm and height {h} cm.',154*h,f'V=πr²h=(22/7)×49×{h}={154*h} cm³.')
        distance=12+2*i;eye=1+i%3
        add('trigonometry',f'An observer\'s eye is {eye} m above ground. A tower top has elevation 45° at horizontal distance {distance} m. Find the tower height in metres.',distance+eye,f'tan45°=1, so the height above eye level equals {distance} m. Add eye height {eye}: {distance+eye} m.')
        hour=i%12;minute=10
        angle=abs(30*hour-5.5*minute);angle=min(angle,360-angle)
        add('clock',f'Find the smaller angle in degrees between clock hands at {hour or 12}:10.',angle,f'Hour-hand angle={30*hour+5}°, minute-hand angle=60°. Difference={abs(30*hour-55)}°. The smaller angle is {fmt(angle)}°.')
        year=2024+i; leap=year%4==0 and (year%100!=0 or year%400==0)
        days=366 if leap else 365
        add('calendar',f'Under the Gregorian calendar, how many days are in {year}?',days,f'{year} '+('is divisible by 4 and is not an excluded century, so it is a leap year with 366 days.' if leap else 'does not meet the leap-year rule, so it has 365 days.'),distractors=[365,366,364,360],difficulty='Easy')


def reasoning():
    specs=[
      ('series','Number & letter series','Inspect first/second differences, ratios and alternating subsequences.','Use the simplest consistent rule; a finite list alone never proves a unique mathematical continuation.','Write differences underneath the series.','Do not assume a constant gap without checking it.'),
      ('coding','Coding & decoding','Alphabet shift: index(new)=(index(old)+k) mod 26.','Apply the same declared encoding rule to every letter.','Map A=0,…,Z=25 for cyclic shifts.','Z wraps around to A.'),
      ('direction','Directions & displacement','Final displacement = (sum east−west, sum north−south); distance=√(x²+y²).','Distinguish path length from shortest distance.','Draw a coordinate grid.','A turn depends on the direction currently faced.'),
      ('ranking','Ranking & order','For one person: total=rank from top+rank from bottom−1.','For two people, count the positions strictly between them.','Place ranks on a number line.','The person counted in both directions is counted twice unless you subtract one.'),
      ('relations','Blood relations','Translate each statement into a family-tree edge.','Use only explicitly stated gender and parentage.','Draw generations on separate rows.','Do not assume a spouse or sibling unless the stem states it.'),
      ('seating','Linear & circular arrangements','For a line, fix orientation before translating left/right.','Use all constraints; test whether the arrangement is unique.','Anchor a fixed position and place immediate neighbours first.','People facing south have their left/right reversed relative to your drawing.'),
      ('syllogism','Syllogisms & Venn logic','All A are B means A⊆B; some A are B means A∩B is nonempty.','Universal statements do not imply that the class has members.','Look for a counterexample to disprove a claimed conclusion.','All A are B does not imply all B are A.'),
      ('inequality','Inequalities','If a>b and b≥c, then a>c.','Chain compatible comparison signs and keep strictness.','Draw ordered quantities in a line.','A>B and C>B alone do not compare A and C.'),
      ('sufficiency','Data sufficiency','A statement is sufficient only if it uniquely determines the requested value.','Test each statement alone, then together.','Try two possible values satisfying the data.','Enough equations is not sufficient if they are dependent.'),
      ('assumption','Assumptions & arguments','A necessary assumption is a condition the argument needs.','Distinguish the author’s claim from external facts.','Negate an assumption and see if the reasoning breaks.','A useful fact is not automatically a necessary assumption.'),
      ('conclusion','Conclusions & deductions','Accept only conclusions forced by the stated premises.','Do not add real-world knowledge to formal deduction.','Construct a model in which premises hold but the conclusion fails.','Possibility is weaker than necessity.'),
      ('analogy','Analogies & classification','Identify the relation before matching a pair.','A shared superficial feature may not preserve the relation.','Describe the relation in one short sentence.','Reverse direction can change the relation.'),
      ('venn','Sets & Venn diagrams','|A∪B|=|A|+|B|−|A∩B|.','Subtract overlap once when counting at least one category.','Fill the intersection first.','Neither=total−union; do not subtract the two groups independently.'),
      ('cubes','Cubes & spatial reasoning','A painted n×n×n cube has 8 corner cubes; exactly-two-face cubes=12(n−2), n≥2.','Classify small cubes into corners, edges, faces and interior.','Count by location rather than drawing every cube.','Interior cubes have no painted face.'),
      ('arrangements','Counting arrangements & constraints','For independent choices multiply; for mutually exclusive cases add.','State whether repetitions and order are allowed.','Count the complement when forbidden cases are simpler.','Do not multiply choices that are not independent.')]
    for key,title,formula,notes,trick,trap in specs:
        topic(key,'Logical',title,formula,notes,trick,trap)
    for i in range(10):
        a=2+i;d=3+i
        seq=[a+j*d for j in range(4)]
        add('series',f'The sequence is arithmetic with a constant difference: {", ".join(map(str,seq))}, ?. Find the next term.',a+4*d,f'Each gap is {d}; add it to {seq[-1]} to obtain {a+4*d}.',difficulty='Easy')
        word=['CODE','MATH','LOGIC','TRAIN','ARRAY','STACK','GRAPH','BINARY','INPUT','SOLVE'][i];shift=i%5+1
        encoded=''.join(chr((ord(c)-65+shift)%26+65) for c in word)
        add('coding',f'Every capital letter is shifted {shift} places forward cyclically (Z wraps to A). Encode {word}.',encoded,f'Apply +{shift} modulo 26 to each letter: {word} → {encoded}.',[word[::-1],word,encoded[::-1],encoded+'A'])
        x=3*(i+1);y=4*(i+1)
        add('direction',f'A person walks {x} m east, then {y} m north. What is the shortest distance from the start in metres?',5*(i+1),f'The legs are perpendicular. √({x}²+{y}²)={5*(i+1)} m (a scaled 3-4-5 triangle).')
        top=4+i;bottom=9+i
        add('ranking',f'A learner ranks {top}th from the top and {bottom}th from the bottom. How many learners are there?',top+bottom-1,f'Total={top}+{bottom}−1={top+bottom-1}; subtract the learner counted twice.',difficulty='Easy')
        name=['Asha','Beena','Charu','Diya','Esha','Farah','Gita','Hema','Isha','Jaya'][i]
        add('relations',f'{name} is the mother of K. K is the father of M. What is {name}\'s relation to M?','Grandmother',f'{name} is one generation above K and two above M; she is M\'s paternal grandmother.',['Mother','Aunt','Sister'],difficulty='Easy')
        n=6+i;position=2+i%3
        add('seating',f'{n} people face north in a row. P is at position {position} from the left; Q is immediately to P\'s right. What is Q\'s position from the right?',n-position,f'Q is {position+1} from the left. From the right: {n}−{position+1}+1={n-position}.')
        nouns=[('coders','readers','artists'),('roses','plants','trees'),('cars','vehicles','buses'),('squares','shapes','circles'),('teachers','workers','singers'),('apples','fruits','pears'),('sparrows','birds','eagles'),('trains','machines','robots'),('novels','books','poems'),('doctors','graduates','dancers')][i];a,b,c=nouns
        add('syllogism',f'All {a} are {b}. No {b} are {c}. Which conclusion must follow?','No A are C',f'Every member of A lies inside B, while B and C are disjoint. Therefore A and C are disjoint too. Here A={a}, B={b}, C={c}.',['All C are A','Some C are A','All B are A'])
        x=i+2
        add('inequality',f'If A > B, B ≥ C, and C = {x}, which is necessarily true?','A > C','A>B≥C implies A>C. Equality of B and C does not remove the strict inequality between A and B.',['A = C','A < C','B < C'])
        a=4+i;b=6+i
        add('sufficiency',f'Find positive integers x and y individually. I: x+y={a+b}. II: x−y={a-b}. Which data suffice?','Both together only',f'I alone allows multiple pairs; II alone also allows multiple pairs. Together, add the equations to get 2x={2*a}, so x={a}, y={b}.',['I alone only','II alone only','Neither, even together'])
        subject=['bus','library','clinic','canteen','lab','gym','museum','help desk','bank branch','study room'][i]
        add('assumption',f'An organiser says: "Opening the {subject} one hour earlier will help people who can attend only before its current opening time." Which assumption is needed?','Those people can use the earlier hour','The proposal helps the stated group only if at least some of that group can attend during the newly available hour.',['Everyone dislikes the current hours','No one uses the current hours','Earlier opening costs nothing'])
        add('conclusion',f'In batch {i+1}, every person who passed module A also passed module B. R did not pass B. What follows?','R did not pass A','A-pass implies B-pass. Its contrapositive is not-B-pass implies not-A-pass.',['R passed A','Nobody passed A','Everyone passed B'])
        pairs=[('Thermometer','temperature','Barometer','pressure'),('Pen','writing','Knife','cutting'),('Bird','nest','Bee','hive'),('Doctor','hospital','Teacher','school'),('Book','pages','Tree','leaves'),('Triangle','three sides','Pentagon','five sides'),('Kilogram','mass','Metre','length'),('Author','book','Composer','music'),('Carpenter','wood','Potter','clay'),('Clock','time','Compass','direction')]
        a,b,c,d=pairs[i]
        add('analogy',f'{a} : {b} :: {c} : ? ',d,f'The relation is preserved: {a} relates to {b} in the same way that {c} relates to {d}.',['colour','speed','weight','sound'] if d not in ['colour','speed','weight','sound'] else ['shape','price','age'])
        total=80+5*i;a=35+i;b=30+i;overlap=10+i
        neither=total-a-b+overlap
        add('venn',f'Of {total} learners, {a} study Python, {b} study SQL and {overlap} study both. How many study neither?',neither,f'At least one={a}+{b}−{overlap}={a+b-overlap}. Neither={total}−{a+b-overlap}={neither}.')
        n=3+i
        add('cubes',f'A cube is painted on all outer faces, then cut into {n}×{n}×{n} equal small cubes. How many have exactly two painted faces?',12*(n-2),f'Only edge cubes excluding corners have exactly two painted faces. Each of 12 edges contributes {n}−2={n-2}; total={12*(n-2)}.')
        letters=3+i;digits=4+i
        add('arrangements',f'A code has one letter chosen from {letters} distinct allowed letters followed by one digit from {digits} allowed digits. How many codes are possible?',letters*digits,f'Each of {letters} letter choices pairs with any of {digits} digit choices: {letters}×{digits}={letters*digits}.')


def interpretation():
    topic('data-tables','DataInterpretation','Tables & data comparison','Growth%=(new−old)/old×100; share%=part/total×100.',
          'Read row/column labels and units first. Distinguish percentage points from relative percentage growth.', 'Compute the denominator before the numerator.','A higher absolute increase does not necessarily mean higher percentage growth.')
    topic('data-sets','DataInterpretation','Caselets & multi-step data','Weighted average=Σ(value×weight)/Σweights.',
          'Translate a caselet into a compact table. Verify totals before answering subquestions.', 'Keep a shared table and annotate units.','Average price per item is weighted by quantities, not by the number of price categories.')
    for i in range(16):
        a=80+20*i;b=a+20;c=2*a
        table=f'A workshop reports units sold:\nProduct | Monday | Tuesday\nP | {a} | {c}\nQ | {b} | {b+10}'
        add('data-tables',table+'\nWhat is the percentage increase in sales of P from Monday to Tuesday?',100,f'P rises from {a} to {c}. Increase={a}; percentage={a}/{a}×100=100%.')
        qty1=10+i;qty2=2*qty1;p1=20+i;p2=35+i
        add('data-sets',f'A shop sells {qty1} notebooks at Rs {p1} each and {qty2} notebooks at Rs {p2} each. Find average revenue per notebook in rupees.',F(qty1*p1+qty2*p2,qty1+qty2),f'Total revenue={qty1}×{p1}+{qty2}×{p2}={qty1*p1+qty2*p2}; total notebooks={qty1+qty2}. Divide to get {fmt(F(qty1*p1+qty2*p2,qty1+qty2))}.')


def verbal_and_technical():
    # Original sentence items and stable concept checks, rather than scraped question text.
    groups = {
      'agreement':('Verbal','Subject–verb agreement','The finite verb agrees with the grammatical subject.','Ignore intervening prepositional phrases when finding the subject.','Find the subject before selecting the verb.','Words next to the verb are not always the subject.',[
       ('Each of the candidates ___ a registration number.','has',['have','are','were'],'Each is singular, so it takes has.'),
       ('The list of approved courses ___ on the noticeboard.','is',['are','were','have'],'List is the singular subject; courses belongs to the of-phrase.'),
       ('Neither of these two solutions ___ efficient.','is',['are','have','were'],'In formal agreement, neither takes a singular verb here.'),
       ('Several participants ___ submitted their forms.','have',['has','is','was'],'Several participants is plural, requiring have.'),
       ('Mathematics ___ my favourite subject.','is',['are','were','have'],'Mathematics names one field and takes a singular verb.'),
       ('The information supplied by the teams ___ useful.','is',['are','have','were'],'Information is an uncountable singular noun.')]),
      'tense':('Verbal','Tenses & aspect','Use present perfect for a past event connected to the present; past perfect for an earlier past event.','Choose tense using time markers and sequence.','Mark which event happened first.','Do not use present perfect with a finished past-time marker such as yesterday.',[
       ('By the time the interview began, she ___ the form.','had completed',['has complete','will complete','completes'],'Completion happened before a past event, so use past perfect.'),
       ('He ___ in this office since 2021 and still works here.','has worked',['worked yesterday','will working','is work'],'Since introduces a starting point continuing to the present.'),
       ('We ___ the test yesterday.','took',['have taken','had take','takes'],'Yesterday is a finished past time, so simple past fits.'),
       ('Look! The bus ___ towards the stop.','is coming',['come','has came','were coming'],'Look signals an action in progress now.'),
       ('If it rains tomorrow, we ___ indoors.','will stay',['would stayed','had stay','staying'],'A real future conditional uses if + present and will + base verb.'),
       ('She usually ___ to work by train.','travels',['is travel','have travelled','travelling'],'Usually describes a regular habit, so use simple present.')]),
      'articles':('Verbal','Articles & determiners','Use a/an by the following sound; the marks a specific referent.','Sound, countability and specificity determine the article.','Say the phrase aloud.','A university starts with a consonant sound; an hour begins with a vowel sound.',[
       ('She waited for ___ hour.','an',['a','the only','no'],'Hour starts with a vowel sound because h is silent.'),
       ('He enrolled at ___ university.','a',['an','any an','no'],'University starts with the consonant sound /y/.'),
       ('I saw a dog. ___ dog was wearing a blue collar.','The',['An','A an','No'],'The second reference identifies the already mentioned dog.'),
       ('She is ___ honest engineer.','an',['a','many','no'],'Honest begins with a vowel sound.'),
       ('___ sun rises in the east.','The',['A','An','Any'],'The sun refers to a unique object in this ordinary context.'),
       ('We need ___ useful example.','a',['an','many','these'],'Useful starts with a /y/ sound and example is singular countable.')]),
      'prepositions':('Verbal','Prepositions & collocations','Use the preposition required by the adjective/verb and intended relationship.','Many combinations are conventional and need contextual practice.','Learn short chunks: interested in, responsible for.','Do not translate a preposition mechanically from another language.',[
       ('She is interested ___ data science.','in',['on','at','from'],'The standard collocation is interested in.'),
       ('He is responsible ___ maintaining the records.','for',['of','to','at'],'Responsible for introduces the duty.'),
       ('The result depends ___ the final assessment.','on',['in','at','from'],'The verb depend takes on in this use.'),
       ('Please comply ___ the instructions.','with',['to','on','for'],'Comply with means act according to a rule.'),
       ('She is proficient ___ Python.','in',['from','of','by'],'Proficient in introduces the skill or language.'),
       ('The session starts ___ 9 a.m.','at',['on','in','over'],'At introduces a precise clock time.')]),
      'voice':('Verbal','Active & passive voice','Passive = object + suitable be + past participle (+ by agent).','Preserve tense, meaning and agreement when changing voice.','Identify subject, verb and object first.','Only transitive uses normally admit a direct passive.',[
       ('Choose the passive form of: The team completed the project.','The project was completed by the team.',['The project is complete the team.','The team was completed by the project.','The project has complete.'],'Simple past completed becomes was completed; project becomes the passive subject.'),
       ('Choose the passive form of: They will announce the results.','The results will be announced.',['The results will announced.','The results were announce.','They will be results.'],'Will + base verb becomes will be + past participle.'),
       ('Choose the active form of: The report was checked by Mira.','Mira checked the report.',['Mira checks the report tomorrow.','The report checked Mira.','Mira was checking by report.'],'Preserve simple past and make the agent Mira the subject.'),
       ('Choose the passive form of: Someone has repaired the printer.','The printer has been repaired.',['The printer has repaired someone.','The printer had repair.','Someone was repaired.'],'Present perfect passive is has/have been + past participle.')]),
      'narration':('Verbal','Reported speech','Report the message with suitable tense, pronoun and time-reference changes.','Backshift is common after a past reporting verb, but universal truths can retain present tense.','Identify who said what and when.','Do not retain the original speaker’s pronouns without checking the referent.',[
       ('Ravi said, "I am tired." Choose the usual reported form.','Ravi said that he was tired.',['Ravi said that I am tired.','Ravi says he tired.','Ravi said that he is tiring yesterday.'],'After said, am normally backshifts to was and I refers to Ravi.'),
       ('Mina said, "I have finished." Choose the usual reported form.','Mina said that she had finished.',['Mina said she finish.','Mina said I had finish.','Mina says she finishing.'],'Present perfect normally backshifts to past perfect.'),
       ('The teacher said, "Water freezes at 0°C at standard pressure." Choose the appropriate report.','The teacher said that water freezes at 0°C at standard pressure.',['The teacher said water has freezing.','The teacher says water froze every future day.','Water said the teacher freezes.'],'A general scientific fact can keep the present tense.'),
       ('He asked me, "Are you ready?" Choose the reported question.','He asked me whether I was ready.',['He asked me whether was I ready.','He asked I am ready?','He said whether you ready.'],'Reported yes/no questions use whether/if and statement word order.')]),
      'parallelism':('Verbal','Parallelism & sentence correction','Coordinate grammatical structures should be parallel.','Compare list items and structures joined by and/or.','Read only the coordinated elements.','Mixing gerunds and infinitives can break a parallel list.',[
       ('Choose the sentence with parallel activity forms.','She enjoys reading, writing, and coding.',['She enjoys reading, to write, and code.','She enjoys to reading and wrote.','She enjoys read, writing, and coded.'],'All three objects of enjoys are gerunds.'),
       ('Choose the sentence with parallel requirement nouns.','The role requires patience, accuracy, and teamwork.',['The role requires patience, accurate, and teams work.','The role requires patient, accuracy, and team.','The role requires to patience and accurately.'],'The coordinated requirements are all nouns.'),
       ('Choose the correct comparison.','This method is more reliable than that one.',['This method is more reliable from that one.','This method is reliable most than that.','This method is more reliable as than.'],'A comparative adjective takes than.'),
       ('Choose the correctly modified sentence.','Walking into the room, Asha noticed the screen.',['Walking into the room, the screen was noticed.','Walking into the room, the screen smiled.','Walking into the room was noticed screen.'],'Asha is the person walking, so she should immediately follow the introductory modifier.')]),
      'vocabulary':('Verbal','Synonyms & antonyms','Use the sense required by context, not merely a related word.','Identify whether the task asks similarity or opposition.','Substitute each candidate into the sentence.','A synonym may fit one sense of a word but not another.',[
       ('Choose the closest synonym of concise.','brief',['careless','complex','loud'],'Concise means expressing much in few words.'),
       ('Choose the opposite of abundant.','scarce',['plentiful','ample','numerous'],'Abundant means plentiful; scarce means in short supply.'),
       ('Choose the closest synonym of diligent.','hardworking',['indifferent','reckless','idle'],'Diligent describes steady, careful effort.'),
       ('Choose the opposite of transparent in the sense of a material transmitting light.','opaque',['clear','visible','bright'],'An opaque material does not transmit visible light through it.'),
       ('Choose the closest synonym of mitigate.','alleviate',['intensify','ignore','create'],'Mitigate means make something less severe.'),
       ('Choose the opposite of reluctant.','willing',['hesitant','unwilling','doubtful'],'Reluctant means unwilling or hesitant; willing is its opposite.'),
       ('Choose the closest synonym of prudent.','cautious',['rash','wasteful','careless'],'Prudent means showing sound judgement and caution.'),
       ('Choose the opposite of temporary.','permanent',['brief','short-lived','transient'],'Temporary is limited in duration; permanent is lasting.')]),
      'idioms':('Verbal','Idioms, phrases & usage','Interpret the conventional figurative meaning in context.','An idiom’s meaning is often not a literal sum of its words.','Learn an example sentence with each idiom.','Do not infer a literal physical action from an idiom.',[
       ('What does "get the ball rolling" mean in a project meeting?','start the activity',['cancel the activity','repeat every task','avoid a decision'],'The idiom means initiate an activity.'),
       ('What does "a blessing in disguise" mean?','Something initially unwelcome that turns out beneficial',['An obvious reward','A secret instruction','A deliberate deception'],'The benefit becomes apparent only later.'),
       ('What does "on the same page" mean in a discussion?','Sharing an understanding',['Reading the same book','Ignoring each other','Ending the discussion'],'It describes agreement or shared understanding.'),
       ('What does "cut corners" usually mean when doing a task?','Skip proper steps to save effort or cost',['Improve every quality check','Expand the task','Follow every rule carefully'],'The expression usually suggests omitting proper procedures.')]),
      'spelling':('Verbal','Spelling & word choice','Choose the standard spelling and the word whose meaning fits.','Separate homophones by their grammatical function.','Check the part of speech the sentence needs.','Similar pronunciation does not imply interchangeable spelling.',[
       ('Choose the correct spelling of the word for a place to stay.','accommodation',['accomodation','acommodation','accommadation'],'Accommodation has double c and double m.'),
       ('Choose the correct spelling of the word meaning keep apart.','separate',['seperate','seperete','separrate'],'The standard spelling is separate.'),
       ('Choose the correct spelling of the word meaning required.','necessary',['neccessary','necesary','nessessary'],'Necessary has one c and double s.'),
       ('Complete: Please ___ my invitation.','accept',['except','expectation','access'],'Accept means receive or agree to; except means excluding.')]),
      'database':('GeneralAwareness','DBMS & SQL','Keys identify rows; joins combine related tables; transactions preserve integrity.','NULL is unknown/missing and needs IS NULL rather than = NULL.','Separate row filtering WHERE from group filtering HAVING.','COUNT(column) excludes NULL values; COUNT(*) counts rows.',[
       ('Which SQL clause filters groups after aggregation?','HAVING',['WHERE','ORDER BY','LIMIT'],'HAVING evaluates a condition on grouped results; WHERE filters input rows.'),
       ('Which constraint uniquely identifies each row and forbids NULL?','PRIMARY KEY',['DEFAULT','CHECK only','ORDER BY'],'A primary key enforces uniqueness and non-nullability.'),
       ('Which SQL predicate tests for a missing value?','IS NULL',['= NULL','== NULL','NULL = NULL'],'NULL uses three-valued logic, so use IS NULL.'),
       ('Which property means a transaction is all-or-nothing?','Atomicity',['Durability','Isolation','Sorting'],'Atomicity commits all transaction operations together or rolls them back.'),
       ('Which join retains all rows from the left table?','LEFT JOIN',['INNER JOIN','CROSS JOIN only','SELF JOIN only'],'A left outer join preserves unmatched left rows with NULL right-side values.'),
       ('What does COUNT(*) return for a table with 5 rows, one containing a NULL field?','5',['4','NULL','0'],'COUNT(*) counts rows regardless of individual field nulls.')]),
      'operating-systems':('GeneralAwareness','Operating systems','A process has its own address space; threads share a process address space.','Scheduling, memory management, files and synchronization are core OS responsibilities.','Identify the shared resource in concurrency questions.','A mutex is not a substitute for all forms of scheduling.',[
       ('Which condition is required for a deadlock?','Circular wait',['Unlimited resources','No mutual exclusion','Automatic preemption always'],'Circular wait is one of the four necessary Coffman conditions.'),
       ('Which memory technique loads pages only when they are referenced?','Demand paging',['Full replication','Disk formatting','Polling'],'Demand paging delays loading a page until it is needed.'),
       ('Threads in the same process normally share which resource?','Address space',['Independent process IDs only','Separate physical computers','Separate file systems by definition'],'Threads share code/data address space, while keeping their own stacks and execution state.'),
       ('Which scheduling policy uses a fixed time quantum?','Round robin',['First-come-first-served only','Shortest job first only','Non-preemptive priority only'],'Round robin cycles through ready processes using a time slice.')]),
      'networks':('GeneralAwareness','Networks & security','TCP provides an ordered byte stream; DNS maps names to records; TLS protects transport.','Authentication checks identity; authorization checks allowed actions.','Identify which layer/function the question describes.','Encryption alone does not decide access permissions.',[
       ('Which service resolves a domain name to address records?','DNS',['DHCP only','FTP','SMTP'],'DNS stores and resolves domain records, including address records.'),
       ('Which protocol provides an ordered reliable byte stream?','TCP',['UDP','ARP','ICMP'],'TCP supplies sequencing, acknowledgements and retransmission.'),
       ('What does authorization decide?','Which actions an identity may perform',['Whether a password is spelt correctly only','How to compress a file','How a CPU schedules tasks'],'Authorization determines permissions after or alongside identity verification.'),
       ('Which practice best reduces SQL injection risk?','Parameterized queries',['Concatenate raw user input','Hide the URL','Use a longer table name'],'Parameterized queries separate executable SQL structure from data values.')]),
      'civics':('GeneralAwareness','Indian polity & static awareness','Distinguish constitutional bodies, legislative houses and levels of government.','These are static foundational checks, not a current-affairs feed.','Make institution-function pairs.','Office holders and exam notifications can change; use current official sources for them.',[
       ('Which is the lower house of the Parliament of India?','Lok Sabha',['Rajya Sabha','Vidhan Parishad','Supreme Court'],'The Lok Sabha is the House of the People and lower house of Parliament.'),
       ('Fundamental Rights are primarily contained in which part of the Indian Constitution?','Part III',['Part I','Part IV','Part IX'],'Part III contains Fundamental Rights; Part IV contains Directive Principles.'),
       ('Which institution audits accounts of the Union and states under constitutional provisions?','Comptroller and Auditor General',['Election Commission','Finance Ministry only','NITI Aayog'],'The CAG is the constitutional auditing authority.'),
       ('Which body administers elections to Parliament and state legislatures?','Election Commission of India',['Union Public Service Commission','Reserve Bank of India','Supreme Court registry'],'The Election Commission supervises and administers these elections.')]),
      'science':('GeneralAwareness','Science, environment & economy basics','Use units and definitions to distinguish related concepts.','Static science and economic concepts support government-exam foundations.','Check whether a question asks a stock, flow, rate or unit.','Nominal growth and inflation-adjusted growth are different.',[
       ('What is the SI unit of electric current?','ampere',['volt','ohm','watt'],'Ampere measures current; volt measures potential difference.'),
       ('Which gas is consumed during photosynthesis?','Carbon dioxide',['Oxygen','Helium','Argon'],'Plants use carbon dioxide and water to produce carbohydrates, releasing oxygen.'),
       ('A sustained rise in the general price level is called what?','Inflation',['Deflation','Depreciation of machinery','Fiscal surplus'],'Inflation refers to a broad increase in prices over time.'),
       ('Which organ filters blood to form urine?','Kidney',['Lung','Stomach','Pancreas'],'Kidneys regulate fluid/solute balance and filter blood to produce urine.')]),
    }
    for key,(section,title,formula,notes,trick,trap,items) in groups.items():
        topic(key,section,title,formula,notes,trick,trap)
        for prompt,right,wrong,why in items:
            add(key,prompt,right,why,wrong)
    topic('reading','Verbal','Reading comprehension & inference','Support each answer with passage evidence; inference must follow without extra assumptions.',
          'Read for the author’s central claim, supporting evidence, contrast and limits.', 'Summarise each paragraph in one line.','A plausible statement may still be unsupported by the passage.')
    topic('para-order','Verbal','Paragraph ordering & coherence','Find the introduction, references, connectors and conclusion.',
          'Pronouns and expressions like this result need an earlier referent.', 'Lock clear sentence pairs before ordering the full paragraph.','A grammatically correct sentence may still be misplaced in the argument.')
    topic('cloze','Verbal','Cloze tests & contextual completion','Choose a word that fits both grammar and the passage’s logical relationship.',
          'Read the full sentence, then surrounding context.', 'Look for contrast, cause or continuation markers.','A common word may be semantically wrong despite fitting grammar.')
    for i,subject in enumerate(['library','bus service','coding club','clinic','sports centre','museum','canteen','study group']):
        passage=f'The {subject} extended its opening hours for a one-month trial. Visits increased during that month. The manager noted that a holiday occurred in the same period and requested more data before attributing the increase to the longer hours.'
        add('reading',passage+'\nWhich conclusion is best supported?','The trial alone does not establish that longer hours caused the increase.','The manager explicitly notes another possible influence and asks for more data. A simultaneous increase is not proof of causation.',['Longer hours definitely caused all of the increase.','The trial proved visits will always increase.','The holiday had no possible effect.'])
        add('para-order',f'Order these sentences about a {subject} survey:\nA: Therefore, the team revised its plan.\nB: The team first collected visitor feedback.\nC: This feedback revealed a need for quieter spaces.','B-C-A','B introduces the feedback; C refers to this feedback; A states the resulting action.',['A-B-C','C-A-B','B-A-C'])
        add('cloze',f'The {subject} received more visitors; ___, its waiting time decreased after the new booking system was introduced.','however','The second clause contrasts higher demand with lower waiting time, so however fits.',['therefore','because','similarly'])
    topic('python-output','Coding','Python output, aliasing & slicing','range(stop) excludes stop; a slice [start:stop] excludes stop; assignment can alias a mutable object.',
          'Trace state line by line, including shared references and loop boundaries.', 'Draw arrows from variable names to list objects.','A=b does not copy a list; b=a[:] creates a shallow copy.')
    topic('complexity','Coding','Complexity & data structures','Count input-dependent operations; binary search halves a sorted search space each step.',
          'State average/worst-case assumptions. Dictionary lookup is expected O(1), not a universal worst-case guarantee.', 'For nested loops multiply counts only when both run their full ranges.','A loop with a doubling counter has logarithmic iteration count.')
    for i in range(12):
        n=3+i
        add('python-output',f'What is printed by this Python code?\ns = 0\nfor i in range({n}):\n    s += i\nprint(s)',n*(n-1)//2,f'range({n}) is 0 through {n-1}. Sum={n}×{n-1}/2={n*(n-1)//2}.')
        add('complexity',f'A sorted array contains n values (n ≥ {10+i}). A search halves the remaining interval at each step. What is the asymptotic worst-case search time?','O(log n)','After k halvings, at most n/2^k candidates remain; reaching one requires k≈log₂n.',['O(n)','O(n²)','O(1)'])


def advanced_and_awareness():
    from itertools import permutations
    topic('probability-advanced','Quant','Conditional probability & sampling','P(A|B)=P(A∩B)/P(B); without-replacement draws use a changing denominator.',
          'Count ordered draws or unordered combinations consistently. State the conditioning event explicitly.', 'Use combinations for an unordered sample.','Do not multiply probabilities as if draws without replacement were independent.')
    topic('replacement','Quant','Repeated mixture replacement','Amount of original solute remaining = initial amount × (1−removedVolume/totalVolume)^k.',
          'After each replacement, assume thorough mixing before the next draw.', 'Track the original component rather than both components.','The fraction removed on later rounds applies to the current mixture, not only to the original solute.')
    topic('constraint-puzzles','Logical','Constraint puzzles & exhaustive reasoning','List feasible assignments, then eliminate those violating any condition.',
          'Record each constraint precisely. A count question may have several feasible arrangements.', 'Place the strongest constraints first.','Do not choose one plausible arrangement and assume it is the only one.')
    topic('data-profit','DataInterpretation','Revenue, cost & multi-step interpretation','Profit=revenue−cost; profit%=profit/cost×100.',
          'Compute revenue as price times quantity for each category; use total cost as the profit-rate denominator.', 'Build separate revenue and cost columns.','A revenue-weighted or quantity-weighted average is not necessarily the same as a simple average.')
    topic('python-state','Coding','Python state tracing & recursion','Aliased lists share mutations; list slicing makes a shallow copy; recursion needs a base case.',
          'Track object identity separately from variable names and trace return values backward.', 'Write the list state after each mutation.','A shallow copy still shares nested mutable elements.')
    for i in range(12):
        red=4+i;blue=6+i;n=red+blue
        ans=F(comb(red,2),comb(n,2))
        add('probability-advanced',f'A bag has {red} red and {blue} blue balls. Two are drawn uniformly without replacement. Find the probability that both are red.',ans,f'Choose 2 red balls in C({red},2)={comb(red,2)} ways out of C({n},2)={comb(n,2)} pairs. Probability={fmt(ans)}.',[F(red*red,n*n),F(red, n),F(red*(red-1),n*n),F(1,n)],difficulty='Hard')
        volume=100;remove=10+5*(i%6);rounds=2+i//6;ans=F(volume)*F(volume-remove,volume)**rounds
        add('replacement',f'A {volume}-litre vessel initially contains pure juice. Remove {remove} litres and replace with water, mix thoroughly, and repeat for {rounds} total removal/replacement rounds. How many litres of original juice remain?',ans,f'Each round keeps {volume-remove}/{volume} of the current original juice. Remaining={volume}×({volume-remove}/{volume})^{rounds}={fmt(ans)} litres.',difficulty='Hard')
        names=['A','B','C','D','E'];gap=1+i%3;limit=4+i%2
        other=1 if i<6 else 2; other_name='B' if other==1 else 'C'
        first=[p for p in permutations(range(1,6)) if p[0]<p[other]]
        second=[p for p in first if abs(p[2]-p[3])==gap]
        valid=[p for p in second if p[4]<=limit]
        add('constraint-puzzles',f'Five people A,B,C,D,E occupy positions 1–5, one person per position. A is left of {other_name}; C and D are exactly {gap} position(s) apart; E is at a position no greater than {limit}. How many arrangements satisfy all conditions? (Use ordinary distance |pos(C)−pos(D)|.)',len(valid),f'Start with 5!=120 distinct position assignments. A<{other_name} leaves {len(first)}. Enforcing |C−D|={gap} leaves {len(second)}. Finally E≤{limit} leaves {len(valid)} valid arrangements. Enumerating with these three tests avoids assuming any unstated adjacency or orientation.',difficulty='Hard')
        q1=15+i;q2=10+i;sp1=80+i;sp2=120+i;cp1=60+i;cp2=90+i
        revenue=q1*sp1+q2*sp2;cost=q1*cp1+q2*cp2;ans=F((revenue-cost)*100,cost)
        add('data-profit',f'A shop sells all its stock at the following unit prices:\nItem | Quantity | Cost price | Selling price\nP | {q1} | {cp1} | {sp1}\nQ | {q2} | {cp2} | {sp2}\nAll prices are in rupees. What is the total profit percentage on total cost?',ans,f'Total revenue={q1}×{sp1}+{q2}×{sp2}={revenue}. Total cost={q1}×{cp1}+{q2}×{cp2}={cost}. Profit={revenue-cost}; profit%={revenue-cost}/{cost}×100={fmt(ans)}%.',difficulty='Hard')
        n=i+2
        add('python-state',f'What is printed by this Python code?\na = [{n}]\nb = a\nc = a[:]\nb.append({n+1})\nprint(len(a), len(c))','2 1','b aliases a, so appending through b changes a. c is a separate shallow list copy made before the append. Thus a has two entries and c has one.',['1 1','2 2','1 2'])
    topic('geography-history','GeneralAwareness','Indian geography & history foundations','Match geographical features and historical events to their defining facts.',
          'Focus on static locations and chronology before adding current affairs from updated official material.', 'Build a timeline and a map rather than memorising isolated names.','Do not infer current political boundaries or appointments from an old reference.')
    items=[
      ('Which Indian state contains the Thar Desert’s largest Indian extent?','Rajasthan',['Kerala','Assam','Bihar'],'The Thar Desert lies mainly in western Rajasthan within India.'),
      ('Which river flows through the city of Varanasi?','Ganga',['Narmada','Tapi','Krishna'],'Varanasi is on the banks of the Ganga.'),
      ('Which range runs along much of India’s western coast?','Western Ghats',['Aravalli only','Himalaya','Vindhya only'],'The Western Ghats extend parallel to much of the western coast.'),
      ('Which movement began with the Dandi March in 1930?','Civil Disobedience Movement',['Quit India Movement','Non-Cooperation Movement','Swadeshi Movement of 1905'],'The Salt March initiated the 1930 Civil Disobedience campaign.'),
      ('In which year did the Quit India Movement begin?','1942',['1930','1919','1947'],'The Quit India resolution and movement date to August 1942.'),
      ('Which civilisation is associated with Harappa and Mohenjo-daro?','Indus Valley Civilisation',['Maya civilisation','Roman civilisation','Mesopotamian civilisation only'],'These are major urban sites of the Indus Valley Civilisation.'),
      ('Which latitude is the Tropic of Cancer approximately?','23.5° N',['23.5° S','66.5° N','0°'],'The Tropic of Cancer is near 23.5 degrees north.'),
      ('Which is a major west-flowing peninsular Indian river?','Narmada',['Godavari','Krishna','Mahanadi'],'The Narmada flows westward into the Arabian Sea.'),
      ('Who chaired the Drafting Committee of the Indian Constitution?','B. R. Ambedkar',['Mahatma Gandhi','Subhas Chandra Bose','Bhagat Singh'],'B. R. Ambedkar chaired the Constitution’s Drafting Committee.'),
      ('On which date did the Constitution of India come into force?','26 January 1950',['15 August 1947','26 November 1949','2 October 1950'],'It was adopted on 26 November 1949 and came into force on 26 January 1950.'),
      ('Which soil is particularly associated with cotton cultivation in the Deccan?','Black soil',['Laterite only','Desert sand','Peaty soil only'],'Black or regur soil retains moisture and is associated with cotton-growing regions.'),
      ('Which ocean lies south of India?','Indian Ocean',['Arctic Ocean','Southern Ocean directly at India','Atlantic Ocean'],'The Indian peninsula projects into the Indian Ocean.')]
    for q,a,d,e in items:add('geography-history',q,a,e,d)
    more=[
      ('Which particle carries a negative electric charge?','Electron',['Proton','Neutron','Photon'],'An electron has negative elementary charge.'),
      ('What is the SI unit of force?','newton',['joule','pascal','watt'],'One newton accelerates one kilogram at one metre per second squared.'),
      ('What is the chemical formula of common table salt?','NaCl',['H₂O','CO₂','CaCO₃'],'Table salt is sodium chloride, NaCl.'),
      ('Which blood component primarily helps clotting?','Platelets',['Red cells only','Plasma water only','Haemoglobin only'],'Platelets contribute to clot formation at damaged vessels.'),
      ('A substance with pH below 7 in ordinary aqueous conditions is generally what?','Acidic',['Neutral','Basic','Always insoluble'],'On the usual aqueous pH scale, values below 7 indicate acidity.'),
      ('Which vitamin is synthesised in skin following suitable sunlight exposure?','Vitamin D',['Vitamin C','Vitamin B12','Vitamin K only'],'UVB exposure enables synthesis of vitamin D in the skin.'),
      ('Which process converts liquid water into vapour at its surface?','Evaporation',['Condensation','Freezing','Sublimation from ice only'],'Evaporation is the liquid-to-gas transition at a surface.'),
      ('Which is a renewable energy source?','Solar energy',['Coal','Petroleum','Natural gas'],'Solar input is continually replenished, unlike fossil fuel reserves.'),
      ('What is the SI unit of power?','watt',['joule','metre','coulomb'],'A watt is one joule of energy transferred per second.'),
      ('Which organelle is a major site of aerobic ATP production in human cells?','Mitochondrion',['Ribosome','Lysosome only','Cell wall'],'Mitochondria host key stages of aerobic respiration and oxidative phosphorylation.')]
    for q,a,d,e in more:add('science',q,a,e,d)


SOURCES = [
 dict(id='coverage',title='IndiaBIX — aptitude topic index',url='https://www.indiabix.com/aptitude/',note='Topic coverage reference; question text in the new bank is original.'),
 dict(id='careerride',title='CareerRide — placement preparation',url='https://www.careerride.com/placement-papers.aspx',note='Cross-check for placement subject coverage.'),
 dict(id='gfg',title='GeeksforGeeks — aptitude overview',url='https://www.geeksforgeeks.org/aptitude/aptitude-questions-and-answers/',note='Cross-check for quantitative, reasoning and verbal topic families.'),
 dict(id='tcs',title='TCS — All India NQT hiring pattern',url='https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring',note='Official Foundation 75 min and Advanced 115 min structure. Practice MCQ counts here are chosen by CodeLab.'),
 dict(id='infosys',title='Infosys — HackWithInfy 2026 sample',url='https://www.infosys.com/careers/hackwithinfy/2026/sample-questions_hwi.pdf',note='Official coding preparation reference; our questions and staged mock timings are independent practice choices.'),
 dict(id='rrb',title='RRB — CEN 05/2024 NTPC graduate notice',url='https://www.rrbcdg.gov.in/uploads/2024/05-NTPCG/Detailed%20CEN%2005-2024%20NTPC.pdf',note='Named notice: CBT-1 indicative 30 maths, 30 reasoning, 40 awareness; 90 min; −1/3 per wrong answer. Not a claim about future notices.'),
 dict(id='gate',title='GATE 2026 — official pattern',url='https://gate2026.iitg.ac.in/question-paper-pattern.html',note='General aptitude is 15 marks; our GA drills are not a full GATE paper and use single-choice practice items.'),
 dict(id='algorithms',title='TheAlgorithms/Python — MIT references',url='https://github.com/TheAlgorithms/Python',note='12 licensed source modules bundled with pinned commit and attribution.'),
 dict(id='js-algorithms',title='JavaScript algorithms — topic reference',url='https://github.com/trekhleb/javascript-algorithms',note='Algorithm and data-structure coverage reference; new judged tasks are original.'),
 dict(id='mit-algorithms',title='MIT OpenCourseWare — Introduction to Algorithms',url='https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-notes/',note='Data structures, heaps, graphs and DP coverage reference. Added coding statements, cases and implementations are authored independently for CodeLab.'),
]


if __name__ == '__main__':
    from quality_questions import extend
    from audit_legacy import review_bank,review_aptitude
    numeric_topics(); reasoning(); interpretation(); verbal_and_technical(); advanced_and_awareness()
    extend(topic,add)
    from variety_questions import extend as extend_variety
    extend_variety(topic,add,QUESTIONS)
    original_count=len(QUESTIONS)
    legacy,audit=review_bank(TOPICS)
    QUESTIONS.extend(legacy)
    aptitude,aptitude_audit=review_aptitude(TOPICS)
    existing={q['q'] for q in QUESTIONS}
    QUESTIONS.extend(q for q in aptitude if q['q'] not in existing)
    assert len({q['q'] for q in QUESTIONS}) == len(QUESTIONS), 'Duplicate prompts'
    assert all(len(set(q['options'])) == 4 and 0 <= q['answer'] < 4 and q['explanation'] for q in QUESTIONS)
    for t in TOPICS:
        t['example'] = next(q for q in QUESTIONS if q['topic'] == t['id'])
    for q in QUESTIONS:
        q['examTags']=['awareness' if q['topic'] in ('science','civics','geography-history') else 'technical'] if q['section']=='GeneralAwareness' else [q['section'].lower()]
    SOURCES.extend([
      dict(id='postgres',title='PostgreSQL — TRUNCATE and transactional behaviour',url='https://www.postgresql.org/docs/current/sql-truncate.html',note='Primary reference for the corrected DELETE/TRUNCATE comparison; behaviour must not be generalised to every database.'),
      dict(id='js-this',title='MDN — JavaScript this',url='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this',note='Primary reference for receiver-based method invocation and the corrected this question.'),
      dict(id='mongo-insert',title='MongoDB — insertOne',url='https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/',note='Primary reference for the explicit single-document insertion method.')])
    data = dict(topics=TOPICS, questions=QUESTIONS, sources=SOURCES, researched='2026-10-17',
                counts=dict(original=original_count,reviewedLegacy=len(legacy),correctedLegacy=audit['changed'],reviewedSectional=len(aptitude),uniqueSectional=sum(q['q'] not in {r['q'] for r in legacy} for q in aptitude)),
                aptitudeReviewed=aptitude,aptitudeAudit=aptitude_audit,auditChanges=audit['changes'],
                roadmaps=json.loads((ROOT/'data/roadmaps.json').read_text(encoding='utf-8')))
    (ROOT/'assets/practice-data.js').write_text('window.CODELAB_PRACTICE='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    print(f'Built {len(QUESTIONS)} explained questions across {len(TOPICS)} topics ({original_count} original; 344 classic/sectional inputs reviewed).')
