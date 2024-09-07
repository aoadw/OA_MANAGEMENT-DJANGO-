from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField


class UserStatusChoices(models.IntegerChoices):
    ACTIVE = 1
    UNACTIVE = 2
    LOCKED = 3


class OAManger(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        """
        创建用户逻辑
        """
        if not realname:
            raise ValueError("必须输入用户姓名")
        email = self.normalize_email(email)
        # self.model 代表指定objects = OAManger()的模型
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('status', UserStatusChoices.ACTIVE)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)


class OAUser(AbstractBaseUser, PermissionsMixin):

    uuid = ShortUUIDField(primary_key=True) # 使用uuid作为主键
    realname = models.CharField(max_length=150,unique=True)
    email = models.EmailField(blank=False,unique=True)
    telephone = models.CharField(blank=False,max_length=15)
    is_staff = models.BooleanField(default=True)
    status = models.IntegerField(choices=UserStatusChoices,default=UserStatusChoices.UNACTIVE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey('OADepartment',on_delete=models.SET_NULL,null=True,related_name='staffs',related_query_name='staffs')
    # 指定related_name的值 使得可以通过这个值，查询这个部门下的员工

    objects = OAManger()

    EMAIL_FIELD = "email"
    # USERNAME_FIELD用来通过 authenticate 鉴权，authenticate函数会将USERNAME_FIELD中指定的参数传给函数中的username参数
    USERNAME_FIELD = "email"
    # 上述两个指定过的参数无需在REQUIRED_FIELDS中指定
    REQUIRED_FIELDS = ["realname",'password']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):

        return self.realname


class OADepartment(models.Model):
    name = models.CharField(max_length=150)
    intro = models.CharField(max_length=150)
    leader = models.OneToOneField(OAUser,on_delete=models.SET_NULL,null=True ,related_name='leader_department',related_query_name="leader_department")
    manager = models.ForeignKey(OAUser,on_delete=models.SET_NULL,null=True,related_name='manger_department',related_query_name="manger_department")
