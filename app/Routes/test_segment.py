from app.magic import router
from app.magic.Services.Segment import analytics


@router.post('/test_segment', tags=['boilerplate'])
def test_segment(id: str, action, body: dict):
    analytics.track(id, action, body)
    return 'done!'
