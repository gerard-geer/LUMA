// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	This is the controller for the more light info dialog.
*/
angular.module('LUMAClientAdminPortal').controller('LightInfoController',
['$scope', 'AdminStateService', 'AdminServerService',
function($scope, AdminStateService, AdminServerService)
{
	$scope.state = AdminStateService;
	
	this.onUpdateSubmit = function()
	{
		AdminServerService.updateLightInfo();
	}
}]);