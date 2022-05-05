#!/usr/bin/env python3

import sys
from sqlalchemy_utils import create_database
from sqlalchemy import create_engine

from lrqc.lrqc_outcome.db.db_schema import Base

url = sys.argv[1]

engine = create_engine(url)

create_database(engine.url)

Base.metadata.create_all(engine)
