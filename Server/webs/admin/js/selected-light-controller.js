// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	Each light listing needs to have an on-click callback so that
	we can raise for it a more specific light dialog.
*/
angular.module('LUMAClientAdminPortal').controller('LightListingController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	this.onLightClick = function(id_number, light)
	{
		// Recreate the selected light on the state.
		AdminStateService.selected = {
			id:id_number,
			name:light[0],
			client:light[1],
			permitted:light[2]
		};
		
		// Change to the light info modal.
		AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.LIGHT_INFO;
	}
	
}]);