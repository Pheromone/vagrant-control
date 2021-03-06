angular.module('angularFlaskServices', ['ngResource'])
    .value('version', '0.5')
    .factory('Instances', function($resource) {
        return $resource('/api/instances/:id', {id:'@id'}, {
            query: {
                method: 'GET',
                params: { id: '' },
                isArray: true
            }
        });
    })
    .factory('MachineIP', function($resource) {
        return $resource('/api/instances/:id/:machineName/ip', {id:'@id'});
    })
    .factory('Domains', function($resource) {
        return $resource('/api/domains/:id', {id:'@id'},{
            update: {
                method: 'PUT',
                params: { id: '' },
            }
        });
    })
    .factory('Htpassword', function($resource) {
        return $resource('/api/htpassword/:slug', {slug:'@slug'});
    })
    .factory('Projects', function($resource) {
        return $resource('/api/projects/:id', {id:'@id'});
    })
    .factory('Hosts', function($resource) {
        return $resource('/api/hosts/:id', {id:'@id'});
    })
    .factory('Teams', function($resource) {
        return $resource('/api/teams/:id', {id:'@id'});
    })
    .factory('AuditLog', function($resource) {
        return $resource('/api/auditlog');
    })
    .factory('Users', function($resource) {
        return $resource('/api/users/:id', {id:'@id'});
    })
    .factory('APIKeys', function($resource) {
        return $resource('/api/APIKeys/:userId/:id', {userId:'@userId', id:'@id'});
    })
    .factory('SSLKeys', function($resource) {
        return $resource('/api/SSLKeys/:id', {id:'@id'});
    })
    .factory('DomainControllers', function($resource) {
        return $resource('/api/domainControllers/:id', {id:'@id'});
    })
    .factory('JobDetails', function($resource) {
        return $resource('/api/jobdetails/:instanceId', {instanceId:'@instanceId'});
    })
;
