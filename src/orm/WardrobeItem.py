from tina4_python import ORM, IntegerField, StringField, JSONField, DateTimeField


class WardrobeItem(ORM):
    """A single garment in the user's digital wardrobe."""

    table_name = "wardrobe_item"

    id = IntegerField(primary_key=True, auto_increment=True)
    name = StringField()
    category = StringField()      # top | bottom | dress | shoes | jacket | accessory
    color = StringField()         # display swatch colour (hex)
    season = StringField()        # summer | winter | all
    style_tags = JSONField()      # e.g. ["casual", "corporate"]
    image_url = StringField()     # optional uploaded image path
    times_worn = IntegerField()
    created_at = DateTimeField()
