// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The controller for adding a light. 
*/
angular.module('LUMAClientAdminPortal').controller('AddLightController',
['$scope', 'AdminStateService', 'AdminServerService',
function($scope, AdminStateService, AdminServerService)
{
	// An interfacing object that is used to store the current light described
	// by the add light form.
	this.newLight = {
		name: 'new light',
		client: 'Research Room',
		address: '127.0.0.1',
		permitted: '1, 2, 3, 4, asdf adf, asdf asdf, asdf',
		exists: false,
		id: 'as',
		r_c: 1,
		g_c: 1,
		b_c: 1
	};
	
	// A function to see if the given dialog matches that of the global state.
	this.isDialog = function(dialogValue)
	{
		return AdminStateService.dialogToShow == dialogValue;
	};
	
	// The on submit callback. This copies our local new light dialog to the
	// global state, and then submits it to the server.
	this.onSubmit = function(light)
	{
		AdminStateService.newLight = light;
		AdminServerService.addNewLight();
	};
	
}]);