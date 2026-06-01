"""
Helper pagination.
Mengambil parameter page dan page_size dari request args.
"""

from flask import request
import config


def get_pagination_params():
    """
    Mengambil page dan page_size dari query string.
    Default: page=1, page_size=DEFAULT_PAGE_SIZE.
    """
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", config.DEFAULT_PAGE_SIZE, type=int)

    page = max(1, page)
    page_size = max(1, min(page_size, config.MAX_PAGE_SIZE))

    return page, page_size


def apply_pagination(query, page, page_size):
    """
    Apply offset dan limit ke SQLAlchemy query.
    Return: (items, total_count)
    """
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    return items, total
