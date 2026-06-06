import uuid
from datetime import datetime, timezone
from typing import Optional, Any, List
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON
from pgvector.sqlalchemy import Vector


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    full_name: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    filename: str = Field(max_length=255)
    file_type: str = Field(max_length=10)
    storage_key: str
    file_size_bytes: Optional[int] = None
    status: str = Field(default="active", max_length=20)
    chunk_count: int = Field(default=0)
    is_processed: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    document_id: uuid.UUID = Field(
        foreign_key="documents.id",
        index=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    chunk_index: int
    content: str
    embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(384))
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    session_id: uuid.UUID = Field(
        foreign_key="chat_sessions.id",
        index=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=20)
    content: str
    sources: Optional[Any] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )