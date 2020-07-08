from app.magic.Services.Doorman import router, CurrentUser, GET_USER


@router.get("/get_current_user", response_model=CurrentUser, tags=['boilerplate'])
def get_current_user(current_user: CurrentUser = GET_USER):
    print(current_user)
    return current_user
