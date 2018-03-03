# Front and back end of the separation of the blog project - back-end projects

Blog has been online, welcome to browse：[https://blog.coderap.com/](https://blog.coderap.com/)

> [中文版说明](https://github.com/LennonChin/BlogBackendProject/blob/master/README_zh-cn.md)

> This repository stores the backend code for blog entries, built using Django and the Django Rest Framework.

> Note: The front-end code repository linked to this repository is linked here [Blog-Frontend-Project] (https://github.com/LennonChin/Blog-Frontend-Project) and the front-end code is implemented using Vue.js + Vue-Router + iView.js.

Control Panel effect display：：

![Home Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend1.png)

![Book List Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend2.png)

![All Post List Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend3.png)

![Add Article Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend4.png)

![Add Article Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend5.png)

![Add Article Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/backend6.png)

## Overall technology stack

1. Python environment: Python 3.6.2

2. Mainly dependent

- [Django==1.10.8](https://github.com/django/django)
- [djangorestframework==3.6.3](https://github.com/encode/django-rest-framework)

> Note: For more technical stack dependencies, see the `requirements.txt` file

## Implemented basic functions

Back-end project has achieved 19 interfaces, the main function points are as follows:

1. The realization of the three sections: articles, atlas and photography, respectively, corresponding to the three different modes of presentation; at the same time to achieve time-axis archiving section;
2. Implementation of the management console in the three sections of the article's release, you can publish Markdown format article (using EditorMD editor);
3 comment function, the current method is to use the nickname + email, the first comment will verify the mailbox (by sending a verification code);
4. Achieve the article encryption function;
5. Implementation of the seven cattle cloud storage services docking, publishing reviews and other operations will upload the image data to the seven Niuniu; currently does not provide the corresponding services within the project, such as the need to docking please buy seven Niuniu storage object services;

> Note: The xadmin, EditorMD and other plug-ins used in the project are developed for the second time. In order to cooperate with the project-specific functions, please do not change the plug-in easily.

## Next will be achieved

1. Access GitHub, WeChat, Weibo, Facebook and other third-party login comments.
2. Add more columns.

## How to use

1. Clone this project
2. local installation of Python3 and pip environment;
3. After installing the virtualenv and virtualenvwrapper environment, execute the following command to create a virtual environment:

```bash
# Create a workspace
> mkvirtualenv BlogBackend
# Activate the workspace
> workon BlogBackend
# Change to the root directory of this project, Install dependencies
> pip install -r requirements.txt
```

4. Next, if you are using PyCharm as a development environment, modify its Project Interpreter to workspace we made above.
5. In this project, sensitive account information is not provided, but stored in `private.py` file, this file is not managed to the warehouse, so you need to create a `private.py` file in the same level `setting.py` file Document, which reads as follows:

```python
#! / usr / bin / python3
# - * - coding: utf-8 - * -
# @Time: 2017/12/29 6:01 PM
# @Author: LennonChin
# @Email: i@coderap.com
# @File: private.py
# @Software: PyCharm

# Database connection configuration
DATABASE_CONFIG = {
    'ENGINE': '', # Database Engine
    'NAME': '', # database name used in the database
    "USER": '', # database user name
    "PASSWORD": '', # database password
    "HOST": '', # database address
    'OPTIONS': {
        "init_command": "SET default_storage_engine = INNODB;",
    }
}

# Send mail server configuration
EMAIL_CONFIG = {
    'EMAIL_HOST': "", # mail server address
    'EMAIL_PORT': 25, # mail server port, usually 25
    'EMAIL_HOST_USER': "", # mail server account
    'EMAIL_HOST_PASSWORD': "", # mail server password
    'EMAIL_USE_TLS': False, # Whether to use TLS encryption connection, generally not used
    'EMAIL_FROM': "" # This item is generally the same as EMAIL_HOST
}

# Qiniu Yun related configuration
PRIVATE_QINIU_ACCESS_KEY = '' # Qiniu Access key
PRIVATE_QINIU_SECRET_KEY = '' # Qiniu Secret key
PRIVATE_QINIU_BUCKET_DOMAIN = '' # Qiniu Bucket domain
PRIVATE_QINIU_BUCKET_NAME = '' # Qiniu name

PRIVATE_MEDIA_URL_PREFIX = '' # Resource prefix used when accessing Cattle Cloud
```
6. Configure the above configs, use the following command to migrate the table:

```bash
> python manage.py makemigrations
> python manage.py migrate
```

> Note: If the migration fails, you can migrate by user, material, base, user_operation, index and remaining modules in that order.

7. Then start the project directly use the following command:

```python
> python manage.py runserver 127.0.0.1:8000
```

By default, if you run the evelopment Server after running '127.0.0.1: 8000`, the provided interface is at http://127.0.0.1:8000/api`, background management address `http://127.0.0.1: 8000/xadmin`.

## License

[Apache-2.0] (https://opensource.org/licenses/Apache-2.0)

Copyright (c) 2016-present, LennonChin