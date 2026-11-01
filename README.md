# Cloudmin RPM groups

Host packages for **Rocky Linux 10** and **AlmaLinux 10**, on x86-64 and ARM64.
The installer enables the distribution's CRB and EPEL repositories and the
current Webmin and Cloudmin repositories. No custom libvirt packages are used.

Debian 13 and Ubuntu 26.04 use the DEB packages in `cloudmin-core-meta` and
`cloudmin-stack-meta`. Cloudmin-Config supports their stock monolithic libvirtd
as well as modular libvirt daemons.

- `cloudmincore`: Cloudmin-Config, Webmin, the Cloudmin module, Etckeeper and Perl libraries.
- `cloudmin-kvm`: QEMU/KVM, modular libvirt, guest-image tools, nftables and Fail2ban.

Webmin's core package includes xterm, nftables, proc, mount, useradmin and init;
these do not need separate packages. Firmware is selected by architecture:
`edk2-aarch64` on ARM64 and `edk2-ovmf` on x86-64.

DNF installs mandatory and default group members normally, including Etckeeper
for configuration history. BIND, Postfix and Firewalld are not group members. Install with weak dependencies
disabled, as cloudmin-install does, to avoid unrelated suggested services.

Keep host dependency changes here. Publish these groups alongside the matching
Cloudmin 10 module, Cloudmin-Config 10.0.0 or newer, and installer.

## Validation

On a disposable supported host, `python3 t/resolve.py` resolves all dependencies
in an empty installroot with `--assumeno`. It installs no packages. The test uses
current development repositories; resolution alone does not verify the contents
of an unpublished Cloudmin 10 build. Use `--distribution-only` to check only OS,
EPEL and Webmin dependencies before publishing the Cloudmin artifacts.

DNF needs `optional_metadata_types=filelists` for file-based Webmin dependencies.
Fresh-install and boot tests are still needed on both distributions and CPU
architectures before calling the matrix production-tested.
