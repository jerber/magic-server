from app.magic import router, CurrentUser, GET_USER


@router.get("/get_current_user", response_model=CurrentUser)
def hello(current_user: CurrentUser = GET_USER):
    return current_user
