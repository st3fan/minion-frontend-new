// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

var minionAdminInvitesModule = angular.module('minionAdminInvitesModule', []);

// Controller for creating invites dialog
minionAdminInvitesModule.controller("AdminCreateInviteController", function($scope, dialog, users, groups) {
    $scope.sender = localStorage.getItem("session.email");
    $scope.invite = {sender: $scope.sender, recipient: ""};
    $scope.groups = groups;
    $scope.roles = ["user", "administrator"];
    $scope.opts = {
        'accept': true,
        'decline': true
    };
    $scope.navItems = app.navContext('admin');

    // todo: do cleanup!
    $scope.cancel = function() {
        dialog.close(null);
    };

    $scope.submit = function(result) {
        result.opts = $scope.opts;
        dialog.close(result);
    }
});


// We don't want to refresh the page to see default orderBy to take place
minionAdminInvitesModule.controller("AdminInvitesController", function($scope, $http, $dialog, $filter, $location) {

    $scope.navItems = app.navContext('admin');

    var base_url = $location.absUrl().split("#!")[0] + '#!/invite';
    var reload = function() {
        $http.get('/api/admin/invites')
            .success(function(response, status, headers, config) {
                $scope.invites = $filter('orderBy')(response.data, 'sent_on');
            });
    };

    $scope.createInvite = function () {
        $http.get('/api/admin/groups')
            .success(function(response, status, headers, config) {
                var d = $dialog.dialog({
                    templateUrl: "static/partials/admin/invites/create-invites.html?x=" + new Date().getTime(),
                    controller: "AdminCreateInviteController",
                    resolve: { users: function() { return $scope.users; },
                               groups: function() { return response.data; }}
                });

                d.open().then(function(result) {
                    if(result) {
                        data1 = {email: result.email, name: result.name, role: result.role, groups: result.groups,
                            invitation: true}

                        sender = localStorage.getItem("session.email");
                        $http.post('/api/admin/users', data1).success(function(response, status, headers, config) {
                            if (response.success) {
                                reload();
                                // now we should be able to send an invite
                                var notify_when = [];
                                if (result.opts.accept)
                                    notify_when.push('accept');
                                if (result.opts.decline)
                                    notify_when.push('decline');
                                data2 = {sender: sender, recipient: result.email, base_url: base_url, notify_when: notify_when}
                                $http.post('/api/admin/invites', data2).success(function(response, status, headers, config) {
                                    if (response.success) {
                                        reload();
                                    }
                                });
                            } else {
                                // TODO Show an error dialog
                            }
                        });
                    }
                });
            });
    };

    $scope.resendInvite = function(id) {
        $http.post('/api/admin/invites/' + id + '/control', {action: 'resend', base_url: base_url})
            .success(function(response, status, headers, config) {
                if (response.success) {
                    reload();
                }
            });
    };

    $scope.removeInvite = function(id) {
        $http.delete('/api/admin/invites/' + id)
            .success(function(response, status, headers, config) {
                if (response.success) {
                    reload();
                }
            });
    };

    $scope.$on('$viewContentLoaded', function() {
        reload();
    });
});
