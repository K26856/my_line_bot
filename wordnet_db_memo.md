## sql
```sql
select distinct s1.name, s2.name, sl.link, s1.synset, s2.synset, sd1.def, sd2.def
from synlink sl, synset s1, synset s2, synset_def sd1, synset_def sd2
where sl.synset1="13987423-n" and
      sl.synset1=s1.synset and
      sl.synset2=s2.synset and
      sl.synset1=sd1.synset and
      sd1.lang="jpn" and
      sl.synset2=sd2.synset and
      sd2.lang="jpn"
      ;
```

```sql
select distinct w.lemma, s1.name, s2.name, sl.link, s1.synset, s2.synset, sd1.def, sd2.def
from word w, sense s, synlink sl, synset s1, synset s2, synset_def sd1, synset_def sd2
where w.lemma="チョコ" and
      w.wordid=s.wordid and
      s.synset=sl.synset1 and
      sl.synset1=s1.synset and
      sl.synset2=s2.synset and
      sl.synset1=sd1.synset and
      sd1.lang="jpn" and
      sl.synset2=sd2.synset and
      sd2.lang="jpn"
      ;
```
      

```sql
select distinct a.hops, s1.name, s2.name, x.lemma 
from ancestor a, 
    (select s.synset, w.wordid, w.lemma 
     from sense s, word w 
     where s.wordid = w.wordid and w.lemma="楽しい"
    ) x, 
    synset s1, 
    synset s2 
where 
    a.synset1=x.synset and 
    a.synset1=s1.synset and 
    a.synset2=s2.synset
order by a.hops;
```

## memo
- variant
    - empty?
- ancestor
    - schema
        - synset1
            - progeny?
        - synset2
            - ancestor?
        - hops
            - 1   : nearest ancestor?
            - max : farthest ancestor?
- sense
     - synset
     - wordid
     - lang
     - rank
     - lexid
     - freq
     - src
- synset
     - synset
     - pos
     - name
     - src
- synset_ex
     - synset
     - lang
     - def
     - sid
- synset_def
    - synset
        - id
    - lang
    - def
    - sid
        - ?
- word
    - wordid
    - lang
    - lemma
    - pron
    - pos
- pos_def
    - abstruct
        - part of speech
        - japanese "品詞"
    - schema
- synlink
    - synset1
    - synset2
    - link
    - src
- xlink
- link_def



## ref
Japanese Wordnet (vXX) © 2009-2011 NICT, 2012-2015 Francis Bond and 2016-2017 Francis Bond, Takayuki Kuribayashi
linked to http://compling.hss.ntu.edu.sg/wnja/index.en.html

## data
```
sqlite> select * from ancestor limit 5;
synset1|synset2|hops
11820323-n|11573660-n|1
11820323-n|11567411-n|2
11820323-n|08108972-n|3
11820323-n|07992450-n|4
11820323-n|07941170-n|5

sqlite> select * from pos_def limit 5;
pos|lang|def
a|eng|adjective
r|eng|adverb
n|eng|noun
v|eng|verb
a|jpn|形容詞

sqlite> select * from synlink limit 5;
synset1|synset2|link|src
07125096-n|07128527-n|hype|eng30
07126228-n|07109847-n|hype|eng30
14123044-n|14122235-n|hype|eng30
14123044-n|14123259-n|hypo|eng30
08030185-n|08197895-n|inst|eng30

sqlite> select * from synset_def limit 5;
synset|lang|def|sid
07125096-n|eng|profane or obscene expression usually of surprise or anger; "expletives were deleted"|0
07126228-n|eng|a word or phrase conveying no independent meaning but added to fill out a sentence or metrical line|0
14123044-n|eng|an acute and highly contagious viral disease marked by distinct red spots followed by a rash; occurs primarily in children|0
08030185-n|eng|a Nicaraguan counterrevolutionary guerrilla force from 1979 to 1990; it opposed a left-wing government, with support from the United States|0
09902017-n|eng|a man who raises (or tends) cattle|0

sqlite> select * from variant limit 5;

sqlite> select * from xlink limit 5;
synset|resource|xref|misc|confidence
00001740-a|sumo|capability|=|
00002098-a|sumo|capability|⊂|
00002312-a|sumo|PositionalAttribute|⊂|
00002527-a|sumo|PositionalAttribute|⊂|
00002956-a|sumo|BiologicalAttribute|⊂|

sqlite> select * from link_def limit 5;
link|lang|def
also|eng|See also
syns|eng|Synonyms
hype|eng|Hypernyms
inst|eng|Instances
hypo|eng|Hyponym

sqlite> select * from sense limit 5;
synset|wordid|lang|rank|lexid|freq|src
07125096-n|1|eng|0|1|1|eng-30
07126228-n|1|eng|0|2|0|eng-30
14123044-n|2|eng|0|1|0|eng-30
08030185-n|3|eng|0|1|0|eng-30
09902017-n|4|eng|0|1|1|eng-30

sqlite> select * from synset limit 5;
synset|pos|name|src
07125096-n|n|expletive|eng30
07126228-n|n|expletive|eng30
14123044-n|n|measles|eng30
08030185-n|n|contras|eng30
09902017-n|n|beef_man|eng30

sqlite> select * from synset_ex limit 5;
synset|lang|def|sid
01785341-a|eng|grim determination|0
01785341-a|jpn|断固たる決心|0
01785341-a|eng|grim necessity|1
01785341-a|jpn|厳しい必要性|1
01785341-a|eng|Russia's final hour, it seemed, approached with inexorable certainty|2

sqlite> select * from word limit 5;
wordid|lang|lemma|pron|pos
1|eng|expletive||n
2|eng|measles||n
3|eng|contras||n
4|eng|beef_man||n
5|eng|dwelling||n
```
