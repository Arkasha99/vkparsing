from django.contrib.auth import logout
from django.shortcuts import render, redirect, render_to_response
import requests
import pdb

def index(request):
    if request.user.is_staff:
        return render(request, 'vka/index.html')
    elif request.user.is_authenticated:
        screen_name = request.user.username
        new_lst = get_friends(get_id(screen_name),5)
        return render(request,'vka/index.html',context={'new_lst':new_lst})
    else:
        return render(request,'vka/index.html')


#Процедура logout
def log_out(request):
    logout(request)
    return redirect('index')



#Получаем вконтактовский айди авторизованного пользователя
def get_id(screen_name):
    token = 'e35597fde35597fde35597fd2ee339288aee355e35597fdbe26316aa15ceb2c8deec608'
    ver = '5.101'
    response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                            params={
                                'access_token': token,
                                'v': ver,
                                'screen_name': screen_name,
                            })
    parse_id = response.json()
    return(parse_id['response']['object_id'])


#С помощью айди пользователя находим айди 5 рандомных друзей, затем по айди находим их
#имена и создаем список имен
def get_friends(user_id, count, order='random'):
    token = 'e35597fde35597fde35597fd2ee339288aee355e35597fdbe26316aa15ceb2c8deec608'
    ver = '5.101'
    response = requests.get('https://api.vk.com/method/friends.get',
                        params={
                            'access_token': token,
                            'v': ver,
                            'user_id': user_id,
                            'order': order,
                            'count': count
                        })
    data = response.json()
    users = ', '.join(map(str,data['response']['items']))
    response = requests.get('https://api.vk.com/method/users.get',
                       params={
                           'access_token': token,
                           'v': ver,
                           'user_ids': users
                       })
    data_one = response.json()
    return [*[d['first_name']+' '+d['last_name'] for d in data_one['response']]]
