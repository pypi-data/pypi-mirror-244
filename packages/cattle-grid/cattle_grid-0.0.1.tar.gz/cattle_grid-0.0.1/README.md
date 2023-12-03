# cattle_grid

cattle_grid is meant to simplify handling authentication in server to
server communication of the Fediverse. cattle_grid checks the HTTP
signatures based on the headers. For this public keys are retrieved
and cached.

For installation instructions see the [documentation](https://bovine.codeberg.page/cattle_grid/).

## Development

One can run the pytest tests via

```bash
poetry install
poetry run pytest
```

## Development with Fediverse pasture

In your Funfedi.dev directory (see [here](https://funfedi.dev/testing_tools/verify_actor/)
for details), run

```bash
cd fediverse-pasture
docker compose --file pasture.yml up pasture_verify_actor
```

Now in the cattle grid directory, run

```bash
poetry run python -mcattle_grid.config --actor_id http://cattle_grid/actor
```

to create a `cattle_grid.toml` file. Then start the docker containers via

```bash
docker compose up
```

By opening [http://localhost:2909/?actor_uri=jskitten@cattle_grid_demo](http://localhost:2909/?actor_uri=jskitten%40cattle_grid_demo), you should then be able to view the verify actor result. By refreshing the page and inspecting the log files, you can also check that the requests only ran once.

## Running GUI tests with the pasture

Start mastodon accessible through your browser

```bash
cd fediverse-pasture
docker compose --file mastodon42.yml --profile nginx up
```

See [Fun Fediverse Development](https://funfedi.dev/fediverse_pasture/applications/mastodon_4_2/) for instructions.

Then you can open [mastodon42web](http://mastodon42web) and lookup `jskitten@cattle_grid_demo`.
When you send a message to this kitten, it should reply with a meow, e.g.

![Kitten meows](mastodon.png)
