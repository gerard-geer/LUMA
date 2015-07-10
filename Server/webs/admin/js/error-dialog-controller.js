// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The error message dialog. All this does is ensure that the markup
	has somewhere to look for the error message.
*/
angular.module('LUMAClientAdminPortal').controller('ErrorDialogController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// We really only need to copy the state's error message to scope.
	$scope.state = AdminStateService;
	
}]);