from app import create_app,db
from app.admin import modles

app = create_app()

from flask_migrate import Migrate,MigrateCommand
migrate=Migrate(app,db)

from flask_script import Manager
manager=Manager(app)
manager.add_command("db",MigrateCommand)



if __name__ == '__main__':
    manager.run()

