'use strict';
//starting point of angular application
// all the angular configurations will be maintained here
var organicApp = angular.module("organicApp", ["ui.router", "ui.bootstrap", "restangular", "ngCookies", "toastr"]);

organicApp.constant("SETTINGS", {
  "STATIC_URL": djsettings.STATIC_URL,
  "TEMPLATE_DIR": djsettings.STATIC_URL + 'js/ngapp/tmplts/'
});

organicApp.config(["$stateProvider", "$urlRouterProvider", "SETTINGS", "RestangularProvider", "toastrConfig",
                    function ($stateProvider, $urlRouterProvider, SETTINGS, RestangularProvider, toastrConfig) {

                      $urlRouterProvider.otherwise('home');

                      //Routing for Learners Menu
//                      $stateProvider.state('profile', {
//                        url: '/profile',
//                        templateUrl: function ($stateParams) {
//                          return SETTINGS.TEMPLATE_DIR + 'profile.html';
//                        },
//                        controller: "ProfileCtrl"
//                      });

                      RestangularProvider.setBaseUrl('/api/v1');
                      RestangularProvider.setRequestSuffix("/");


                      //Error pages
                      $stateProvider.state('page403', {
                        url: '/forbidden',
                        templateUrl: function ($stateParams) {
                          return SETTINGS.TEMPLATE_DIR + 'error/403.html';
                        }
                      });

                      angular.extend(toastrConfig, {
                        closeButton: true,
                        timeOut: 2000,
                        positionClass: 'toast-position'
                      });
                    }]);

organicApp.run(["$rootScope", "SETTINGS", function ($rootScope, SETTINGS) {
  //Add settings in $rootScope so that they can be directly accessed in HTML
  $rootScope.SETTINGS = SETTINGS;
}]);
