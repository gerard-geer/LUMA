// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The dialog controller. Allows each dialog to see if it needs to be displayed.
*/
angular.module('LUMAClientAdminPortal').controller('DialogController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// Bind some elements of the state to the controller for use in the markup.
	this.DIALOG_ENUM = AdminStateService.DIALOG_ENUM;
	this.state = AdminStateService;
	
	// A function to see if the given dialog matches that of the global state.
	this.isDialog = function(dialogValue)
	{
		return AdminStateService.dialogToShow == dialogValue;
	}
	
	// A function that allows dialogs to change their caste.
	this.setDialog = function(dialogValue)
	{
		AdminStateService.showDialog = true;
		AdminStateService.dialogToShow = dialogValue;
	}
}]);