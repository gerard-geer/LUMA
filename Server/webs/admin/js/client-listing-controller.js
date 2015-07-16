// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	Each client listing also needs to have an on-click callback to
	organize its goods into a nice object.
*/
angular.module('LUMAClientAdminPortal').controller('ClientListingController',
['$scope', 'AdminStateService',
function($scope, AdminStateService)
{
	this.onLightClick = function(clientName, clientAddress)
	{
		// Recreate the selected light on the state.
		AdminStateService.selected = {
			name:clientName,
			address:clientAddress
		};
		
		// Change to the light info modal.
		AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.CLIENT_INFO;
	}
	
}]);