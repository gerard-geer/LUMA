// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The task controller. Allows each task container to set interface
	state upon ngClick.
*/
angular.module('LUMAClientAdminPortal').controller('ErrorDialogController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// We really only need to copy the state's error message to scope.
	$scope.state = AdminStateService;
	
}]);