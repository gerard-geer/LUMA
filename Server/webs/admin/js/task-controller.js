// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The task controller. Allows each task container to set interface
	state upon ngClick.
*/
angular.module('LUMAClientAdminPortal').controller('TaskController',
['$scope', 'AdminStateService', 'AdminServerService',
function($scope, AdminStateService, AdminServerService)
{
	// Bind some elements of the state to the controller for use in the markup.
	this.DIALOG_ENUM = AdminStateService.DIALOG_ENUM;
	// Let's just go ahead and get the server service up and running.
	this.server = AdminServerService;
	
	// A function to set which dialog is open.
	this.setDialog = function(dialogValue)
	{
		AdminStateService.showDialog = true;
		AdminStateService.dialogToShow = dialogValue;
	}
}]);