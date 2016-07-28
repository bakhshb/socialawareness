from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist
import logging
from .helper import OntologyManager
import json


logger = logging.getLogger(__name__)

#send User Bluetooth 
# curl -X GET  -H "Content-Type: application/json" -H 'Authorization: Token f386ccc6c18ffe7863cd705340c3f138967033f3' -d "{'bluetooth':''}" http://localhost:8000/api/bluetooth/
class RegisterUserBluetooth(APIView):
	permission_classes = (IsAuthenticated,)

	def dispatch(self, *args, **kwargs):
		return super(RegisterUserBluetooth, self).dispatch(*args, **kwargs)
	def post(self, request):
		logger.info("Register User Bluetooth")
		data = request.data
		bluetooth = data.get('user_bluetooth','')

		user = request.user
		onto = OntologyManager(user)
		onto_user = onto.get_user()
		onto.create_bluetooth(bluetooth)
		logger.debug(onto_user.has_bluetooth)
		# onto.save_ontology()

		return Response(status = status.HTTP_200_OK,data={'status':status.HTTP_200_OK })

#send User Bluetooth 
# curl -X GET  -H "Content-Type: application/json" -H 'Authorization: Token f386ccc6c18ffe7863cd705340c3f138967033f3' -d "{'bluetooth':''}" http://localhost:8000/api/bluetooth/
class FindMutualFriends(APIView):
	permission_classes = (IsAuthenticated,)

	def dispatch(self, *args, **kwargs):
		return super(FindMutualFriends, self).dispatch(*args, **kwargs)
	def post(self, request):
		logger.info("Receiving Surrounding Bluetooth")
		data = request.data
		bluetooth = data.get('bluetooth','')

		# Finding the user by bluetooth address in the ontology
		onto_received = OntologyManager()
		onto_received_user = onto_received.get_user_by_bluetooth(bluetooth)
		if onto_received_user is None:
			logger.debug("No Match Found")
			return Response(status = status.HTTP_204_NO_CONTENT, data={'status': status.HTTP_204_NO_CONTENT})
		
		onto_received_user_friends = onto_received.get_friends_name()

		# Getting the current user detail from ontology
		user = request.user
		onto_current = OntologyManager(user)
		onto_current_user_friends = onto_current.get_friends_name()
		# Comapring both friend list and finding mutual friends
		mutual = set(onto_current_user_friends) & set(onto_received_user_friends)

		return Response(status = status.HTTP_200_OK,data=mutual)



		
# curl -X GET -H 'Authorization: Token f386ccc6c18ffe7863cd705340c3f138967033f3' http://localhost:8000/api/ontology/
class OwlReadyOntology (APIView):
	permission_classes = (IsAuthenticated,)

	def get (self, request, format=None):
		user = request.user
		onto_friendlist=[]
		onto= OntologyManager(user)
		onto_friendlist = onto.get_friends_name()

		return Response (status=status.HTTP_200_OK, data= onto_friendlist)
