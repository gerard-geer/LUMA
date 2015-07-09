// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The task controller. Allows each task container to set interface
	state upon ngClick.
*/
angular.module('LUMAClientAdminPortal').controller('TaskController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// Bind some elements of the state to the controller for use in the markup.
	this.DIALOG_ENUM = AdminStateService.DIALOG_ENUM;
	
	// A function to see if the given dialog matches that of the global state.
	this.isDialog = function(dialogValue)
	{
		return AdminStateService.dialogToShow == dialogValue;
	}
}]);