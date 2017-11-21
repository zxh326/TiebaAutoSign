## TiebaAutoSign
#### 设计初版需求：


* #### 数据库设计：
    * `User` 表 ：
        * `id`: `primarykey NOTNULL AUTO` 
        * `user_name`：`primarykey`,`NOT NULL` 登陆用户名之一
        * `email`：`primarykey`,`NOT NULL` 登陆用户名之一
        * `password`：`sha256 salt` 
        * `is_admin`：`check 1 or 0` 
        * `is_active`：`check 1 or 0` 
        * `regis_date`： `date`
    
    * `User_profile`：
        * `uid `：`FROREIGN KEY (User.id)`
        * `bduss`：`char`
        * `level`：`int`
        * `tieba_count`：
        * `sign_day_sum`：总签到天数
        * `sign_count`：当天已签到数量

    * `tieba_list`：
        * `uid`:`FROREIGN KEY (User_profile.uid)`
        * `fid`:贴吧uid 
        * `tieba_name`：贴吧名字
        * `error_code`：错误代码，[0,10042,99999]
        * `error_info`：签到消息,默认NULL
        * `sign_status`: 当天签到状态 （每晚更新与签到冲突暂时没想到比较完善解决办法）
    
    * `session` : django

    * `system_config`:
        pass



        

* #### 功能：
    * 签到
        * 根据设置时间（默认1点）对`tieba_list`所有表进行访问
          涉及到访问量大考虑分表，
            * 考虑两个签到模式
                * 1，随机抽取贴吧签到，多个用户并行（效率慢，对用户公平）
                * 2，根据用户注册顺序进行抽取贴吧签到，单一用户（效率快）
                * 暂时依照第一类方法做
                
    * 绑定贴吧BDUSS之后自动进行一次
    * 更新贴吧表 （1.查重更新，2.覆盖更新）
    * 当天 实时签到数量统计


* #### 页面
    * **已登陆**：
        * **菜单**：
            * **个人资料**：
                * 个人昵称/邮箱
                * 百度BDUSS绑定
                * 邮件订阅每日签到Status（可选）
                * 更改密码
                * **TODO** 头像设置/以及百度贴吧昵称获取

            * [ 管理员 ]
                * **用户管理**
                    * 是否绑定贴吧
                    * 贴吧个数
                    * 封禁
                    * 删除
                    * **TODO** level （级别）

                * **系统设置**
                    * 站点昵称
                    * 每日签到时间（默认 0）（django-crontab）
                    * 站长邮箱SMTP设置
                    * 签到进程数 （process）（4）
                    * **TODO** 注册是否需要验证码
                    * **TODO** 注册是否需要邀请码

                * **统计信息**
                    * 所有用户签到统计（**TODO** 图表形式 ）
