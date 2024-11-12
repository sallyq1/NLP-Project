from typing import Annotated
from fastapi import Depends
from supabase import Client, create_client
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session

load_dotenv('../.env.local')

supabase_url = os.getenv('SUPABASE_CONNECTION_STRING')

engine = create_engine(supabase_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


supabase_url2 = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
supabase_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

supabase: Client = create_client(supabase_url2, supabase_key)
