// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The task controller. Allows each task container to set interface
	state upon ngClick.
*/
angular.module('LUMAClientAdminPortal').controller('AddLightController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// An interfacing object that is used to store the current light described
	// by the add light form.
	this.newLight = {
		name: null,
		client: null,
		address: null,
		permitted: null,
		exists: true,
		id: null,
		r_c: null,
		g_c: null,
		b_c: null
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
	};
	
}]);