from random import choice, randint,randrange
from datetime import datetime
import asyncio
import os
from random import choice, random
from time import sleep, time
from telethon.sync import TelegramClient
from telethon.sync import events, functions, errors
import telethon
from telethon.tl.functions.contacts import GetContactsRequest, ImportContactsRequest, DeleteContactsRequest, ResolveUsernameRequest

from telethon.tl.types import InputPhoneContact, InputGeoPoint, InputPeerChannel, InputChannel, InputChatPhoto, InputPhoto, InputChatUploadedPhoto, InputFile, InputPeerUser

# ======== token
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.help import GetUserInfoRequest
from telethon.tl.types import ChannelParticipant
from telethon.tl.types import InputChannel, ChannelAdminLogEventsFilter, ChannelParticipantsSearch
from telethon.tl.functions.account import UpdateProfileRequest

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest, DeleteChannelRequest, EditPhotoRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest,GetMessagesReactionsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUserSelf
from telethon.tl.functions.messages import ImportChatInviteRequest
# from telethon.tl.functions.channels import 
# CheckUsernameRequest()
import os,json
from time import time
from starco.debug import Debug
from starco.utils import path_maker
from .utils import *
from starco.proxy import PROXY
import nest_asyncio
nest_asyncio.apply()

class TlgApp:
    def __init__(self, number, key='17203958', hash='82cefc4001e057c9d1488ab90e23d54f', loop=None, debug_mode=True,country_diring=False,auto_connect=True, **kwargs) -> None:
        '''
        relative_path='.'
        path_list =['accounts',number]
        js_path_list =['accounts',number]
        proxy={'proxy_type':'http,socks5','ip','port','username','password'}
        '''
        self.timeout=kwargs.get('timeout',10)
        self.proxy = kwargs.get('proxy')
        relative_path = kwargs.get('relative_path', '.')
        self.debug = Debug(debug_mode, relative_path='.')
        self.number_int = get_number(number)
        if not self.number_int :raise Exception('cant detect number from session_name')
        self.number = f"+{self.number_int}"
        self.auto_connect =   auto_connect   
        
        path_list:list = kwargs.get('path_list', ['accounts',str(self.number_int)])
        js_path_list= kwargs.get('js_path_list', ['accounts',str(self.number_int)])
        
        if country_diring:
            path_list.insert(-1,get_country_name(self.number))
            js_path_list.insert(-1,get_country_name(self.number))

        self.base_path = path_maker(path_list, relative_path)
        self.json_path = path_maker(js_path_list, relative_path)

        self.key = key
        self.hash = hash

        self.path = f'{self.base_path}/{session_number(self.number_int)}'

        self.status = False
        if type(loop) == type(None):
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.client: TelegramClient = None
        self.init_client()
        self.js('last_check_time',int(time()))

        #################

        self.d = {}
        self.events = []
        self.last_schedual = 0  # time()
        self.sleep_min = 20
        self.checked_ids = []

    async def _get_status(self):
        try:
            res = await self.client.get_me()
        except:
            return False
        if res == None:
            return False
        return True

    def get_status(self):

        return self.loop.run_until_complete(self._get_status())

    def connect(self):
        async def act(self: TlgApp):
            try:
                await self.client.connect()
                return True
            except:pass
            return False

        self.loop.run_until_complete(act(self))

    def init_client(self):
        versions = ['9.0', "8.9", "8.4", "9.2", "9.1", "9.3", "8.6", "7.9"]
        appvs = ["7.84", "7.43", "8.0", "4.9", "7.19","7.21", "7.34", "7.42", "7.86", "8.0", "1.34"]
        langs = ["en"]
        device = ''
        # choice(devices)
        version = choice(versions)
        appv = choice(appvs)
        lang = choice(langs)
            
        extra = {
            'device_model': 'Telegram Desktop 4.6.5',
        }
        prx = self.js('proxy')
        if prx:
            extra['proxy'] = PROXY(**prx).make_proxy()

        elif self.proxy:
            extra['proxy'] = PROXY(**self.proxy).make_proxy()

        self.client = TelegramClient(
            session=self.path, 
            api_id=self.key,
              api_hash=self.hash,
              timeout=self.timeout, 
              **extra)
        self.status = True
        def setjs(self,k,v):
            if self.js(k):
                self.js(k,v)
        setjs(self,'session_file',self.number)
        setjs(self,'phone',self.number)
        setjs(self,'register_time',int(time()))
        setjs(self,'app_id',self.key)
        setjs(self,'app_hash',self.hash)
        setjs(self,'app_version',version)
        setjs(self,'avatar',"null")
        setjs(self,'device',device)
        setjs(self,'sex',"null")
        setjs(self,'system_lang_pack',lang)
        setjs(self,'ipv6',self.client._use_ipv6)
        setjs(self,'proxy', self.proxy)
        
        if self.auto_connect:            
            self.connect()

    def js(self,key,value=None):
        if self.json_path:
            # print(key,value)
            js_path = f"{self.json_path}/{self.number}.json"
            
            try:
                with open(js_path,'r') as f:
                    data = f.read()
                data =json.loads(data)
            except:data={}
            if type(value)==type(None):
                return data.get(key)
            data[key]=value
            with open(js_path,'w') as f:
                data = f.write(json.dumps(data))

    def get_status(self):
        return self.loop.run_until_complete(self._get_status())

    def disconnect(self):
        async def act(self):
            try:
                await self.client.disconnect()
                self.status = False
                return
            except:
                try:
                    await self.client.disconnect()
                    self.status = False
                    return
                except:
                    pass
        return self.loop.run_until_complete(act(self))

    def do_login(self, first_step=False, **args):
        '''
            steps: 0=> auto
                   1=>send code 
                   2=> enter code :args= code
                   3=> enter 2fa   :args= p2fa
        '''
        
        step = self.d.get('step')
        if first_step:
            step = 0
        if step == 0:
            self.d['code'] = ''
            self.d['hash'] = ''
            self.d['p2fa'] = ''
            step = 1
        hash = args.get('hash', '')
        code = str(args.get('code', ''))
        p2fa = str(args.get('p2fa', ''))
        if step == 1:
            if self.get_status():
                return 'session_is_active'
            out = self.loop.run_until_complete(self._send_code_request())
            if out[0]:
                self.d['step'] = 2
                self.d['hash'] = out[1]
                return ''
            return out[1]
        elif step == 2:
            if hash == '':
                hash = self.d.get('hash', '')
            out = self.loop.run_until_complete(self.sign_in(code, hash))
            if out[0]:
                self.d['step'] = 0
                # me = self.client.get_me()
                # self.js('first_name', me.first_name)
                # self.js('last_name', me.last_name)
                # self.js('username', me.username)
            if out[1] == 'need_pass2':
                self.d['step'] = 3
                self.d['code'] = code
                self.d['hash'] = hash
            return out[1]
        elif step == 3:
            if code == '':
                code = self.d.get('code', '')
            if hash == '':
                hash = self.d.get('hash', '')
            out = self.loop.run_until_complete(
                self.sign_in(code, hash, p2fa))
            if out[0]:
                self.d['step'] = 0
                # me = self.client.get_me()
                # self.js('first_name', me.first_name)
                # self.js('last_name', me.last_name)
                # self.js('username', me.username)
                self.js('password_2fa',p2fa)
            return out[1]
        self.d['step'] = 0
        return False, 'wrong parameter in (do_login)'

    def login_loop(self):
        res = self.do_login(first_step=True)
        if res == 'session_is_active':
            # print(res)
            return
        inp = input('code:')
        while True:
            res = self.do_login(code=inp)
            if res == 'need_pass2':
                inp = input('pass2:')
                break
            elif res != '':
                # print(res)
                inp = input('code:')
            else:
                print('success login')
                return

        while True:
            res = self.do_login(p2fa=inp)
            if res != '':
                # print(res)
                inp = input('pass2:')
            else:
                print('success login')
                return
    
    def send_code_request(self):
        return self.loop.run_until_complete(self._send_code_request())

    async def _send_code_request(self):
        '''
            if have error session been removed
        '''
        try:

            auth = await self.client.send_code_request(self.number)
            auth_hahs = auth.phone_code_hash

            return True, auth_hahs
        except errors.PhoneNumberBannedError:
            return False, f'⚠️خطا در ارسال کد به شماره {self.number} شماره شما از تلگرام مسدود شده است !'
        except errors.PhoneNumberInvalidError:
            return False, f'⚠️ شماره {self.number} اشتباه است.'
        except errors.FloodWaitError as e3:
            return False, f'⏳ شماره {self.number} از سمت تلگرام محدود شده است و تا {e3.seconds} ثانیه دیگر قابل ثبت نیست.'
        except errors.PhoneNumberOccupiedError:
            return False, '⚠️خطا در ارسال کد !'
        except errors.PhoneNumberUnoccupiedError:

            return False, '⚠️خطا در ارسال کد !'
        except ConnectionError:
            return False, '❌ارور در ارسال کد لطفا دوباره امتحان کنید.'
        except Exception as e:
            self.debug.debug(e)
            return False, '⚠️خطا در ارسال کد !'

    async def sign_in(self, code, hash, p2fa=None):
        try:
            await self.client.sign_in(phone=f'{self.number}', code=(code), phone_code_hash=hash)
            return True, ''

        except errors.SessionPasswordNeededError as e:
            if p2fa:
                try:
                    await self.client.sign_in(password=str(p2fa))
                    return True, ''
                except Exception as e:

                    return False, "wrong_pass2"
            else:
                return False, "need_pass2"

        except errors.PhoneCodeExpiredError:

            return False, 'expied_code'
        except errors.PhoneCodeInvalidError:

            return False, 'wrong_code'
        except Exception as e:
            self.debug.debug(e)
            return False, 'unknow_error'

    async def sign_up(self, code, hash):
        try:
            fname = 'fname'
            lname = 'lname'

            await self.client.sign_up(code=code, first_name=fname, last_name=lname, phone_code_hash=hash)

            return True, ''
        except errors.SessionPasswordNeededError:

            return False, "need_pass2"
        except errors.PhoneCodeExpiredError:

            return False, 'expied_code'
        except errors.PhoneCodeInvalidError:

            return False, 'wrong_code'
        except Exception as e:
            self.debug.debug(e)
            return False, 'unknow_error'

    def get_telegram_code(self):
        async def act(self):
            try:
                async for dialog in self.client.iter_dialogs():
                    tmp = dialog.to_dict()
                    if tmp.get('_') == 'Dialog' and tmp.get('name') == 'Telegram':
                        code = dialog.message.message
                        if 'Login code' in code:
                            find = re.findall('Login code: (\d{5}).',code)
                            if find:
                                return find[0]
                    break
                        

            except Exception as e:
                self.debug.debug(e)
        return self.loop.run_until_complete(act(self))

    def destroy_others_session(self):
        async def act(self: TlgApp):
            async with self.client as client:
                result = await client(functions.account.GetAuthorizationsRequest())
                for i in result.authorizations:
                    i = i.to_dict()
                    if not i['current']:
                        await client(functions.account.ResetAuthorizationRequest(hash=i['hash']))

        return self.loop.run_until_complete(act(self))

    def remove_session(self):
        self.disconnect()
        try:os.remove(self.path)
        except:pass

    def just_this_sessions_is_active(self):
        async def act(self: TlgApp):
            res = False
            async with self.client as client:
                result = await client(functions.account.GetAuthorizationsRequest())
                current_exist = False
                for i in result.authorizations:
                    i = i.to_dict()
                    print(i)
                    if i['current']:
                        current_exist = True
                res = len(result.authorizations) == 1 and current_exist
            return res
        return self.loop.run_until_complete(act(self))

    def do_change_or_set_2fa(self, old_p2fa: str, new_p2fa: str):
        async def act(self: TlgApp, old_p2fa, new_p2fa):
            if old_p2fa == '':
                try:
                    await self.client.connect()
                    await self.client.edit_2fa(new_password=new_p2fa)
                    self.js('password_2fa',new_p2fa)
                    return True
                except Exception as e:
                    self.debug.debug(e)
                    return False
            else:
                try:
                    if str(new_p2fa) != str(old_p2fa):
                        await self.client.connect()
                        await self.client.edit_2fa(str(old_p2fa), new_password=new_p2fa)
                        self.js('password_2fa',new_p2fa)
                        return True
                except Exception as e:
                    self.debug.debug(e)
                    return False
            return True

        return self.loop.run_until_complete(act(self, old_p2fa, new_p2fa))

    def change_info(self,  first_name=None, last_name=None, bio=None):
        async def act():
            try:
                await self.client(UpdateProfileRequest(first_name=first_name, last_name=last_name, about=bio))
                return True
            except Exception as e:
                self.debug.debug(e)
            return False

        return self.loop.run_until_complete(act())
    
    def change_profile_photo(self, photo_path:str):
        async def act():
            try:
                pic = await self.client.upload_file(photo_path)
                print(pic)
                await self.client(UploadProfilePhotoRequest(file=pic))
                return True
            except Exception as e:
                self.debug.debug(e)

            return False

        return self.loop.run_until_complete(act())


    def send_message(self,entity, message,delete_dialog=False,**kargs):
        async def act(self:TlgApp,entity, message,**kargs):
            res = await self.client.send_message(entity, message,**kargs)
            if delete_dialog:
                await self.client.delete_dialog(entity)
            return res
        return self.loop.run_until_complete(act(self,entity, message,**kargs))
        
    def download(self,entity,size,out_file_name):
        async def act(self:TlgApp,entity,size,out_file_name):
            async for message in self.client.iter_messages(entity,limit=1, reverse=False):
                try:                
                    if type(message.media)!=type(None):
                        print(message.media)
                        gsize=message.media.document.size
                        if size==gsize:
                            await self.client.download_media(message,out_file_name)
                            return True
                except:pass
            return False

        return self.loop.run_until_complete(act(self,entity,size,out_file_name))

    def upload(self,entity,path,caption,force_document=False):
        async def act(self:TlgApp,entity,path,caption,force_document):
            try:
                res = await self.client.send_file(entity,path,caption=caption,force_document=force_document)
                return res
            except:pass
        return self.loop.run_until_complete(act(self,entity,path,caption,force_document))
    
    def seen_post(self, entity, ids:list[int]=[],limit=5):

        async def _seen_post():
            '''
            if ids==[] use limit
            '''
            try:
                if not ids:
                    list_of_id = []
                    async for msg in self.client.iter_messages(entity, limit=limit):
                        list_of_id += [int(msg.id)]
                else:list_of_id = ids
                await self.client(GetMessagesViewsRequest(peer=entity, id=list_of_id, increment=True))

                return True
            except Exception as e:
                self.debug.debug(e)
            return False
            
        return self.loop.run_until_complete(_seen_post())
        
    def react_post(self, entity, ids:list[int]=[],limit=5):

        async def _react_post():
            '''
            if ids==[] use limit
            '''
            try:
                if not ids:
                    list_of_id = []
                    async for msg in self.client.iter_messages(entity, limit=limit):
                        list_of_id += [int(msg.id)]
                else:list_of_id = ids
                await self.client(GetMessagesReactionsRequest(peer=entity, id=list_of_id))

                return True
            except Exception as e:
                self.debug.debug(e)
            return False
            
        return self.loop.run_until_complete(_react_post())

    def join_channel(self, channel):
        async def _join_channel():
            try:
                res = await self.client(JoinChannelRequest(channel))
                print(res)
                return True
            except Exception as e:
                self.debug.debug(e)
                return False
        return self.loop.run_until_complete(_join_channel())

    def leave_channel(self, channel):
        async def _leave_channel():
            try:
                await self.client(LeaveChannelRequest(channel))
                return True
            except Exception as e:
                self.debug.debug(e)
        return self.loop.run_until_complete(_leave_channel())
    
    def set_channel_photo(self, channel, pic):
        async def _set_channel_photo():
            try:
                upload_file_result = await self.client.upload_file(file=pic)
                input_chat_uploaded_photo = InputChatUploadedPhoto(
                    upload_file_result)
                await self.client(EditPhotoRequest(channel, input_chat_uploaded_photo))
                return True
            except Exception as e:
                self.debug.debug(e)
            return False
        return self.loop.run_until_complete(_set_channel_photo())
        
    def create_public_channel(self, title, username,  firt_msg=None):

        async def _create_public_channel():
            try:
                createdPrivateChannel = await self.client(CreateChannelRequest(title=title,
                                                                            about='',
                                                                            geo_point=InputGeoPoint(
                                                                                lat=1,
                                                                                long=2,
                                                                                accuracy_radius=42
                                                                            ),
                                                                            address='address'
                                                                            ))
                # if you want to make it public use the rest
                newChannelID = createdPrivateChannel.__dict__[
                    "chats"][0].__dict__["id"]
                newChannelAccessHash = createdPrivateChannel.__dict__[
                    "chats"][0].__dict__["access_hash"]
                desiredPublicUsername = username
                CH = InputPeerChannel(channel_id=newChannelID,
                                    access_hash=newChannelAccessHash)
                checkUsernameResult = await self.client(CheckUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))
                if (checkUsernameResult == True):
                    try:
                        publicChannel = await self.client(UpdateUsernameRequest(CH, desiredPublicUsername))
                    except:
                        pass
                    
                    if firt_msg:
                        await self.client.send_message(CH,firt_msg)
                    return True
                else:
                    await self.client(DeleteChannelRequest(CH))
            except Exception as e:
                self.debug.debug(e)
            return False

        return self.loop.run_until_complete(_create_public_channel())

    def get_all_dialogs(self):
        '''return groups entity'''
        async def act():
            ids = []
            try:
                async for dialog in self.client.iter_dialogs():
                    tmp = dialog.to_dict().get('entity', {})
                    ids += [tmp.to_dict()]
            except Exception as e:
                self.debug.debug(e)
            return ids
        return self.loop.run_until_complete(act())

    def get_channel_id(self, inputs):

        async def _get_channel_id():
            res = 0
            try:
                res = await self.client.get_entity(inputs)
                res = res.id
            except Exception as e:
                self.debug.debug(e)

            try:
                res = int(res)
            except:
                pass

            return res
        return self.loop.run_until_complete(_get_channel_id())

    def export_contacts(self,convert_to_dict=True):

        async def _export_contacts():
            try:
                contacts = await self.client(GetContactsRequest(0))
                if len(contacts.users) > 0:
                    res = []
                    for i in contacts.users:
                        if convert_to_dict:
                            i = i.to_dict()
                        res += [i]
                    return res
                return []
            except Exception as e:
                return []
        return self.loop.run_until_complete(_export_contacts())

    def import_contacts(self, list_number:list):

        async def _import_contacts():
            try:
                contacts = []
                for i in list_number:
                    number = '+'+(str(i).replace('+', ''))
                    contacts += [InputPhoneContact(client_id=randrange(-2**63, 2**63),
                                                phone=number, first_name=number, last_name='')]
                res = await self.client(ImportContactsRequest(contacts=contacts))

                return res

            except Exception as e:
                self.debug.debug(e)
            return []
        return self.loop.run_until_complete(_import_contacts())

    def delete_contacts(self, id:list):
        async def _delete_contacts():
            try:
                await self.client(DeleteContactsRequest(id))
                return True
            except Exception as e:
                self.debug.debug(e)
        return self.loop.run_until_complete(_delete_contacts())

    def get_all_groups(self):
        '''return groups entity'''
        async def _get_all_groups():
            ids = []
            try:
                async for dialog in self.client.iter_dialogs():
                    tmp = dialog.to_dict().get('entity', {})
                    if tmp:
                        entity = tmp
                        tmp = tmp.to_dict()
                        if tmp['_'] == 'Channel' and (tmp['gigagroup'] or tmp['megagroup']) and not tmp['restricted']:
                            ids += [entity]
            except Exception as e:
                self.debug.debug(e)
            return ids
        return self.loop.run_until_complete(_get_all_groups())

    def number_maker(self, count=1):
        pidh = ['911', '912', '933', '936', '937', '938', '939', '902', '990']
        res = []
        for _ in range(count):
            number = f"+98{choice(pidh)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
            res += [number]
        return res

    def get_user_status_by_username(self, username):
        async def _get_user_status_by_username():
            try:
                res = await self.client.get_entity(username)
                status = res.status.to_dict()['_']
                return status
            except:
                pass
            return ''
        return self.loop.run_until_complete(_get_user_status_by_username())

    def on_new_message(self,func,**kargs):
        '''
        func(self:TlgApp,event,**kargs)
        '''
        @self.client.on(event=events.NewMessage)
        async def action(event):
            try:
                func(self,event,**kargs)
            except Exception as e:
                print(e)

        self.client.run_until_disconnected()

    def get_user_info(self, PeerUser):
        async def _get_user_info():
            res = await self.client(GetFullUserRequest(PeerUser))
            return res
        return self.loop.run_until_complete(_get_user_info())

    def delete_old_dialoges(self,after_sec=864000):

        async def _delete_old_dialoges():
            out=0
            try:
                async for dialog in self.client.iter_dialogs():
                    tmp = dialog.to_dict()
                    if tmp.get('_') == 'Dialog':
                        send_time = tmp['message'].to_dict()['date'].timestamp()
                        past = int((int(time()) - send_time))
                        if past > after_sec:
                            user = tmp['entity']
                            await self.client.delete_dialog(user)
                            out+=1


            except Exception as e:
                self.debug.debug(e)
            return out

        return self.loop.run_until_complete(_delete_old_dialoges())

    def copy_posts(self, from_id:int, to_id:int,offset_id:int, limit:int):
        '''return list of copied id'''
        async def _cp_posts():
            entity = {}
            out = []
            async for dialog in self.client.iter_dialogs():
                tmp = dialog.to_dict().get("entity", {})
                if tmp:
                    if tmp.to_dict().get('id') == from_id:
                        entity = tmp
                        break
            if entity:
                async for message in self.client.iter_messages(entity,offset_id=offset_id,limit=limit, reverse=True):
                    try:
                        id = message.to_dict().get('id')
                        await self.client.send_message(to_id, message)
                        out += [id]
                    except:
                        pass
            return out
        return self.loop.run_until_complete(_cp_posts())
        
    def get_members_info(self,username=None,id=None,access_hash=None):
        '''
        username for public group
        id,access hash for private

        '''
        async def _get_group_members_info():
            out = []
            if username!=None:
                o= await self.client(ResolveUsernameRequest(username))
                id = o.chats[0].id
                access_hash = o.chats[0].access_hash
            chat = InputChannel(id,access_hash)
            async for i in self.client.iter_participants( chat, limit=10000, aggressive=True):
                    try:
                        out += [i.to_dict()]
                    except:pass
            return out
        return self.loop.run_until_complete(_get_group_members_info())

    def join_private_group(self, group_hash_id):
        '''return id,access_hash'''
        async def _join_group():
            try:
                res = await self.client(ImportChatInviteRequest(group_hash_id))
                chats = res.to_dict().get('chats')
                if chats:
                    chat = chats[0]
                    id = chat['id']
                    access_hash=  chat['access_hash']
                return id,access_hash
            except Exception as e:
                print(e)
            return None,None
        return self.loop.run_until_complete(_join_group())