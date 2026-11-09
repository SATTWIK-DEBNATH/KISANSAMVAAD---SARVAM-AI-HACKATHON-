# ============================================================================
# KisanSamvaad Python Supabase Backend Service Client
# File: backend/app/db/supabase_client.py
# ============================================================================

import os
from typing import Optional, Dict, Any, List

# Check if supabase package is installed, otherwise provide resilient fallback
try:
    from supabase import create_client, Client
    SUPABASE_SDK_AVAILABLE = True
except ImportError:
    SUPABASE_SDK_AVAILABLE = False
    Client = Any  # type: ignore

class SupabaseService:
    """
    Singleton service manager for Supabase integration in FastAPI backend.
    Enforces security boundaries:
    - Service Role Key is strictly confined to server-side background tasks.
    - User JWT validation ensures client requests cannot bypass RLS.
    """
    _instance: Optional["SupabaseService"] = None

    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        self.anon_key: str = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
        self.service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
        self._admin_client: Optional[Client] = None
        self._anon_client: Optional[Client] = None

    @classmethod
    def get_instance(cls) -> "SupabaseService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def is_configured(self) -> bool:
        return bool(self.url and (self.anon_key or self.service_role_key) and SUPABASE_SDK_AVAILABLE)

    def get_admin_client(self) -> Optional[Client]:
        """
        Retrieves a Supabase client configured with the high-privilege Service Role Key.
        Used strictly for trusted server processes, such as ICAR batch jobs and system migrations.
        """
        if not self.is_configured or not self.service_role_key:
            return None
        if self._admin_client is None:
            self._admin_client = create_client(self.url, self.service_role_key)
        return self._admin_client

    def get_client_for_token(self, jwt_token: str) -> Optional[Client]:
        """
        Instantiates a Supabase client scoped to an authenticated user's JWT.
        Row Level Security (RLS) policies are automatically enforced by PostgreSQL.
        """
        if not self.is_configured:
            return None
        client = create_client(self.url, self.anon_key)
        # Attach caller JWT to postgrest headers
        client.postgrest.auth(jwt_token)
        return client

    def verify_jwt_user(self, jwt_token: str) -> Optional[Dict[str, Any]]:
        """
        Validates the cryptographically signed JWT via Supabase Auth API.
        """
        if not self.is_configured:
            return None
        try:
            client = create_client(self.url, self.anon_key)
            user_response = client.auth.get_user(jwt_token)
            if user_response and user_response.user:
                return {
                    "id": user_response.user.id,
                    "email": user_response.user.email,
                    "phone": user_response.user.phone,
                    "user_metadata": user_response.user.user_metadata,
                }
        except Exception:
            return None
        return None

# Global convenience accessor
supabase_service = SupabaseService.get_instance()
