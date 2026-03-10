#!/bin/bash

alembic upgrade head
uvicorn src.api.main:app