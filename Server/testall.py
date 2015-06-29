from testaliasmanager import testAliasManager
from testlightmanager import testLightManager
from testclientmanager import testClientManager
from testrequesthandler import testRequestHandler

"""
Tests all of the Alias Manager, Light Manager, Client Manager,
and Request Handler.

This requires that the server and client are using the test configuration files.
"""
if __name__ == '__main__':
	testAliasManager()
	testLightManager()
	testClientManager()
	testRequestHandler()