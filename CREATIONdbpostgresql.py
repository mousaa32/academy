import psycopg2 as psy


con = psy.connect   (   host="localhost",
                        database="flaskhtml",
                        user="postgres",
                        password="Diop1957+",
                        port="5432"
                        )



cur = con.cursor()

cur.execute("""CREATE TABLE  IF NOT EXISTS referentiel(
                        id_ref SERIAL PRIMARY KEY,
                        nom_ref VARCHAR(255) NOT NULL)
        """)

cur.execute("""CREATE TABLE  IF NOT EXISTS promo(
                        id_promo SERIAL PRIMARY KEY ,
                        nom_promo VARCHAR(255) NOT NULL,
                        date_debut DATE,
                        date_fin DATE,
                        id_ref INTEGER ,
                        FOREIGN KEY (id_ref)
                        REFERENCES referentiel(id_ref))
        """)
cur.execute("""CREATE TABLE  IF NOT EXISTS apprenants(
                        id_app SERIAL PRIMARY KEY,
                        matricule VARCHAR(255) ,
                        prenom VARCHAR(255) ,
                        nom  VARCHAR(255) ,
                        email VARCHAR(255) ,
                        statut VARCHAR(255) ,
                        DatNais DATE,
                        numero_tel VARCHAR(255) ,
                        id_promo INTEGER,
                        FOREIGN KEY (id_promo)
                        REFERENCES promo(id_promo))
        """)
cur.execute("""CREATE TABLE  IF NOT EXISTS  utilisateur(
                        id_user SERIAL PRIMARY KEY,
                        prenom VARCHAR(255) ,
                        nom  VARCHAR(255) ,
                        email VARCHAR(255) ,
                        password VARCHAR(255),
                        etat VARCHAR(255),
                        imagebyte bytea)
        """)




con.commit()
con.close()
