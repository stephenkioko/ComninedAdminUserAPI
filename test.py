from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset done")

    with app.test_client() as client:
        #test signup as normal user
        res = client.post('/signup', json = {"username":"jeniffer",
                                             "email":"jeniffer@test.com",
                                             "password":"jeniffer1",
                                             "role": "user"})

        print("signup", res.status_code, res.get_json())

        #test signup as an admin
        res = client.post('/signup', json={
            "username":"adminUser",
            "email":"admin@test.com",
            "password":"admin1",
            "role":"admin",
            "admin_key":"my_secretkey"
        })
        print("signup", res.status_code, res.get_json())

        #test login
        res = client.post('/login', json = {"username":"jeniffer",
                                            "password":"jeniffer1"})

        print("login", res.status_code, res.get_json())

        #test duplicate
        res = client.post('/signup', json={
            "username": "jeniffer",
            "password": "jeniffer1"
        })
        print("Duplicate signup", res.status_code, res.get_json())