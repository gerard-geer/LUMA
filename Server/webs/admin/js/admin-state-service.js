// LUMA Copyright (c) Gerard Geer 2014-2015 
					
/*
	The Admin Portal's state service. This essentially serves as a globally
	accessible singleton that stores state between disjoint controllers.
*/
angular.module('LUMAClientAdminPortal').factory('AdminStateService', [function() {
    
	var dialogEnum = {
		NO_DIALOG: 0,
		NEW_LIGHT: 1,
		NEW_CLIENT: 2,
		LIGHT_LISTING: 4,
		CLIENT_LISTING: 8,
		LIGHT_INFO: 16,
		CLIENT_INFO: 32,
		DETAILED_CLIENT_INFO: 64,
		ERROR: 128
	}
	return {
		// An object in which to create and store a new light before subission.
		newLight: null,
		// And object in which to create and store a new client before 
		// it is submitted.
		newClient: null,
		// A slot for potential error messages.
		errorMessage: null,
		// Whether or not to show dialogs at all.
		showDialog: false,
		// What dialog to show.
		dialogToShow: dialogEnum.NO_DIALOG,
		// THe dialog enumerator.
		DIALOG_ENUM: dialogEnum,
		// A place to store listings.
		listing: null,
		// A place to store lights selected from the light listing.
		selected: null
    };
}]);