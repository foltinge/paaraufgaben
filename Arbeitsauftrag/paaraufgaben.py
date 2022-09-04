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

n=2 # Anzahl der von jedem SuS ausgehenden (und eingehenden) Pfeile. Die Anzahl
# der Nachbarn ist 2*n (hier 4)
# Das folgende Programm erzeugt einen gerichteten Graphen, bei dem von jedem SuS
# n Pfeile ausgehen bzw. eintreffen


while True:
    np=n*anzahl # Anzahl der Paare, die erzeugt werden müssen

    paare=[]

    rein=[0]*anzahl # Anzahl der eintreffenden Pfeile
    raus=[0]*anzahl # Anzahl der ausgehenden Pfeile
    # Am Ende muss gelten rein[i]=raus[i]=n
    v=0
    while v<10000:
        while True:
            i=random.randrange(anzahl)
            j=random.randrange(anzahl)
            if i!=j:
                break
        # (i,j) ist ein Pfeil von i nach j
        if raus[i]<n and rein[j]<n and (i,j) not in paare and (j,i) not in paare: # Weder (i,j) noch (j,i) darf es schon geben
            raus[i]+=1
            rein[j]+=1 # Die Anzahlen rein[], raus[] werden aktualisiert
            paare.append((i,j))
            v=0
            np-=1
            if np==0:
                break
        v+=1
    else:
        continue # die maximale Iterationszahl wurde erreicht, d.h. keine Lösung
    break # Lösung gefunden

# print(paare)

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


# Aufgaben drucken, zuerst schueler.tex, dann kontrolle.tex

#print(paare)
#print(aufgnr)

# Im folgenden wird Old-School- Formatierung mit % verwendet, da dies
# am besten verträglich mit LaTeX ist

with open("_schueler.tex",mode="w") as f:
    for k in range(anzahl):
        print(r"""\begin{center}\large %s, Name: \emph{%s}\end{center}
%s\\""" % (ueberschrift,namen[k],auftrag),file=f)
        for i,j in paare: #Wenn der SuS links steht, linke Seite der Aufgabe
            if i==k:
                print(r"\vfill Mit \emph{%s}:"%namen[j],file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                print(r"""\begin{center}%s%s\underline{\hspace{\widthof{%s}*\real{2}}}
\end{center}"""%(aa[0],trenner,aa[1]),file=f)

            if j==k: #Wenn der SuS rechts steht, rechte Seite der Aufgabe
                print(r"\vfill Mit \emph{%s}:"%namen[i],file=f)
                aa=aufgaben[aufgnr[(i,j)]]
                print(r"""\begin{center}\underline{\hspace{\widthof{%s}*\real{2}}}
%s%s\end{center}"""%(aa[0],trenner,aa[1]),file=f)
               
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



