# cloudmin-yum-groups
Group definition files for yum/dnf used by cloudmin-install on RHEL/Rocky/Alma

# What's this?

When installing Cloudmin on a RHEL/Rocky/Alma system, it uses dnf to install all of the dependencies and Cloudmin itself.

If you're helping out with the install script, dependencies *must* be added here (and in the Debian/Ubuntu metapackages, which will be posted soon, as well), rather than directly in the install script.

# Optional vs. Mandatory

When performing a group install, yum will install all of the packages listed in the group labeled either "mandatory" or "optional". The difference is that "optional" packages can be disabled with command line switches. The decision for what is mandatory and optional for Cloudmin system is somewhat arbitrary, but my position right now is that if Cloudmin needs something to perform its core functions, it is mandatory and if it is a feature that a lot of people like but some number of systems never use the package, it is optional. Err on the side of requiring fewer rather than more packages.

# Group Names

*Cloudmin Core* - This is the really core Cloudmin packages that have the same name across all RPM-based distros. Specifically, all of the Webmin modules, Perl modules, etc., and should be installable on *any* RPM-based distribution with Perl 5.16 or above, as long as the Webmin RPM installs and functions correctly. Even if you can't use the Cloudmin install script or the automated install on your Linux distribution, if you have a dnf-based distro, you can install this group of packages to get Webmin and all of its modules, and have them update via dnf.

*Cloudmin KVM* - This is all the other dependencies for a full-featured Cloudmin system using KVM for virtualization.

*Cloudmin Xen* - This is all the other dependencies for a full-featured Cloudmin system using Xen for virtualization.
