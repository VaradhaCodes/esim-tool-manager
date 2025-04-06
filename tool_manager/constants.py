# constants.py

# These are our "official" references so everything else
# can rely on the same data instead of scattering it around.

SUPPORTED_TOOLS = ["ngspice", "kicad"]

# We set desired "official" versions. If the user has a mismatch,
# we might prompt them to upgrade.
EXPECTED_VERSIONS = {
    "ngspice": "41.0.0",
    "kicad": "9.0"
}

# In the future, if we add more Windows tools, we'll
# just slot them in here to keep everything consistent.
