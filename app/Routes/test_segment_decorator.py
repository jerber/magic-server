from app.magic import router
from app.magic.Services.Doorman import CurrentUser, GET_USER
from app.magic.Services.Segment.decorator import segment


@router.get("/segment_decorator", response_model=CurrentUser, tags=["seg"])
@segment(keywords=["current_user"])
async def get_curr_user_w_seg(current_user: CurrentUser = GET_USER):
    return current_user
