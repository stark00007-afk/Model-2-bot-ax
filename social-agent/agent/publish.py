"""Publishers. Only X is implemented in v1; other platforms are added one at a time."""
import os


def publish_x(text: str) -> str:
    import tweepy

    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_SECRET"],
    )
    resp = client.create_tweet(text=text)
    return str(resp.data["id"])


_LINKEDIN_RESERVED = set("|{}@[]()<>\\*_~")


def _linkedin_escape(text: str) -> str:
    # LinkedIn's post text format treats these characters as markup. '#' is left alone so hashtags work.
    return "".join("\\" + c if c in _LINKEDIN_RESERVED else c for c in text)


def publish_linkedin(text: str) -> str:
    import requests

    resp = requests.post(
        "https://api.linkedin.com/rest/posts",
        headers={
            "Authorization": f"Bearer {os.environ['LINKEDIN_ACCESS_TOKEN']}",
            "LinkedIn-Version": os.environ.get("LINKEDIN_API_VERSION", "202510"),
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json={
            "author": os.environ["LINKEDIN_PERSON_URN"],  # looks like urn:li:person:AbC123
            "commentary": _linkedin_escape(text),
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.headers.get("x-restli-id", "unknown")


def publish_facebook(text: str) -> str:
    import requests

    version = os.environ.get("FACEBOOK_API_VERSION", "v23.0")
    resp = requests.post(
        f"https://graph.facebook.com/{version}/{os.environ['FACEBOOK_PAGE_ID']}/feed",
        data={"message": text, "access_token": os.environ["FACEBOOK_PAGE_TOKEN"]},
        timeout=30,
    )
    resp.raise_for_status()
    return str(resp.json().get("id", "unknown"))


PUBLISHERS = {"x": publish_x, "linkedin": publish_linkedin, "facebook": publish_facebook}
