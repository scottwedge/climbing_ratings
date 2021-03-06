"""Package setup for climbing_ratings"""

# Copyright 2019 Dean Scarff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, Extension
from Cython.Build import cythonize


CYTHON_CFLAGS = [
    "-Ofast",
    "-march=native",
    "-mtune=native",
    "-ffast-math",
    "-fno-math-errno",
    "-fno-associative-math",
    "-fno-reciprocal-math",
]

bradley_terry = Extension(
    "climbing_ratings.bradley_terry",
    ["climbing_ratings/bradley_terry.pyx"],
    extra_compile_args=CYTHON_CFLAGS,
)

climber_helpers = Extension(
    "climbing_ratings.climber_helpers",
    ["climbing_ratings/climber_helpers.pyx"],
    extra_compile_args=CYTHON_CFLAGS,
)

long_description = """
climbing_ratings is a library for estimating ratings for the sport of rock
climbing.  The ratings can be used to predict route difficulty and climber
performance on a particular route.

The algorithms are based on the Whole-History Rating system."""

if __name__ == "__main__":
    setup(
        name="climbing_ratings",
        author="Dean Scarff",
        author_email="dos@scarff.id.au",
        description="Estimate climber and route ratings from ascents data",
        long_description=long_description,
        version="1.1.1",
        url="https://github.com/p00ya/climbing_ratings",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: POSIX",
            "Programming Language :: Cython",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        license="Apache License 2.0",
        data_files=[("", ["LICENSE.txt"])],
        packages=["climbing_ratings", "climbing_ratings.tests"],
        package_data={"climbing_ratings": ["*.pyx"]},
        platforms=["POSIX"],
        install_requires=["numpy"],
        setup_requires=["cython"],
        test_suite="climbing_ratings.tests.test_suite",
        tests_require=["numpy"],
        ext_modules=cythonize(
            [bradley_terry, climber_helpers],
            compiler_directives={
                "language_level": 3,
                "boundscheck": False,
                "cdivision": True,
                "embedsignature": True,
                "initializedcheck": False,
                "nonecheck": False,
                "wraparound": False,
            },
        ),
    )
