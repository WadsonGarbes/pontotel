from marshmallow import validate, schema, fields
from app import ma
from app.models import Usuario

class PaginationSchema(ma.Schema):
   page = ma.Int(missing=1)
   per_page = ma.Int(missing=10)

class InvalidPayloadSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)


class UnauthorizedSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)


class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)


class PaginationLinksSchema(ma.Schema):
    next = ma.URL(dump_only=True)
    prev = ma.URL(dump_only=True)
    self = ma.URL(dump_only=True)


class PaginatedMetaSchema(ma.Schema):
    page = ma.Int(missing=1)
    per_page = ma.Int(missing=10)
    total_items = ma.Int()
    total_page = ma.Int()


class PaginatedItemsUserSchema(ma.Schema):
    email = ma.String()
    id = ma.Int()
    login = ma.String() 
    nome = ma.String()
    sobrenome = ma.String()

class PaginatedUserSchema(ma.Schema):
    class Meta:
        ordered = True
        
    _links = fields.Nested(PaginationLinksSchema())
    _meta = fields.Nested(PaginatedMetaSchema())
    items = fields.List(fields.Nested(lambda: PaginatedItemsUserSchema()))
    

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        ordered = True

    id = ma.auto_field(dump_only=True)
    login = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=60))
    email = ma.auto_field(required=True, validate=[validate.Length(max=60),
                                                   validate.Email()])
    nome = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    sobrenome = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    senha = ma.String(required=True, load_only=True)

