from distutils.core import setup

files = ["res/*"]

setup(name="Porthole",
      version="1",
      description="Porthole",
      author="Mario Aichinger",
      author_email="aichingm@gmail.com",
      url="https://github.com/aichingm/porthole",
      packages=['Porthole'],
      package_data={'Porthole': files},
      package_dir={'Porthole': 'src'},
      scripts=["porthole"],
      long_description="""A minimalistic frameless text-driven window to the world wide web!"""
      )
