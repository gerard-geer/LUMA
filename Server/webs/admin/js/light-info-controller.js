// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	This is the controller for the more light info dialog.
*/
angular.module('LUMAClientAdminPortal').controller('LightInfoController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	$scope.light = AdminStateService.selectedLight;
	
}]);