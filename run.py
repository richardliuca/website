import portfolio, os, json
app = portfolio.create_app()

# with app.app_context():
#     portfolio.db.create_all()

@app.cli.command('create_db', with_appcontext=True)
def create_db():
    portfolio.db.create_all()

@app.cli.command('reset_db', with_appcontext=True)
def reset_database():
    portfolio.db.drop_all()
    portfolio.db.create_all()
    create_admin()

def create_admin():
    from portfolio import Admin
    from portfolio import bcrypt

    file_path = os.path.join(app.instance_path, 'admin.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        master = Admin(
            name=data['name'],
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']))
        portfolio.db.session.add(master)
        portfolio.db.session.commit()


if __name__ == '__main__':
    app.run()
