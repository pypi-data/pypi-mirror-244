import os

from pocketbase import Client
from pocketbase.models.record import Record
from pocketbase.models.utils import BaseModel
from pocketbase.models.utils.list_result import ListResult
from pocketbase.services.record_service import RecordAuthResponse
from streamlit.connections import BaseConnection
from streamlit.runtime.caching import cache_data


class PocketBaseConnection(BaseConnection[Client]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = self._connect(**kwargs)

    def _connect(self, **kwargs) -> Client:
        """
        Connect to PocketBase.

        Parameters
        ----------
        pb_url : str
            The base url for the PocketBase connection. This corresponds to the
            ``[connections.<connection_name>.pb_url]`` config section in ``st.secrets``.
        kwargs : dict
            Any other kwargs to pass to this connection class' ``_connect`` method.

        Returns
        -------
        Client

        Raises
        ------
        ValueError
            If the ``pb_url`` kwarg is not provided and there is no ``pb_url`` config
            section in ``st.secrets``.
        """
        if "pb_url" in kwargs:
            pb_url = kwargs.pop("pb_url")
        elif "pb_url" in os.environ:
            pb_url = os.environ["pb_url"]
        else:
            raise ValueError("Missing base url for PocketBase connection")

        return Client(pb_url)

    def cursor(self) -> Client:
        """
        Return the PocketBase client.

        Returns
        -------
        Client
        """
        return self._client

    def auth_with_password(
            self,
            collection_id_or_name="users",
            username_or_email="",
            password="",
            body_params={},
            query_params={},
    ) -> RecordAuthResponse:
        """
        Authenticate with PocketBase using a username and password.

        Parameters
        ----------
        collection_id_or_name : str, optional
            The collection id or name to authenticate with. Defaults to "users".
        username_or_email : str, optional
            The username or email to authenticate with. Defaults to "".
        password : str, optional
            The password to authenticate with. Defaults to "".
        body_params : dict, optional
            Any additional body params to pass to the request. Defaults to {}.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.

        Returns
        -------
        RecordAuthResponse
        """
        return self._client.collection(collection_id_or_name).auth_with_password(
            username_or_email, password, body_params, query_params
        )

    def is_logged_in(self) -> bool:
        """
        Check if the user is logged in.

        Returns
        -------
        bool
        """
        return self.cursor().auth_store.token is not None

    def user(self) -> Record:
        """
        Return the user record.

        Returns
        -------
        Record
        """
        return self.cursor().auth_store.model

    def get_list(
            self, collection_id_or_name, page=1, per_page=30, query_params={}, ttl=0
    ) -> ListResult:
        """
        Get a list of records from a collection.

        Parameters
        ----------
        collection_id_or_name : str
            The collection id or name to get records from.
        page : int, optional
            The page number to get. Defaults to 1.
        per_page : int, optional
            The number of records to get per page. Defaults to 30.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.
        ttl : int, optional
            The number of seconds to cache the result for. Defaults to 0.

        Returns
        -------
        ListResult
        """

        @cache_data(ttl=ttl)
        def _get_list(collection_id_or_name, page=1, per_page=30, query_params={}):
            return self._client.collection(collection_id_or_name).get_list(
                page, per_page, query_params
            )

        return _get_list(collection_id_or_name, page, per_page, query_params)

    def get_one(
            self, collection_id_or_name, record_id, query_params={}, ttl=0
    ) -> BaseModel:
        """
        Get a single record from a collection.

        Parameters
        ----------
        collection_id_or_name : str
            The collection id or name to get the record from.
        record_id : str
            The id of the record to get.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.
        ttl : int, optional
            The number of seconds to cache the result for. Defaults to 0.

        Returns
        -------
        BaseModel
        """

        @cache_data(ttl=ttl)
        def _get_one(collection_id_or_name, record_id, query_params={}):
            return self._client.collection(collection_id_or_name).get_one(
                record_id, query_params
            )

        return _get_one(collection_id_or_name, record_id, query_params)

    def create(
            self, collection_id_or_name, body_params={}, query_params={}, ttl=0
    ) -> BaseModel:
        """
        Create a record in a collection.

        Parameters
        ----------
        collection_id_or_name : str
            The collection id or name to create the record in.
        body_params : dict, optional
            Any additional body params to pass to the request. Defaults to {}.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.
        ttl : int, optional
            The number of seconds to cache the result for. Defaults to 0.

        Returns
        -------
        BaseModel
        """

        @cache_data(ttl=ttl)
        def _create(collection_id_or_name, body_params={}, query_params={}):
            return self._client.collection(collection_id_or_name).create(
                body_params, query_params
            )

        return _create(collection_id_or_name, body_params, query_params)

    def update(
            self, collection_id_or_name, record_id, body_params={}, query_params={}, ttl=0
    ) -> BaseModel:
        """
        Update a record in a collection.

        Parameters
        ----------
        collection_id_or_name : str
            The collection id or name to update the record in.
        record_id : str
            The id of the record to update.
        body_params : dict, optional
            Any additional body params to pass to the request. Defaults to {}.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.
        ttl : int, optional
            The number of seconds to cache the result for. Defaults to 0.

        Returns
        -------
        BaseModel
        """

        @cache_data(ttl=ttl)
        def _update(collection_id_or_name, record_id, body_params={}, query_params={}):
            return self._client.collection(collection_id_or_name).update(
                record_id, body_params, query_params
            )

        return _update(collection_id_or_name, record_id, body_params, query_params)

    def delete(self, collection_id_or_name, record_id, query_params={}, ttl=0) -> bool:
        """
        Delete a record from a collection.

        Parameters
        ----------
        collection_id_or_name : str
            The collection id or name to delete the record from.
        record_id : str
            The id of the record to delete.
        query_params : dict, optional
            Any additional query params to pass to the request. Defaults to {}.
        ttl : int, optional
            The number of seconds to cache the result for. Defaults to 0.

        Returns
        -------
        bool
        """

        @cache_data(ttl=ttl)
        def _delete(collection_id_or_name, record_id, query_params={}):
            return self._client.collection(collection_id_or_name).delete(
                record_id, query_params
            )

        return _delete(collection_id_or_name, record_id, query_params)

    def logout(self) -> None:
        """
        Logout the user.
        """
        self._client.auth_store.clear()
