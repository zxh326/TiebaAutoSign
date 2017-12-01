from django.db.models import Q
from datetime import datetime
from .models import UserProfile
from .models import TiebaList
from .util import get_tbs, do_sign
from threading import Thread
# from multiprocessing import Pool


def thread_sign(user_tbs, user_bduss, tiebas):
    for to_sign_tieba in tiebas:
        # print (to_sign_tieba.fid,to_sign_tieba.tiebaname)
        info = do_sign(user_tbs, user_bduss, to_sign_tieba.fid,
                       to_sign_tieba.tiebaname)

        print(info)
        error_code = info['error_code']
        to_sign_tieba.error_code = error_code

        # 没有消息就是最好的消息
        """error_code
            0      => 成功
            160002 => 成功
            340011 => 成功
            340006 => 失败/（贴吧被封忽略）
        """
        if error_code == '0' or error_code == '160002' or error_code == '340011' or error_code == '340006':
            if error_code == '0':
                to_sign_tieba.error_msg = 'success'
            else:
                to_sign_tieba.error_msg = info['error_msg']
            to_sign_tieba.is_sign = datetime.now()
        else:
            res_code = 1
            to_sign_tieba.error_msg = info['error_msg']

        to_sign_tieba.save()
    # print ()


def do_sign_user(user_id):
    """do_sign_user
    params:
        user_id
    return:
        res_code
        0 done
        1 部分失败
    """
    res_code = 0
    to_sign_tiebas = TiebaList.objects.filter(
        Q(user_id=user_id), Q(is_sign__lt=datetime.now()))

    if len(to_sign_tiebas) == 0:
        return res_code

    user_bduss = UserProfile.objects.get(user_id=user_id).bduss
    user_tbs = get_tbs(user_bduss)

    splist = lambda l: [l[i:i + 20] for i in range(len(l)) if i % 20 == 0]

    # print (len(splist(to_sign_tiebas)))
    # for to_sign_tieba in to_sign_tiebas:
    #     # print(to_sign_tieba.tiebaname)
    #     info = do_sign(user_tbs, user_bduss, to_sign_tieba.fid,
    #                    to_sign_tieba.tiebaname)

    #     print (info)
    Threads = list()
    for Tmps in splist(to_sign_tiebas):
        # print (Tmps)
        Threads.append(Thread(target=thread_sign,
                       args=(user_tbs, user_bduss, Tmps)))
    for t in Threads:
        t.start()
    for t in Threads:
        t.join()

    return res_code


def doo():
    """
        进程池 pool > 5 
        todo 用户过多 过滤 标记用户
    """

    all_users = UserProfile.objects.filter(~Q(bduss='null'))

    for tmp in all_users:
        do_sign_user(tmp.user_id)

    # print('1')

