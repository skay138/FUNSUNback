#redis
import redis
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.conf import settings
from .models import Funding
from .serializers import FundingSerializer

class PublicFundingsCache:
    update_interval = settings.REDIS_CACHE.get('UPDATE_INTERVAL', 5)
    expiration_time = settings.REDIS_CACHE.get('EXPIRATION_TIME', 24 * 60 * 60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_cached_data(self):
            cached_data = self.redis_client.get('cached_data')
            if cached_data:
                return json.loads(cached_data)
            return None
    
    def update_cached_data(self):
        cached_time_str = self.redis_client.get('public_punding_cached_time')
        if cached_time_str:
            cached_time = datetime.fromisoformat(cached_time_str.decode())
            if datetime.now() - cached_time > timedelta(seconds=self.update_interval):
                self._update_cached_data()
        else:
            # 'public_punding_cached_time' 키에 해당하는 값이 없는 경우 새로운 값을 설정
            self._update_cached_data()

    def _update_cached_data(self):
        fundings = Funding.objects.filter(public=True).order_by('-id').select_related('author')
        serializer = FundingSerializer(fundings, many=True)
        data = serializer.data
        self.redis_client.set('cached_data', json.dumps(data, cls=DjangoJSONEncoder), ex=self.expiration_time)
        self.redis_client.set('public_punding_cached_time', datetime.now().isoformat())
        print("캐싱 완료")