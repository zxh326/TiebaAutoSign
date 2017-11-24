from django.db.models import Q
from datetime import datetime
from .models import UserProfile
from .models import TiebaList
from .util import get_tbs, do_sign
# from multiprocessing import Pool


def do_sign_user(user_id):
    """do_sign_user
        0       成功
        160002  成功
        340011  成功
        340006  失败/忽略
    """

    to_sign_tiebas = TiebaList.objects.filter(user_id=user_id)

    user_bduss = UserProfile.objects.get(user_id=user_id).bduss

    # print (len(to_sign_tiebas))

    user_tbs = get_tbs(user_bduss)

    for to_sign_tieba in to_sign_tiebas:
        info = do_sign(user_tbs, user_bduss, to_sign_tieba.fid,
                       to_sign_tieba.tiebaname)
        error_code = info['error_code']
        to_sign_tieba.error_code = error_code
        # 没有消息就是最好的消息
        if error_code == 0 or error_code == 160002 or error_code == 1101 or error_code == 1102:
            pass
        try:
            to_sign_tieba.error_msg = info['error_msg']
        except:
            to_sign_tieba.error_msg = 'success'

        to_sign_tieba.is_sign = datetime.now()
        to_sign_tieba.save()
    return True


def doo():
    # all_users = UserProfile.objects.filter(~Q(bduss='null'))
    # for tmp in all_users:
    #     do_sign_user(tmp.user_id)
    
    print('1')
