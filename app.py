import random
chaine="azertyxrtcuyiu12587902vyuQDEPMLIOYRZAVGFS"  
taille=10
matricule=""
while len(matricule)<taille:
    if len(matricule)==5:
        matricule=matricule+"-"
        # print(matricule)
    else:
        matricule=matricule+random.choice(chaine)
        print(matricule)

# print(matricule)        