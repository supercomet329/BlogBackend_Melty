# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-23 03:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='标题', max_length=100, verbose_name='标题')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='material/banner/image/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('index', models.IntegerField(default=0, help_text='顺序', verbose_name='顺序')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialCamera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(help_text='设备', max_length=30, verbose_name='设备')),
                ('version', models.CharField(help_text='版本', max_length=200, verbose_name='版本')),
                ('environment', models.CharField(help_text='环境', max_length=200, verbose_name='环境')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '相机型号',
                'verbose_name_plural': '相机型号列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='类别名', max_length=30, verbose_name='类别名')),
                ('subname', models.CharField(default='', help_text='别名', max_length=30, verbose_name='别名')),
                ('code', models.CharField(default='', help_text='code', max_length=30, verbose_name='code')),
                ('desc', models.TextField(default='', help_text='类别描述', verbose_name='类别描述')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='material/category/image/%Y/%m')),
                ('category_type', models.CharField(choices=[('1', '一级类目'), ('2', '二级类目'), ('3', '三级类目')], help_text='类目级别', max_length=20, verbose_name='类目级别')),
                ('is_tab', models.BooleanField(default=False, help_text='是否导航', verbose_name='是否导航')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('parent_category', models.ForeignKey(blank=True, help_text='父目录', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='material.MaterialCategory', verbose_name='父类目级别')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialCommentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_content', models.TextField(help_text='原始内容', verbose_name='原始内容')),
                ('formatted_content', models.TextField(blank=True, help_text='处理后内容', null=True, verbose_name='处理后内容')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '评论详细信息',
                'verbose_name_plural': '评论详细信息列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialCommentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_level', models.IntegerField(default=0, help_text='评论级别', verbose_name='评论级别')),
                ('like_num', models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数')),
                ('unlike_num', models.IntegerField(default=0, help_text='反对数', verbose_name='反对数')),
                ('comment_num', models.IntegerField(default=0, help_text='评论数', verbose_name='评论数')),
                ('is_hot', models.BooleanField(default=False, help_text='是否热门', verbose_name='是否热门')),
                ('is_recommend', models.BooleanField(default=False, help_text='是否推荐', verbose_name='是否推荐')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='user.GuestProfile', verbose_name='作者')),
                ('parent_comment', models.ForeignKey(blank=True, help_text='根评论', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comment', to='material.MaterialCommentInfo', verbose_name='根评论')),
            ],
            options={
                'verbose_name': '评论基本信息',
                'verbose_name_plural': '评论基本信息列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='版权名', max_length=30, verbose_name='版权名')),
                ('subname', models.CharField(help_text='版权别名', max_length=30, verbose_name='版权别名')),
                ('desc', models.CharField(blank=True, help_text='简介', max_length=255, null=True, verbose_name='简介')),
                ('link', models.URLField(blank=True, help_text='版权参考链接', null=True, verbose_name='版权参考链接')),
                ('color', models.CharField(choices=[('#878D99', '灰色'), ('#409EFF', '蓝色'), ('#67C23A', '绿色'), ('#EB9E05', '黄色'), ('#FA5555', '红色')], default='blue', help_text='颜色', max_length=20, verbose_name='颜色')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '授权',
                'verbose_name_plural': '授权列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=30, verbose_name='名称')),
                ('desc', models.CharField(help_text='简介', max_length=100, verbose_name='简介')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='material/master/image/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('experience', models.FloatField(default=0, help_text='熟练度', verbose_name='熟练度')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '技能',
                'verbose_name_plural': '技能列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='标题', max_length=100, verbose_name='标题')),
                ('subtitle', models.CharField(blank=True, help_text='子标题', max_length=100, null=True, verbose_name='子标题')),
                ('abstract', models.CharField(blank=True, help_text='摘要', max_length=255, null=True, verbose_name='摘要')),
                ('desc', models.CharField(blank=True, help_text='简介', max_length=255, null=True, verbose_name='简介')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='material/picture/image/%Y/%m', verbose_name='图片')),
                ('link', models.URLField(blank=True, help_text='链接', null=True, verbose_name='链接')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('camera', models.ForeignKey(blank=True, help_text='拍摄相机', null=True, on_delete=django.db.models.deletion.CASCADE, to='material.MaterialCamera', verbose_name='拍摄相机')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=30, verbose_name='名称')),
                ('desc', models.CharField(help_text='简介', max_length=100, verbose_name='简介')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='material/social/image/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '社交平台',
                'verbose_name_plural': '社交平台列表',
            },
        ),
        migrations.CreateModel(
            name='MaterialTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='标签名', max_length=30, verbose_name='标签名')),
                ('subname', models.CharField(help_text='标签别名', max_length=30, verbose_name='标签别名')),
                ('color', models.CharField(choices=[('blue', '蓝色'), ('green', '绿色'), ('red', '红色'), ('orange', '黄色')], default='blue', help_text='颜色', max_length=20, verbose_name='颜色')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('category', models.ForeignKey(blank=True, help_text='类别', null=True, on_delete=django.db.models.deletion.CASCADE, to='material.MaterialCategory', verbose_name='类别')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签列表',
            },
        ),
        migrations.CreateModel(
            name='PostBaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='标题', max_length=100, verbose_name='标题')),
                ('subtitle', models.CharField(blank=True, help_text='子标题', max_length=100, null=True, verbose_name='子标题')),
                ('abstract', models.CharField(blank=True, help_text='摘要', max_length=255, null=True, verbose_name='摘要')),
                ('desc', models.CharField(blank=True, help_text='简介', max_length=255, null=True, verbose_name='简介')),
                ('author', models.CharField(blank=True, help_text='作者', max_length=20, null=True, verbose_name='作者')),
                ('post_type', models.CharField(blank=True, choices=[('article', '文章'), ('album', '图集'), ('movie', '电影'), ('book', '图书'), ('book/note', '图书笔记')], help_text='POST类别', max_length=20, null=True, verbose_name='POST类别')),
                ('click_num', models.IntegerField(default=0, help_text='点击数', verbose_name='点击数')),
                ('like_num', models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数')),
                ('comment_num', models.IntegerField(default=0, help_text='评论数', verbose_name='评论数')),
                ('front_image', models.ImageField(blank=True, help_text='封面图', null=True, upload_to='material/post/image/%y/%m', verbose_name='封面图')),
                ('front_image_type', models.CharField(choices=[('0', '无'), ('1', '小图'), ('2', '大图')], default='0', help_text='封面图类别', max_length=20, verbose_name='封面图类别')),
                ('is_hot', models.BooleanField(default=False, help_text='是否热门', verbose_name='是否热门')),
                ('is_recommend', models.BooleanField(default=False, help_text='是否推荐', verbose_name='是否推荐')),
                ('is_banner', models.BooleanField(default=False, help_text='是否是Banner', verbose_name='是否是Banner')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('browse_password', models.CharField(blank=True, help_text='浏览密码', max_length=20, null=True, verbose_name='浏览密码')),
                ('browse_password_encrypt', models.CharField(blank=True, help_text='浏览密码加密', max_length=100, null=True, verbose_name='浏览密码加密')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('category', models.ForeignKey(help_text='类别', on_delete=django.db.models.deletion.CASCADE, to='material.MaterialCategory', verbose_name='类别')),
                ('license', models.ForeignKey(blank=True, help_text='版权', null=True, on_delete=django.db.models.deletion.CASCADE, to='material.MaterialLicense', verbose_name='版权')),
            ],
            options={
                'verbose_name': '所有博文',
                'verbose_name_plural': '所有博文列表',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('post', models.ForeignKey(help_text='文章', on_delete=django.db.models.deletion.CASCADE, to='material.PostBaseInfo', verbose_name='文章')),
                ('tag', models.ForeignKey(help_text='标签', on_delete=django.db.models.deletion.CASCADE, to='material.MaterialTag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签列表',
            },
        ),
        migrations.AddField(
            model_name='postbaseinfo',
            name='tags',
            field=models.ManyToManyField(through='material.PostTag', to='material.MaterialTag'),
        ),
        migrations.AddField(
            model_name='materialcommentinfo',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.PostBaseInfo', verbose_name='所属文章'),
        ),
        migrations.AddField(
            model_name='materialcommentinfo',
            name='reply_to_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='be_comments', to='user.GuestProfile', verbose_name='被回复人'),
        ),
        migrations.AddField(
            model_name='materialcommentinfo',
            name='reply_to_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='material.MaterialCommentInfo', verbose_name='父级评论'),
        ),
        migrations.AddField(
            model_name='materialcommentdetail',
            name='comment_info',
            field=models.OneToOneField(blank=True, help_text='基本信息', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='material.MaterialCommentInfo', verbose_name='基本信息'),
        ),
        migrations.AddField(
            model_name='materialbanner',
            name='category',
            field=models.ForeignKey(default='1', help_text='类别', on_delete=django.db.models.deletion.CASCADE, to='material.MaterialCategory', verbose_name='类别'),
        ),
    ]
