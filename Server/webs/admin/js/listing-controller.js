// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The listing controller. Simply governs the behavior of the 
	light, client, and whatever, listing.
*/
angular.module('LUMAClientAdminPortal').controller('ListingController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	// We really only need to copy state to scope. The DOM can do the rest.
	$scope.state = AdminStateService;
	
}]);