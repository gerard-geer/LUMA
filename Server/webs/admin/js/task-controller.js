// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The task controller. Allows each task container to set interface
	state upon ngClick.
*/
angular.module('LUMAClientAdminPortal').controller('TaskController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// Bind the state service to the scope so we can have two-way binding.
	$scope.state = AdminStateService;
}