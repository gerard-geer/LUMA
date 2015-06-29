// LUMA Copyright (c) Gerard Geer 2014-2015 

angular.module('LUMAClient').controller('EditorController', 
['$scope','LUMAServerService','LUMAStateService',
function($scope,LUMAServerService,LUMAStateService){
	$scope.state = LUMAStateService;
}]);