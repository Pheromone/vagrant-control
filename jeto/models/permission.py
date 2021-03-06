#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from collections import namedtuple
from functools import partial
from flask.ext.principal import Permission

from jeto import db

InstanceNeed = namedtuple('instance', ['method', 'value'])
StartInstanceNeed = partial(InstanceNeed, 'start')
StopInstanceNeed = partial(InstanceNeed, 'stop')
ProvisionInstanceNeed = partial(InstanceNeed, 'provision')
DestroyInstanceNeed = partial(InstanceNeed, 'destroy')
ViewInstanceNeed = partial(InstanceNeed, 'view')
RunScriptInstanceNeed = partial(InstanceNeed, 'runScript')
SyncInstanceNeed = partial(InstanceNeed, 'sync')
RSyncInstanceNeed = partial(InstanceNeed, 'rsync')

HostNeed = namedtuple('host', ['method', 'value'])
ViewHostNeed = partial(HostNeed, 'view')

ProjectNeed = namedtuple('project', ['method', 'value'])
ViewProjectNeed = partial(ProjectNeed, 'view')

DomainNeed = namedtuple('project', ['method', 'value'])
ViewDomainNeed = partial(DomainNeed, 'view')
CreateDomainNeed = partial(DomainNeed, 'create')
EditDomainNeed = partial(DomainNeed, 'edit')

SSLKeyNeed = namedtuple('sslkey', ['method', 'value'])
ViewSSLKeyNeed = partial(SSLKeyNeed, 'view')


class StartInstancePermission(Permission):
    def __init__(self, instanceId):
        need = StartInstanceNeed(unicode(instanceId))
        super(StartInstancePermission, self).__init__(need)


class StopInstancePermission(Permission):
    def __init__(self, instanceId):
        need = StopInstanceNeed(unicode(instanceId))
        super(StopInstancePermission, self).__init__(need)


class ProvisionInstancePermission(Permission):
    def __init__(self, instanceId):
        need = ProvisionInstanceNeed(unicode(instanceId))
        super(ProvisionInstancePermission, self).__init__(need)


class DestroyInstancePermission(Permission):
    def __init__(self, instanceId):
        need = DestroyInstanceNeed(unicode(instanceId))
        super(DestroyInstancePermission, self).__init__(need)


class ViewInstancePermission(Permission):
    def __init__(self, instanceId):
        need = ViewInstanceNeed(unicode(instanceId))
        super(ViewInstancePermission, self).__init__(need)


class RunScriptInstancePermission(Permission):
    def __init__(self, instanceId):
        need = RunScriptInstanceNeed(unicode(instanceId))
        super(RunScriptInstancePermission, self).__init__(need)


class SyncInstancePermission(Permission):
    def __init__(self, instanceId):
        need = SyncInstanceNeed(unicode(instanceId))
        super(SyncInstancePermission, self).__init__(need)


class RSyncInstancePermission(Permission):
    def __init__(self, instanceId):
        need = RSyncInstanceNeed(unicode(instanceId))
        super(RSyncInstancePermission, self).__init__(need)


class ViewHostPermission(Permission):
    def __init__(self, hostId):
        need = ViewHostNeed(unicode(hostId))
        super(ViewHostPermission, self).__init__(need)


class ViewProjectPermission(Permission):
    def __init__(self, projectId):
        need = ViewProjectNeed(unicode(projectId))
        super(ViewProjectPermission, self).__init__(need)


class TeamPermissionsGrids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objectId = db.Column(db.Integer)
    objectType = db.Column(db.String(64))
    action = db.Column(db.String(64))
    team_id = db.Column(
        db.Integer,
        db.ForeignKey('team.id')
    )


class UserPermissionsGrids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objectId = db.Column(db.Integer)
    objectType = db.Column(db.String(64))
    action = db.Column(db.String(64))
    user_id = db.Column(
        db.String(64),
        db.ForeignKey('user.id')
    )


class ViewDomainPermission(Permission):
    def __init__(self, projectId):
        need = ViewDomainNeed(unicode(projectId))
        super(ViewDomainPermission, self).__init__(need)


class EditDomainPermission(Permission):
    def __init__(self, projectId):
        need = EditDomainNeed(unicode(projectId))
        super(EditDomainPermission, self).__init__(need)


class CreateDomainPermission(Permission):
    def __init__(self, projectId):
        need = CreateDomainNeed(unicode(projectId))
        super(CreateDomainPermission, self).__init__(need)


class SSLKeyPermission(Permission):
    def __init__(self, SSLId):
        need = ViewSSLKeyNeed(unicode(SSLId))
        super(SSLKeyPermission, self).__init__(need)
