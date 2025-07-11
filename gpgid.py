#!/usr/bin/env python

import os
import shutil
import tempfile
import zipfile

import gnupg

FILE_BASENAME = "identity"
FILE_FORMAT = "zip"

class GPGIdentity:

    def __init__(self):
        self.gnupghome_ephemeral = tempfile.TemporaryDirectory()

        #  self.gpg = gnupg.GPG(gnupghome=self.gnupghome_ephemeral.name)
        #  self.gpg.encoding = "utf-8"

    def generate(self):
        self.start_gpg()

        params = {
                "key_type": "RSA",
                "key_length": 2048,
                "no_protection": True,
                }
        input_data = self.gpg.gen_key_input(**params)
        master_key = self.gpg.gen_key(input=input_data)

        subkey = self.gpg.add_subkey(master_key=master_key.fingerprint,
                                     master_passphrase="")

        self.master_key = master_key
        self.subkey = subkey

        shutil.make_archive(base_name=FILE_BASENAME,
                            format=FILE_FORMAT,
                            root_dir=self.gnupghome_ephemeral.name)


    def load(self):
        with zipfile.ZipFile(name=f"{FILE_BASENAME}.{FILE_FORMAT}",
                             mode="r") as identity_file:  # pyright: ignore

            identity_file.extractall(path=self.gnupghome_ephemeral.name)

        self.start_gpg()

    def start_gpg(self):
        self.gpg = gnupg.GPG(gnupghome=self.gnupghome_ephemeral.name)
        self.gpg.encoding = "utf-8"

