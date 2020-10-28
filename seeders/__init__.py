def main():
    from . import (
        seed_operator_types,
        seed_regions,
        seed_titles,
        seed_townships,
    )
    from .lib import get_user

    user = get_user()
    seed_operator_types.seed(user)
    seed_titles.seed(user)
    seed_regions.seed(user)
    seed_townships.seed(user)
