from sqladmin import Admin, ModelView

from app.models import Book, Author

class AuthorAdmin(ModelView, model=Author):
    column_list = [Author.id, Author.name]
    name = "Author"
    name_plural = "Authors"
class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.author_id, Book.year, Book.summary]
    name = "Books"
    name_plural = "Books"

def setup_admin(app,engine):
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(BookAdmin)
    admin.add_view(AuthorAdmin)
    return admin
