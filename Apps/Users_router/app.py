from fastapi import APIRouter,Header
from typing import List

from fastapi import Depends,  HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from Apps.Users_router import schemas,models
from Apps.Users_router.dependencies import User
from Apps.Users_router.dependencies.User import verify_token_access
from ..dependencies.database import engine,redis_instance


models.Base.metadata.create_all(bind=engine)


user_app = APIRouter(tags=["API for Users"],
                prefix="/API")


@user_app.get('/')
async def hello():
    return {"hello": "demo_router"}


@user_app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = User.get_user_by_phone(db, user.u_phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return User.create_user(db=db, user=user)


@user_app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token:str=Header(None)):
    users = User.get_users(db, skip=skip, limit=limit)
    return users


@user_app.post("/user_login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    class response_mode(schemas.Respone):
        data: schemas.UserLoginResponse = None
    res_mode = response_mode()

    # 1> 查询用户是否存在
    db_user = User.get_user_by_phone(db, user.u_phone)
    if db_user is None:
        res_mode.msg = "user is not exist"
        res_mode.status = 400
        return res_mode
    # 2> 检验账号密码是否匹配
    if not (user.u_password == db_user.u_password):
        res_mode.msg = "The Account and Password not match"
        res_mode.status = 400
        return res_mode
    # 2> 生成token令牌
    token_str = "this is token"
    try:
        redis_instance.set(user.u_phone,token_str,ex = 60*30)
        # print(type(redis_instance.get(user.u_phone)))
    except Exception as e:
        print(e)
    res_mode.msg = 'ok'
    data_mode = schemas.UserLoginResponse(u_phone=db_user.u_phone,
                                          u_name=db_user.u_name,
                                          token=token_str)

    res_mode.data = data_mode
    return res_mode


@user_app.post("/user_setup/{phone}")
def SetUp(user:schemas.UserSetUp,
        db: Session = Depends(get_db),
        admin_status= Depends(verify_token_access)):

    class response_mode(schemas.Respone):
        data: str=None
    res_mode = response_mode()
    print(res_mode)
    # 1> 查询是否存在token
    if not admin_status[0]:
        res_mode.msg = "please login"
        res_mode.status = 400
        return res_mode
    # 1> 查询用户是否存在
    db_user = User.get_user_by_phone(db, user.u_phone)
    db_user_admin = User.get_user_by_phone(db, admin_status[1])
    if db_user is None:
        res_mode.msg = "user is not exist"
        res_mode.status = 400
        return res_mode
    # 2> 查询操作者是否有权限
    if db_user_admin.u_level < 100:
        res_mode.msg = "user has no permissions"
        res_mode.status = "400"
        return res_mode
    res_mode.msg = "ok"
    res_mode.status = 200
    db.query(models.User).filter(models.User.u_phone == user.u_phone).update({"u_phone"   :user.u_phone,
                    "u_name"    :user.u_name,
                    "u_password":user.u_password,
                    "u_gender"  :user.u_gender,
                    "u_level"   :user.u_level,
                    "is_active" :user.is_active})
    db.commit()
    return res_mode


@user_app.get("/user_setup/{phone}")
def SetUp(phone:str,
            db: Session = Depends(get_db),
            admin_status= Depends(verify_token_access)):

    class response_mode(schemas.Respone):
        data: schemas.UserSetUp = None
    res_mode = response_mode()
    # 1> 查询是否存在token
    if not admin_status[0]:
        res_mode.msg = "please login"
        res_mode.status = "400"
        return res_mode
    # 2> 查询用户是否存在
    db_user = User.get_user_by_phone(db, phone)
    db_user_admin = User.get_user_by_phone(db, admin_status[1])
    if db_user is None:
        res_mode.msg = "user is not exist"
        res_mode.status = "400"
        return res_mode
    # 3> 查询操作者是否有权限
    if db_user_admin.u_level < 100:
        res_mode.msg = "user has no permissions"
        res_mode.status = "400"
        return res_mode
    # 4> 获取用户数据
    data_mode = schemas.UserSetUp(u_phone   =db_user.u_phone,
                                u_name      =db_user.u_name,
                                u_password  =db_user.u_password,
                                u_gender    =db_user.u_gender,
                                u_level     =db_user.u_level,
                                is_active   =db_user.is_active)
    res_mode.data = data_mode
    return res_mode





