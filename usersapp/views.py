import datetime

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
import pandas as pd

from usersapp.serializers import *
from usersapp.models import *
from usersapp.models import *

from rest_framework import authentication, permissions
from rest_framework import generics, mixins

import json
from django_pandas.io import read_frame
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from datetime import timedelta
import datetime
from datetime import datetime


# user Registration
class RegisterApi(generics.GenericAPIView):
    # fetching serializer data
    serializer_class = UserSerializer
    # adding authentications & auth user with role
    # authentication_classes = []

    # post method for user registration
    def post(self, request, *args, **kwargs):
        '''
        This function is used for post data into database of particuar model and
            method is POST this method is used for only post the data and this function
            contating serializer data fetching serializer data and register  user with details
        '''
        parameters = request.data.copy()
        serializer = self.get_serializer(data=parameters)
        # validating serializer
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "User Created Successfully.  Now perform Login to get your token"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'user name already exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)



# user Login
class LoginAPIView(generics.GenericAPIView):
    # adding authentications & auth user with role
    # fetching serializer data
    serializer_class = LoginSerializer

    def post(self, request):
        '''
        getting serializer data and checking validating data sending data
        into the responce body with status code
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if serializer.is_valid():
        user = serializer.data
        print(user,'data user id')
        userid = (user['id'])
        '''from the login serializer getting the user id'''
        m = datetime.today()
        '''getting the today date'''
        user = serializer.data
        userid = (user['id'])
        '''from the login serializer getting the user id'''
        getting_ids = ClockIn(user_id=userid, login_date=m)
        '''if the date is not today it will create the record'''
        getting_ids.save()
        '''returning the serializer data'''
        return Response(serializer.data, status=status.HTTP_200_OK)



class ClockedHours(generics.GenericAPIView):

    def get(self,request):
        try:
            # get login&logout details with particular values filter yesterday date data
            queryset = ClockIn.objects.filter(login_date__lt=datetime.date.today()).values('login_time',
                                                                                            'user__name',
                                                                                            'login_date')

            querySet3 = ClockOut.objects.filter(logout_date__lt=datetime.date.today()).values('logout_time',
                                                                                               'user__name',
                                                                                               'logout_date')

            # add queryset into dataframe
            df1 = pd.DataFrame(queryset)
            df2 = pd.DataFrame(querySet3)

            # rename the colums here user id
            df2.rename(columns={'user__name': 'name'}, inplace=True)

            df1 = df1.sort_values(['user__name', 'login_time'])
            df2 = df2.sort_values(['name', 'logout_time'])

            df = pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)
            df['logout_time'] = pd.to_timedelta(df['logout_time'].astype(str))

            df['login_time'] = pd.to_timedelta(df['login_time'].astype(str))

            df['diiffrences'] = df['logout_time'] - df['login_time']

            diff = df[['login_date', 'user__name', 'name', 'diiffrences']]

            group1 = diff.groupby(['user__name', 'name', 'login_date']).sum('')

            d = group1.reset_index()
            c = d[['diiffrences']]

            # converting the data into dictionary format
            data_dict = d.to_dict('records')

            # dump the dict data into json
            json_data = json.dumps(data_dict, default=str)

            # loads the dump data again ,and send the responce
            python_obj = json.loads(json_data)

            # store the data into database
            for i in range(0, len(python_obj)):
                credit, created = ProductiveHours.objects.get_or_create(user_id=python_obj[i]['user__name'],
                                                                        user=python_obj[i]['name'],
                                                                        login_date=python_obj[i]['login_date'],
                                                                        diiffrences=python_obj[i]['diiffrences'])
                # ProductiveHours.objects.create(user_id=python_obj[i]['user_id'], user=python_obj[i]['user'], login_date=python_obj[i]['login_date'], diiffrences=python_obj[i]['diiffrences'])
            # get the queryset for all data
            obj = ProductiveHours.objects.all()
            df = read_frame(obj)

            # get the latest record from every user
            latest_prod = df.sort_values('diiffrences').groupby(['login_date', 'user_id']).tail(1)

            timer_dict = latest_prod.to_dict('records')

            # dump the data into json format
            timetr_json_data = json.dumps(timer_dict, default=str)
            # loads the data into the format
            timertr_json_data = json.loads(timetr_json_data)
            # send the response
            return Response({"productive_hours": timertr_json_data}, status=status.HTTP_200_OK)
        except:
            return Response('no time data in your database please check your database',
                            status=status.HTTP_404_NOT_FOUND)


class Current_Week(generics.GenericAPIView):
    def get(self,request):
        try:
            date = datetime.today()

            today = date.today()
            seven_day_before = today - timedelta(days=7)
            week_start = date.today()
            week_start -= timedelta(days=week_start.weekday())
            one_week_ago = datetime.today() - timedelta(days=7)

            # get login&logout details with particular values filter yesterday date data

            # queryset = ClockIn.objects.filter(login_date__gte)
            queryset = ClockIn.objects.filter(login_date__gte=one_week_ago).values('login_time','user__name','login_date')

            querySet3 = ClockOut.objects.filter(logout_date__gte=one_week_ago).values('logout_time','user__name','logout_date')

            # add queryset into dataframe
            df1 = pd.DataFrame(queryset)
            df2 = pd.DataFrame(querySet3)

            # rename the colums here user id
            df2.rename(columns={'user__name': 'name'}, inplace=True)

            df1 = df1.sort_values(['user__name', 'login_time'])
            df2 = df2.sort_values(['name', 'logout_time'])

            df = pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)
            df['logout_time'] = pd.to_timedelta(df['logout_time'].astype(str))

            df['login_time'] = pd.to_timedelta(df['login_time'].astype(str))

            df['diiffrences'] = df['logout_time'] - df['login_time']

            diff = df[['login_date', 'user__name', 'name', 'diiffrences']]

            group1 = diff.groupby(['user__name', 'name', 'login_date']).sum('')

            d = group1.reset_index()
            c = d[['diiffrences']]

            # converting the data into dictionary format
            data_dict = d.to_dict('records')

            # dump the dict data into json
            json_data = json.dumps(data_dict, default=str)

            # loads the dump data again ,and send the responce
            python_obj = json.loads(json_data)

            # store the data into database
            for i in range(0, len(python_obj)):
                credit, created = ProductiveHours.objects.get_or_create(user_id=python_obj[i]['user__name'],
                                                                        user=python_obj[i]['name'],
                                                                        login_date=python_obj[i]['login_date'],
                                                                        diiffrences=python_obj[i]['diiffrences'])
                # ProductiveHours.objects.create(user_id=python_obj[i]['user_id'], user=python_obj[i]['user'], login_date=python_obj[i]['login_date'], diiffrences=python_obj[i]['diiffrences'])
            # get the queryset for all data
            obj = ProductiveHours.objects.all()
            df = read_frame(obj)

            # get the latest record from every user
            latest_prod = df.sort_values('diiffrences').groupby(['login_date', 'user_id']).tail(1)

            timer_dict = latest_prod.to_dict('records')

            # dump the data into json format
            timetr_json_data = json.dumps(timer_dict, default=str)
            # loads the data into the format
            timertr_json_data = json.loads(timetr_json_data)
            # send the response
            return Response({"current_week": timertr_json_data}, status=status.HTTP_200_OK)
        except:
            return Response('no time data in your database please check your database',
                            status=status.HTTP_404_NOT_FOUND)



# cuurent month
class Current_Month(generics.GenericAPIView):

    def get(self,request):
        try:
            # current month data
            current_month = datetime.now().month

            # queryset = ClockIn.objects.filter(login_date__gte)
            queryset = ClockIn.objects.filter(login_date__month=current_month).values('login_time','user__name','login_date')

            querySet3 = ClockOut.objects.filter(logout_date__month=current_month).values('logout_time','user__name','logout_date')

            # add queryset into dataframe
            df1 = pd.DataFrame(queryset)
            df2 = pd.DataFrame(querySet3)

            # rename the colums here user id
            df2.rename(columns={'user__name': 'name'}, inplace=True)

            df1 = df1.sort_values(['user__name', 'login_time'])
            df2 = df2.sort_values(['name', 'logout_time'])

            df = pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)
            df['logout_time'] = pd.to_timedelta(df['logout_time'].astype(str))

            df['login_time'] = pd.to_timedelta(df['login_time'].astype(str))

            df['diiffrences'] = df['logout_time'] - df['login_time']

            diff = df[['login_date', 'user__name', 'name', 'diiffrences']]

            group1 = diff.groupby(['user__name', 'name', 'login_date']).sum('')

            d = group1.reset_index()
            c = d[['diiffrences']]

            # converting the data into dictionary format
            data_dict = d.to_dict('records')

            # dump the dict data into json
            json_data = json.dumps(data_dict, default=str)

            # loads the dump data again ,and send the responce
            python_obj = json.loads(json_data)

            # store the data into database
            for i in range(0, len(python_obj)):
                credit, created = ProductiveHours.objects.get_or_create(user_id=python_obj[i]['user__name'],
                                                                        user=python_obj[i]['name'],
                                                                        login_date=python_obj[i]['login_date'],
                                                                        diiffrences=python_obj[i]['diiffrences'])
                # ProductiveHours.objects.create(user_id=python_obj[i]['user_id'], user=python_obj[i]['user'], login_date=python_obj[i]['login_date'], diiffrences=python_obj[i]['diiffrences'])
            # get the queryset for all data
            obj = ProductiveHours.objects.all()
            df = read_frame(obj)

            # get the latest record from every user
            latest_prod = df.sort_values('diiffrences').groupby(['login_date', 'user_id']).tail(1)

            timer_dict = latest_prod.to_dict('records')

            # dump the data into json format
            timetr_json_data = json.dumps(timer_dict, default=str)
            # loads the data into the format
            timertr_json_data = json.loads(timetr_json_data)
            # send the response
            return Response({"Current_mmonth": timertr_json_data}, status=status.HTTP_200_OK)
        except:
            return Response('no time data in your database please check your database',
                            status=status.HTTP_404_NOT_FOUND)


class Logout(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        '''getting serializers data (only refresh token)'''
        sz.is_valid(raise_exception=True)
        '''if token is invalid raise the exception'''
        data = sz.data
        '''assign variable to the serializer data'''

        user = OutstandingToken.objects.get(token=data['refresh']).user_id
        '''getting the user_id based on the token stored in the Outstandingtoken table'''
        m = datetime.today()
        '''getting the today date'''
        name = ClockOut.objects.create(user_id=user, logout_date=m)
        '''creating the new record if it is  new date '''
        name.save()
        sz.save()  ###saving the token in outstanding table
        return Response({'message': 'Succssfully Logout'}, status=status.HTTP_204_NO_CONTENT)
