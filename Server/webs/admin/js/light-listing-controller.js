// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The light listing controller. Simply governs the behavior of the 
	light listing.
*/
angular.module('LUMAClientAdminPortal').controller('LightListingController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// We really only need to copy the state's error message to scope.
	$scope.state = AdminStateService;
	
}]);