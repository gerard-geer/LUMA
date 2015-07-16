// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	This basically just makes state accessible to the client info modal.
*/
angular.module('LUMAClientAdminPortal').controller('ClientInfoController',
['$scope', 'AdminStateService', 'AdminServerService',
function($scope, AdminStateService, AdminServerService)
{
	$scope.state = AdminStateService;
	
	this.onUpdateSubmit = function()
	{
		alert(JSON.stringify($scope.state.selected));
	}
}]);