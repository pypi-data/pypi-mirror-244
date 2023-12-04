# Copyright 2023 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import glob
import logging
import os
import pathlib

import pmb.build
import pmb.config
import pmb.chroot
import pmb.chroot.apk
import pmb.helpers.run


def init_abuild_minimal(args, suffix="native"):
    """ Initialize a minimal chroot with abuild where one can do
        'abuild checksum'. """
    marker = f"{args.work}/chroot_{suffix}/tmp/pmb_chroot_abuild_init_done"
    if os.path.exists(marker):
        return

    pmb.chroot.apk.install(args, ["abuild"], suffix, build=False)

    # Fix permissions
    pmb.chroot.root(args, ["chown", "root:abuild",
                           "/var/cache/distfiles"], suffix)
    pmb.chroot.root(args, ["chmod", "g+w",
                           "/var/cache/distfiles"], suffix)

    # Add user to group abuild
    pmb.chroot.root(args, ["adduser", "pmos", "abuild"], suffix)

    pathlib.Path(marker).touch()


def init(args, suffix="native"):
    """ Initialize a chroot for building packages with abuild. """
    marker = f"{args.work}/chroot_{suffix}/tmp/pmb_chroot_build_init_done"
    if os.path.exists(marker):
        return

    init_abuild_minimal(args, suffix)

    # Initialize chroot, install packages
    pmb.chroot.apk.install(args, pmb.config.build_packages, suffix,
                           build=False)

    # Generate package signing keys
    chroot = args.work + "/chroot_" + suffix
    if not os.path.exists(args.work + "/config_abuild/abuild.conf"):
        logging.info("(" + suffix + ") generate abuild keys")
        pmb.chroot.user(args, ["abuild-keygen", "-n", "-q", "-a"],
                        suffix, env={"PACKAGER": "pmos <pmos@local>"})

        # Copy package signing key to /etc/apk/keys
        for key in glob.glob(chroot +
                             "/mnt/pmbootstrap/abuild-config/*.pub"):
            key = key[len(chroot):]
            pmb.chroot.root(args, ["cp", key, "/etc/apk/keys/"], suffix)

    # Add gzip wrapper that converts '-9' to '-1'
    if not os.path.exists(chroot + "/usr/local/bin/gzip"):
        with open(chroot + "/tmp/gzip_wrapper.sh", "w") as handle:
            content = """
                #!/bin/sh
                # Simple wrapper that converts -9 flag for gzip to -1 for
                # speed improvement with abuild. FIXME: upstream to abuild
                # with a flag!
                args=""
                for arg in "$@"; do
                    [ "$arg" == "-9" ] && arg="-1"
                    args="$args $arg"
                done
                /bin/gzip $args
            """
            lines = content.split("\n")[1:]
            for i in range(len(lines)):
                lines[i] = lines[i][16:]
            handle.write("\n".join(lines))
        pmb.chroot.root(args, ["cp", "/tmp/gzip_wrapper.sh",
                               "/usr/local/bin/gzip"], suffix)
        pmb.chroot.root(args, ["chmod", "+x", "/usr/local/bin/gzip"], suffix)

    # abuild.conf: Don't clean the build folder after building, so we can
    # inspect it afterwards for debugging
    pmb.chroot.root(args, ["sed", "-i", "-e", "s/^CLEANUP=.*/CLEANUP=''/",
                           "/etc/abuild.conf"], suffix)

    # abuild.conf: Don't clean up installed packages in strict mode, so
    # abuild exits directly when pressing ^C in pmbootstrap.
    pmb.chroot.root(args, ["sed", "-i", "-e",
                           "s/^ERROR_CLEANUP=.*/ERROR_CLEANUP=''/",
                           "/etc/abuild.conf"], suffix)

    pathlib.Path(marker).touch()


def init_compiler(args, depends, cross, arch):
    cross_pkgs = ["ccache-cross-symlinks"]
    if "gcc4" in depends:
        cross_pkgs += ["gcc4-" + arch]
    elif "gcc6" in depends:
        cross_pkgs += ["gcc6-" + arch]
    else:
        cross_pkgs += ["gcc-" + arch, "g++-" + arch]
    if "clang" in depends or "clang-dev" in depends:
        cross_pkgs += ["clang"]
    if cross == "crossdirect":
        cross_pkgs += ["crossdirect"]
        if "rust" in depends or "cargo" in depends:
            if args.ccache:
                cross_pkgs += ["sccache"]
            # crossdirect for rust installs all build dependencies in the
            # native chroot too, as some of them can be required for building
            # native macros / build scripts
            cross_pkgs += depends

    pmb.chroot.apk.install(args, cross_pkgs)
