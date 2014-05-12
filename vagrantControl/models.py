# -=- encoding: utf-8 -=-
import re
from vagrantControl import db
from vagrantControl.core import redis_conn
# Kept only for debugging
# from vagrantControl import app
from flask.ext.sqlalchemy import orm
from flask import request, session
from sh import ls
from settings import ETH

import time
from rq import Queue, Connection


class BaseException(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidPath(BaseException):
    pass


class InstanceNotFound(BaseException):
    pass


class BackendProvider():
    def stop(self, instanceId):
        raise NotImplementedError("Should have implemented this")

    def start(self, instanceId):
        raise NotImplementedError("Should have implemented this")

    def pause(self, instanceId):
        raise NotImplementedError("Should have implemented this")

    def kill(self, instanceId):
        raise NotImplementedError("Should have implemented this")

    def get_all_instances(self):
        raise NotImplementedError("Should have implemented this")


class VagrantBackend(BackendProvider):
    def __init__(self):
        self.instances = VagrantInstance.query.all()

    def get(self, instanceId):
        return VagrantInstance.query.get(int(instanceId))

    def find(self, instanceId=None, path=None):
        for instance in self.instances:
            if instance.id == instanceId or instance.path == path:
                return instance

        return None

    def get_all_instances(self):
        return self.instances

    def create(self, request):
        if 'environment' in request:
            environment = request['environment']
        else:
            environment = ''

        instance = VagrantInstance(None, request['path'], request['name'],
                                   environment)
        if self._check_instance(request['path']):
            db.session.add(instance)
            db.session.commit()
        else:
            raise InvalidPath('Path {} given is invalid or cant be read'
                              .format(request['path']))

        return instance

    def delete(self, instanceId):
        instance = VagrantInstance.query.get(instanceId)
        instance.delete()

    def _check_instance(self, path):
        try:
            ls(path + '/Vagrantfile')
        except:
            return False
        return True

    def stop(self, instanceId):
        instance = VagrantInstance.query.get(instanceId)
        return instance.stop()

    def start(self, instanceId, provider):
        instance = VagrantInstance.query.get(instanceId)
        return instance.start(provider)


class VagrantInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)
    name = db.Column(db.String)
    environment = db.Column(db.String)

    def __init__(self, id, path, name, environment):
        self.id = id
        self.path = path
        self.name = name
        self.environment = environment
        self.init_on_load()

    def __unicode__(self):
        return self.path

    def __str__(self):
        return self.__unicode__()

    def post(self):
        print request.json
        return self

    @orm.reconstructor
    def init_on_load(self):
        # self.status = self._status()
        # if 'running' in self.status:
        #    self.ip = self._ip()
        pass

    def _status(self):
        results = self._submit_job('status', path=self.path)
        results = re.findall(r'.*\\n\\n(.*)\\n\\n.*', results, re.M)
        # We remove the whitespace in between each word
        results = [' '.join(result.split()) for result in results]
        return results

    def _ip(self):
        results = self._submit_job('ip', path=self.path)
        return results

    def start(self, provider=None):
        results = self._submit_job(
            'run',
            path=self.path,
            eth=ETH,
            environment=self.environment,
            provider=provider
        )
        self.status = self._status()
        return results

    def stop(self):
        results = self._submit_job('stop', path=self.path)
        self.status = self._status()
        return results

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        self._submit_job('destroy', path=self.path)

    def _submit_job(self, action, **kwargs):
        with Connection():
            queue = Queue('high', connection=redis_conn)
            action = 'worker.{}'.format(action)
            job = queue.enqueue(action, **kwargs)

            if 'jobs' not in session:
                session['jobs'] = []

            session['jobs'].append(job.id)
            while job.result is None:
                time.sleep(0.5)

        return job.result
