PyCon Program Committee Web App
-------------------------------

The goal of this app is to provide a useful tool for asynchronous review of
PyCon talk submissions. The program committee's job is extensive and daunting,
and I'm trying to knock together a simple web app to allow the work to proceed
as efficiently and effectively as I can. Requiring large groupings of
busy professionals to come together at the same time to chat on IRC is hard,
and doesn't feel very scalable. This is my first step towards understanding how
to scale the whole thing.



Configuring the Applications
------------------------
As currently configured, the application connects to a local postgresql
database, with username, password, and database name 'test'. The unit tests
will create the tables for you, or I presume you can do something like
`psql test < tables.sql`.

The application picks up configuration from environment variables. I like to
use the envdir tool, but you can set them however you like. A complete set of
configuration values, reasonable for testing, are available in `dev-config/`.
The exception is `MANDRILL_API_KEY`. You'll have to get your own one of
those.

You can install envdir via `brew install daemontools` on OS X, and `apt-get
install daemontools` on Ubuntu and Debian.



Running the Application
-----------------
Make a virtualenv, `pip install -r requirements.pip`. Run the application
locally via `envdir dev-config ./app.py`, run the tests via
`envdir dev-config py.test`.



Understanding The PyCon Talk Review Process
------------
The process runs in two rounds; the first is called "kittendome", and is
basically the process of winnowing out talks. Talks which aren't relevant for
PyCon, have poorly prepared proposals, or otherwise won't make the cut, get
eliminated from consideration early. Talks aren't compared to one another; a
low-ish bar is set, and talks that don't make it over the bar are removed.

The second part of the process is "thunderdome". In thunderdome, talks are
moved into groups, and those groups are then reviewed one at a time, with
a winner or two picked from every group. Some groups feel weak enough that no
winners are picked.
