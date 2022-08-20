import random


# Namen, die mit * anfangen, werden nicht eingelesen:
namen=[]
with open("namen.txt",mode="r") as f:
    for nn in f:
        nnn=nn.strip()
        if nnn[0]!="*":
            namen.append(nnn)
        
anzahl=len(namen)

# print(anzahl)

n=4 # Anzahl der Leute, die mit einer Person gepaart werden

# Das folgende Programm erzeugt einen d-regulären Graphen,
# jeder Punkt ist mit n anderen Punkten verbunden.
# n*anzahl muss gerade sein.
# Quelle: https://de.wikipedia.org/wiki/Regulärer_Graph
# https://networkx.github.io/documentation/stable/reference/generated/networkx.generators.random_graphs.random_regular_graph.html
# gesucht wird eine symmetrische Matrix m(i,j)=m(j,i) nur mit 0 und 1, 0<=i,j<=anzahl-1
# deren Zeilensummen (und damit Spaltensummen) = n sind.



while True:
    np=n*anzahl//2 # Anzahl der Paare, die erzeugt werden müssen

    paare=[]

    s=[0]*anzahl # Zeilensummen, die alle <= n sein müssen
    v=0
    while v<10000:
        while True:
            i=random.randrange(anzahl)
            j=random.randrange(anzahl)
            if i!=j:
                break
        if i>j:
            i,j=j,i # sortiert
        if s[i]<n and s[j]<n and (i,j) not in paare:
            s[i]+=1
            s[j]+=1 # wegen der Symmetrie der Matrix
            paare.append((i,j))
            v=0
            np-=1
            if np==0:
                break
        v+=1
    else:
        continue # die maximale Iterationszahl wurde erreicht, d.h. keine Lösung
    break # Lösung gefunden

#print(paare)

#Einlesen von aufgaben.tex: Erste Zeile: Überschrift, danach: Arbeitsauftrag,
# dann Liste mit:
#linke Seite&rechte Seite&Ergebnis

#es wird eine Datei _schueler.tex und eine _kontrolle.tex erzeugt.
aufgaben=[]
with open("aufgaben.tex",mode="r") as f:
    ueberschrift=f.readline()
    auftrag=f.readline()
    trenner=(f.readline()).strip()
    for aa in f:
        aaa=aa.strip()
        aufgaben.append(aaa.split("&"))


anzaufg=len(aufgaben) # Anzahl der Aufgaben, bei 7 oder mehr Aufgaben ist man auf der
# sicheren Seite


# Aufgaben zuordnen:
aufgnr=dict() # einem Paar (i,j) zugeordnete Aufgabennummer
aufgri=dict() # einem Paar (i,j) zugeordnete boolsche Variable (linker oder rechter Teil)

for k,l in paare:
    # Alle Aufgaben, die schon zu k und l benachbart sind, werden gesammelt
    nachbarn=set()
    for i,j in paare:
        if k==i or k==j or l==i or l==j: # i,j ist Nachbar von k,l
            if (i,j) in aufgnr:
                nachbarn.add(aufgnr[(i,j)])
    if len(nachbarn)>=anzaufg:
        raise ValueError("Zu wenige Aufgaben!")
        # Jetzt muss eine Aufgabe gewählt werden, die nicht in nachbarn vorkommt
        # da an k,l maximal 2*3=6 Aufgaben hängen, findet sich eine, wenn es
        # mind. 7 Aufgaben gibt.
    while True:
        a=random.randrange(anzaufg)
        if a not in nachbarn:
            break
    aufgnr[(k,l)]=a
    aufgri[(k,l)]=random.random()>0.5

# Aufgaben drucken, zuerst schueler.tex, dann kontrolle.tex

#print(paare)
#print(aufgnr)


with open("_schueler.tex",mode="w") as f:
    for k in range(anzahl):
        print("""\\begin{{center}}\\large {0},
        Name: \\emph{{{1}}}
        \\end{{center}}{2}\\\\""".format(ueberschrift,namen[k],auftrag),file=f)
        for i,j in paare:
            if i==k:
                print("\\vfill Mit \\emph{{{0}}}:".format(namen[j]),file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                ri=aufgri[(i,j)]
                if ri:
                    print("""\\begin{{center}}\\underline{{\\phantom{{{0}}}\\phantom{{{0}}}}}
                    {2}{1}\\end{{center}}""".format(aa[0],aa[1],trenner),file=f)
                else:
                    print("""\\begin{{center}}{0}{2}
                    \\underline{{\\phantom{{{1}}}\\phantom{{{1}}}}}
                    \\end{{center}}""".format(aa[0],aa[1],trenner),file=f)
            if j==k:
                print("\\vfill Mit \\emph{{{0}}}:".format(namen[i]),file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                ri=aufgri[(i,j)]
                if not ri:
                    print("""\\begin{{center}}\\underline{{\\phantom{{{0}}}\\phantom{{{0}}}}}
                    {2}{1}\\end{{center}}""".format(aa[0],aa[1],trenner),file=f)
                else:
                    print("""\\begin{{center}}{0}{2}
                    \\underline{{\\phantom{{{1}}}\\phantom{{{1}}}}}
                    \\end{{center}}""".format(aa[0],aa[1],trenner),file=f)
        if k<anzahl-1:
            print("\\newpage",file=f)

with open("_kontrolle.tex",mode="w") as f:
#Aufgaben drucken
#     for aa in aufgaben:
#         print("{0}{3}{1} Ergebnis:  {2}\\\\[1ex]".format(aa[0],aa[1],aa[2],trenner),file=f)
#         
        

    for k in range(anzahl):
        print("\\textbf{{Ergebnisse von {0}:}}\\\\".format(namen[k]),file=f)
        for i,j in paare:
            aa=aufgaben[aufgnr[(i,j)]]
            if i==k:
                print("""mit {0}: {1}{4}{2} => Ergebnis:  {3}
                \\\\""".format(namen[j],aa[0],aa[1],aa[2],trenner),file=f)
            if j==k:
                print("""mit {0}: {1}{4}{2} => Ergebnis:  {3}
                \\\\""".format(namen[i],aa[0],aa[1],aa[2],trenner),file=f)
        if k<anzahl-1:
            print("\\vspace*{1ex}",file=f)
            print("",file=f)



