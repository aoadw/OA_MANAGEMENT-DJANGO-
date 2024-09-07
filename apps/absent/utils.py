# 封装获取审批人的函数
def get_responser(request):
    user = request.user
    # 如果登录用户为部门领导人
    if user.department.leader.uuid == user.uuid:
        if user.department.name == '董事会':
            responser = None
        else:
            responser = user.department.manager
    else:
        responser = user.department.leader
    return responser