import portfolio, os, json
app = portfolio.create_app()

@app.cli.command('create_db', with_appcontext=True)
def create_db():
    portfolio.db.create_all()

@app.cli.command('delete_db', with_appcontext=True)
def delete_db():
    portfolio.db.drop_all()

@app.cli.command('reset_admin', with_appcontext=True)
def reset_admin():
    portfolio.db.drop_all()
    portfolio.db.create_all()
    create_admin()

def create_admin():
    from portfolio.models import Admin
    from portfolio import bcrypt

    file_path = os.path.join(app.instance_path, 'admin.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            master = Admin(name=data['name'],
                        email=data['email'],
                        password=bcrypt.generate_password_hash(data['password']))
            portfolio.db.session.add(master)
            portfolio.db.session.commit()
    except FileNotFoundError:
        print('File not found')
        print('Expected admin.json file inside instance folder')
        print('With properties: name, email, password')

@app.cli.command('dummy', with_appcontext=True)
def create_dummy_post():
    from portfolio.models import Post, Tag
    from datetime import datetime
    import random
    tag1 = Tag(name='project')
    tag2 = Tag(name='note')
    tag3 = Tag(name='Hello')
    tag4 = Tag(name='GoodBye')
    tag5 = Tag(name='Ciao')
    for i in range(20):
        fir = [random.choice((tag1, tag2))]
        sec = [random.choice((tag3, tag4, tag5))]
        fir.extend(sec)
        new_post = Post(complete=True,
                        tags=fir,
                        title= f'Test Title {i}',
                        body=datetime.utcnow(),
                        admin_id=1)
        portfolio.db.session.add(new_post)
        portfolio.db.session.commit()


if __name__ == '__main__':
    app.run()
