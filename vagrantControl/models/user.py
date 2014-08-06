# -=- encoding: utf-8 -=-

from flask.ext.principal import UserNeed, RoleNeed, Permission

from vagrantControl import db
from vagrantControl.models.team import teams_users

ROLE_DEV = 'dev'
ROLE_ADMIN = 'admin'


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    given_name = db.Column(db.String(128))
    family_name = db.Column(db.String(128))
    picture = db.Column(db.String(256))
    role = db.Column(db.String(32), default=ROLE_DEV)
    last_login = db.Column(db.DateTime)
    teams = db.relationship(
        'Team',
        secondary=teams_users,
        backref=db.backref('teams', lazy='dynamic')
    )
    permissions_grids = db.relationship(
        'UserPermissionsGrids',
        backref='user',
    )

    def __init__(self, id, name, email, given_name,
                 family_name, picture, role=ROLE_DEV, last_login=None,
                 permissions_grids=None):
        self.id = id
        self.name = name
        self.email = email
        self.given_name = given_name
        self.family_name = family_name
        self.picture = picture
        self.role = role
        self.last_login = last_login

    def __unicode__(self):
        return 'User {} : {}, Role :{}'.format(
            self.id,
            self.name,
            self.role
        )

    def __str__(self):
        return self.__unicode__()

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def is_admin(self):
        if self.role == ROLE_ADMIN:
            return True
        return False

    def has_permission(self, permissionType, objectId):
        permission = permissionType(objectId)
        admin = Permission(RoleNeed(ROLE_ADMIN))
        return permission.can() or admin.can()