from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import models

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        load_instance = True
        exclude = ('password_hash',)

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Task
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
