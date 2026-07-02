from pytest import raises

from portfolio.content import Profile, Technology, get_hero_logo_technologies


def _profile_data(hero_logos: list[str] | None = None) -> dict:
    data = {
        "name": "Kent Vugs Nielsen",
        "avatar": "/assets/images/profile-picture.jpg",
        "hero_lines": ["I Do Data Science"],
        "links": {
            "github": "https://github.com/kvugs",
            "linkedin": "https://www.linkedin.com/in/vugs/",
        },
    }

    if hero_logos is not None:
        data["hero_logos"] = hero_logos

    return data


def _profile(hero_logos: list[str]) -> Profile:
    return Profile.model_validate(_profile_data(hero_logos=hero_logos))


def _technology(tag: str, label: str | None = None) -> Technology:
    return Technology.model_validate(
        {
            "tag": tag,
            "label": label or tag.title(),
            "icon": f"/assets/icons/{tag}.svg",
        }
    )


def test_profile_requires_hero_logos() -> None:
    with raises(ValueError, match="hero_logos"):
        Profile.model_validate(_profile_data())


def test_profile_rejects_empty_hero_logos() -> None:
    with raises(ValueError, match="hero_logos"):
        _profile([])


def test_profile_rejects_bad_hero_logo_slug() -> None:
    with raises(ValueError, match="lowercase kebab-case"):
        _profile(["Python"])


def test_get_hero_logo_technologies_preserves_profile_order() -> None:
    profile = _profile(["pytorch", "python", "databricks"])

    technologies = [
        _technology("python", "Python"),
        _technology("databricks", "Databricks"),
        _technology("pytorch", "PyTorch"),
    ]

    hero_logos = get_hero_logo_technologies(profile, technologies)

    assert [technology.tag for technology in hero_logos] == [
        "pytorch",
        "python",
        "databricks",
    ]


def test_get_hero_logo_technologies_rejects_unknown_tag() -> None:
    profile = _profile(["python", "unknown-tool"])
    technologies = [_technology("python", "Python")]

    with raises(ValueError, match="Missing tag"):
        get_hero_logo_technologies(profile, technologies)


def test_get_hero_logo_technologies_rejects_duplicate_tags() -> None:
    profile = _profile(["python", "python"])
    technologies = [_technology("python", "Python")]

    with raises(ValueError, match="Duplicate value"):
        get_hero_logo_technologies(profile, technologies)


def test_get_hero_logo_technologies_rejects_more_than_four_logos() -> None:
    profile = _profile(["one", "two", "three", "four", "five"])

    technologies = [
        _technology("one"),
        _technology("two"),
        _technology("three"),
        _technology("four"),
        _technology("five"),
    ]

    with raises(ValueError, match="number of hero logos"):
        get_hero_logo_technologies(profile, technologies)


def test_get_hero_logo_technologies_rejects_selected_technology_without_icon() -> None:
    profile = _profile(["python"])

    technologies = [
        Technology.model_validate(
            {
                "tag": "python",
                "label": "Python",
                "icon": None,
            }
        )
    ]

    with raises(ValueError, match="icon cannot be None"):
        get_hero_logo_technologies(profile, technologies)


def test_get_hero_logo_technologies_rejects_selected_technology_without_label() -> None:
    profile = _profile(["python"])

    technologies = [
        Technology.model_validate(
            {
                "tag": "python",
                "label": None,
                "icon": "/assets/icons/python.svg",
            }
        )
    ]

    with raises(ValueError, match="label cannot be None"):
        get_hero_logo_technologies(profile, technologies)
