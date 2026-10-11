from tina4_python import ORM, IntegerField, StringField, DateTimeField


class User(ORM):
    """A registered ClosetIQ user."""

    table_name = "user"

    id = IntegerField(primary_key=True, auto_increment=True)
    email = StringField()
    password_hash = StringField()
    display_name = StringField()
    created_at = DateTimeField()
