from django.shortcuts import render
import facebook

def get_messages(request,data):
    print(data)
    # print(request.GET['alldata'])
    all_data = request.session['alldata']
    msg_list = {}
    for key, val in all_data.items():
        for key2, val2 in all_data[key].items():
            if key2 =='username':
                username = val2
            if key2 =='msgs':
                msg_list[username] = val2
    final_dict ={}
    for key,val in msg_list.items():
        if key == data:
            final_dict = msg_list[key]
        else:
            pass
    return render(request,'chatui.html',{'msgs':final_dict,'alldata':all_data,'user':data})

def get_conv_data(api,conv,args):
    conv_data_dict = {}
    for chat_id in conv['data']:
        print(chat_id['id'])
        args_pars = {'fields' : 'participants'}
        sender = api.get_object(chat_id['id'],**args_pars)
        # print(sender)
        username =sender['participants']['data'][0]['name']
        userid=sender['participants']['data'][0]['id']
        chat_id = chat_id['id']
        conv_data_dict[str(chat_id)] = {}
        conv_data_dict[chat_id]['userid'] = userid
        conv_data_dict[chat_id]['username'] = username
        # print("===============")
        msg = api.get_object(chat_id+'/messages')
        # print(msg)
        msg_list= []
        for el in msg['data']:
            msg =[]
            content = api.get_object( el['id'], **args)   #adding the field request
            # print(content['message'],el['created_time'])
            msg.append(content['message'])
            msg.append(el['created_time'])
            msg_list.append(msg)
        conv_data_dict[chat_id]['msgs'] = msg_list
        # print(conv_data_dict)
        # print("====================================>\n")
    return conv_data_dict

# Create your views here.
def index(request):
    at = 'EAAITB2zlt7gBAChAGq0Fd3vvy1ldHeTWq7Ez4s9YvOSiZC4ZCVOYIOTx1XUxAPtDggtdZAwPybCZCvH5h7op94wY9c4NuADG4y5AvPttyGYXnxsPqlZAD4PdOwwVRIJGdoZB2MTinB4c81AUdO6E6GatDZBwEzjqH6wCntzFALOeuYZCDqWInlSZAEIMT12VSl7UZD'
    pid = '159212752918254'
    api = facebook.GraphAPI( at )
    args = {'fields' : 'message'}  #requested fields
    conv = api.get_object( 'me/conversations')
    all_data = get_conv_data(api,conv,args)
    request.session['alldata'] = all_data
    return render(request,'home.html',{'alldata':all_data})