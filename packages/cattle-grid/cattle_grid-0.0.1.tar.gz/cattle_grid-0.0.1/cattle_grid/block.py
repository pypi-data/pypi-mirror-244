import click

from .config import Config


@click.command()
@click.option(
    "--source",
    help="URL or file to import blocklist from",
    default="https://seirdy.one/pb/FediNuke.txt",
)
@click.option(
    "--clean",
    is_flag=True,
    default=False,
    help="Sets the blocklist to test empty list",
)
@click.option("--add", help="Adds domain to blocklist")
@click.option("--remove", help="Removes domain from blocklist")
def update_blocklist(source, clean, add, remove):
    config = Config.load()

    if clean:
        config.domain_blocks = set()
    elif add:
        config.domain_blocks = config.domain_blocks | {add}
    elif remove:
        config.domain_blocks = config.domain_blocks - {remove}
    else:
        config.add_blocks_from_url_or_file(source)

    config.save()


if __name__ == "__main__":
    update_blocklist()
