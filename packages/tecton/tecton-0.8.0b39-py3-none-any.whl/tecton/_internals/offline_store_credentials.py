from typing import Dict
from typing import Optional

from tecton._internals import metadata_service
from tecton_core import conf
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_proto.common.id_pb2 import Id
from tecton_proto.metadataservice.metadata_service_pb2 import GetOfflineStoreCredentialsRequest


class MDSOfflineStoreOptionsProvider(OfflineStoreOptionsProvider):
    def get_options(self, feature_view_id: Id) -> Optional[Dict[str, str]]:
        response = metadata_service.instance().GetOfflineStoreCredentials(
            GetOfflineStoreCredentialsRequest(feature_view_id=feature_view_id)
        )
        if not response.HasField("aws"):
            return None
        return {
            "AWS_ACCESS_KEY_ID": response.aws.access_key_id,
            "AWS_SECRET_ACCESS_KEY": response.aws.secret_access_key,
            "AWS_SESSION_TOKEN": response.aws.session_token,
            "AWS_REGION": conf.get_or_raise("CLUSTER_REGION"),
        }


INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS = {
    "s3": [MDSOfflineStoreOptionsProvider(), *DEFAULT_OPTIONS_PROVIDERS["s3"]]
}
