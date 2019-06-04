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
    for i in range(20):
        fir = [random.choice((Tag(name='project', post_id=i+1), Tag(name='note', post_id=i+1)))]
        sec = [random.choice((Tag(name='Hello', post_id=i+1), Tag(name='GoodBye', post_id=i+1), Tag(name='Ciao', post_id=i+1)))]
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
