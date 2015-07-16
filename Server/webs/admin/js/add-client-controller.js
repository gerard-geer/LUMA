// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The controller for adding a light. Creates a model for the add client
	dialog to interact with via the state service, and on submit, sends that
	model to the server via the server service.
*/
angular.module('LUMAClientAdminPortal').controller('AddClientController',
['$scope', 'AdminStateService', 'AdminServerService',
function($scope, AdminStateService, AdminServerService)
{
	// An interfacing object that is used to store the current light described
	// by the add light form.
	this.newClient = {
		name: 'new client',
		address: 'not a real address',
	};
	
	// The on submit callback. This copies our local new light dialog to the
	// global state, and then submits it to the server.
	this.onSubmit = function(client)
	{
		AdminStateService.newClient = client;
		AdminServerService.addNewClient();
	};
	
}]);