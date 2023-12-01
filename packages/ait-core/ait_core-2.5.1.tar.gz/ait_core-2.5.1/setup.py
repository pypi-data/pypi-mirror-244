# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ait',
 'ait.core',
 'ait.core.bin',
 'ait.core.server',
 'ait.core.server.handlers',
 'ait.core.server.plugins']

package_data = \
{'': ['*'], 'ait': ['data/*'], 'ait.core': ['data/*']}

install_requires = \
['bottle==0.12.23',
 'gevent',
 'gevent-websocket==0.10.1',
 'gipc>=1.1.0,<2.0.0',
 'greenlet==1.1.3',
 'jsonschema==3.0.2',
 'pyyaml==5.3.1',
 'pyzmq==24.0.0',
 'requests>=2.22.0',
 'setproctitle>=1.2.3,<2.0.0']

entry_points = \
{'console_scripts': ['ait-bsc = ait.core.bin.ait_bsc:main',
                     'ait-bsc-create-handler = '
                     'ait.core.bin.ait_bsc_create_handler:main',
                     'ait-bsc-stop-handler = '
                     'ait.core.bin.ait_bsc_stop_handler:main',
                     'ait-ccsds-send-example = '
                     'ait.core.bin.ait_ccsds_send_example:main',
                     'ait-cmd-hist = ait.core.bin.ait_cmd_hist:main',
                     'ait-cmd-send = ait.core.bin.ait_cmd_send:main',
                     'ait-create-dirs = ait.core.bin.ait_create_dirs:main',
                     'ait-dict-writer = ait.core.bin.ait_dict_writer:main',
                     'ait-limits-find-dn = '
                     'ait.core.bin.ait_limits_find_dn:main',
                     'ait-mps-seq-convert = '
                     'ait.core.bin.ait_mps_seq_convert:main',
                     'ait-pcap = ait.core.bin.ait_pcap:main',
                     'ait-pcap-segment = ait.core.bin.ait_pcap_segment:main',
                     'ait-seq-decode = ait.core.bin.ait_seq_decode:main',
                     'ait-seq-encode = ait.core.bin.ait_seq_encode:main',
                     'ait-seq-print = ait.core.bin.ait_seq_print:main',
                     'ait-seq-send = ait.core.bin.ait_seq_send:main',
                     'ait-server = ait.core.bin.ait_server:main',
                     'ait-table-decode = ait.core.bin.ait_table_decode:main',
                     'ait-table-encode = ait.core.bin.ait_table_encode:main',
                     'ait-tlm-csv = ait.core.bin.ait_tlm_csv:main',
                     'ait-tlm-db-insert = ait.core.bin.ait_tlm_db_insert:main',
                     'ait-tlm-send = ait.core.bin.ait_tlm_send:main',
                     'ait-tlm-simulate = ait.core.bin.ait_tlm_simulate:main',
                     'ait-yaml-validate = ait.core.bin.ait_yaml_validate:main',
                     'build_sphinx = poetry_cli.build_sphinx:main']}

setup_kwargs = {
    'name': 'ait-core',
    'version': '2.5.1',
    'description': "NASA JPL's Ground Data System toolkit for Instrument and CubeSat Missions",
    'long_description': '\n.. image:: https://github.com/NASA-AMMOS/AIT-Core/actions/workflows/full_build.yaml/badge.svg?branch=master\n   :target: https://github.com/NASA-AMMOS/AIT-Core/actions\n   :alt: Build and Lint Status\n\n.. image:: https://readthedocs.org/projects/ait-core/badge/?version=latest\n    :target: https://ait-core.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nThe AMMOS Instrument Toolkit (Formerly the Bespoke Links to Instruments\nfor Surface and Space (BLISS)) is a Python-based software suite\ndeveloped to handle Ground Data System (GDS), Electronic Ground Support\nEquipment (EGSE), commanding, telemetry uplink/downlink, and sequencing\nfor instrument and CubeSat Missions. It is a generalization and expansion\nof tools developed for a number of ISS\nmissions.\n\nGetting Started\n===============\n\nYou can read through the `Installation and Configuration\nPage <http://ait-core.readthedocs.io/en/latest/installation.html>`__ for\ninstruction on how to install AIT Core.\n\nYou can read through the `New Project Setup\nPage <http://ait-core.readthedocs.io/en/latest/project_setup.html>`__\nfor instructions on how to use AIT on your next project.\n\nJoin the Community\n==================\n\nThe project\'s `User and Developer Mailing List <https://groups.google.com/forum/#!forum/ait-dev>`__ is the best way to communicate with the team, ask questions, brainstorm plans for future changes, and help contribute to the project.\n\nThis project exists thanks to the dedicated users, contributors, committers, and project management committee members. If you\'d like to learn more about how the project is organized and how to become a part of the team please check out the `Project Structure and Governance <https://github.com/NASA-AMMOS/AIT-Core/wiki/Project-Structure-and-Governance>`__ documentation.\n\nContributing\n============\n\nThank you for your interest in contributing to AIT! We welcome contributions from people of all backgrounds and disciplines. While much of the focus of our project is software, we believe that many of the most critical contributions come in the form of documentation improvements, asset generation, user testing and feedback, and community involvement. So if you\'re interested and want to help out please don\'t hesitate! Send us an email on the public mailing list below, introduce yourself, and join the community.\n\nCommunication\n-------------\nAll project communication happens via mailing lists. Discussions related to development should happen on the public `Developer and User Mailing List <https://groups.google.com/forum/#!forum/ait-dev>`__. If you\'re new to the community make sure to introduce yourself as well!\n\nDev Installation\n----------------\nAs always, we encourage you to install AIT into a virtual environment of your choosing when you set up your development environment. AIT uses `poetry` for package management. Before setting up your development environment you will need the following installed and ready to use:\n\n- A virtual environment "manager" of your choosing with a configured and activated virtual environment. Since AIT uses `poetry` you can consider leveraging its `environment management <https://python-poetry.org/docs/managing-environments/>`__ functionality as well.\n    - Using `poetry shell` is also very convenient for development testing and simplifying environment management. You should make sure to install the package into the shell to get access to the development dependencies as well. It\'s recommended that you use `poetry shell` when running the tox builds because other virtual environment managers will often prevent tox from accessing `pyenv`-installed Python versions.\n- `pyenv <https://github.com/pyenv/pyenv>`__ so you can easily install different Python versions\n- `poetry <https://python-poetry.org/docs/#installation>`__ installed either to your specific virtual environment or system-wide, whichever you prefer.\n\nInstall the package in "editable" mode with all the development dependencies by running the following::\n\n    poetry install\n\nAs with a normal installation you will need to point `AIT_CONFIG` at the primary configuration file. You should consider saving this in your shell RC file or your virtual environment configuration files so you don\'t have to reset with every new shell::\n\n    export AIT_CONFIG=/path/to/ait-core/config/config.yaml\n\nYou should configure `pre-commit` by running the following. This will install our pre-commit and pre-push hooks::\n\n    pre-commit install && pre-commit install -t pre-push\n\nFinally, you should install the different Python versions that the project supports so they\'re accessible to `tox`. Using `pyenv` is the easiest way to accomplish this::\n\n    cat .python-version | xargs -I{} pyenv install --skip-existing {}\n\nDev Tools\n---------\n\nTox\n~~~\nUse `tox` to run a thorough build of the toolkit that checks test execution across different Python versions, verifies the docs build, runs the linting pipeline, and checks that the repo packages cleanly. Make sure you run `tox` in Poetry\'s `shell` without another virtual environment active to avoid problems with `tox` finding different python versions for the tests. You can run all of the development tools with::\n\n    tox\n\nYou can see the available `tox` test environments by passing `-l` and execute a specific one by passing its name to `-e`. Run `tox -h` for more info.\n\nTests\n~~~~~\n\nUse `pytest` to manually run the test suite::\n\n    pytest\n\nOr via `tox` for a specific python version::\n\n    tox -e py310\n\n\nCode Checks\n~~~~~~~~~~~\nWe run ``black``, ``flake8``, ``mypy``, and a few other minor checkers on the code base. Our linting and code check pipeline is run whenever you commit or push. If you\'d like to run it manually you can do so with the following::\n\n    pre_commit run --color=always {posargs:--all}\n\nIndividual calls to the tools are configured in ``.pre-commit-config.yaml``. If you\'d like to run a specific tool on its own you can see how we call them there.\n\nYou can run all the linting tools with tox as well::\n\n    tox -e lint\n\n\nDocumentation\n~~~~~~~~~~~~~\n\nAIT uses Sphinx to build its documentation. You can build the documentation with::\n\n    poetry run build_sphinx\n\nTo view the documentation, open ``doc/build/html/index.html`` in a web browser. If you just want to check that the docs build is working you can use tox::\n\n    tox -e docs\n\nIf you need to update the auto-generated documentation you can run the following command to rebuild all of the package documentation::\n\n    sphinx-apidoc --separate --force --no-toc -o doc/source ait --implicit-namespaces\n\nPlease make sure to update the docs if changes in a ticket result in the documentation being out of date.\n\n\nProject Workflow\n----------------\nIssue Tracking\n~~~~~~~~~~~~~~\nAll changes need to be made against one or more tickets for tracking purposes. AIT uses GitHub Issues along with Zenhub to track issue in the project. All tickets should have (outside of rare edge-cases):\n\n- A concise title\n- An in-depth description of the problem / request. If reporting a bug, the description should include information on how to reproduce the bug. Also include the version of the code where you’re seeing the bug.\n\nIf you’re going to begin work on a ticket make sure to progress the ticket through the various Pipeline steps as appropriate as well as assigning yourself as an Assignee. If you lack sufficient permissions to do so you can post on the ticket asking for the above to be done for you.\n\nCommit Messages\n~~~~~~~~~~~~~~~\nAIT projects take a fairly standard approach to commit message formatting. You can checkout Tim Pope\'s blog for a good starting point to figuring out how to format your commit messages. All commit messages should reference a ticket in their title / summary line::\n\n    Issue #248 - Show an example commit message title\n\nThis makes sure that tickets are updated on GitHub with references to commits that are related to them.\n\nCommit should always be atomic. Keep solutions isolated whenever possible. Filler commits such as "clean up white space" or "fix typo" should be rebased out before making a pull request. Please ensure your commit history is clean and meaningful!\n\nCode Formatting and Style\n~~~~~~~~~~~~~~~~~~~~~~~~~\nAIT makes a best-effort attempt at sticking with PEP-8 conventions. This is enforced automatically by ``black`` and checked by ``flake8``. You should run the ``pre-commit`` linting pipeline on any changes you make.\n\nTesting\n~~~~~~~\nWe do our best to make sure that all of our changes are tested. If you\'re fixing a bug you should always have an accompanying unit test to ensure we don\'t regress!\n\nCheck the Developer Tips section below for information on running each repository\'s test suite.\n\nPull Requests and Feature Branches\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nAll changes should be isolated to a feature branch that links to a ticket. The standard across AIT projects is to use issue-### for branch names where ### is the issue number found on GitHub.\n\nThe title of a pull request should include a reference to the ticket being fixed as mentioned for commit messages. The description of a pull request should provide an in-depth explanation of the changes present. Note, if you wrote good commit messages this step should be easy!\n\nAny tickets that are resolved by the pull request should be referenced with GitHub\'s syntax for closing out tickets. Assuming the above ticket we would have the following in a pull request description:\n\nChanges are required to be reviewed by at least one member of the AIT PMC/Committers groups, tests must pass, and the branch must be up to date with master before changes will be merged. If changes are made as part of code review please ensure your commit history is cleaned up.\n\nResolve #248\n--------------\n',
    'author': 'AMMOS Instrument Toolkit Development Team',
    'author_email': 'ait-pmc@googlegroups.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NASA-AMMOS/AIT-Core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
