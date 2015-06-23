angular.module('LUMAClient').controller('EditorController', 
['$scope','LUMAServerService','LUMAStateService',
function($scope,LUMAServerService,LUMAStateService){
	$scope.state = LUMAStateService;
}]);