#!/usr/bin/env python3
"""Resolve the complete stack in an empty installroot on a disposable EL10 VM."""
import pathlib
import platform
import shutil
import subprocess
import tempfile
import sys
import xml.etree.ElementTree as ET
import libcomps

root = pathlib.Path(__file__).resolve().parents[1]
packages = []
for name in ['cloudmin-core-comps.xml', 'cloudmin-comps.xml']:
    comps = libcomps.Comps()
    if comps.fromxml_f(str(root / name)) == -1:
        raise SystemExit('Invalid comps metadata: ' + name)
    group = ET.parse(root / name)
    for item in group.findall('.//packagereq'):
        if item.get('type') in ('mandatory', 'default') and item.get('arch', platform.machine()) == platform.machine():
            packages.append(item.text)
if '--distribution-only' in sys.argv:
    packages = [p for p in packages if p not in ('cloudmin-config', 'webmin-server-manager')]
assert 'etckeeper' in packages
assert not {'bind', 'postfix', 'firewalld', 'fail2ban-firewalld'} & set(packages)
with tempfile.TemporaryDirectory(prefix='cloudmin-resolve-', dir='/var/tmp') as work:
    # An empty root lacks Rocky's mirror suffix variable supplied by rocky-repos.
    var = pathlib.Path('/etc/dnf/vars/rltype')
    if var.is_file():
        dest = pathlib.Path(work) / 'etc/dnf/vars'
        dest.mkdir(parents=True)
        shutil.copyfile(var, dest / 'rltype')
    result = subprocess.run(['dnf', '--assumeno', '--releasever=10', '--installroot='+work,
        '--setopt=reposdir=/etc/yum.repos.d', '--setopt=install_weak_deps=False',
        '--setopt=strict=1', '--setopt=optional_metadata_types=filelists', '--repofrompath=cloudmin-test,https://download.cloudmin.dev',
        '--repofrompath=webmin-test,https://download.webmin.dev',
        '--setopt=cloudmin-test.gpgkey=https://download.webmin.com/developers-key.asc',
        '--setopt=webmin-test.gpgkey=https://download.webmin.com/developers-key.asc',
        'install', *packages],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = result.stdout
    print(text)
    # --assumeno returns failure after displaying a successfully solved transaction.
    if 'Transaction Summary' not in text or any(s in text for s in ['No match for argument', 'conflicting requests', 'Problem:']):
        raise SystemExit('Fresh RPM dependency resolution failed')
    print('Fresh RPM dependency resolution passed; no packages were installed')
