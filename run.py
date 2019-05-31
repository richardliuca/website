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
            master = Admin(
                name=data['name'],
                email=data['email'],
                password=bcrypt.generate_password_hash(data['password']))
            portfolio.db.session.add(master)
            portfolio.db.session.commit()
    except FileNotFoundError:
        print('File not found')
        print('Expected admin.json file inside instance folder')
        print('With properties: name, email, password')

if __name__ == '__main__':
    app.run()
