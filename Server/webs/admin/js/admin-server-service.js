// LUMA Copyright (c) Gerard Geer 2014-2015 
					
/*
	The lUMA Server Service. This functions as a singleton that
	encapsulates interactions with the server, and stores the
	selected query result and the state of the requested light.
*/
angular.module('LUMAClientAdminPortal').factory('AdminServerService', 
['$http', 'AdminStateService', function($http, AdminStateService) {
	
	// Split up the permitted string into a list, and trim the entries.
	function listify(permitted)
	{
		permitted = permitted.split(',');
		for(var i = 0; i < permitted.length; ++i)
		{
			// YOU SHALT NOT HAVE SPACES.
			permitted[i] = permitted[i].replace(/ /g,'');
		}
		return permitted;
	}
	
	// Sanitizes the values passed in for the new light.
	function sanitizeNewLight(nl)
	{
		if (nl.name == null || nl.name == '')
		{
			return 'Name must be a non-empty string.';
		}
		if (nl.client == null || nl.client == '')
		{
			return 'Client must be a non-empty string.';
		}
		if (nl.address == null || nl.address == '')
		{
			return 'Address must be a non-empty string.';
		}
		if (nl.permitted == null || nl.permitted == '')
		{
			return 'Permitted must contain at least one UUID.';
		}
		if (nl.exists && (nl.id == null || nl.id == ''))
		{
			return 'ID must be a non-empty string.';
		}
		else if (!nl.exists) nl.id='';
		if (!nl.exists && isNaN( parseInt(nl.r_c) ) )
		{
			return 'Red pin number is not an integer.';
		}
		else if (nl.exists) nl.r_c=0;
		if (!nl.exists && isNaN( parseInt(nl.g_c) ) )
		{
			return 'Green pin number is not an integer.';
		}
		else if (nl.exists) nl.g_c=0;
		if (!nl.exists && isNaN( parseInt(nl.b_c) ) )
		{
			return 'Blue pin number is not an integer.';
		}
		else if (nl.exists) nl.b_c=0;
		
		return '';
	}
	
	// Sanitizes the values passed in for new clients.
	function sanitizeNewClient(nc)
	{
		if (nc.name == null || nc.name == '')
		{
			return 'Name must be a non-empty string.';
		}
		if (nc.address == null || nc.address == '')
		{
			return 'Address must be a non-empty string.';
		}
		return '';
	}
	
	// A function to perform adding lights.
	function performLightAdd()
	{
		
		// Sanitize the light.
		test = sanitizeNewLight(AdminStateService.newLight);
		
		// If the light doesn't pass sanitation, we have to throw up the
		// ol' error box.
		if (test != '')
		{
			AdminStateService.errorMessage = test;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			return;
		}
		
		// Just a less verbose copy of the new light that we can manipulate.
		nl = {
			name: AdminStateService.newLight.name,
			client: AdminStateService.newLight.client,
			address: AdminStateService.newLight.address,
			permitted: AdminStateService.newLight.permitted,
			id: AdminStateService.newLight.id,
			exists: AdminStateService.newLight.exists,
			r_c: parseInt(AdminStateService.newLight.r_c),
			g_c: parseInt(AdminStateService.newLight.g_c),
			b_c: parseInt(AdminStateService.newLight.b_c)
		}
		
		// Split up the permitted string into a list, and trim the entries.
		nl.permitted = listify(nl.permitted);
		
		// Finally we can send the request to the server.
		$http.post('resources/lights/', nl).
		success(function(response)
		{
			// Let's just go ahead and log the raw response.
			console.log("Light Add response:");
			console.log(response);
			
			// Now if the light was successful we close the add-light dialog.
			if(response.success)
			{
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.NO_DIALOG;
				AdminStateService.showDialog = true;
			}
			// And if it wasn't, we bring up the error dialog.
			else
			{
				AdminStateService.errorMessage = response.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
				AdminStateService.showDialog = true;
			}
		}).
		error(function(response)
		{
			// Log the response anyhow.
			console.log("Light Add response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
	// The function that sends new client requests to the server.
	function performClientAdd()
	{
		// Take the hinkiness out of it.
		test = sanitizeNewClient(AdminStateService.newClient);
		
		// If the light doesn't pass sanitation, we present an error.
		if (test != '')
		{
			AdminStateService.errorMessage = test;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			return;
		}
		
		// Create a copy so we don't have to type as much.
		nc = {
			name: AdminStateService.newClient.name,
			address: AdminStateService.newClient.address
		}
		
		// Now with our fresh object we can send a request to the server.
		$http.post('/resources/clients/', nc).
		success(function(response)
		{
			// Let's just go ahead and log the raw response.
			console.log("Cient Add response:");
			console.log(response);
			
			// Now if the light was successful we close the add-light dialog.
			if(response.success)
			{
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.NO_DIALOG;
				AdminStateService.showDialog = true;
			}
			// And if it wasn't, we bring up the error dialog.
			else
			{
				AdminStateService.errorMessage = response.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
				AdminStateService.showDialog = true;
			}
		}).
		error(function(response)
		{
			// Log the response anyhow.
			console.log("Client Add response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
	// A function to request a listing from the server.
	function performListingRequest(path)
	{
		// Not much to this one.
		$http.get(path).
		success(function(response)
		{
			console.log("Client listing response:");
			console.log(response);
			// Store the light listing on the state for access elsewhere.
			AdminStateService.listing = response;
		}).
		error(function(response)
		{
			console.log("Client listing response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
	// A function to perform a light info update.
	function performLightInfoUpdate()
	{
		console.log('before');
		console.log(JSON.stringify(AdminStateService.selected));
		
		// Make sure the new permitted list is actually a list.
		if( typeof AdminStateService.selected.permitted == 'string' )
		{
			AdminStateService.selected.permitted = listify(AdminStateService.selected.permitted);
		}
		console.log('after');
		console.log(JSON.stringify(AdminStateService.selected));
		
		$http.put('resources/lights/', AdminStateService.selected).
		success(function(response)
		{	
			console.log("Light info update response:");
			console.log(response);
			if(response.success==true)
			{
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.NO_DIALOG;
			AdminStateService.showDialog = false;
			}
			if(response.success==false)
			{
				AdminStateService.errorMessage = response.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			}
			if(response.client.success==false && response.client.message!=null)
			{
				AdminStateService.errorMessage += 
				'\nWhen processing new client: '+response.client.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			}
			if(response.name.success==false && response.name.message!=null)
			{
				AdminStateService.errorMessage += 
				'\nWhen processing new name: '+response.name.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			}
			if(response.permitted.success==false && response.name.message!=null)
			{
				AdminStateService.errorMessage += 
				'\nWhen processing new permitted list: '+response.permitted.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			}
		}).
		error(function(response)
		{
			
			console.log("Light info update response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
	// A function to perform a client info update.
	function performClientInfoUpdate()
	{
		// Not much to do here besides send the request.
		$http.put('resources/clients/', AdminStateService.selected).
		success(function(response)
		{
			console.log("Light info update response:");
			console.log(response);
			
			if(response.success==true)
			{
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.NO_DIALOG;
			AdminStateService.showDialog = false;
			}
			if(response.success==false)
			{
				AdminStateService.errorMessage = response.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			}
		}).
		error(function(response)
		{
			console.log("Light info update response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
    return {
		addNewLight: function(){performLightAdd();},
		addNewClient: function(){performClientAdd();},
		getLightListing: function(){performListingRequest('resources/lights/');},
		getClientListing: function(){performListingRequest('resources/clients/');},
		updateLightInfo: function(){performLightInfoUpdate();},
		updateClientInfo: function(){performClientInfoUpdate();}
    };
}]);