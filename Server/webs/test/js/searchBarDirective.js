angular.module('LUMAClient', [])
    .directive('searchBar', function () {
        return {          
            restrict: 'E',
            replace:true,
            templateUrl:'search-bar.html'			
        };
    });