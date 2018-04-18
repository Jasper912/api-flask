### 生产环境部署

#### virtualenv
    pip install virtualenv

#### flask
    (env)pip install -r requrments

## uwsgi

* pip install uwsgi==2.0.15

    ```
    auto-procname = true
    procname-prefix-spaced = flipgame-actapi
    socket = 0.0.0.0:2360
    chmod-socket=770
    master = true
    wsgi-file = run.py
    callable = app
    touch-reload = /data/vhost/flipgame-actapi/reload
    uid = www-data
    gid = www-data
    processes = 1
    max-requests = 100000
    disable-logging = true
    virtualenv = /home/wbdev/virtualenv/flipgame-actapi
    chdir = /data/vhost/flipgame-actapi/
    gevent = 100
    gevent-monkey-patch = true
    daemonize = /data/log/flipgame-actapi/uwsgi.log
    stats = 127.0.0.1:9198
    pidfile = /tmp/uwsgi-flipgame-actapi.pid

    ```

* 启动:

    ```
        uwsgi --ini uwsgi.ini
    ```

* 修改配置文件重启uwsgi:

    ```
        uwsgi --reload /tmp/uwsgi-flipgame-actapi.pid
    ```

* 查看uwsgi进程状态:

    ```
        uwsgitop 127.0.0.1:9198
    ```

* ps查看uwsgi master进程:

    ```
        ps aux |  grep flipgame-actapi // auto-procname改变了进程的名字, grep uwsgi 搜索不出东西
    ```
