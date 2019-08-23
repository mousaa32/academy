from flask import Flask,render_template,request,redirect,url_for,flash,session,escape
import psycopg2 as psy
import datetime


def connexiondb():
        try:
                con = psy.connect(
                        host="ec2-54-235-92-244.compute-1.amazonaws.com",
                        database="dafou8j1079e8s",
                        user="pgzjuspcpktsxz",
                        password="d955645e2c878bca231ea21bf354e795978142c4eb8165922da9011c059ff1f3",
                        port=5432
                        )
                return con
        except(Exception) as error:
                print("probleme connection",error)

con = connexiondb()
cur = con.cursor()


app = Flask(__name__)
app.secret_key="flash message"
#connect to the database


 ############################################################# login ########################################################

@app.route('/')
def login():

    return  render_template('login.html')
                                                    ####################### connection #####################


@app.route('/',methods= ['GET','POST'])
def registre():
    if 'email' in session:
        redirect(url_for('listuser'))

    if request.method == "POST":
        session['psdw']=request.form['password']
        session['email']=request.form['email'].lower()
        cur.execute("SELECT email,password FROM utilisateur where email='" + session['email'] + "'and password='" + session['psdw'] + "' and etat ='actif' ")
        data =cur.fetchall()
        con.commit()
        for row in data:
            if data == None:
                flash("mot de passe ou nom d'utilisateur incorect")
                return  redirect(url_for('login'))
            elif row[0] == 'sarr@gmail.com' and row[1]== '1957':
                    session['email']=request.form['email']
                    return redirect(url_for('listuser'))
            else :
                # flash(" connection reussi")
                session['email']=request.form['email']
                return redirect(url_for('accueil'))

    flash("mot de passe ou nom d'utilisateur incorect")
    return  redirect(url_for('login'))

                                ####################### logout#####################


@app.route('/logout')
def logout():
    if 'email' in session:
        # session.clear()
        session.pop('email','psdw')
        return  redirect(url_for('login'))
    session.pop('email','psdw')
    return  redirect(url_for('login'))
         ############################################################# super user  ########################################################
                                #######################   liste user#####################

@app.route('/listuser')
def listuser():
    if 'email' in session:
        cur.execute("select * from  utilisateur where id_user != 1 and etat='actif' ")
        data =cur.fetchall()
        cur.close
        email_session=escape(session['email']).capitalize()
        return  render_template('admin.html',utilisateur=data,a=email_session)

    return redirect(url_for('login'))


                                ####################### add user #####################

@app.route('/insertuser',methods= ['POST'])
def insertuser():
    if 'email' in session:
        cur.execute("""select email,password FROM utilisateur  """)
        user_ver =cur.fetchall()
        con.commit()

        if request.method == "POST":
            # id_user=request.form['id_user']
            prenom=request.form['prenom'].lower()
            nom=request.form['nom'].lower()
            email=request.form['email'].lower()
            password=request.form['password']
            etat=request.form['etat'].lower()
            image=request.form['image']

            ####pour verifier  si l'email ou le numero telephone  de l'utilisateur existe deja
            control_promo=False
            for row in user_ver:
                if row[0].lower() == email.lower() or row[1].lower()  == password.lower():
                    control_promo =True
                    break

            if control_promo == True  :
                flash("utilisateur existe deja ")
                return redirect(url_for('listuser',l=user_ver))
            else:
                flash("utilisateur  ajoute avec succé ")
                cur.execute(""" INSERT INTO  utilisateur (prenom,nom,email,password,etat,imagebyte) VALUES(%s,%s,%s,%s,%s,%s)""",
                (prenom,nom,email,password,etat,image))
                con.commit()
                return redirect(url_for('listuser',l=user_ver))

            return redirect(url_for('listuser',l=user_ver))
    return redirect(url_for('login'))

                                #######################  delete user #####################


@app.route('/deleteuser/<string:id_data>',methods=['POST','GET'])
def deleteuser(id_data):
    if 'email' in session:
        cur.execute("DELETE FROM  utilisateur WHERE id_user =%s" ,(id_data,))
        con.commit()
        return redirect(url_for('listuser'))
    return redirect(url_for('login'))

                                #######################  annuler user #####################

@app.route('/anuleruser/<string:id_data>',methods=['POST','GET'])
def anuleruser(id_data):
    if 'email' in session:
        cur.execute("""UPDATE utilisateur SET etat='annulé' WHERE id_user =%s""",(id_data,))
        con.commit()
        return redirect(url_for('listuser'))
    return redirect(url_for('login'))

  ####################### liste  user annuler #####################

@app.route('/annuler/listannuler',methods= ['GET','POST'])
def  listuserannulr():
    if 'email' in session:
        cur.execute("""select *
        FROM utilisateur WHERE etat='annulé' """)
        datappnul =cur.fetchall()
        con.commit()
        return  render_template('lisanuser.html',annuler=datappnul)
    return redirect(url_for('login'))


####################### desactiver l'annulation du user  #####################

@app.route('/réactiver/<string:id_data>',methods=['POST','GET'])
def  réactiver(id_data):
    if 'email' in session:
        cur.execute("""UPDATE utilisateur SET etat='actif' WHERE id_user =%s""",(id_data,))
        con.commit()
        return redirect(url_for('listuser'))
    return redirect(url_for('login'))

   ######   ####################################################### page d'accueil  ########################################################
@app.route('/accueil')
def accueil():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        return  render_template('milieuimg.html',email_admin=email_session)
    return redirect(url_for('login'))

 ############################################################# scolarite  ########################################################


                                ####################### inscription #####################
@app.route('/inscription',methods= ['POST','GET'])
def inscription():
        if 'email' in session:
            email_session=escape(session['email']).capitalize()
        #on peut ajouter  une inscription que si le date debut n'est encore venu
            cur.execute("""select * from  promo""")
            data =cur.fetchall()
            con.commit()

            cur.execute("""select  apprenants.email,apprenants.numero_tel FROM apprenants  """)
            app_ver =cur.fetchall()
            con.commit()

            if request.method == "POST":
                # matricule=request.form['matricule']
                prenom=request.form['prenom'].strip()
                nom=request.form['nom'].strip()
                email=request.form['email'].lower()
                statut=request.form['statut']
                dateNaissance=request.form['date']
                telephone=request.form['numero']
                id_promo=int(request.form['promo'])
                

                #verification matricule
                cur.execute("""select MAX(id_app) from apprenants""")
                resultat=cur.fetchall()
                con.cursor()

                for mat in resultat :
                    i =mat[0]
                date_actu=datetime.datetime.today().strftime("%d-%m-%Y-")

                if i == None:
                    m = 1
                    matricule="SA-"+str(date_actu)+str(m)
                else :
                    m = i+1
                    matricule = "SA-"+str(date_actu)+str(m)

                ####pour verifier  si l'email ou le numero telephone  de l'apprenant existe deja
                control_promo=False
                for row in app_ver:
                    if row[0].lower() == email.lower() or row[1] == telephone:
                        control_promo =True
                        break

                if control_promo == True  :
                    flash("apprenant existe deja ")
                    return  render_template('inscription.html',pro=data,l=app_ver)

                else:
                    cur.execute(""" INSERT INTO apprenants(matricule,prenom,nom,email,statut,datnais,numero_tel,id_promo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (matricule,prenom,nom,email,statut,dateNaissance,telephone,id_promo))
                    con .commit()

                    flash("apprenant ajouté avec succé")
                    return  render_template('inscription.html',pro=data,l=app_ver)
            return  render_template('inscription.html',pro=data,l=app_ver,email_admin=email_session)
        return redirect(url_for('login'))


                                 #######################  modifier inscription ####################
@app.route('/modifier',methods= ['GET','POST'])
def modifier():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()

        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
        FROM apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='inscrit' """)
        datapp =cur.fetchall()
        con.commit()

        cur.execute("select * from promo")
        datapro=cur.fetchall()
        con.commit()

        if request.method == "POST":
                details = request.form
                id_data = details['id_app']
                matricule = details['matricule']
                prenom = details['prenom']
                nom = details['nom']
                email = details['email'].lower()
                telephone = details['numero']
                statut=details['statut']
                dateNaissance=details['datnais']
                id_promo=int(details['id_promo'])


                cur.execute("""UPDATE apprenants SET matricule=%s,prenom=%s ,nom=%s ,email=%s ,statut=%s,datnais=%s,numero_tel=%s,id_promo=%s WHERE id_app=%s""",
                (matricule,prenom,nom,email,statut,dateNaissance,telephone,id_promo,id_data))

                con.commit()


                cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
                apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
                from apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='inscrit' """)
                datapp2 =cur.fetchall()
                con.commit()

                flash("donnees modifiees")
                return  render_template('modifier.html', apprenants=datapp2,promo=datapro)
        return  render_template('modifier.html', apprenants=datapp,promo=datapro,email_admin=email_session)
    return redirect(url_for('login'))

                                ####################### page anuulée avec liste des inscrits #####################
@app.route('/annuler',methods= ['POST','GET'])
def  listinscritannul():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        # flash("données supprimeés")
        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
                apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
                from apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='inscrit' """)
        datapp2 =cur.fetchall()
        con.commit()

        con.commit()


        return  render_template('annuler.html',annuler=datapp2,email_admin=email_session)
    return redirect(url_for('login'))

                        ########################## action anuulé #########################

@app.route('/annuler/<string:id_data>',methods= ['POST','GET'])
def  annuler(id_data):

        # flash("données supprimeés")
        cur.execute("""UPDATE apprenants SET statut='annulé' WHERE id_app =%s""",(id_data,))

        con.commit()

        # return  render_template('annuler.html')
        return redirect(url_for('listinscritannul'))

                                ####################### liste des anuulés #####################
@app.route('/annuler/listannuler1',methods= ['GET','POST'])
def  listannduler():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
        FROM apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='annulé' """)
        datappnul =cur.fetchall()
        con.commit()

        return  render_template('listeanuler.html',annuler=datappnul,email_admin=email_session)
    return redirect(url_for('login'))
                                ####################### page liste des inscrits avec action suspendre  #####################

@app.route('/suspendre',methods= ['GET','POST'])
def listinscritsuspendre():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
        FROM apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='inscrit' """)
        datappnul =cur.fetchall()
        con.commit()

        return render_template('suspendre.html',suspendre=datappnul,email_admin=email_session)
    return redirect(url_for('login'))

                         ########################## action suspendre #########################
@app.route('/suspendre/<string:id_data>',methods= ['POST','GET'])
def suspendre(id_data):
    cur.execute("""UPDATE apprenants SET statut='suspendre' WHERE id_app=%s""",(id_data,))
    con.commit()

    return redirect(url_for('listinscritsuspendre'))


                              ####################### liste des suspendus #####################
@app.route('/suspendre/listsuspendus',methods= ['GET','POST'])
def  listaduler():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
        FROM apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='suspendre' """)
        datappnul =cur.fetchall()
        con.commit()

        return  render_template('listesuspendre.html',suspendre=datappnul,email_admin=email_session)
    return redirect(url_for('login'))


                            ####################### réinscription #####################
@app.route('/suspendre/listsuspendus/réinscrire',methods= ['GET','POST'])
def reinscrire():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()

        cur.execute("select * from promo")
        datapromo=cur.fetchall()
        print(datapromo)

        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
        FROM apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='suspendre' """)
        datappnul =cur.fetchall()
        # print(datappnul)
        # con.commit()
        # cur.close()

        if request.method == "POST":
            details = request.form
            id_data = details['id_app']
            matricule = details['matricule']
            prenom = details['prenom']
            nom = details['nom']
            email = details['email']
            statut=details['statut']
            dateNaissance=details['datnais']
            telephone = details['numero']
            id_promo=int(details['idpromo'])


            cur.execute("""UPDATE apprenants SET matricule=%s,prenom=%s ,nom=%s ,email=%s ,statut=%s,datnais=%s,numero_tel=%s,id_promo=%s WHERE id_app=%s""",
            (matricule,prenom,nom,email,statut,dateNaissance,telephone,id_promo,id_data))
            con.commit()

            cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
            apprenants.statut,apprenants.datnais,apprenants.numero_tel,promo.nom_promo
            from apprenants ,promo WHERE promo.id_promo=apprenants.id_promo and apprenants.statut='suspendre' """)
            datapp2 =cur.fetchall()
            con.commit()

            flash("réinscription réussie")
            return  render_template('listesuspendre.html',suspendre=datapp2,promo=datapromo)
        return  render_template('listesuspendre.html',suspendre=datappnul,promo=datapromo,email_admin=email_session)
    return redirect(url_for('login'))
############################################################ promo  ###########################################################

                            ####################### nouveau promo #####################

@app.route('/nouveaupro',methods= ['GET','POST'])
def nouveaupromo():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("select * from referentiel")
        data =cur.fetchall()

        cur.execute("select nom_promo from promo ")
        prom_ver=cur.fetchall()
        con.commit()

        if request.method == "POST":
            details = request.form
            nom_promo=details['nom_promo']
            date_debut=details['date_debut']
            date_fin=details['date_fin']
            id_ref=details['option1']

            ####pour verifier  si le nom promo existe deja
            while date_debut < date_fin :
                control_promo=False
                for row in prom_ver:
                    if row[0].lower().replace(' ', '').strip() == nom_promo.lower().replace(' ', '').strip():
                        control_promo =True
                        break

                if control_promo == True  :
                    flash("promo exist deja ")
                    return  render_template('nouveaupro.html',l=prom_ver,p=data)

                else:
                    cur.execute("INSERT INTO promo(nom_promo,date_debut,date_fin,id_ref) VALUES(%s,%s,%s,%s)",
                    (nom_promo,date_debut,date_fin,id_ref))
                    con.commit()
                    flash("promo ajouté avec succé")
                    return  render_template('nouveaupro.html',l=prom_ver,p=data)
            flash("promo non ajouté,veuillez verifier bien les dates des promos ")
            return  render_template('nouveaupro.html',l=prom_ver,p=data)
        return  render_template('nouveaupro.html',l=prom_ver,p=data,email_admin=email_session)
    return redirect(url_for('login'))

                            ####################### modifier promo #####################

@app.route('/modifierpromo',methods=['POST','GET'])
def modipromo():
            # pour le methode GET
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select * from promo""")
        data =cur.fetchall()
        con.commit()

        cur.execute("select * from referentiel")
        data1 =cur.fetchall()
        con.commit()

        if request.method == "POST":
                details = request.form
                id_data = details['id_promo']
                nom_promo = details['nom_promo']
                date_debut = details['date_debut']
                date_fin = details['date_fin']
                id_ref=int(details['id_ref'])

                cur.execute("""UPDATE promo SET nom_promo=%s ,date_debut=%s ,date_fin=%s ,id_ref=%s WHERE id_promo=%s""",
                (nom_promo,date_debut,date_fin,id_ref,id_data))
                con.commit()

                cur.execute("select * from promo")
                data2 =cur.fetchall()
                con.commit()
                flash("donnees modifiees")

                # pour le methode POST
                return  render_template('modifpromo.html',promo=data2,ref=data1)
        return render_template('modifpromo.html',promo=data,ref=data1,email_admin=email_session)
    return redirect(url_for('login'))
                            ####################### liste promo #####################

@app.route('/lister')
def listepromo():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select  promo.id_promo, promo.nom_promo,promo.date_debut,
        promo.date_fin from  promo """)
        data =cur.fetchall()
        con.commit()
        return render_template('listpromo2.html',promo=data,email_admin=email_session)
    return redirect(url_for('login'))


@app.route('/listerp/<string:id_data>',methods=['POST','GET'])
def listeparpromo(id_data):
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("""select apprenants.id_app,apprenants.matricule,apprenants.prenom,apprenants.nom,apprenants.email,
        apprenants.statut,apprenants.datnais,apprenants.numero_tel
        from apprenants WHERE apprenants.id_promo=%s """,(id_data))
        datapp2 =cur.fetchall()
        con.commit()
        return render_template('aprntparpromo.html',apprenants=datapp2,email_admin=email_session)
    return redirect(url_for('login'))




###########################################################  referentiel  #########################################################

                            ####################### nouveau referentiel #####################

@app.route('/nouveauref',methods= ['GET','POST'])
def nouveauref():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        
        cur.execute(" select nom_ref from referentiel ")
        nref=cur.fetchall()
        con.commit()

        if request.method == "POST":
            details = request.form
            nom_ref=details['nom_ref']
            ####pour verifier  si le nom existe deja
            control_ref=False
            for row in nref:
                if row[0].lower().replace(' ', '') == nom_ref.lower().replace(' ', ''):
                    control_ref =True
                    break
            if control_ref == True  :
                flash("referentiel exist deja")
                return  render_template('nouveauref.html',l=nref)

            else:
                flash("referentiel ajouté avec succé")
                cur.execute("INSERT INTO referentiel(nom_ref) VALUES(%s)",(nom_ref,))
                con.commit()

                return  render_template('nouveauref.html',l=nref)

        return  render_template('nouveauref.html',l=nref,email_admin=email_session)
    return redirect(url_for('login'))

                                ####################### liste referentiel#####################
@app.route('/listeref')
def listeref():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("select * from referentiel")
        data =cur.fetchall()
        con.commit()
        return render_template('listeref.html',referentiel=data,email_admin=email_session)
    return redirect(url_for('login'))

                                ####################### modifier referentiel#####################
@app.route('/modifieref', methods=['POST','GET'])
def modifieref():
    if 'email' in session:
        email_session=escape(session['email']).capitalize()
        cur.execute("select * from referentiel")
        data =cur.fetchall()
        con.commit()
        if request.method == "POST":

                details = request.form
                id_data = details['id_ref']
                nomref = details['nom_ref']

                cur.execute("""UPDATE referentiel SET nom_ref=%s WHERE id_ref=%s""",(nomref,id_data))
                flash("donnees modifiees")
                con.commit()

                cur.execute("select * from referentiel")
                data1 =cur.fetchall()
                con.commit()
                flash("referentiel modifié avec succé")
                return render_template('modifieref.html',referentiel=data1)
        return render_template('modifieref.html',referentiel=data,email_admin=email_session)
    return redirect(url_for('login'))
                                ####################### supprimer referentiel #####################

@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
    cur.execute("DELETE FROM  referentiel WHERE id_ref =%s" ,(id_data,))
    con.commit()
    # flash("données supprimeés")

    return redirect(url_for('modifieref'))




if __name__ == '__main__':
    app.run(debug=True)
