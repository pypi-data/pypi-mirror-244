import aiohttp
import logging
from quart import Quart, request, render_template

from tortoise.contrib.quart import register_tortoise

from .config import Config
from .signature import SignatureChecker
from .public_key_cache import PublicKeyCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(filename="cattle_grid.toml"):
    config = Config.load(filename=filename)
    app = Quart(__name__)

    register_tortoise(
        app,
        db_url=config.db_url,
        modules={"models": ["cattle_grid.model"]},
        generate_schemas=True,
    )

    bovine_actor = config.bovine_actor
    public_key_cache = PublicKeyCache(bovine_actor)
    signature_checker = SignatureChecker(public_key_cache.from_cache)

    @app.before_serving
    async def startup():
        app.config["session"] = aiohttp.ClientSession()
        await bovine_actor.init(session=app.config["session"])

    @app.after_serving
    async def shutdown():
        await app.config["session"].close()

    @app.get("/")
    async def index():
        return await render_template("index.html")

    @app.get(config.actor_path)
    async def handle_get_actor():
        return config.actor, 200, {"content-type": "application/activity+json"}

    @app.get("/.well-known/webfinger")
    async def webfinger():
        resource = request.args.get("resource")
        if not resource:
            return "", 400
        if resource != config.actor_acct_id:
            return "", 404
        return config.webfinger, 200, {"content-type": "application/jrd+json"}

    @app.get("/auth", defaults={"path": "/"})
    @app.get("/auth/<path:path>")
    async def handle_get(path):
        logger.debug("got request to %s", path)
        if "signature" not in request.headers:
            logger.debug("no signature")
            return "", 200

        owner = await signature_checker.verify_signature(request.headers)

        if owner:
            if config.is_blocked(owner):
                return "", 403
            return "", 200, {"x-cattle-grid-requester": owner}

        logger.info(
            "invalid signature for request to %s => access denied",
            request.headers.get("X-Original-Uri", ""),
        )
        logger.info("Signature %s", request.headers.get("signature"))

        return "", 401

    return app
