class Template:
	def __init__(
			self,
			variants: list[int],
			price: int,
			name: str,
			blueprint: int,
			publish_data: dict[str: bool]
	):
		self.variants = variants
		self.price = price
		self.name = name
		self.blueprint = blueprint
		self.publish_data = publish_data

	def __str__(self):
		return f"{self.name} template"


Test = Template(
	name='Test template',
	price=3599,
	blueprint=6,
	variants=[
		11872, 11873, 11874, 11875, 11876, 11877, 11896, 11897, 11898, 11899, 11900, 11901, 11902, 11903, 11904,
		11905, 11906, 11907, 11974, 11975, 11976, 11977, 11978, 11979, 11986, 11987, 11988, 11989, 11990, 11991,
		12016, 12017, 12018, 12019, 12020, 12021, 12022, 12023, 12024, 12025, 12026, 12027, 12052, 12053, 12054,
		12055, 12056, 12057, 12070, 12071, 12072, 12073, 12074, 12075, 12100, 12101, 12102, 12103, 12104, 12105,
		12106, 12107, 12108, 12109, 12110, 12111, 12124, 12125, 12126, 12127, 12128, 12129, 12148, 12149, 12150,
		12151, 12152, 12153, 12172, 12173, 12174, 12175, 12176, 12177, 12190, 12191, 12192, 12193, 12194, 12195,
		23955, 24005, 24021, 24031, 24039, 24088, 24138, 24153, 24164, 24171
	],
	publish_data={
		"title": True,
		"description": True,
		"images": True,
		"variants": True,
		"tags": True,
		"keyFeatures": True,
		"shipping_template": True
	}

)
