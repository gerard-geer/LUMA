// LUMA Copyright (c) Gerard Geer 2014-2015 
					
/*
	The Admin Portal's state service. This essentially serves as a globally
	accessible singleton that stores state between disjoint controllers.
*/
angular.module('LUMAClientAdminPortal').factory('AdminStateService', [function() {
    
	var dialogEnum = {
		NO_DIALOG: 0,
		NEW_LIGHT: 1
	}
	return {
		// An object in which to create and store a new light.
		newLight: null,
		// Whether or not an error was returned on an action.
		isError: false,
		// What dialog to show.
		dialogToShow: dialogEnum.NO_DIALOG,
		// THe dialog enumerator.
		DIALOG_ENUM: dialogEnum
    };
}]);