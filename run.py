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
    from portfolio.models import Admin, Tag
    from portfolio import bcrypt

    file_path = os.path.join(app.instance_path, 'admin.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            master = Admin(name=data['name'],
                        email=data['email'],
                        password=bcrypt.generate_password_hash(data['password']))

            project_tag = Tag(name='project')
            note_tag = Tag(name='note')
            portfolio.db.session.add_all([master, project_tag, note_tag])
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
    tag1 = Tag.query.get(1)
    tag2 = Tag.query.get(2)
    tag3 = Tag(name='hello')
    tag4 = Tag(name='goodbye')
    tag5 = Tag(name='ciao')
    for i in range(20):
        fir = [random.choice((tag1, tag2))]
        sec = [random.choice((tag3, tag4, tag5))]
        fir.extend(sec)
        new_post = Post(complete=True,
                        tags=fir,
                        date_posted=datetime.now(),
                        title= f'Test Title {i}',
                        body='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                        admin_id=1)
        portfolio.db.session.add(new_post)
        portfolio.db.session.commit()

@app.cli.command('search', with_appcontext=True)
def search():
    from portfolio.models import Post

    post = Post.query.get(21)

    print(post.body)
    print(type(post.body))


if __name__ == '__main__':
    app.run()
