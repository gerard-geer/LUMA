// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	Each light listing needs to have an on-click callback so that
	we can raise for it a more specific light dialog.
*/
angular.module('LUMAClientAdminPortal').controller('LightListingController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	
	this.onLightClick = function(light)
	{
		AdminStateService.selectedLight = light;
		alert(light);
	}
	
}]);