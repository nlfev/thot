# Third-Party Licenses

This document lists the open-source software components used in the NLF Database Management System and their respective licenses.

## License Compatibility

All third-party components used in this project are compatible with the AGPL-3.0-or-later license under which this software is distributed.

---

## Backend Dependencies (Python)

### Core Framework & Web Server

#### FastAPI
- **License:** MIT License
- **Copyright:** © Sebastián Ramírez
- **Description:** Modern, fast web framework for building APIs
- **Homepage:** https://fastapi.tiangolo.com/
- **License Text:** https://github.com/tiangolo/fastapi/blob/master/LICENSE

#### Uvicorn
- **License:** BSD 3-Clause License
- **Copyright:** © Encode OSS Ltd.
- **Description:** ASGI web server implementation
- **Homepage:** https://www.uvicorn.org/
- **License Text:** https://github.com/encode/uvicorn/blob/master/LICENSE.md

### Database

#### SQLAlchemy
- **License:** MIT License
- **Copyright:** © 2005-2023 SQLAlchemy authors and contributors
- **Description:** SQL toolkit and Object-Relational Mapping (ORM) library
- **Homepage:** https://www.sqlalchemy.org/
- **License Text:** https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE

#### psycopg2-binary
- **License:** LGPL 3.0
- **Copyright:** © 2001-2021 Federico Di Gregorio
- **Description:** PostgreSQL database adapter for Python
- **Homepage:** https://www.psycopg.org/
- **License Text:** https://github.com/psycopg/psycopg2/blob/master/LICENSE
- **Note:** LGPL allows linking with AGPL software

#### Alembic
- **License:** MIT License
- **Copyright:** © 2009-2023 Michael Bayer
- **Description:** Database migration tool for SQLAlchemy
- **Homepage:** https://alembic.sqlalchemy.org/
- **License Text:** https://github.com/sqlalchemy/alembic/blob/main/LICENSE

### Data Validation & Serialization

#### Pydantic
- **License:** MIT License
- **Copyright:** © Samuel Colvin and other contributors
- **Description:** Data validation using Python type annotations
- **Homepage:** https://pydantic-docs.helpmanual.io/
- **License Text:** https://github.com/pydantic/pydantic/blob/main/LICENSE

### Security & Authentication

#### PyJWT
- **License:** MIT License
- **Copyright:** © José Padilla
- **Description:** JSON Web Token implementation
- **Homepage:** https://pyjwt.readthedocs.io/
- **License Text:** https://github.com/jpadilla/pyjwt/blob/master/LICENSE

#### bcrypt
- **License:** Apache License 2.0
- **Copyright:** © The bcrypt developers
- **Description:** Password hashing library
- **Homepage:** https://github.com/pyca/bcrypt/
- **License Text:** https://github.com/pyca/bcrypt/blob/main/LICENSE

#### pyotp
- **License:** MIT License
- **Copyright:** © Mark Percival and Contributors
- **Description:** Python One-Time Password Library
- **Homepage:** https://github.com/pyauth/pyotp
- **License Text:** https://github.com/pyauth/pyotp/blob/develop/LICENSE

#### qrcode
- **License:** BSD 3-Clause License
- **Copyright:** © Lincoln Loop
- **Description:** QR Code image generator
- **Homepage:** https://github.com/lincolnloop/python-qrcode
- **License Text:** https://github.com/lincolnloop/python-qrcode/blob/main/LICENSE

### PDF Processing

#### PyPDF
- **License:** BSD 3-Clause License
- **Copyright:** © Mathieu Fenniak and PyPDF contributors
- **Description:** PDF toolkit for Python
- **Homepage:** https://pypdf.readthedocs.io/
- **License Text:** https://github.com/py-pdf/pypdf/blob/main/LICENSE

#### ReportLab
- **License:** BSD License (ReportLab Open Source License)
- **Copyright:** © ReportLab Inc.
- **Description:** PDF generation library
- **Homepage:** https://www.reportlab.com/opensource/
- **License Text:** https://bitbucket.org/rptlab/reportlab/src/default/LICENSE.txt

#### PyMuPDF (fitz)
- **License:** GNU Affero General Public License v3.0 (AGPL-3.0)
- **Copyright:** © Artifex Software, Inc.
- **Description:** Python bindings for MuPDF - PDF and document processing
- **Homepage:** https://pymupdf.readthedocs.io/
- **License Text:** https://github.com/pymupdf/PyMuPDF/blob/master/COPYING
- **Note:** AGPL-licensed, same as this project

### Image Processing

#### Pillow (PIL Fork)
- **License:** HPND (Historical Permission Notice and Disclaimer)
- **Copyright:** © 1997-2011 Secret Labs AB, © 1995-2011 Fredrik Lundh, © 2010-2023 Jeffrey A. Clark and contributors
- **Description:** Python Imaging Library
- **Homepage:** https://pillow.readthedocs.io/
- **License Text:** https://github.com/python-pillow/Pillow/blob/main/LICENSE

### Utilities

#### python-multipart
- **License:** Apache License 2.0
- **Copyright:** © Andrew Dunham
- **Description:** Streaming multipart parser for Python
- **Homepage:** https://github.com/andrew-d/python-multipart
- **License Text:** https://github.com/andrew-d/python-multipart/blob/master/LICENSE.txt

#### python-dotenv
- **License:** BSD 3-Clause License
- **Copyright:** © Saurabh Kumar
- **Description:** Read key-value pairs from .env files
- **Homepage:** https://github.com/theskumar/python-dotenv
- **License Text:** https://github.com/theskumar/python-dotenv/blob/main/LICENSE

#### aiofiles
- **License:** Apache License 2.0
- **Copyright:** © Tin Tvrtković
- **Description:** File support for asyncio
- **Homepage:** https://github.com/Tinche/aiofiles
- **License Text:** https://github.com/Tinche/aiofiles/blob/main/LICENSE

#### python-dateutil
- **License:** Apache License 2.0 / BSD 3-Clause
- **Copyright:** © Gustavo Niemeyer
- **Description:** Extensions to the standard Python datetime module
- **Homepage:** https://dateutil.readthedocs.io/
- **License Text:** https://github.com/dateutil/dateutil/blob/master/LICENSE

### Logging

#### python-json-logger
- **License:** BSD 2-Clause License
- **Copyright:** © Zakaria Zajac
- **Description:** JSON log formatter
- **Homepage:** https://github.com/madzak/python-json-logger
- **License Text:** https://github.com/madzak/python-json-logger/blob/master/LICENSE

### Development & Testing

#### pytest
- **License:** MIT License
- **Copyright:** © Holger Krekel and pytest-dev team
- **Description:** Testing framework
- **Homepage:** https://pytest.org/
- **License Text:** https://github.com/pytest-dev/pytest/blob/main/LICENSE

#### pytest-asyncio
- **License:** Apache License 2.0
- **Copyright:** © pytest-asyncio contributors
- **Description:** Pytest support for asyncio
- **Homepage:** https://github.com/pytest-dev/pytest-asyncio
- **License Text:** https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE

#### pytest-cov
- **License:** MIT License
- **Copyright:** © pytest-cov contributors
- **Description:** Coverage plugin for pytest
- **Homepage:** https://github.com/pytest-dev/pytest-cov
- **License Text:** https://github.com/pytest-dev/pytest-cov/blob/master/LICENSE

#### httpx
- **License:** BSD 3-Clause License
- **Copyright:** © Encode OSS Ltd.
- **Description:** HTTP client for Python
- **Homepage:** https://www.python-httpx.org/
- **License Text:** https://github.com/encode/httpx/blob/master/LICENSE.md

#### Black
- **License:** MIT License
- **Copyright:** © Black Contributors
- **Description:** Python code formatter
- **Homepage:** https://github.com/psf/black
- **License Text:** https://github.com/psf/black/blob/main/LICENSE

#### Flake8
- **License:** MIT License
- **Copyright:** © Flake8 contributors
- **Description:** Python style guide enforcement tool
- **Homepage:** https://github.com/PyCQA/flake8
- **License Text:** https://github.com/PyCQA/flake8/blob/main/LICENSE

#### isort
- **License:** MIT License
- **Copyright:** © Timothée Mazzucotelli and contributors
- **Description:** Python import sorting utility
- **Homepage:** https://github.com/PyCQA/isort
- **License Text:** https://github.com/PyCQA/isort/blob/main/LICENSE

#### IPython
- **License:** BSD 3-Clause License
- **Copyright:** © IPython Development Team
- **Description:** Interactive Python shell for development
- **Homepage:** https://ipython.org/
- **License Text:** https://github.com/ipython/ipython/blob/main/COPYING.rst

---

## Frontend Dependencies (JavaScript/Node.js)

### Core Framework

#### Vue.js
- **License:** MIT License
- **Copyright:** © 2013-present Evan You
- **Description:** Progressive JavaScript framework for building user interfaces
- **Homepage:** https://vuejs.org/
- **License Text:** https://github.com/vuejs/core/blob/main/LICENSE

#### Vite
- **License:** MIT License
- **Copyright:** © 2019-present Evan You & Vite Contributors
- **Description:** Next generation frontend tooling
- **Homepage:** https://vitejs.dev/
- **License Text:** https://github.com/vitejs/vite/blob/main/LICENSE

### State Management & Routing

#### Pinia
- **License:** MIT License
- **Copyright:** © 2019-present Eduardo San Martin Morote
- **Description:** Vue Store - intuitive, type safe and flexible
- **Homepage:** https://pinia.vuejs.org/
- **License Text:** https://github.com/vuejs/pinia/blob/v2/LICENSE

#### Vue Router
- **License:** MIT License
- **Copyright:** © 2013-present Evan You
- **Description:** Official router for Vue.js
- **Homepage:** https://router.vuejs.org/
- **License Text:** https://github.com/vuejs/router/blob/main/LICENSE

### Internationalization

#### Vue I18n
- **License:** MIT License
- **Copyright:** © 2016 kazuya kawaguchi
- **Description:** Internationalization plugin for Vue.js
- **Homepage:** https://vue-i18n.intlify.dev/
- **License Text:** https://github.com/intlify/vue-i18n-next/blob/master/LICENSE

### HTTP Client

#### Axios
- **License:** MIT License
- **Copyright:** © 2014-present Matt Zabriskie
- **Description:** Promise based HTTP client
- **Homepage:** https://axios-http.com/
- **License Text:** https://github.com/axios/axios/blob/main/LICENSE

### Documentation

#### Swagger UI Distribution
- **License:** Apache License 2.0
- **Copyright:** © SmartBear Software
- **Description:** API documentation UI
- **Homepage:** https://swagger.io/tools/swagger-ui/
- **License Text:** https://github.com/swagger-api/swagger-ui/blob/master/LICENSE

### Development & Testing

#### Vitest
- **License:** MIT License
- **Copyright:** © 2021-present Anthony Fu, Matías Capeletto
- **Description:** Blazing fast unit test framework
- **Homepage:** https://vitest.dev/
- **License Text:** https://github.com/vitest-dev/vitest/blob/main/LICENSE

#### @vue/test-utils
- **License:** MIT License
- **Copyright:** © 2013-present Evan You
- **Description:** Official testing utilities for Vue.js
- **Homepage:** https://test-utils.vuejs.org/
- **License Text:** https://github.com/vuejs/test-utils/blob/main/LICENSE

#### happy-dom
- **License:** MIT License
- **Copyright:** © David Ortner
- **Description:** JavaScript implementation of a web browser for Node.js
- **Homepage:** https://github.com/capricorn86/happy-dom
- **License Text:** https://github.com/capricorn86/happy-dom/blob/master/LICENSE

#### @vitejs/plugin-vue
- **License:** MIT License
- **Copyright:** © 2019-present Evan You & Vite Contributors
- **Description:** Official Vue plugin for Vite
- **Homepage:** https://github.com/vitejs/vite/tree/main/packages/plugin-vue
- **License Text:** https://github.com/vitejs/vite/blob/main/LICENSE

#### ESLint
- **License:** MIT License
- **Copyright:** © OpenJS Foundation and contributors
- **Description:** JavaScript and Vue linting engine
- **Homepage:** https://eslint.org/
- **License Text:** https://github.com/eslint/eslint/blob/main/LICENSE

#### eslint-plugin-vue
- **License:** MIT License
- **Copyright:** © eslint-plugin-vue contributors
- **Description:** Official ESLint plugin for Vue.js
- **Homepage:** https://github.com/vuejs/eslint-plugin-vue
- **License Text:** https://github.com/vuejs/eslint-plugin-vue/blob/master/LICENSE

---

## License Categories Summary

### Compatible Open Source Licenses Used

1. **MIT License** - Most permissive, AGPL-compatible
   - FastAPI, SQLAlchemy, Pydantic, PyJWT, Vue.js, Vite, Axios, and many others

2. **BSD License (2-Clause & 3-Clause)** - Permissive, AGPL-compatible
   - Uvicorn, PyPDF, ReportLab, python-dotenv, and others

3. **Apache License 2.0** - Permissive, AGPL-compatible
   - bcrypt, aiofiles, Swagger UI, and others

4. **LGPL 3.0** - Copyleft for libraries, AGPL-compatible when linking
   - psycopg2-binary

5. **AGPL-3.0** - Strong copyleft, same as this project
   - PyMuPDF

6. **HPND** - Historical permissive license, AGPL-compatible
   - Pillow

---

## Obtaining Source Code

As required by the AGPL-3.0-or-later license, the complete source code of this application, including all modifications, is available at:

**[Git Repository Link - To Be Added]**

The repository has not yet been published on GitHub/Gitea. It will be published with full source code and license notices.

For any of the third-party components listed above, their source code is available at the respective project homepages and repository links provided.

---

## License Compliance Statement

This software complies with all license obligations of the included third-party components. All permissive licenses (MIT, BSD, Apache 2.0) allow use in AGPL-licensed projects. The LGPL-licensed psycopg2 is used as a library, which is permitted. PyMuPDF shares the same AGPL license as this project.

---

## Questions?

If you have any questions about licensing or need access to specific source code, please contact the project maintainers.
Once published, please open issues via the project Git repository.

---

**Last Updated:** March 7, 2026

**Project License:** GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)
