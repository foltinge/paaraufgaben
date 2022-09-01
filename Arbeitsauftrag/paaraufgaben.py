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

# Im folgenden wird Old-School- Formatierung mit % verwendet, da dies
# am besten verträglich mit LaTeX ist

with open("_schueler.tex",mode="w") as f:
    for k in range(anzahl):
        print(r"""\begin{center}\large %s, Name: \emph{%s}\end{center}
%s\\""" % (ueberschrift,namen[k],auftrag),file=f)
        for i,j in paare:
            if i==k:
                print(r"\vfill Mit \emph{%s}:"%namen[j],file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                ri=aufgri[(i,j)]
                if ri:
                    print(r"""\begin{center}\underline{\hspace{\widthof{%s}*\real{2}}}
%s%s\end{center}"""%(aa[0],trenner,aa[1]),file=f)
                else:
                    print(r"""\begin{center}%s%s
\underline{\hspace{\widthof{%s}*\real{2}}}\end{center}"""%(aa[0],trenner,aa[1]),file=f)
            if j==k:
                print(r"\vfill Mit \emph{%s}:"%namen[i],file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                ri=aufgri[(i,j)]
                if not ri:
                    print(r"""\begin{center}\underline{\hspace{\widthof{%s}*\real{2}}}
%s%s\end{center}"""%(aa[0],trenner,aa[1]),file=f)
                else:
                    print(r"""\begin{center}%s%s\underline{\hspace{\widthof{%s}*\real{2}}}
\end{center}"""%(aa[0],trenner,aa[1]),file=f)
        if k<anzahl-1:
            print(r"\newpage",file=f)

with open("_kontrolle.tex",mode="w") as f:
#Aufgaben drucken
#     for aa in aufgaben:
#         print("{0}{3}{1} Ergebnis:  {2}\\\\[1ex]".format(aa[0],aa[1],aa[2],trenner),file=f)
#         
        

    for k in range(anzahl):
        print(r"\begin{minipage}{\textwidth}",file=f)
        print(r"\textbf{Ergebnisse von %s:}\\"%namen[k],file=f)
        for i,j in paare:
            aa=aufgaben[aufgnr[(i,j)]]
            if i==k:
                print(r"""mit %s: %s%s%s => Ergebnis: %s
\\"""%(namen[j],aa[0],trenner,aa[1],aa[2]),file=f)
            if j==k:
                print(r"""mit %s: %s%s%s => Ergebnis: %s
\\"""%(namen[i],aa[0],trenner,aa[1],aa[2]),file=f)
        print(r"\end{minipage}",file=f)
        if k<anzahl-1:
            print(r"\vspace*{3ex}",file=f)
            print("",file=f)



