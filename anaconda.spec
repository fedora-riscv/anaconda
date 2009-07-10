%define livearches %{ix86} x86_64 ppc ppc64
%define _libdir %{_prefix}/lib

Summary: Graphical system installer
Name:    anaconda
Version: 12.2
Release: 1%{?dist}
License: GPLv2+
Group:   Applications/System
URL:     http://fedoraproject.org/wiki/Anaconda

# To generate Source0 do:
# git clone http://git.fedorahosted.org/git/anaconda.git
# git checkout -b archive-branch anaconda-%{version}-%{release}
# make dist
Source0: %{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Versions of required components (done so we make sure the buildrequires
# match the requires versions of things).
%define dmver 1.02.17-6
%define gettextver 0.11
%define genisoimagever 1.1.9-4
%define intltoolver 0.31.2-3
%define libnlver 1.0
%define libselinuxver 1.6
%define mkinitrdver 5.1.2-1
%define pykickstartver 1.56
%define rpmpythonver 4.2-0.61
%define slangver 2.0.6-2
%define yumver 2.9.2
%define rhplver 0.170
%define partedver 1.8.1
%define pypartedver 2.0.0
%define syscfgdatever 1.9.0
%define pythonpyblockver 0.24-1
%define libbdevidver 5.1.2-1
%define e2fsver 1.41.0
%define nmver 1:0.7.1-3.git20090414
%define dbusver 1.2.3
%define createrepover 0.4.7
%define yumutilsver 1.1.11-3
%define iscsiver 6.2.0.870-3
%define pythoncryptsetupver 0.0.6

BuildRequires: audit-libs-devel
BuildRequires: bzip2-devel
BuildRequires: device-mapper-devel >= %{dmver}
BuildRequires: e2fsprogs-devel >= %{e2fsver}
BuildRequires: elfutils-devel
BuildRequires: gettext >= %{gettextver}
BuildRequires: gtk2-devel
BuildRequires: intltool >= %{intltoolver}
BuildRequires: isomd5sum-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXxf86misc-devel
BuildRequires: libnl-devel >= %{libnlver}
BuildRequires: libselinux-devel >= %{libselinuxver}
BuildRequires: libsepol-devel
BuildRequires: libxml2-python
BuildRequires: mkinitrd-devel >= %{mkinitrdver}
BuildRequires: newt-devel
BuildRequires: pango-devel
BuildRequires: popt-devel
BuildRequires: pykickstart >= %{pykickstartver}
BuildRequires: python-devel
BuildRequires: python-urlgrabber
BuildRequires: rhpl
BuildRequires: rpm-python >= %{rpmpythonver}
BuildRequires: slang-devel >= %{slangver}
BuildRequires: xmlto
BuildRequires: yum >= %{yumver}
BuildRequires: zlib-devel
BuildRequires: NetworkManager-devel >= %{nmver}
BuildRequires: NetworkManager-glib-devel >= %{nmver}
BuildRequires: dbus-devel >= %{dbusver}
%ifarch %livearches
BuildRequires: desktop-file-utils
%endif
BuildRequires: iscsi-initiator-utils-devel >= %{iscsiver}

Requires: policycoreutils
Requires: rpm-python >= %{rpmpythonver}
Requires: comps-extras
Requires: rhpl >= %{rhplver}
Requires: parted >= %{partedver}
Requires: pyparted >= %{pypartedver}
Requires: yum >= %{yumver}
Requires: libxml2-python
Requires: python-urlgrabber
Requires: system-logos
Requires: pykickstart >= %{pykickstartver}
Requires: system-config-date >= %{syscfgdatever}
Requires: device-mapper >= %{dmver}
Requires: device-mapper-libs >= %{dmver}
Requires: dosfstools
Requires: e2fsprogs >= %{e2fsver}
Requires: gzip
%ifarch %{ix86} x86_64 ia64
Requires: dmidecode
%endif
Requires: python-pyblock >= %{pythonpyblockver}
Requires: libbdevid >= %{libbdevidver}
Requires: libbdevid-python
Requires: libuser-python
Requires: newt-python
Requires: authconfig
Requires: gnome-python2-gtkhtml2
Requires: system-config-firewall
Requires: cryptsetup-luks
Requires: python-cryptsetup >= %{pythoncryptsetupver}
Requires: mdadm
Requires: lvm2
Requires: util-linux-ng >= 2.15.1
%ifnarch s390 s390x ppc64
Requires: system-config-keyboard
%endif
Requires: hal, dbus-python
Requires: cracklib-python
Requires: python-bugzilla
%ifarch %livearches
Requires: usermode
Requires: zenity
%endif
Requires: createrepo >= %{createrepover}
Requires: squashfs-tools
Requires: genisoimage >= %{genisoimagever}
%ifarch %{ix86} x86_64
Requires: syslinux >= 3.73
Requires: makebootfat
Requires: device-mapper
%endif
%ifarch s390 s390x
Requires: openssh
%endif
Requires: isomd5sum
Requires: yum-utils >= %{yumutilsver}
Requires: NetworkManager >= %{nmver}
Requires: dhclient
Requires: dhcpv6-client
Requires: anaconda-yum-plugins
Requires: libselinux-python >= %{libselinuxver}
Obsoletes: anaconda-images <= 10
Provides: anaconda-images = %{version}-%{release}
Obsoletes: anaconda-runtime < %{version}-%{release}
Provides: anaconda-runtime = %{version}-%{release}
Obsoletes: booty

%description
The anaconda package contains the program which was used to install your
system.  These files are of little use on an already installed system.

%prep
%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" | xargs %{__rm}

%ifarch %livearches
desktop-file-install --vendor="" --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/liveinst.desktop
%endif

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%ifarch %livearches
%post
update-desktop-database &> /dev/null || :
%endif

%ifarch %livearches
%postun
update-desktop-database &> /dev/null || :
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc ChangeLog
%doc docs/command-line.txt
%doc docs/install-methods.txt
%doc docs/kickstart-docs.txt
%doc docs/mediacheck.txt
%doc docs/anaconda-release-notes.txt
/lib/udev/rules.d/70-anaconda.rules
%{_bindir}/mini-wm
%{_sbindir}/anaconda
%ifarch i386 i486 i586 i686 x86_64
%{_sbindir}/gptsync
%{_sbindir}/showpart
%endif
%{_datadir}/anaconda
%{_prefix}/lib/anaconda
%{_prefix}/lib/anaconda-runtime
%ifarch %livearches
%{_bindir}/liveinst
%{_sbindir}/liveinst
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_datadir}/applications/*.desktop
%endif

%changelog
* Thu Jul 09 2009 David Cantrell <dcantrell@redhat.com> - 12.2-1
- mdmon added to install.img (Jacek.Danecki)
- Remove some unnecessary code. (clumens)
- Use a method yum provides, rather than inventing our own. (clumens)
- Remove _catchallCategory.  yum handles this for us now. (clumens)
- Write out NM_CONTROLLED=no for NICs used for FCoE (hdegoede)
- Add support for biosraid using mdadm (hdegoede)
- Reverse: "Support for MD containers" (hdegoede)
- When all udev_is-foo() checks fail return instead of backtracing (hdegoede)
- 70-anaconda.rules: always import blkid output (hdegoede)
- Make sure to have "self" as an argument. (clumens)
- Add kickstart fcoe command (hdegoede)
- Use the yum preconf object to do $releasever substitution. (clumens)
- Indicate LV status according to lv_attr active bit (#491754) (dcantrell)
- Include lv_attr in lvm.lvs() return value. (dcantrell)
- Fix list of 64-bit arches. (notting)
- We also need -DUSESELINUX if we want to call matchPathContext. (clumens)
- Clean up some arch code. (notting)
- Update /etc/hosts with hostname for loopback IP address (#506384)
  (rvykydal)
- Add missing LAYER2 and PORTNO handling for s390x. (dcantrell)
- Ignore configure.ac when generating updates.img (dcantrell)
- AC_ARG_WITH -> AC_ARG_ENABLE (dcantrell)
- dhclient now reads config files from /etc/dhcp (dcantrell)
- no "rhgb quiet" on s390 to enable visible boot progress and system
  automation (#509881) (maier)
- fix backtrace in s390 reipl support due to missing anaconda.id.fsset
  (#509877) (maier)
- Put sleep in /bin on the initrd (#505639). (clumens)
- Also include the grep programs. (clumens)
- Add programs from vim-minimal, coreutils, and util-linux-ng. (clumens)
- Move programs that aren't s390-specific into the main image. (clumens)
- Look for /bin/sh, not /sbin/busybox. (clumens)
- No longer symlink binaries to busybox. (clumens)
- No longer require busybox. (clumens)

* Mon Jul 06 2009 Chris Lumens <clumens@redhat.com> - 12.1-1
- Include the rest of the libs isys needs to link against (#509572).
  (clumens)
- Add FCoE disks to the devicetree with a type of FcoeDiskDevice (hdegoede)
- Add FcoeDiskDevice class to storage/devices.py (hdegoede)
- Add FCoE support to storage/udev.py (hdegoede)
- Write out configuration of FCoE to installed system (hdegoede)
- Initial FCoE support (hdegoede)

* Thu Jul 02 2009 Chris Lumens <clumens@redhat.com> - 12.0-1
- network --bootproto no longer implies DHCP. (clumens)
- Don't unconditionally skip the network config screen in kickstart. (clumens)
- Allow creating new groups through kickstart. (clumens)
- Set focus on hostname entry in network UI screen (#494135) (rvykydal)
- Fix upgrade selected in UI after storage reset (#503302) (rvykydal)
- Add support for specifying upgrade partition in ks (#471232) (rvykydal)
- Add missing liveinst/* files. (dcantrell)
- Update code that checks for devices that contain install media. (dlehman)
- Rework tracking of devices containing installation media. (#497087) (dlehman)
- Add function storage.udev.udev_resolve_devspec. (dlehman)
- Prevent false positives in devtree's device lookup methods. (dlehman)
- Skip exceptionDisks if exn originated in devtree.populate. (#497240) (dlehman)
- Stop using rhpl.arch in writeRpmPlatform() (katzj)
- Move simpleconfig (back) into anaconda from rhpl (katzj)
- Use iutil arch specifiers rather than rhpl (katzj)
- Remove unused rhpl imports (katzj)
- Switch to using iutil.isS390 instead of rhpl.getArch (katzj)
- Stop using rhpl.translate (katzj)
- Default to /boot on ext4 (katzj)
- Allow /boot on ext4 now that we have a grub that allows it (katzj)
- Make sure the library directory is always set (notting)
- Write out "MAILADDR root" into mdadm.conf (#508321) (rvykydal)
- Do not install grub more times than needed. (rvykydal)
- Ensure we set the SELinux context correctly on symlinks (#505054) (katzj)
- udev dropped vol_id (#506360) (katzj)
- Handle installing multilib into the installer intramfs correctly. (notting)
- Set LIBDIR appropriately on PPC64. (notting)
- Fix grub upgrade (#505966) (rvykydal)
- Include yum.log in anacdump.txt too. (rvykydal)
- Access format options property instead of mountopts attr. (#506219) (dlehman)
- Be more careful about identifying NFS fstab entries. (dlehman)
- Don't add leading directory for files twice. (#503830) (dlehman)
- booty changes for iswmd (Jacek.Danecki)
- Support for MD containers. (Jacek.Danecki)
- New iswmd parameter for kernel cmdline (Jacek.Danecki)
- New udev rule for using mdadm for isw_raid_member (Jacek.Danecki)
- Use isohybrid to make boot.iso a hybrid image (katzj)
- Log yum messages. (rvykydal)
- Tell booty to rescan for bootable drivers when an extra disks get
  added (hdegoede)
- Do not encourage VNC when doing kickstart text installs (#506534) (dcantrell)
- Rename bootstrap to autogen.sh (dcantrell)
- Include the contents of /proc/cmdline in exception reports (katzj)
- Include libwrap library for sshd and telnet in s390 installs (jgranado)
- Enforcing matching rootfs type on LVs as well as for partitions
  (#504743) (katzj)
- Remove problem packages before attempting a re-download (#501887). (clumens)
- Be more explicit about what's lacking on EFI systems (#501341). (clumens)
- If not enough memory is installed, enforce swap partition creation
  (#498742). (clumens)
- Convert to using automake/autoconf. (dcantrell)
- Convert po/ subdirectory to GNU gettext template system. (dcantrell)
- Restructure liveinst/ for the new build system. (dcantrell)
- Add m4/ subdirectory with autoconf macros. (dcantrell)
- Removed py-compile script. (dcantrell)
- Rename anaconda.spec to anaconda.spec.in (dcantrell)
- Ignore autoconf and automake files in the tree. (dcantrell)
- Removed toplevel Makefile and Makefile.inc (dcantrell)
- Show MAC address of network device in combo box (#504216) (dcantrell)
- Remove loader/tr/.cvsignore (dcantrell)
- Increase max NIC identification duration to 5 minutes (#473747). (dcantrell)
- Use /sbin/ipcalc for IP address validation (#460579) (dcantrell)
- Fix an obvious traceback when doing part --ondisk= (#504687). (clumens)
- Catch errors from bootloader installation (#502210). (clumens)
- Remove umask temporarily so device permissions are correct
  (#383531, wmealing).
- Remove the name check on driver disk packages (#472951). (clumens)
- Make the installation key text more descriptive (#474375). (clumens)
- Fix discovery of existing raid/lvm for ks install without clearpart
  (#503310, #503681) (rvykydal)
- Use the F12 version of the bootloader command. (clumens)
- It's /sbin/fsadm, not /sbin/e2fsadm (#504043). (clumens)
- Remove the bootloader --lba32 option. (clumens)
- Use gettext.ldngettext when necessary (#467603) (dcantrell)
- Test NM_CONTROLLED setting correctly in network.py (#502466) (dcantrell)
- Show unknown partitions as "Unknown" in partition editor. (dcantrell)
- Add a type hint on popup windows (rstrode). (clumens)
- Use the F12 version of the driverdisk command. (clumens)
- Remove driverdisk --type, since mount can figure that out. (clumens)
- Fix an error when editing an unreachable repo (#503454). (clumens)
- If /etc/rpm/platform is found, move it out of the way. (clumens)
- We no longer write out /etc/rpm/platform, so don't offer to upgrade
  it. (clumens)
- Remove locals containing "passphrase" or "password" from exns
  (#503442). (clumens)
- Make progress bars modal (#493263, #498553, rstrode). (clumens)
- Make sure to import os.path if we are going to use it. (jgranado)
- ipcalc is copied to /usr/lib. (jgranado)
- Limit the trigger to block type devices. (jgranado)
- We need ipcalc for new s390 installation script. (jgranado)
- Fix off-by-one errors in read. (notting)
- sysconfig file changed names for system-config-firewall (katzj)
- Don't write out firewall settings if they already exist (#502479) (katzj)
- Make sure that the devices are correctly detected (#491700) (jgranado)
- Make the save-to-bugzilla dupe detection smarter. (clumens)
- If network --device=MAC is given, translate to device name
  (#185522). (clumens)
- Add a function to convert MAC addresses to device names. (clumens)
- Move /boot checks from sanityCheck into Platform.checkBootRequest. (clumens)
- Return translated strings from checkBootRequest. (clumens)
- Check that /boot is on a Mac disk label for PPC installs (#497745). (clumens)
- Call checkBootRequest from sanityCheck. (clumens)
- Put some space in that big scary warning. (clumens)
- fond -> found (clumens)
- Use powers of two in swapSuggestion (#463885). (clumens)
- Trim "mapper/" off device names in the bootloader UI (#501057). (clumens)
- Make the weak password dialog comply with the HIG (#487435). (clumens)
- Add a newline to a cmdline mode string (#497575). (clumens)

* Tue Jun 02 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.59-1
- Do not show disabled repos such as rawhide during the install (#503798).
  (jkeating)

* Sun May 31 2009 David Lehman <dlehman@redhat.com> - 11.5.0.58-1
- Pass --force to lvresize so it doesn't ask for confirmation. (dlehman)
- Fix a typo in action sorting for resize actions (fs vs. device). (#501000)
  (dlehman)
- Sending translation for French (mrtom)

* Thu May 28 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.57-1
- Create and use unique ids for Device instances. (#500808) (dlehman)
- Adjust remaining PartitionDevices' names after removing a partition.
  (dlehman)

* Tue May 26 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.56-1
- Ensure matching rootfs type to live type with autopart (#501876) (katzj)

* Tue May 26 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.55-1
- Fix blank network device descriptions in the loader. (#501757) (notting)
- Make sure the right _isMigratable gets used for Ext3FS (#501585). (clumens)

* Tue May 19 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.54-1
- We are not guaranteed to have a partedDisk in the udev code (#501556,
  #501428). (clumens)
- The location of the options wiki page has changed. (clumens)
- Disable BETANAG. (clumens)
- Install a en_US.UTF-8 locale in the first stage image. (notting)
- Reset font when changing language. (notting)
- Set locale to en_US.UTF-8 when initializing the console. (notting)

* Mon May 18 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.53-1
- LVMVolumeGroupDevice stores pesize in MB, kickstart expects it in KB.
  (dlehman)
- Don't schedule a format resize if reformat scheduled. (#500991) (dlehman)
- Deactivate md arrays regardless of state if the device is present.
  (#496441) (dlehman)
- Lame hack to make sure --size= is never 0 (#500905). (clumens)
- Don't filter out partitions that haven't been allocated (#500932).
  (clumens)
- Write out PE size as an integer, since that's what anaconda wants
  (#501049). (clumens)
- Set clearPartType to None on preupgrade too (#499321). (clumens)
- Fix indentation of line to remove cancelled actions from the list.
  (#500932) (dlehman)
- Consider active-idle state of md device as accepatable status of device
  (#497407) (rvykydal)
- Fix detection of cciss disks (#499408) (dchapman)
- Get existing fs size for xfs. (dcantrell)
- Get existing fs size for ntfs. (dcantrell)
- Get existing fs size for jfs. (dcantrell)
- Get existing fs size for ext2, ext3, and ext4. (dcantrell)
- Compute existing filesystem size using fs info utility. (dcantrell)
- Do not allow users to migrate ext4 to ext4. (dcantrell)
- Correct handling of formats on encrypted preexisting LVs. (#499828)
  (dlehman)
- Ignore unrecognized device-mapper devices we find. (#499967) (dlehman)
- loader: Mount /tmp as tmpfs not ramfs so we can swap it out (ajax)
- format.mountpoint -> lvd.mountpoint (#500913). (clumens)
- Treat the loop labels as devices without a label.(#493219) (jgranado)
- Add the partition table partition after initializing (#498602). (clumens)

* Wed May 13 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.52-1
- Add a Mac OS boot line to yaboot.conf (#499964). (clumens)
- Catch IOError when enabling repos (#500439). (clumens)
- Use a newer version of the kickstart Partition command. (clumens)
- Fix a traceback when installing over previous installs on PPC (#499963).
  (clumens)
- Fix a typo when probing exception disks. (clumens)
- Add support for --noformat too. (clumens)
- Add support for --onpart, --ondrive, and --useexisting. (clumens)
- Make the storage.writeKS method useful and called from instdata (#493703).
  (clumens)
- Add writeKS methods to the device objects. (clumens)
- Add writeKS methods to all the format objects. (clumens)
- upd-instroot: Add gdbserver (ajax)
- Remove text-mode syslinux help (katzj)
- If clearPartType is None, don't attempt to clear a device (#499321).
  (clumens)
- Only set clearpart data if the command was provided in the kickstart file.
  (clumens)
- Override previously defined mountpoints in kickstart (#499746). (clumens)
- Yet another font package name has changed (#499322). (clumens)
- Set new mountpoint correctly for existing encrypted LVs. (#496363)
  (dlehman)
- Once a partition is part of another device it cannot be modified.
  (#496760) (dlehman)
- Maintain request sort order by using req_disks instead of parents.
  (dlehman)
- Do not set a parent on the /mnt/sysimage/dev bind mount object (#499724).
  (clumens)
- Skip .pyc files in subdirectories when running make updates. (clumens)
- Remove 'lowres' option. (ajax)
- Run tune2fs on newly formatted ext[34] filesystems. (#495476) (dlehman)

* Thu May 07 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.51-1
- Don't clear the first partition on any disk with a Mac disk label
  (#492154). (clumens)
- Add detailedMessageWindow to the cmdline class (#499700). (clumens)
- Don't traceback when a freespace partition is present (#499662). (clumens)
- Do nomodeset when doing xdriver=vesa (ajax)
- Fix calculation of smallest PV's size in the lvm dialog. (#493753)
  (dlehman)
- Fix KeyError when partition numbers change during allocation. (#497911)
  (dlehman)
- Update EFI CD booting code in mk-images (pjones)

* Wed May 06 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.50-1
- Use storage objects throughout the partition editing UI code (#491806,
  #496002). (clumens)
- Verify filesystems after the live resize (katzj)
- Verify with fsck after resizing filesystems (katzj)
- IBM improvements to linuxrc.s390 (#475350) (dcantrell)
- Write out correct hostname during LiveCD installs (#492515) (dcantrell)
- Enter in hostname entry field advances to next screen (#494135) (dcantrell)
- Check if we'll clear a partition after setting its format attr. (#499251)
  (dlehman)
- Don't pass the default clearPartType value to the device tree. (dlehman)
- Fix some logic errors in storage.partitioning.shouldClear. (dlehman)
- Forward port various iscsi fixes from 5.4 iscsi work (hdegoede)
- Avoid writing out NAME= in ifcfg files (#497485) (dcantrell)
- Retry network configuration in loader (#492009) (dcantrell)
- Make sure /boot ends up on the same disk as Apple Bootstrap (#497390).
  (clumens)
- Handle that the default bootloader entry can sometimes be None (#496618).
  (clumens)
- The PS3 bootloader allows booting from ext4 filesystems (#498539).
  (clumens)
- Support LVM PE sizes > 128MB (#497733) (cristian.ciupitu)
- Set ANACONDAVERSION on most livecd installs. (clumens)
- getDependentDevices is in devicetree, not storage (#499144). (clumens)

* Mon May 04 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.49-1
- Collect network interfaces from NetworkManager (#493995) (dcantrell)
- Handle fstab entries whose filesystem we don't recognize.(#498120)
  (dlehman)
- Add an error signifying an unrecognized entry in /etc/fstab. (dlehman)
- Don't drop discovered format with unknown devices when parsing fstab.
  (dlehman)
- Fix display of paths for device-mapper device in bootloader widget.
  (dlehman)
- Don't call udevDeviceFormat if we're just going to clear the device
  (#497323). (clumens)
- Pass clearPartType to the devicetree as well. (clumens)
- Break the complex should-clear logic out of clearPartitions. (clumens)
- Handle clearpart in the early kickstart pass too. (clumens)
- Correct setting the SELinux context on mountpoints (#494995). (clumens)
- make resetFileContext return the context set (wwoods)
- Allow editing of the hdiso source partition so it can be mounted
  (#498591). (clumens)
- Add a ignoreProtected= parameter to deviceImmutable that does the obvious.
  (clumens)
- Be more aggressive unmounting before install starts (#498260) (katzj)
- Add %%{?dist} to the release number in the spec file. (dcantrell)
- Configure network in kickstartNetworkUp() iff NM is not connected
  (#490518) (dcantrell)
- Don't segfault with "ks someotherparam" (#498307). (clumens)
- Fix the arch upgrade check in yuminstall.py, too (#498280). (clumens)
- Move _resetRpmDb into iutil so we can access it everywhere. (clumens)
- Don't mount bind mounts last, that makes /dev break. (pjones)
- Pass anaconda to storage.FSSet.turnOnSwap. (dlehman)
- Ignore spurious formatting on partitioned devices. (dlehman)
- Revert "DeviceError only returns a message, not (message, device) tuple
  (#496343)." (dlehman)
- Fix action sorting for partitions on the same disk. (#498064) (dlehman)
- Fix traceback in second editing of existing raid dev (#497234). (rvykydal)
- Allow existing LVs with filesystems to be resized (#490913) (dcantrell)
- Rate limit pulse() calls to ProgressWindow. (pjones)
- Don't populate flags.cmdline with "True" values when no = is used. (pjones)
- Add "nomodeset" to the list of command line arguments copied to grub.conf
  (pjones)
- Use device.format.mountType insead of device.format.type for fstab.
  (pjones)
- Initialize x86 class variables before efiBootloaderInfo.__init__() (pjones)
- Fix a segfault on nfs+kickstart (pjones)
- Fix an error when raising FormatCreateException. (clumens)
- Add more windows to the rescue interface class (#498014). (clumens)
- Remove requirement for EFI machines to be x86, since IA64 is too
  (#497934). (clumens)
- Fix the kernel package selection on ppc64 machines (#497264). (clumens)
- Include fsck.ext4 and mkfs.ext4 in the images (#497996). (clumens)
- Properly restore SIGCHLD if X startup fails (wwoods)
- Fix kickstart PV references handling for lvm on raid (#497352). (rvykydal)

* Fri Apr 24 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.48-1
- Fix handling of swap files. (#496529) (dlehman)
- Pass anaconda to turnOnSwap so we can use swap files. (dlehman)
- Fix incorrect attribute name use for retrofit flag. (dlehman)
- Use slightly better checks when testing for 0 size (#493656, #497186,
  #497389). (clumens)
- If the LV has no child, don't attempt to grab its format (#497239).
  (clumens)
- Apply the global passphrase when doing kickstart autopart (#497533).
  (clumens)
- Add support for encryption passphrase retrofits. (dlehman)
- Bring luks_add_key and luks_remove_key back into devicelibs.crypto.
  (dlehman)
- Don't let lvremove failures from incomplete vgs crash the install.
  (#497401) (dlehman)
- Allow setting a mountpoint w/o formatting an encrypted partition.
  (#495417) (dlehman)
- Remove encryption from preexisting device if "Encrypt" is deactivated.
  (dlehman)
- Fix indentation of preexisting partition handling block. (dlehman)
- The device passed to the luks passphrase dialogs is a string. (#492123)
  (dlehman)
- Protect against tracebacks from the partition isFoo properties. (dlehman)
- Fix handling of bind mounts. (#496406) (dlehman)
- Add more filesystem checks. (clumens)
- Support vfat filesystems in the partitioning UI (#496351). (clumens)
- Remove devices in leaves first order (#496630) (hdegoede)
- Don't remove an inconsistent lvm partition from the devicetree (#496638)
  (hdegoede)
- Move isEfi to be a property on Platform instead of on X86 (#497394).
  (clumens)
- Support --encrypted --useexisting on kickstart installs (#497147).
  (clumens)
- When making a RAID device, require that some members be selected
  (#491932). (clumens)
- When catching an OSError, handle it as an object instead of a tuple
  (#497374). (clumens)
- Enforce the fstype that holds /boot on kickstart installs (#497238).
  (clumens)
- Fix ps3 platform support (#497203) (katzj)
- Clean up rpmdb locks at the end of the install (#496961) (katzj)
- Don't allow /boot to be on an encrypted device (#496866). (clumens)
- Use the correct unmount method (#496764). (clumens)

* Tue Apr 21 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.47-1
- Fix adding of fifth partition in UI (#496930). (rvykydal)
- Define the fd variable before it can ever be referenced (#496930).
  (clumens)
- Fix preservation of format attrs for preexisting luks partitions. (dlehman)
- Set md member devices' uuids after creating an array. (dlehman)
- Don't try to get size for nodev and bind filesystems. (dlehman)
- Include the device path in DeviceError exceptions. (dlehman)
- Mdadm's incremental mode ignores the auto option, so don't use it.
  (dlehman)
- Use incremental mode for all md member addition during probing. (dlehman)
- Try to name existing md arrays based on their preferred minor. (dlehman)
- Reimplement mdexamine using a more easily parseable output format.
  (dlehman)
- Fix position of "--run" option to mdadm assemble. (dlehman)
- Handle passphrase prompts without a traceback in cmdline mode. (#492123)
  (dlehman)
- Fix another device vs. string problem in EFI bootloader config (#496669).
  (clumens)
- Add the device's name to mdadm.conf (#496390). (clumens)
- Show normal cursor during passphrase entry (#496534) (msivak)
- Fix traceback in cmdline mode after exception handling cleanup (#496644)
  (katzj)
- DeviceError only returns a message, not (message, device) tuple (#496343).
  (clumens)

* Fri Apr 17 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.46-1
- Clean up argument list after changing from rhpl to iutil for
  execWithRedirect (jkeating)
- Fix NameError traceback setting up bootloader in EFI installs (wwoods)
- No longer force ISOs to be on ext2, ext3, or vfat partitions. (clumens)
- Sending translation for German (ckpinguin)
- Split text mode exn saving into multiple screren (#469380). (clumens)
- Copy /tmp/program.log to /mnt/sysimage/var/log/. (clumens)
- Fix member preselection in raid UI. (rvykydal)
- Fix editing of raid device (persistence of level choice) (#496159)
  (rvykydal)
- Fix ks --useexisting and --noformat options of logvol and volgroup
  (rvykydal)
- Make sure inconsistencies dont screw us up. (jgranado)
- Re-implement the inconsistency functionality. (jgranado)
- Allow the use of "-" in the lvm names. (495329) (jgranado)
- Make sure we "insist" on mdadm commands. (491729) (jgranado)
- [PATCH] Possible fix for some encryption related bugs during the Custom
  Layout editation (#495848) (msivak)

* Thu Apr 16 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.45-1
- Touch /.autorelabel when running under rescue mode (#491747). (clumens)
- Add support for fingerprint-based logins (#481273). (clumens)
- Add a "File Bug" button to the catch-all partitioning exception handler.
  (clumens)
- Remove the early catch-all exception handler (#495933). (clumens)
- Implement the save to USB using devicetree devices. (jgranado)
- Use size instead of currentSize when comparing lv sizes (hdegoede)
- Make sure all pv's of an lv's vg are setup before resizing an lv (hdegoede)
- Do not try to teardown a non existing format (hdegoede)
- Center the bootloader configuration dialog (#495802). (clumens)
- Destroy (potential) stale metadata when creating a new partition (hdegoede)
- use partition req_base_size instead of size in partitionCompare()
  (hdegoede)
- Fix changing size of newly created partitions (hdegoede)
- Don't traceback on invalid filesystem detection (#495156) (dcantrell)
- Check to see if formatcb is None. (jgranado)
- Use the PV name when logging error messages. (jgranado)
- Don't set up the device to obtain minSize anymore. (dlehman)
- Improve estimate of md arrays' size. (dlehman)
- Determine minimum size for filesystems once, from constructor. (dlehman)
- Fix estimate of LUKS header size for newly encrypted devices. (#493575)
  (dlehman)
- Fix two syntax problems with generated mdadm.conf entries. (#495552)
  (dlehman)
- Default to AES-XTS cipher mode with 512 bit key for new LUKS devices.
  (dlehman)
- When going back from a failed shrink, reset the device action set.
  (clumens)
- If we can't communicate while logging in to bugzilla, error (#492470).
  (clumens)
- Make save to usb work. (jgranado)
- We don't always have a formatcb either (#495665). (clumens)
- The entry is named lvsizeentry now. (jgranado)

* Mon Apr 13 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.44-1
- Default to SHA512 password encoding algorithm. (dcantrell)
- Handle format combo box not existing (#495288) (dcantrell)

* Mon Apr 13 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.43-1
- Run programs with LC_ALL=C in case we're parsing output (#492549).
  (clumens)
- A volume group device has a "peSize" attribute (not "pesize"). (dlehman)
- Remove uncommitted new lv from dict on cancel. (dlehman)
- Use the correct value when setting new extent size. (#493753) (dlehman)
- Fix image generation so all ELF binaries have their deps included
  (#495231). (clumens)
- Clean up the code in editLogicalVolume function. (jgranado)
- Setup the disks before partitioning as the nodes are needed. (jgranado)
- Rescan the devices when we are saving a traceback. (jgranado)
- Close file descriptors when an error occurs. (jgranado)
- Aesthetic changes to "editLogicalVolume" function. (jgranado)
- When deallocating a partition also set its disk attribute to None
  (hdegoede)
- Check self.partedPartition not being None before using it (#495077)
  (hdegoede)
- growPartitions: Change op_func (back to) add when an iteration succeeds
  (hdegoede)
- partedPartition can be None while growing partitions (#495076) (hdegoede)

* Thu Apr 09 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.42-1
- Fix display of format type for devices. (dlehman)
- Fix handling of priority option from swap fstab entries. (#494992)
  (dlehman)
- Some fs types cannot be passed to programs (#495061, #493075). (clumens)
- When a new module is loaded, update the kernel_filesystems list. (clumens)
- Add more Indic fonts (#494261, pnemade).
- Remove the message saying you can make your own layout (#495015). (clumens)
- Put e100 (and other) firmware in its own directory if needed (#494778).
  (clumens)
- Run /bin/umount instead of calling umount(2) in _isys.umount (#493333)
  (dcantrell)
- Add doPwUmount() and mountCommandWrapper() to isys (#493333) (dcantrell)
- Preserve symlinks and only collect deps on ELF executables. (dcantrell)
- Use $(ARCHIVE_TAG) throughout the updates target. (dcantrell)
- partedUtils doesn't exist anymore (katzj)
- Revert "Show the header in certain non-lowres cases" (#493153) (katzj)
- Pre-existing partitions names may change (#494833) (hdegoede)
- Use getDeviceNodeName() instead of basename of device node. (hdegoede)
- Fix ks raid --useexisting and --noformat (rvykydal)
- Fix processing of --level and --device options of ks raid commands.
  (rvykydal)
- Don't start pdb immediately in debug mode (katzj)
- Fix EDD BIOS disk order detection in general and make it work with dmraid
  (hdegoede)
- Update extended partition geometry when we change it (hdegoede)

* Tue Apr 07 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.41-1
- Make sure we have a clean lvm ignore list when we initialize. (jgranado)
- We need to search by name without the "mapper" prefix. (jgranado)
- Create a min_max constraint to avoid alignments issues. (jgranado)
- Don't exit the installer from filesystem errors. (dlehman)
- Try not to raise exceptions from minSize calculators. (dlehman)
- Don't traceback when PVs are encrypted or are not partitions. (dlehman)
- Adjust device dependencies when backing out device encryption. (#493257)
  (dlehman)
- Include filesystem type in mount log message. (dlehman)
- Load filesystem modules on demand (#490795, #494108). (clumens)
- Use existing partitions when --onpart is used for PVs or raid members
  (#493065) (rvykydal)
- Raise message, not exception when size set in LV dialog is too big.
  (rvykydal)
- Raise an error when remofing an extended part with logical parts.
  (jgranado)
- Esthetic changes to storage/partitioning.py. (jgranado)
- dmraid.py is no longer being used by anything, so remove it. (clumens)
- Remove partedUtils.py. (clumens)
- This is the only place isEfiSystemPartition is used, so pull it in.
  (clumens)
- getReleaseString now lives in the storage module. (clumens)
- Stop lying about our support for dmraid and multipath in kickstart.
  (clumens)
- Remove some old, unused code that also uses biosGeometry. (clumens)
- For very small disks, don't try to display a stripe in the graph
  (#480484). (clumens)
- Fix reading the console= parameter from the cmdline (#490731). (clumens)
- For dmraid partititons device node name != name (hdegoede)
- When a partition request gets unallocated, set the name back to req#
  (hdegoede)
- Do not use getPartitionByPath() in allocatePartitions() (hdegoede)
- Remove no longer used iscsi_get_node_record function (hdegoede)
- Try to handle devices which live in a subdir of /dev properly (hdegoede)
- Split DeviceTree.addUdevDevice into several smaller methods. (dlehman)
- Don't traceback from failure finding minimum fs size. (#494070) (dlehman)
- udev_settle after format teardown to avoid EBUSY on device teardown.
  (#492670) (dlehman)
- Add a parted.Device attribute to all existing StorageDevices. (dlehman)
- If no partitioning commands are given, apply the UI selections (#490880).
  (clumens)
- Update font package names for ml_IN, si_LK, etc. (#493792, #493794).
  (clumens)
- Fix a typo in the city name for Nepali (#493803). (clumens)
- Fix writing out the partition= line on PPC (#492732). (clumens)
- Do not check size when adding LV to growing VG (bug #492264) (rvykydal)

* Thu Apr 02 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.40-1
- Don't let device names affect action order in general case. (dlehman)
- Round up when aligning to pesize for space used. (#493656) (dlehman)
- Improve handling for various nodev filesystems in fstab. (#493685,
  #493202) (dlehman)
- Present the correct max lv size in the dialog. (dlehman)
- Use the head of the current branch, not master, for scratch archives.
  (dlehman)
- Make a top level StorageError that all others are based on. (dlehman)
- Remove unused PRePDevice class. (dlehman)
- Make the disk model an attribute of DiskDevice. (dlehman)
- Handle format actions in cancelAction() (dcantrell)
- Fix format check box for pre-existing partitions (#491675) (dcantrell)
- Remove temporary directory used in _getExistingSize() (dcantrell)
- Activate storage before looking up the hdiso source drive (#491781).
  (clumens)
- Remove isys.getDeviceByToken since it is no longer used. (clumens)
- Don't allow the rootfs on live installs to not match (#493206, #492727)
  (katzj)
- Create setup and teardown functs for dmraid devs. (jgranado)
- put xfs back where it belongs (sandeen)
- Fix up the other caller of unmountCD to pass in a device (#493537).
  (clumens)

* Wed Apr 01 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.39-1
- Prevent sensitive information in kickstart files from ending up in
  tracebacks. (clumens)
- It's 2009, let's ignore floppy drives now (#493338, #493377). (clumens)
- Remove DmRaidArrayDevice level attribute (#493293) (hdegoede)
- get_containing_device takes two arguments (#493266). (clumens)
- Fix the check for if there's enough space available on / and /usr
  (#492614). (clumens)
- Fix testing if a PPC partition is bootable (#492726). (clumens)
- Look for a PReP "partition" by examining the format, not the flags
  (#492426). (clumens)
- Fix a few more pylint warnings and errors in storage/* (hdegoede)
- Fix some pylint warnings in iw/*.py (hdegoede)
- Don't start our audit daemon with the livecd installer (katzj)
- If there's a problem finding removable disks, disable save-to-disk.
  (clumens)
- Move %%pre processing to much earlier in the install process. (clumens)
- If there are no installs to rescue via kickstart, display an error.
  (clumens)
- Add an early kickstart processing pass. (clumens)
- Fixes of errors shown by pylint that didn't get into the beta build.
  (mgracik)
- Adjust the dmraid ignoring logic. (jgranado)
- Reference the format by type, not name.(#492596) (jgranado)
- Sending translation for Chinese (Simplified) (leahliu)
- Increase udev_settle timeout in udev_get_block_devices. (#492049) (dlehman)
- Fix check for fully defined md array when raidlevel is 0. (#491796)
  (dlehman)
- Fix a typo ('isEFI' should be 'isEfi'). (dlehman)
- Make sure the pvs are set up before doing lvremove or vgremove. (dlehman)
- Don't write out md member devices to a config file for assemble. (dlehman)
- Fix the supported property of filesystems and prepboot format. (dlehman)
- Return early from doAutoPartition if partition allocation fails. (dlehman)
- Reset storage instance if autopart fails. (#492158) (dlehman)
- Assign weights to partition requests when doing manual or kickstart
  installs. (clumens)
- Refresh windows immediately to make sure they appear. (clumens)
- Fix problem with format and migrate combo box activation. (dcantrell)
- Fix typo in upgrade.py (dcantrell)
- Move _scheduleLVs and growLVM calls to be inside try/except (dcantrell)
- Correct bounds checking problems in 'Shrink current system' (dcantrell)
- Require libselinux-python (#489107) (dcantrell)
- Do not prompt for NIC selection in cmdline mode (#492586) (dcantrell)
- Do not write /etc/hosts since setup owns that now (#491808) (dcantrell)
- Remove unused self._resize variable. (dcantrell)
- Having 2 raidsets in the same group of devs is possible. (jgranado)
- getDevice returns a string.  Use that to look up the device object
  (#492465). (clumens)
- Take into account i386->i586 when warning on upgrade arch mismatch.
  (clumens)
- Remove unused getVG{Free,Used}Space methods. (clumens)
- We can no longer display Russian correctly in text mode (#491394).
  (clumens)
- Clean up the reinitialize LVM warning message (#491888). (clumens)
- Update translation files (#484784). (clumens)
- Include the storage directory when building the .po files. (clumens)
- Merge commit 'origin/anaconda-storage-branch' (clumens)
- Keep VG size property non-negative (rvykydal)
- Grow LVs for kickstart requests too (rvykydal)
- Handle not finding the upgrade root gracefully. (jgranado)
- Use self.name to report that we could not eject cd. (jgranado)
- Fix ppoll() timeout=infinity usage in auditd (#484721). (pjones)
- Use correct parse method for the upgrade command (#471232) (wwoods)
- Rename /etc/modprobe.d/anaconda to /etc/modprobe.d/anaconda.conf (clumens)
- Handle FTP servers that both want and don't want PASS after USER
  (#490350). (clumens)
- Only select the Core group in text mode (#488754). (clumens)
- Add created user to default group created for the user. (rvykydal)

* Wed Mar 25 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.38-1
- Fix pylint errors in iw/*.py (hdegoede)
- Rework CryptTab.parse (dlehman).
- Code fixes of errors shown by pylint (mgracik).
- Don't underflow on the busy cursor stack. (clumens)
- "vg" is not valide inside this if. (jgranado)
- Device is sometimes None. (jgranado)
- Fix typo. (#492042) (dlehman)

* Tue Mar 24 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.37-1
- Start with a basic /etc/hosts file (#491634) (dcantrell)
- Do not flag every existing partition for resize (#491803) (dcantrell)
- Remove unused noformatCB() function. (dcantrell)
- Remove unnecessary istruefalse() function. (dcantrell)
- Build new _isys.so for updates.img if needed. (dcantrell)
- Get the UUID of each md array we create. (#491796) (dlehman)
- Call udev_settle after committing changes to a disk (#491529) (hdegoede)
- Be a little bit smarter about allocating space to grow parts. (#491761)
  (dlehman)
- Check that partition is on the disk before trying to remove it. (#491997)
  (dlehman)
- Work around a bug in mdadm incremental assembly. (dlehman)
- Use the same units (MB) for extent size that we do for everything else.
  (dlehman)
- Put line breaks in between crypttab entries. (#491938) (dlehman)
- Register the NoDevFS class. (clumens)
- fslabels -> labels. (clumens)
- NFSDevice does not take exists= as a parameter. (clumens)
- Override _setDevice and _getDevice in NFS. (clumens)
- Move resolveDevice into the DeviceTree class. (clumens)
- Move most of the parseFSTab logic into its own function. (clumens)
- We don't even use partedUtils in this module. (clumens)
- PReP formats can never be active. (#491865) (dlehman)
- Move protectedPartition setup into storageInitialize (#491781). (clumens)
- Use the mount and unmount methods on OpticalDevice.format now. (clumens)
- Add a format for ISO9660 filesystems. (clumens)
- getDeviceByName does not expect the CD device to start with "/dev/"
  (#491768). (clumens)
- Write the same arch to .discinfo as iutil.getArch() gives us (#490977).
  (clumens)
- Don't remove partitions twice. (jgranado)

* Mon Mar 23 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.36-1
- Add EFI, Apple Bootstrap, and PPC PReP Boot formats. (dlehman)
- Remove all implicit calls to self.format.destroy from Device classes.
  (dlehman)
- Pop the busy cursor when we're done with the wait window (#491736).
  (clumens)
- If the new size and old size are the same, treat as a no-op (#491496).
  (clumens)
- Let mountFilesystems handling bind mounting /dev (#490772). (clumens)
- Not all FileDevices have parents, so don't assume. (clumens)
- Bind mount formats are mountable. (clumens)
- If a filesystem is already mounted, don't raise an error. (clumens)
- Fix a typo calling the superclass's constructor. (clumens)
- Add a fake device for bind mounting /dev. (clumens)
- If there was an exception leading to the urlgrabber error, log it.
  (clumens)
- Fix the import of checkbootloader (#491574). (clumens)
- Add a missing import (#491605). (clumens)

* Fri Mar 20 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.35-1
- Fix traceback in FSSet.crypttab. (#491160) (dlehman)
- Fix traceback on upgrade. (#491446) (dlehman)
- Do not include .h and .sh files in updates.img (dcantrell)
- Make PartitionDevice resize work. (dcantrell)
- Reset mouse pointer if we find an unreadable disk. (dcantrell)
- Use label attr instead of non-existent fslabel attr. (#491120) (dlehman)
- Need to notify the kernel of changes before udev settle (katzj)
- Revert "mount and umount commands are in /sbin now, remove from /usr/sbin"
  (dcantrell)
- Make some fixes to the rescue mode system selection UI (#489973, #489977).
  (clumens)
- Fix text mode autopartitioning (#491282). (clumens)
- Do not use _rnetdev as fstab option for network based / (hdegoede)
- Make root= line in grub.conf and path spec in fstab consistent (hdegoede)
- Fix a reference to the partitions list (#491335). (clumens)
- Do not traceback at the very beginning of rescue mode (msivak)
- Fix traceback when editing encrypted mdraid device in UI. (rvykydal)

* Thu Mar 19 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.34-1
- Catch FSError when detecting storage, prevent user from continuing.
  (dcantrell)
- If we have no error string, place None in the tuple. (dcantrell)
- Move OUTPUT_TERMINAL definition to isys.h (dcantrell)
- mount and umount commands are in /sbin now, remove from /usr/sbin
  (dcantrell)
- Avoid SIGSEGV in doPwMount() when NULL is last parameter (#491192)
  (dcantrell)
- Attempt disk commits 5 times before raising an exception. (dcantrell)
- Add boot partition size limit properties and size validation method.
  (dlehman)
- Make sure boot flag gets set. (#491170) (dlehman)
- Make bootable a property of PartitionDevice. (dlehman)
- After setting up our random UUID, inform the storage layer (katzj)
- Handle system crappyness. (jgranado)
- Fix up checking for live image backing (katzj)
- Let's not remove our mountpoints (katzj)
- Fix writing the default= line in grub.conf (#490756). (clumens)
- Revert "Fix pruning of destroy actions for preexisting devices." (dlehman)
- Add more blacklisting (katzj)
- Blacklist the live image backing device (katzj)
- Move blockdev blacklisting to be a function (katzj)
- Inhibit devkit-disks during a live install (katzj)
- try to unmount everything from /media on live installs (katzj)
- Fix live installs to not traceback (katzj)
- Fix New partition in UI (rvykydal)

* Thu Mar 19 2009 David Lehman <dlehman@redhat.com> - 11.5.0.33-1
- Rework the lvm dialog. (#490301,#490966,#490681,#489870) (dlehman)
- Improve chances of uniqueness from Storage.createSuggestedLVName. (dlehman)
- Fix pruning of destroy actions for preexisting devices. (dlehman)
- Devices should not be resizable unless they exist. (dlehman)
- Try to activate an existing md array after adding each member. (dlehman)
- Indicate filesystem is mountable if we have a mount command. (dcantrell)
- Mount existing filesystems read-only when getting size. (dcantrell)
- Fix some errors in the updates target. (dcantrell)
- Place all mount.* commands in /sbin (dcantrell)
- Fix error message reading and writing in doPwMount() (dcantrell)
- Use booleans in isys.mount() and isys.umount() (dcantrell)
- Add a FIXME comment for setting uuid in VG / LV create (hdegoede)
- Do not traceback when writing anaconda.ks with iscsi with auth info.
  (hdegoede)
- Do not write LV uuid to grub.conf, but the filesystem uuid (hdegoede)
- If a mountpoint depends on a network disk at _netdev to its fstab options
  (hdegoede)
- Do not hang when creating raid array with member having filesystem
  detected (#490891) (rvykydal)
- Destroy and create luks child of raid array too when editing in UI.
  (rvykydal)
- Editing non-existent raid device by destroying and creating actions
  (rvykydal)
- actionDestroyFormat call takes device, not format (rvykydal)
- Fix getChildren call in partition UI (rvykydal)
- Fix removing of devices with the same name from	tree when adding
  create action. (rvykydal)
- Do not duplicate requested minor number in edit raid UI list. (rvykydal)
- Offer available partitions when editing non-preexisting raid request.
  (rvykydal)
- Don't try to fit the whole StorageDevice.__str__ output into the UI
  (#490406). (clumens)
- Make PartitionDevice handle both normal and dmraid partitions (hdegoede)
- Stop overriding __init__ in DMRaidPartitionDevice (hdegoede)
- Set format UUID after creating a format (hdegoede)
- Fix result of updateSysfsPath to be consistent with initial sysfsPath
  values (hdegoede)
- Use getDevicesByInstance() for storage.partitions (hdegoede)
- We no longer use iscsiadm anywhere (hdegoede)

* Tue Mar 17 2009 Jesse Keating <jkeating@redhat.com> - 11.5.0.32-1
- Typo fix. (clumens)
- Make platform.checkBootRequest work better and not use diskset anymore. (clumens)
- Fix a traceback when looking for PS3 boot partitions (#490738). (clumens)
- FormatArgs -> FormatOptions (#490737). (clumens)
- Fix ppoll() timeout=infinity usage in auditd (#484721). (pjones)
- Simplify kernel package selection. (clumens)
- Look at CPU flags instead of /proc/iomem to determine PAE-ness (#484941). (clumens)
- Tell NM not to touch interfaces when / is on a network disk (hdegoede)
- Get iscsi going with the new storage code (hdegoede)
- Use minihal instead of isys.hardDriveDict in list-harddrives (#488122). (clumens)
- storage.disks never includes disks without media present. (clumens)
- Changed the getDevicebyLabel() to getDeviceByLabel() in devicetree.py (mgracik)

* Mon Mar 16 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.31-1
- Don't use disk.maximizePartition anymore. (dlehman)
- Only schedule implicit format destruction if there is formatting to
  destroy. (dlehman)
- Reset encryptionPassphrase when we reset the rest of storage. (dlehman)
- Do not create a LUKSDevice if we do not have a way to map the device.
  (dlehman)
- Fix handling of new extended partitions during partition allocation.
  (dlehman)
- Fix bug in dependency list for partitions. (dlehman)
- Fix inconsistency in variable use in search for free space. (dlehman)
- Check for disk name being in disk.name not in clearPartDisks (dcantrell)
- Create a Makefile target to generate updates.img automatically. (dcantrell)
- When creating free space, handle cases other than clearpart --drives=
  (clumens)
- Ignore loop and ram devices (hdegoede)
- devicetree: fix slave addition of incomplete dm / md devices (hdegoede)
- Catch LVMErrors too when tearing down devices (hdegoede)
- Install udev rules in /lib/udev/rules.d instead of in runtime dir
  (hdegoede)
- Ignore disk devices with missing media (#488800). (clumens)
- Use correct parse method for the upgrade command (#471232) (wwoods)
- Fix creation of fs options for preexisting encrypted devices. (dlehman)
- Fix lots of buggy behavior in the partition dialog. (dlehman)
- Handle FTP servers that both want and don't want PASS after USER
  (#490350). (clumens)
- Fixed the names of the variables for lvm.py functions. (mgracik)
- editPartitionRequest -> editPartition in iw/partition_gui.py (#490384).
  (clumens)
- clampPVSize -> clampSize in lvm.py (#490295). (clumens)
- Fix the obvious and stupid typo (#490296). (clumens)
- isys.umount removes mount directory by default (rvykydal)
- Fix tempfile.mkdtemp call. (rvykydal)
- Initialize attribute _mountpoint before using it (rvykydal)
- devicetree.py has _ignoredDisks instead of ignoredDisks. (jgranado)
- Create separate resize actions for formats and devices. (dcantrell)
- Use os.statvfs() to get existing filesystem size. (dcantrell)
- Add resizeArgs for Ext2FS and fix it for BtrFS. (dcantrell)
- Report when we cannot find any free space partitions. (dcantrell)
- Improve resizeDialog text. (dcantrell)
- Raise FSResizeError if filesystem cannot be resized. (dcantrell)
- Handle resizing when setting targetSize for PartitionDevice (dcantrell)
- Let users set the size property of StorageDevices. (dcantrell)
- Add support for kickstart's '--initlabel' option to clearpart. (dlehman)
- Fix display of LV format type for encrypted LVs. (dlehman)
- Make paths somewhat flexible so we'll work in normal environments.
  (dlehman)

* Fri Mar 13 2009 David Lehman <dlehman@redhat.com> - 11.5.0.30-1
- Fix supportable attribute for cmdline-enabled fstypes. (dlehman)
- Access private attribute for luks dict. (dlehman)
- Schedule format create for newly encrypted preexisting partition. (dlehman)
- Don't traceback if vg.teardown fails in recursive teardown. (dlehman)
- Schedule format create action for newly encrypted preexisting LV. (dlehman)
- Make sure we return something other than None for new requests. (dlehman)
- Add __str__ methods to Device objects. (clumens)
- Add mediaPresent and eject to the OpticalDevice class. (clumens)
- Use the right import path for checkbootloader (#490049). (clumens)
- Rename /etc/modprobe.d/anaconda to /etc/modprobe.d/anaconda.conf (clumens)
- Don't clear partitions containing the install media. (dlehman)
- Wait til everyone knows the format/fs is no longer active. (dlehman)
- Save a copy of the device stack so we can destroy the format. (#489975)
  (dlehman)
- Add a deep copy method to Device since we can't just use copy.deepcopy.
  (dlehman)
- Fix infinite loops in partition screen populate. (#490051) (dlehman)
- Default to a name based on the uuid for existing luks mappings. (dlehman)
- Use the correct keyword for luks map names ('name', not 'mapName').
  (dlehman)
- Fix getting of number of total devices of sw raid. (rvykydal)
- Only select the Core group in text mode (#488754). (clumens)
- Added test case for devicelib mdraid.py. (mgracik)
- Add created user to default group created for the user. (rvykydal)
- Fix editing of existing logical volume. (rvykydal)
- Add a list that lvm should ignore. (jgranado)

* Thu Mar 12 2009 David Lehman <dlehman@redhat.com> - 11.5.0.29-1
- Don't create a PartitionDevice for devices that do not exist (#489122).
  (clumens)
- A getter doesn't usually take a parameter (#489965). (clumens)
- Do not write "Running..." to stdout, as that could be tty1. (clumens)
- Call storage.exceptionDisks, not diskset.exceptionDisks. (#489615)
  (dlehman)
- Fix typo. (jgranado)
- Fix typo. (dlehman)
- Add udev rules for handling for mdraid arrays. (dlehman)
- Honor the zerombr kickstart directive. (dlehman)
- currentSize is expected to be a float, so convert it to one (#489882).
  (clumens)
- It's clearPartDisks, not clearPartDrives. (clumens)
- Get rid of the mappings and ksID as well. (clumens)
- Make sure the device has a diskType before attempting to check what it is.
  (clumens)
- Update the volgroup command to work with the new storage code. (clumens)
- Update the raid command to work with the new storage code. (clumens)
- Update the part command to work with the new storage code. (clumens)
- Update the logvol command to work with the new storage code. (clumens)
- addPartRequest is no longer needed. (clumens)
- Don't set default partitioning in every kickstart case. (clumens)
- Clear partitions before scheduling requests. (clumens)
- Always go through doAutoPart. (clumens)
- Format modules import fix (mgracik)
- Fixed the format modules import (mgracik)
- Allow overriding the anaconda udev rules from an updates.img (hdegoede)
- If a pv somehow does not contain a vg_name, do not try to get other vg
  info (hdegoede)

* Wed Mar 11 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.28-1
- Fix a few bugs in the lvm dialog. (#489022) (dlehman)
- Modify livecd.py to work with new storage backend. (dlehman)
- Be explicit about resetting Disks' partedDisk attribute. (#489678)
  (dlehman)
- Deactivate devices after we've finished scanning them. (dlehman)
- Handle the case of removing an unallocated partition from the tree.
  (dlehman)
- Try again to set up LVs when we've just added a new PV to the VG. (dlehman)
- Set partition flags in format create/destroy execute methods. (dlehman)
- Make sure we use the newly committed parted.Partition after create.
  (dlehman)
- Make device teardown methods more resilient. (dlehman)
- Initialize storage in rescue mode so we can find roots (#488984). (clumens)
- We also need to pack up the extra args tuple, too. (clumens)
- doLoggingSetup keeps growing new arguments, so put them into a dict
  (#489709). (clumens)
- Fix anaconda udev rules to not require pre-existing device nodes (hdegoede)
- Hook up 'Shrink current system' dialog to new storage code. (dcantrell)
- Fix _getCheckArgs() in class FS. (dcantrell)

* Tue Mar 10 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.27-1
- Fix action pruning to handle more complex scenarios. (dlehman)
- Schedule destruction of any existing formatting along with the device.
  (dlehman)
- Add a size attribute to mdraid arrays. (dlehman)
- Speed up partitioning screen redraws by trimming workload where possible.
  (dlehman)
- Create partitions with exactly the geometry we calculate. (dlehman)
- Fix name collision between formats.mdraid and devicelibs.mdraid. (dlehman)
- Destruction of the member device formatting will be handled elsewhere.
  (dlehman)
- Fix a typo (jkeating)
- Fix pruning between two destroy actions on the same device (rvykydal)
- Use the pyblock functions when possible. (jgranado)
- We are searching a list, not a dict now (rvykydal)

* Mon Mar 09 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.26-1
- Move the recursive teardown of all devices out of processActions. (dlehman)
- Clean up handling of /proc, /sys, /dev/pts, /dev/shm entries. (dlehman)
- Fix several minor bugs preventing upgrade/rescue mount. (#488946) (dlehman)
- Only populate the device tree on demand. (dlehman)
- Prune actions by device based on path, not object-id. (dlehman)
- Rewrite action sort so it works correctly. (dlehman)
- Do a separate disk.commit for each partition add/remove. (dlehman)
- Fix bug keeping track of best free region/type/disk info. (dlehman)
- Return early if doAutoPart is False, but clearpart first if kickstart.
  (dlehman)
- Recognize PS3 as a valid machine type (#489263). (clumens)
- Move the mdRaidBootArches logic into the platform module. (clumens)
- stdout and stderr may also need to be created. (clumens)
- Fix booty for dmraid (hdegoede)
- It's self.origrequest, not self.origreqest (#489036). (clumens)
- Added crypto.py unittest; Updated devicelibs tests baseclass.py and lvm.py
  (mgracik)
- Start storage before parsing the kickstart file. (clumens)
- Make sure autopart without any clearpart command will fail. (clumens)
- Update storage flag on ks autopart (rvykydal)
- Use correct storage attribute for ks clearpart (rvykydal)
- Catch the new _ped.DiskLabelException for unrecognized disklabels.
  (dlehman)
- Catch all failures from making parted objects in exceptionDisks. (dlehman)
- various dmraid fixes. (jgranado)
- Implement the format disk question as a callback. (jgranado)
- Add dmraid functionality to new storage code. (jgranado)
- Do not pass None values into nonmandatory arguments, you are screwing the
  default values.. (msivak)

* Thu Mar 05 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.25-1
- Schedule device destroy actions for partitions last. (dlehman)
- Pass storage.disks, not storage, to createAllowed.... (#488860) (dlehman)
- Nodev filesystems always exist. And the device is arbitrary. (dlehman)
- Include proc, &c filesystems in fstab and FSSet.{mount/umount}Filesystems.
  (dlehman)
- Remove FSSet.writeFSTab. That job is handled elsewhere. (dlehman)
- Add properties to FSSet to provide the nodev entries. (dlehman)
- Fix incomplete format in Storage.deviceImmutable. (dlehman)
- Make sure we use the same disk the free space is on. (#488807) (dlehman)
- Prevent clobbering of name 'mdraid' by qualifying it. (dlehman)
- Handle unformatted disks and cdroms in Storage.exceptionDisks. (dlehman)
- Add resizeArgs property for resizable filesystems. (dcantrell)
- Fill out class NTFS a bit more. (dcantrell)
- Add fsckProg property to class FS. (dcantrell)
- Ext2FS.migratable(self) -> Ext2FS.migratable (dcantrell)
- Fix StorageDevice.minSize() and PartitionDevice.maxSize() (dcantrell)
- Center resize window on the screen. (dcantrell)
- Do not raise DeviceError if not bootable device is found. (dcantrell)
- Do an even more thorough job of ignoring disks libparted doesn't like.
  (clumens)
- Fix a couple problems on the "Change device" bootloader dialog. (clumens)
- Fix a typo when writing out the mdadm config file. (clumens)
- Remove all uses of isys.cdromList, which no longer exists. (clumens)
- Check to see if we're on S390 on the congrats screen (#488747). (clumens)
- Handle non-fatal errors more gracefully in addUdevDevice. (dlehman)
- partRequests no longer exists, so don't try to import it (#488743).
  (clumens)
- When building the exceptionDisks list, skip devices libparted doesn't
  like. (clumens)
- Iterate over devicetree.devices.values, not devicetree. (dlehman)
- Add a get() method to Flags, since it pretends to be a dictionary.
  (clumens)
- Stop with the fsset usage. (dlehman)
- Format message string after translation not before (msivak)
- We need newer python-cryptsetup because of the default values for cipher
  and keysize for luskFormat (msivak)
- If a drive is not initialized, offer reinitialization or ignoring the
  drive to the user (msivak)
- More syntax errors / traceback fixes (hdegoede)
- Fix syntax errors (rvykydal)
- Implement Storage.sanityCheck, mostly from old partitions code. (dlehman)

* Thu Mar  5 2009 Dave Lehman <dlehman@redhat.com> - 11.5.0.24-3
- Fix booty's desire to import fsset.
- Fix attempt to set read-only attr "removable" in DiskDevice.__init__

* Thu Mar 05 2009 Peter Jones <pjones@redhat.com> - 11.5.0.24-2
- Add EFI boot.iso generation.

* Wed Mar  4 2009 Dave Lehman <dlehman@redhat.com> - 11.5.0.24-1
- Storage test day.

* Fri Feb 20 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.23-1
- Remove old content from utils/ (dcantrell)
- Ensure request.drive is always a list (#485622) (dcantrell)
- Pick up pyblock if it exists in block/ on an updates.img. (dcantrell)
- Don't check for a swapfs on things that aren't partitions (#485977).
  (clumens)
- Perform ext3->ext4 filesystem migration if ext4migrate is given (#484330).
  (clumens)
- Translate i?86 into i386 as a base arch. (jkeating)
- Teach upd-instroot about i586 arch, for sake of glibc.i586/openssl.i586
  (jkeating)
- Fix the obvious typo. (clumens)
- filer.login raises an exception with it can't login, not returns None
  (#486454). (clumens)
- Take into account that a parted.Partition's _fileSystem can be None
  (#485644). (clumens)

* Thu Feb 19 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.22-1
- Updated Romanian translation (alexxed)
- Remove the qla2xxx line from mk-images again (wwoods).
- Fix broken shell syntax from 3bdcd64d2 (jkeating)
- The VLGothic-fonts package has changed name and location (#486080).
  (clumens)

* Tue Feb 17 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.21-1
- Building for i586 only now in Fedora. (dcantrell)

* Tue Feb 17 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.20-1
- Fix indentation on upd-instroot (kanarip)
- Fix the indentation in mk-images (kanarip)
- Remove unused iface_netmask2prefix() function. (dcantrell)
- A parted.Disk has no attribute named "dev".  It's named "device"
  (#486007). (clumens)
- Use brandpkgname for the efi art too (katzj)
- Let's use the product string for a brandpackage name. (kanarip)
- Fix indentation in mk-images.efi (kanarip)
- Fix indentation in buildinstall script (kanarip)
- It's part.active, not part.is_active(). (clumens)
- File the basic traceback as the first comment instead of a generic
  message. (clumens)
- Encode our upgrade policy in productMatches/versionMatches and enforce it.
  (clumens)
- If we'd show package selection on kickstart installs, also show tasksel.
  (clumens)

* Fri Feb 13 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.19-1
- Fix build errors in the new net.c code. (clumens)

* Fri Feb 13 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.18-1
- Require pyparted >= 2.0.0 (dcantrell)
- Update to use the new pyparted. (dcantrell, clumens)
- Replace non UTF-8 char for hiding password chars with UTF-8 (#485218)
  (hdegoede)
- Use a better test for when we're in text mode (#484881). (clumens)
- Add iBFT support to loader (msivak)
- Hardlink the initrd.img since we're linking the vmlinuz as well. (jkeating)
- Check if ld-linux.so.2 is a link already, before removing it (dcantrell)

* Wed Feb 11 2009 Hans de Goede <hdegoede@redhat.com> - 11.5.0.17-1
- Revert broken German translation fixes so that we will build again
- Sync up module list (#484984) (katzj)

* Wed Feb 11 2009 Hans de Goede <hdegoede@redhat.com> - 11.5.0.16-1
- Rewrite iscsi support using libiscsi (hdegoede)

* Mon Feb 09 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.15-1
- Fix gptsync/lib.c for gcc strict aliasing rules. (dcantrell)
- Fix gcc warning for gptsync memset() usage. (dcantrell)

* Mon Feb 09 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.14-1
- Rewrite mdio_read() in linkdetect.c for strict aliasing rules. (dcantrell)

* Mon Feb 09 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.13-1
- Check that required kickstart commands are present early on (#483048).
  (clumens)
- Simplify the text mode interface. (clumens)
- Fix truncated translation string for livecd installs (#484430). (clumens)
- Calcutta -> Kolkata (#484638). (clumens)
- Fix runpychecker.sh to find zonetab module (hdegoede)
- Strip invalid characters from automatically made VG/LV names (#483571).
  (clumens)
- Fix systemtime setting during installation (#6175, #461526). (rvykydal)
- Workaround MMC block devs showing up not as disks from hal (#481431)
  (katzj)
- Add some new false positives to pychecker false positives filtering
  (hdegoede)
- Make kickstart timezone value check consistent with system-config-date
  (#483094) (rvykydal)
- Make ext4 default in UI filesystem selection (bug #481112) (rvykydal)
- Redirect iscsiadm's stderr away from the console. (clumens)
- Pay attention to the stderr parameter to execWithCapture. (clumens)
- For python2.6, our showwarnings function must take a line= parameter.
  (clumens)
- If ext4dev is seen in the /etc/fstab, treat it as ext4 instead (#474484).
  (clumens)
- Make sure to call _getConfig from our YumSorter subclass. (clumens)
- Set proper text mode font for Greeks (#470589) (msivak)
- Lots of translation updates.

* Thu Jan 29 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.12-1
- If ks=nfs:... is given, don't try to find the file via boot options
  (#480210). (clumens)
- Fix cdrom install on machines with no network devices (wwoods)
- updated fuzzy strings (jsingh)
- Use modinfo to find out what firmware we need in initrd (wwoods)
- Use the preconf object for yum configuration now (jantill). (clumens)
- Updated Dutch translation adn only 1 -fuzzy- string left (zuma)
- Add a boot target for the xdriver=vesa parameter and document it. (clumens)
- repo.proxy is now a property, so check before setting it (#481342).
  (clumens)

* Wed Jan 21 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.11-1
- Fix a logic problem with network file write outs. (480769) (jkeating)
- Only run selectBestKernel, selectBootloader, etc. for new installs.
  (wwoods)

* Mon Jan 19 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.10-1
- btrfs install support (sandeen)
- Default / to be ext4 (katzj)
- Allow live installs to use ext4 as root and make the error message clearer
  (katzj)
- Add support for Maithili and Nepali (#473209). (clumens)

* Fri Jan 16 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.9-1
- Cracklib moved locations, account for this in our keepfiles. (jkeating)
- Look in the right path for kernel module lists. (jkeating)
- Fix more problems in expandModuleSet, based on a patch from markmc
  (#480307). (clumens)
- Allow ext4 without magic argument (keep a flag for migrate) (katzj)
- Fix pulling in network modules (katzj)
- Support mounting NTFS filesystems (#430084) (katzj)
- dejavu fonts changed package names, pick up new names. (jkeating)
- TightVNC is now the default VNC server in Fedora (#480308). (clumens)
- Only skip (over)writing netconfig if we have an actual instPath (jkeating)
- The sets module is deprecated, so no longer use it. (clumens)

* Wed Jan 14 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.8-1
- Fix D-Bus usage in get_connection in loader (jkeating)

* Wed Jan 14 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.7-1
- How to get raw pages from the wiki has changed again. (clumens)
- Make sure the 'anaconda' file gets the right detected type (alsadi,
  #479574).
- Include the missing import. (clumens)

* Thu Jan 08 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.6-1
- Collect DSO deps for NetworkManager plugins. (dcantrell)

* Thu Jan 08 2009 Chris Lumens <clumens@redhat.com> - 11.5.0.5-1
- NetworkManager system settings plugins were renamed, change mk-images.
  (dcantrell)
- Add a message to install.log when package installation is done (#476953).
  (clumens)
- Add support for specifying which partition to upgrade (atodorov, #471232).
  (clumens)
- pykickstart has a new version of the upgrade command. (clumens)
- Log all calls to mount to /tmp/program.log as well. (clumens)
- Log everything from execWithRedirect or execWithCapture (#467690).
  (clumens)
- Update partedUtils.py:findExistingRootPartitions to return UUID
  (atodorov). (clumens)
- Don't skip the method screen when going back and forth (#477991). (clumens)
- Die on errors from upd-instroot/mk-images rather than continuing on (katzj)
- The FTP USER command does not need to be followed by a PASS (#477536).
  (clumens)

* Mon Jan 05 2009 David Cantrell <dcantrell@redhat.com> - 11.5.0.4-1
- Workaround compile error due to (# 478663) (hdegoede)
- Various packaging fixed from review (#225246) (hdegoede)
- Show the header in certain non-lowres cases (#478765, alsadi AT
  ojuba.org). (clumens)
- Remove doMultiMount. (clumens)
- Use mount -t auto instead of passing a list of valid fstypes (#477328).
  (clumens)
- Fix case sensitivity when searching for headers (kanarip)
- Fix a traceback in checking for network install (ricky AT
  fedoraproject.org). (clumens)

* Tue Dec 23 2008 David Cantrell <dcantrell@redhat.com> - 11.5.0.3-1
- Initialize domainname to None (#477831) (dcantrell)
- Do not import unused modules. (dcantrell)
- Call '/sbin/udevadm settle' instead of /sbin/udevsettle (dcantrell)

* Tue Dec 23 2008 David Cantrell <dcantrell@redhat.com> - 11.5.0.2-1
- Require latest pykickstart for repo command (clumens)
- Remove libdhcp* from scripts/upd-instroot (dcantrell)
- methodstr -> self.methodstr (dcantrell)
- Rewrite iface_ip2str() to use libnm-glib (dcantrell)
- Fix a few syntax error caugh by pychecker (hdegoede)
- Remove isys.e2fslabel() and isys.getraidsb() (dcantrell)

* Thu Dec 18 2008 David Cantrell <dcantrell@redhat.com> - 11.5.0.1-1
- Remove plural forms from po/tg.mo (katzj)

* Thu Dec 18 2008 David Cantrell <dcantrell@redhat.com> - 11.5.0.0-1
- Reduce direct D-Bus calls in isys/iface.c. (dcantrell)
- Allow 'ks' to function as it once did (#471812) (dcantrell)
- Fix telnet install support (#471082) (dcantrell)
- Call 'udevadm settle' instead of 'udevsettle'. (dcantrell)
- When using anaconda with kickstart file with UI mode - do not show the VNC
  question (#476548) (msivak)
- Check error from asprintf() correctly for dhcpclass handling. (dcantrell)
- Use libnm_glib in net.c:get_connection() (dcantrell)
- Add libnm_glib CFLAGS and LIBS to loader's Makefile. (dcantrell)
- BR NetworkManager-glib-devel. (dcantrell)
- Only write the short hostname to the localhost line (#474086) (dcantrell)
- Updated Tajik Translation - Victor Ibragimov (victor.ibragimov)
- Copy /etc/dhclient-DEV.conf file to target system (#476364) (dcantrell)
- Use macros for D-Bus paths (dcantrell)
- Let X tell us when it's launched rather than just sleeping. (ajax)
- When there's no baseurl, set a default of [] instead of [''] (#476208).
  (clumens)
- cracklib now raises exceptions on bad passwords (rzhou, #476312). (clumens)
- Make sure ssh doesn't get duplicated in the open port list (#474937).
  (clumens)
- mdraid1: default to putting grub on partition instead of mbr (#217176)
  (hdegoede)
- Don't install the games group as part of office/productivity (#472324).
  (clumens)
- Don't dump encryption passphrases. (dlehman)
- Write anacdump.txt upon receipt of SIGUSR2 (from clumens). (dlehman)
- Use stacks instead of tracebacks in traceback handlers. (dlehman)
- Unmount swap devices when migrating filesystems, then reactivate
  (#473260). (clumens)
- Handle both /dev/sr0 and sr0, since that's what cdromList gives (#475083).
  (clumens)
- In iface_ip2str(), make sure to advance to next item before continue.
  (dcantrell)
- We already have _GNU_SOURCE defined in Makefile.inc (dcantrell)
- Remove XXX comment in net.c about GATEWAY (dcantrell)
- Use strverscmp() from glibc in place of rpmvercmp() (dcantrell)
- Remove readLine() function from loader/loadermisc.c (dcantrell)
- Do not write SEARCH line to ifcfg-DEVICE file (#474858) (dcantrell)
- Preserve existing network configuration files during install (#461550)
  (dcantrell)
- Send unique vendor class identifier unless user specifies one. (dcantrell)
- Avoid tracebacks when filling in static network config fields (#474275)
  (dcantrell)
- Prevent network install when no network devices are found (#470144)
  (dcantrell)
- Remove markup from text before printing it in cmdline mode (#470253).
  (clumens)
- Move strip_markup() into iutil. (clumens)
- Fix up plural forms header so that python doesn't blow up for us (katzj)
- Change text to reflect Jesse's comments (katzj)
- Add support for the Tajik language (#455963). (clumens)
- Add a button to the UI to ignore all missing packages. (clumens)
- First small eu.po transtation, just to be sure that the system is set up
  OK. (mikel.paskual)
- mini-wm: Turn on automatic window redirection. (ajax)
- Better naming for LVM volume groups and logical volumes (#461682)
  (dcantrell)
- Partition requests can be None when populating the tree. (#474284)
  (dlehman)
- Say we are unable to configure the network interface (#467960) (dcantrell)
- Match textw/network_text.py strings to iw/network_gui.py (#470145)
  (dcantrell)
- In addSnap(), check snapshots for data key before continuing (#433824)
  (dcantrell)
- Load FCP modules early for CD/DVD install (#184648) (dcantrell)
- Update mk-s390-cdboot.c to work with large kernel images (#184648)
  (dcantrell)
- Make sure fstype exists before we try to test it (#473498). (clumens)
- Updated a small correction in kn locale (svenkate)
- Use modules.* files for finding modules of a type rather than modinfo
  (katzj)
- Make complete text mention updates (#244431) (katzj)
- Make text for autopartitioning types clearer (#441350) (katzj)
- Allow installing grub on the MBR if /boot is on mdraid (#217176) (hdegoede)
- Fix some spelling errors in German translation (fabian)
- Make the required media dialog less wordy (#469557). (clumens)
- returnNewestByName now raises an error instead of returning [] (#472462).
  (clumens)
- Fix death on login of an OLPC on a live image (katzj)
- Fix ld-*.so globbing for glibc-2.9 . (pjones)
- Do not bring up network for non-remote kickstart locations (#471658)
  (dcantrell)
- Resolve dm-X devices returned by pvdisplay. (#448129) (dlehman)
- More shell script syntax fixing (katzj)
- Only bring up the network dialog on package failures if required
  (#471502). (clumens)

* Wed Nov 12 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.58-1
- Add comps groups for new repos that are added (#470653) (katzj)
- Support upgrades of systems whose rootfs is on an LV. (#471288) (dlehman)
- Use hasPassphrase() instead of directly accessing passphrase member.
  (dlehman)
- Don't dump private class members (those with leading "__") (dlehman)
- Explicitly close the CD drive after the user hits "continue" (#375011)
  (pjones)
- Fix shell syntax error (#471090) (ivazqueznet)
- Save the /etc/fstab before overwriting it on upgrades (#452768, #470392).
  (clumens)

* Tue Nov 11 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.57-1
- Fix more UnicodeDecodeErrors, hopefully for good this time (#470733).
  (clumens)
- iscsi do missing value check only once (hdegoede)
- Don't try to label XFS filesystems on livecd installs (#470951). (clumens)
- Include cracklib .mo files and look up strings in the right domain.
  (clumens)
- Bugzilla has changed its return values for a couple queries. (clumens)
- Set the default keyboard based on the language (#470446). (clumens)
- Prevent traceback for vnc installs on KVM guests (#470559) (dcantrell)
- Bring up networking early enough for syslog= param (#470513) (dcantrell)
- Sleep a bit before calling udevsettle in iscsiTarget.login (#470073,
  #466661) (hdegoede)
- kickstart, iscsi do not call iscsi.startup after startIBFT has been called
  (hdegoede)
- Do not stop and restart iscsid when rescanning disks/partitions (#470223)
  (hdegoede)
- iscsi.startup should not login to targets as we are already logged in
  (#470230) (hdegoede)
- Remove obsolete normally never reached code from _stopIscsiDaemon
  (#470229) (hdegoede)
- The function getEncryptedDevice gets called correctly expect when we are
  in (jgranado)
- More translations

* Thu Nov 06 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.56-1
- Don't have the key icon take up so much space on the LUKS dialog
  (#470338). (clumens)
- Avoid getting linux-base in the kernel list (katzj)
- Deselect groups when we reset things also (#469854) (katzj)
- make iscsi login code wait for udev to create the devices (#466661,
  #470073) (hdegoede)
- Set the correct path when using the directory chooser. (clumens)
- We always need a wait window, not just when the repo has a name. (clumens)
- Set initial state of IP configuration fields in text mode (#469933)
  (dcantrell)
- Prevent traceback when there are no network devices (#469339) (dcantrell)
- Indentation fix. (pjones)
- Let users edit net settings on network failure in stage 1 (#465887)
  (dcantrell)
- Move startNewt later to avoid printing extra messages on the screen
  (#469687). (clumens)

* Mon Nov 03 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.55-1
- Revert "Make sure dialog deletions take effect sooner (#455676)." (clumens)
- Don't set up the launcher for the installer on XO (katzj)
- Whitespace cleanups for timezone.py (dcantrell)
- Do not store mount options in loaderData->instRepo (#467760) (dcantrell)
- Make sure we look up the IP address for the correct device (#469439)
  (dcantrell)
- Remove unused bool() function. (dcantrell)
- Check for required space for / on live installs (#468867) (katzj)
- Add a basic method for checking the minimal size needed for a backend
  (katzj)
- Fix typo that somehow snuck in (katzj)
- If there's no language selected, don't traceback (#469578). (clumens)
- Improve filtering of non-available groups (#469438) (katzj)
- filer.py: set defaultProduct in __init__ (hdegoede)
- Fix indentation error in filer.py (again) (hdegoede)
- Rebuild keymaps to get rid of trq.map (#469433). (clumens)
- Provide sample punch card reader script for s390x (#462953) (dcantrell)
- Fix a typo that shouldn't have even gotten though. (clumens)
- Check that the platform and product are also correct (#469367). (clumens)
- Remove cio_ignore functionality for s390x (dcantrell)
- Remove bootdisk/s390 (dcantrell)
- If method=nfs: is given, check if it's really an NFSISO install (#468885).
  (clumens)
- Get the right list elements for the iscsi text interface (#466902).
  (clumens)
- Don't traceback when displaying error messages (#469372). (clumens)
- Make sure we differentiate locked luks devs from deleted ones. (dlehman)
- Fix a typo that breaks kickstart with encryption. (#469318) (dlehman)

* Thu Oct 30 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.54-1
- Call startNewt earlier than network bring up (#469171). (clumens)
- Write out the path to the repo, not anaconda-ks.cfg (#467753). (clumens)
- Allow specifying devices by path if they're files (#468504) (katzj)
- Fix the last pychecker warnings in master (hdegoede)
- Add --strict option to runpychecker.sh (hdegoede)

* Wed Oct 29 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.53-1
- Don't sleep(5) after xrandr (ajax)
- Force DPI to 96 even harder (#458738) (ajax)
- Don't try to switch VT to the one that X is on (ajax)
- Only copy /etc/resolv.conf if instPath != '/' (dcantrell)
- 'is not' -> '!=' (dcantrell)
- Write --dhcpclass instead of --class to the anaconda ks file. (jgranado)
- Fix 2 issues in pyparted found by pychecker (hdegoede)
- Add a bit of documentation to the top of runpychecker.sh (hdegoede)
- Add runpychecker.sh script and pychecker-false-positives file (hdegoede)
- Fix saving tracebacks via scp while in text mode. (clumens)
- Search for the hash in the whiteboard, not as the entire whiteboard.
  (clumens)
- Fix various syntax errors caught by PyChecker (hdegoede)
- Wouldn't it be nice to have some real documentation in filer.py? (clumens)
- Make sure the productVersion given by .treeinfo exists in bugzilla
  (#468657). (clumens)

* Mon Oct 27 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.52-1
- Let DNS lookups work from %%post scripts (#468132) (dcantrell)
- Do not use /.tmp for temporary files (#468720) (dcantrell)
- Don't treat encrypted PVs as available if we don't have the key. (#465240)
  (dlehman)
- Do all new device passphrase prompting from partitioningComplete. (dlehman)
- Fix the obviously stupid typo. (clumens)
- There's a new version of the firewall command for F10 (#467753). (clumens)
- Another fix for printing package summaries in text mode (#468283).
  (clumens)
- Fix traceback in network.bringUp() (#468651) (dcantrell)
- lvresize requires a --force arg now (#468478) (katzj)
- Include return code on resize failure error message (#468479) (katzj)

* Fri Oct 24 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.51-1
- Catch UnicodeDecodeError so traceback messages display anyway. (dcantrell)
- Do not write NM_CONTROLLED=yes to ifcfg files (#468028) (dcantrell)
- Log D-Bus messages at ERROR or INFO level. (dcantrell)
- Write dhcpclass to the dhclient conf file for the device (#468436)
  (dcantrell)
- Tell NetworkManager not to touch network interfaces when / is a netfs
  (hans)
- Catch more X failures and fallback to text (#467158). (clumens)
- Fix a typo when using network --gateway (#468364). (clumens)
- Fix icon (#468273) (katzj)
- Remove extra debug info. (pjones)
- Fix the damn spinner in the progress bar. (pjones)
- Fix whitespace. (pjones)
- Fix "looking for installation images" when there's no disc at all. (pjones)
- Make sure dialog deletions take effect sooner (#455676). (clumens)
- Make cdrom drive door status messages be INFO not DEBUG. (pjones)
- Don't switch to tty6 on vnc installs. (clumens)
- Update font list (#462295). (clumens)
- Don't display the entire lengthy device description (#467825). (clumens)
- Fix ext4 detection on existing partitions (#467047) (rvykydal)
- Make sure we handle the /tmp/method file for FTP correctly (#467753).
  (clumens)
- Do not write NM_CONTROLLED=yes to ifcfg files (#468028) (dcantrell)
- Revert "dhclient-script not needed for NetworkManager" (clumens)
- Skip Installation Repo when writing out repo kickstart lines. (clumens)
- Correct media check docs (#468061). (clumens)
- Many translation updates

* Fri Oct 17 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.50-1
- Update several font package names that we were missing. (clumens)
- Only bring up the netconfig dialog if the repo requires networking.
  (clumens)
- cmdline.py: Fix a small typo in a message (rh 467338) (hansg)
- Enable CCW devices used for installation (#253075) (dcantrell)
- I don't know what trq.map.trq-map is, but let's not include it. (clumens)
- If networking is needed for yum repos, bring it up before fetching
  repodata. (clumens)
- Force DPI to 96 when launching X. (#458738) (ajax)
- Lots of translation updates.

* Tue Oct 14 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.49-1
- Make kickstart installs work again (#374271, #392021, #448096, #466340,
  #466304) (dcantrell)
- Let users go Back when loading updates. (dcantrell)
- Write ifcfg files to /etc/sysconfig/network-scripts instead of /.tmp
  (dcantrell)
- Handle unknown hosts in getDefaultHostname (#466775) (dcantrell)
- Try to look up the hostname by the IP address NM reports (#466775)
  (dcantrell)
- NM no longer provides the hostname as a property (#466775). (clumens)
- ext4dev -> ext4 (esandeen). (clumens)
- Move persistent network udev rule to under /etc (#464844). (clumens)
- Update keymaps to include latest Romanian settings (#466117). (clumens)
- Take ip= parameter values by not resetting ipinfo_set. (dcantrell)

* Fri Oct 10 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.48-1
- Remove unnecessary STEP_IP code. (dcantrell)
- Fix how configureTCPIP() returns. (dcantrell)
- Write new sysconfig data to a tmpdir first, then move in place. (dcantrell)
- Write NM_CONTROLLED=yes rather than NM_CONTROLLED= (dcantrell)
- Get rid of some iface flags that were not doing anything anymore.
  (dcantrell)
- Generate new config files in /.tmp in writeEnabledNetInfo() (dcantrell)
- Remove unused variables from configureTCPIP() (dcantrell)
- Do not call get_connection() twice for DHCP. (dcantrell)
- Ask for language and keyboard in rescue mode (#466525). (clumens)
- Fix bringing up the network in rescue mode (#466523). (clumens)
- If we don't have a translation for a lang name, just use the English
  (#466515) (katzj)
- Disable some more IPv6 checks. (clumens)
- Fix a typo (second part of #466374) (katzj)

* Thu Oct 09 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.47-1
- Tag problems in pkgcvs.  Wish we still had force-tag

* Thu Oct 09 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.46-1
- Pull in static network settings from the boot: line (#465270) (dcantrell)
- Do not segfault when going back to select a new interface (#465887)
  (dcantrell)
- Do not test for DNS settings in mountNfsImage() (dcantrell)
- Populate struct iface correctly in setupIfaceStruct() (dcantrell)

* Thu Oct 09 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.45-1
- Fix sorting of repos so we always return an integer value (#466174).
  (clumens)
- Change the upgrade progress bar to pulse (#466053). (clumens)
- Mark iscsi disks not used for / as autostart (rh461840) (hans)
- Always display the wait window when fetching repo information. (clumens)
- Lazily unmount everything before killing NetworkManager (#463959).
  (clumens)
- lang-names really does need to depend on subdirs (katzj)
- Reset targetLang on language change (#465981) (katzj)
- Honor static net parameters with NM (#465270) (dcantrell)

* Mon Oct 06 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.44-1
- Do not rely on loaderData->noDns to tell if we have DNS configured.
  (dcantrell)
- Skip askmethod dialog if user passes repo= and stage2= (dcantrell)
- Reset resolver in get_connection() (dcantrell)
- Fix problems dealing with PXE boot and the ksdevice= parameter. (dcantrell)
- Disable more IPv6 code in loader for now. (dcantrell)
- Write BOOTPROTO=static for manual IPv4 config. (dcantrell)
- Disable IPv6 widgets for F-10. (dcantrell)
- Add iwlagn driver firmware (#465508). (clumens)
- Move starting HAL to after we've probed for hardware. (clumens)
- Don't try to load a couple modules that no longer exist. (clumens)
- The Chinese font package has changed names (#465290). (clumens)
- Fix a traceback when there's no ksdevice given (#465638). (clumens)
- Fix traceback in post install configuration (hans)

* Fri Oct 03 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.43-1
- Disable IPv6 interface widgets in loader for now. (dcantrell)
- Start NetworkManager earlier (#462083) (hans)
- Work around gtk2 bug (#465541) (hans)
- Move our yum.conf out of /etc (#465160) (katzj)
- Correctly display the IP address a vnc viewer should connect to (#465353).
  (clumens)
- lohit-fonts-malayam has been replaced by smc-fonts-meera (#456449).
  (clumens)
- Fix a typo in cleaning up repos. (clumens)
- Fix the mount error reading for real this time (pjones, #465250). (clumens)
- Support ksdevice=link when booting from boot.iso. (dcantrell)
- Automatically select NIC based on ksdevice= boot parameter. (dcantrell)

* Wed Oct 01 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.42-1
- Revert "Finally controlled the plural issue at #508  in Japanese"
  (dcantrell)

* Wed Oct 01 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.41-1
- Fix text inconsistency (#465165). (clumens)
- If there's an error running Xvnc, also print it to the console. (clumens)
- Set the installation repo when using the askmethod UI (#463472). (clumens)
- Fix a segfault when the wrong HDISO repo parameter is given. (clumens)
- Remove the 'Installation Repo' cache directory after install (#464853).
  (clumens)
- If there aren't any usable NICs, don't write out a config (#465127).
  (clumens)
- It helps to specify what the method string should be split on (#464855).
  (clumens)
- Gateway and nameserver are optional for static network configuration.
  (dcantrell)
- Store nameserver in NetworkDevice object. (dcantrell)
- Fix a traceback calling enableNetwork (#464849). (clumens)
- Enable groups when creating new repos since yum doesn't do that now.
  (clumens)
- Update FQDN patch to fix a couple tracebacks (#464191). (clumens)
- Fix static network configuration from boot.iso installs. (dcantrell)
- Use all caps naming for the netdev keys. (dcantrell)
- Left justify text in ui/netconfig.glade interface. (dcantrell)
- Use the right attribute for repo URLs. (clumens)
- Use fullscreen for small screens (#444943) (katzj)
- Another try at fixing up reading errors from mount. (clumens)
- Don't traceback if no baseurl has been set yet. (clumens)
- Allow users to enter a hostname or FQDN during installation (#464191)
  (dcantrell)
- Whitespace cleanups. (dcantrell)
- Fix mk-s390-cdboot on s390x (#184648) (dcantrell)
- Run all text through unicode() before putting it into the TextBuffer.
  (clumens)
- Add reverse chap iscsi bits for kickstart (hans)
- Properly center the passphrase entry dialog. (clumens)
- Fix test for an empty hostname. (clumens)
- Support installs to SD via MMC (#461884) (katzj)
- Set ANACONDA_PRODUCTNAME, etc from /etc/system-release (#464120) (alsadi)
- Reduce code duplication by moving methods into backend (katzj)
- Select packages after repos are set up (#457583) (katzj)
- Add a basic reset method (katzj)
- Cleanups and simplifications to repo setup (clumens) (katzj)
- Revert "Revert "lang-names should really only depend on lang-table""
  (katzj)
- Fix lang-name generation + fix traceback with LANG=C (katzj)
- Allow going back to the method selection screen on error (#463473).
  (clumens)
- Make the boot loader device dialog less ugly (#463489). (clumens)
- Look in images/ for install.img on HDISO (#463474). (clumens)
- Sort Installation Repo to the top of the repo list. (clumens)
- Fuzzy string to fix translation build (katzj)

* Wed Sep 24 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.40-1
- Fix network interface bring up in text mode (#463861, #462592) (dcantrell)
- Bring back isys.resetResolv() and fix NetworkManager polling in
  network.py. (dcantrell)
- Poll 'State' property from NetworkManager in network.bringUp() (dcantrell)
- Log error in rescue mode is network.bringUp() fails. (dcantrell)
- Set the first network device in the list to active. (dcantrell)
- Get rid of firstnetdevice in Network (dcantrell)
- Do not write /lib/udev.d rules if instPath is '' (dcantrell)
- Fix problems with bringDeviceUp() calls (#463512) (dcantrell)

* Mon Sep 22 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.39-1
- Fix a traceback when getting the interface settings (#462592). (clumens)
- self.anaconda -> anaconda (clumens)

* Sat Sep 20 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.38-1
- Restore old lang-names generation method (dcantrell)
- Remount /mnt/sysimage/dev after migrating filesystems. (clumens)
- Use the instroot parameter like we should be doing. (clumens)

* Fri Sep 19 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.37-1
- Set the filename on the traceback when we upload it (wwoods).
- Don't worry about errors looking up protected partitions on upgrades.
  (clumens)
- Fix test for allowing the installation source to be on the root fs
  (#462769). (clumens)
- lang-names should really only depend on lang-table (katzj)
- Don't make the .desktop file unless we actually need to (katzj)
- Fix lang-name generation (katzj)
- Look for xrandr in the search path. (clumens)
- Make the textw network screen match the iw interface by only prompting for
  hostname (#462592) (dcantrell)
- Pick up hostname if we have it, otherwise use localhost.localdomain
  (#461933) (dcantrell)
- dhclient-script not needed for NetworkManager (dcantrell)
- Add getDefaultHostname() to network.py (dcantrel)
- Write out NETMASK and BROADCAST correctly in loader. (dcantrel)
- Fix problems with manual network configuration in loader. (dcantrel)
- anaconda-yum-plugins is now in its own source repo. (clumens)
- Remove most of the network configuration from text mode as well (#462691).
  (clumens)
- Add an extra newline to the empty partition table message. (clumens)
- Fixup DiskSet._askForLabelPermission() (markmc)

* Mon Sep 15 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.36-1
- Remove invalid i18n stuff to let anaconda build. (dcantrell)
- Remove doConfigNetDevice() prototype. (dcantrell)

* Mon Sep 15 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.35-1
- Call network.bringDeviceUp() instead of old isys functions. (dcantrell)
- Pass device name to network.setDNS() and network.setGateway(). (dcantrell)
- NetworkManager fixes in network.py (dcantrell)
- Remove code from isys not needed for NetworkManager. (dcantrell)
- Avoid writing out NM_CONTROLLED more than once. (dcantrell)
- Write out final ifcfg-DEVICE files correctly. (dcantrell)
- Use POSIX and LSB hostname length limit. (dcantrell)
- Consistent whitespace usage in network.py (dcantrell)
- Do not try to start hald or dbus-daemon from anaconda. (dcantrell)
- On HDISO installs, mark LABEL= and UUID= partitions as protected. (clumens)
- Do encrypted device passphrase retrofits while activating partitioning.
  (dlehman)
- Use one passphrase for all new LUKS devices and offer retrofit to old
  ones. (dlehman)
- There's only one passphrase member (encryptionPassphrase) in Partitions.
  (dlehman)
- Only add LUKSDevice instances to PV requests as needed. (dlehman)
- New device passphrase is now always global w/ option to retrofit. (dlehman)
- Don't prompt for a passphrase when creating encrypted devices. (dlehman)
- Define a method to add a passphrase to an existing LUKS device. (dlehman)
- Fix a traceback when starting a shell in rescue mode (#462148). (clumens)
- md, lock_nolock, and dm_emc kernel modules no longer exist. (clumens)
- Fix iscsi disk detection with newer kernels (rh 461839, 461841) (hans)
- Fix the crash reported in bug 454135 (hans)
- Make iBFT reading explicit from a higher level (hans)
- Add ibft flag to ease in testing. (hans)
- Support iSCSI CHAP and Reverse CHAP authentication (rhbz#402431,
  rhbz#432819) (hans)
- Don't set iscsi devices to autostart (rhbz#437891) (hans)
- Add full CHAP support to iSCSI. (rhbz#432819) (hans)
- Do not try to initialize iSCSI, when no portal (#435173) (hans)
- Fix wrong function names for iscsi login/start (rhbz#295154) (hans)
- Set an attribute when iscsid is started (#431904). (hans)
- Better fixes for iscsi probing (patch from jlaska) (hans)
- Make sure ISCSIADM and such are defined (rhbz#431924) (hans)
- Fix iscsi so that mkinitrd can actually talk to the running daemon (hans)
- Make iscsi/ibft work (hans)
- Add mk-images changes forgotten in previous commit (hans)
- Add support for iSCSI iBFT table (#307761) (hans)

* Thu Sep 11 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.34-1
- Always start NM so we can talk to it in the boot.iso case (#461071).
  (clumens)
- Use the device path to identify LUKS devs in /etc/fstab. (#460700)
  (dlehman)
- Use the LUKS UUID instead of device nodes in all references. (#460700)
  (dlehman)
- LUKSDevice.getScheme() no longer cares if the dev has a passphrase.
  (#461203) (dlehman)
- Correct translation to fix the build. (clumens)
- Add the method string back into anaconda-ks.cfg. (clumens)
- Let's try pulling libsqlite into the initrd one more time. (clumens)
- Don't traceback at the end of live installs (katzj)
- Correct the message telling you to use a VNC password. (clumens)
- Remove unused TIMEZONES= crud. (clumens)
- print doesn't yet support the file= syntax in our version of python.
  (clumens)
- Catch errors from using the wrong bugzilla field and display them.
  (clumens)
- Fix line wrapping on part type screen (jlaska, #461759).
- rep_platform has been renamed to platform. (clumens)

* Tue Sep 09 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.33-1
- Include NetworkManager and dbus libraries on 64-bit arches (#461632).
  (clumens)
- We need libsqlite3.so in upd-instroot before it can be in the initrd.
  (clumens)
- Fix partitions growing (backport of rhbz #442628) (rvykydal)
- Kickstart timezone validity check fixed (#461526) (rvykydal)
- Add more kernel crypto modules (#443545). (clumens)
- Make the progress bar move when downloading the install.img (#461182).
  (clumens)
- Add overrideDHCPhostname as an attribute. (clumens)
- Fix saving to remote hosts (#461500). (clumens)
- short_desc is now summary. (clumens)
- Use print() as a function. (pjones)

* Sat Sep 06 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.32-1
- Use struct audit_reply instead of struct auditd_reply_list (dcantrell)

* Sat Sep 06 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.31-1
- Use --service=NAME in firewall.py when calling lokkit (dcantrell)
- Make NM work for the DHCP case, at least (dcbw) (#461071). (clumens)
- Sleep a little after dbus to give it time before HAL connects. (clumens)
- Add libsqlite to the initrd, which is needed by NSS libs. (clumens)
- Add more dlopen()ed libraries to the initrd. (clumens)
- Fix various problems with the exn saving UI (#461129). (clumens)
- Fail gracefully if we can't talk to NetworkManager over DBus. (dcantrell)
- Reword text for easy of translating plurals (#460728). (clumens)
- Make sure /bin/sh is linked to /bin/bash (dcantrell)
- Do not include /usr/lib/gconv in install.img (dcantrell)
- Add /etc/NetworkManager/dispatcher.d to the install.img. (clumens)
- Remove last vestiges of rhpxl and pirut. (clumens)
- Only one list of packages in upd-instroot, thanks. (clumens)
- Add xrandr back into the install.img (#458738). (clumens)
- Add a couple more directories to search paths. (clumens)
- Do repo setup and sack setup as separate steps. (clumens)
- Fix a typo that was causing repos in the kickstart file to be skipped
  (#451020). (clumens)

* Fri Aug 29 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.30-1
- Fix a traceback with unencrypted autopart. (dlehman)
- doLoggingSetup has grown some new arguments (#460654). (clumens)
- Updated German translation (fabian)
- Remove references to isConfigured in network.py (dcantrell)
- Define the NM_STATE_* constants in isys.py (dcantrell)
- Rewrite NetworkWindow to only prompt for hostname. (dcantrell)
- Pad the icon more in network.glade (dcantrell)
- Removed iface_dns_lookup() (dcantrell)
- Don't pass NULL to dbus_message_unref() (dcantrell)
- New network configuration screen for GTK+ UI. (dcantrell)
- Pass family to iface_ip2str() call (dcantrell)
- Rewrite iface_ip2str() to talk to NetworkManager over D-Bus (dcantrell)
- New translation (besnik)
- Pull in the gtkrc file so we can find the theme. (clumens)
- Use signed git tags (katzj)
- Skip networkDeviceCheck in dispatch.py (dcantrell)
- Do not call has_key() on NetworkDevice, use isys.NM_* (dcantrell)
- Separate lines per BR. (dcantrell)
- Remove invalid line iw/autopart_type.py (dcantrell)
- Fix syntax error in yuminstall.py, fix pychecker warnings. (dcantrell)
- Updated Hungarian translation (sulyokpeti)
- Add missing () to function definitions. (dcantrell)
- Fix err handling in doMultiMount() (dcantrell)
- Revert "Pass --follow to git-log" (dcantrell)
- Remove references to /tmp/netinfo (dcantrell)
- Gather network settings from NetworkManager and ifcfg files. (dcantrell)
- Update the pot file and refresh the pos (katzj)
- For all HTTP/FTP repos, keep the cached repodata (#173441). (clumens)
- Fix a traceback when trying to set the status whiteboard on a bug.
  (clumens)
- When the wrong filesystem type is used, raise a more explicit error.
  (clumens)
- Don't copy the install.img over in single media cases (#216167). (clumens)
- Remove isys.getopt() (dcantrell)
- Remove code not used in net.c (dcantrell)
- Write to /etc/sysconfig/network-scripts/ifcfg-INTERFACE (dcantrell)
- mystrstr() -> strstr() (dcantrell)
- Expand getDeviceProperties to return all devices. (dcantrell)
- Pass --follow to git-log (dcantrell)
- Support accessing preexisting LUKS devs using LRW or XTS ciphers.
  (#455063) (dlehman)
- Use yum's handling of optional/default/mandatory package selection
  (#448172). (clumens)
- List iSCSI multipath devices in the installer UI. (dcantrell)
- Fix text wrap width on the partition type combo, for real this time
  (#221791) (dlehman)
- For /dev/hvc0 terminals, set TERM to vt320 (#219556). (dcantrell)
- The Timer class is no longer used. (clumens)
- Handle preexisting swraid w/ encrypted member disks/partitions. (dlehman)
- Don't try to close a dm-crypt mapping that is not open. (dlehman)
- Remove unused silo code that wouldn't even build if it were used. (clumens)
- Remove some really old, really unused code. (clumens)
- Add another mount function that takes a list of fstypes to try. (clumens)
- Download progress indicator for FTP and HTTP in stage 1. (dcantrell)
- Make sure we wait for NetworkManager. (dcantrell)
- Renamed loader2 subdirectory to loader (hooray for git) (dcantrell)
- Do not include wireless.h or call is_wireless_device() (dcantrell)
- Add getDeviceProperties() and rewrite getMacAddress() (dcantrell)
- Do not include wireless.h (dcantrell)
- Rewrite isys.isWireless() to use D-Bus and NetworkManager (dcantrell)
- Rewrite isys.getIPAddress() to use D-Bus and NetworkManager. (dcantrell)
- Include ../isys/ethtool.h instead of ../isys/net.h. (dcantrell)
- Rename isys/net.h to isys/ethtool.h, removed unnecessary typedefs.
  (dcantrell)
- Removed waitForLink() function in loader. (dcantrell)
- Remove initLoopback() function in loader (dcantrell)
- Use D-Bus properties to get current NM state. (dcantrell)
- Use dbus in hasActiveNetDev() and _anyUsing() (dcantrell)
- Use NetworkManager instead of libdhcp. (#458183) (dcantrell)
- When mount fails, pass the error message up to the UI layer. (clumens)
- Bring askmethod back to prompt for the location of install.img. (clumens)

* Fri Aug 22 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.29-1
- Enable yum plugins. (clumens)
- In the preupgrade case, repo=hd: means an exploded tree on the hard drive.
  (clumens)
- Remove preupgrade-specific hacks. (clumens)
- Add conf files for our yum plugins so they can be enabled. (clumens)
- Create a subpackage containing the yum plugins. (clumens)
- Add the new blacklist and whiteout yum plugins. (clumens)
- Allow retrying if the ISO images aren't found (for the USB case). (clumens)
- Include "--encrypted" in anaconda-ks.cfg partitioning as needed. (#459430)
  (dlehman)
- Support establishing a global passphrase when creating encrypted devices.
  (dlehman)
- Display the lock icon for encrypted RAID members. (#459123) (dlehman)
- More descriptive drive message when warning on format. (dcantrell)
- Need to import rhpl for things like switching to pdb. (clumens)
- Fix traceback in passphrase handling code for encrypted RAID requests.
  (#459121) (dlehman)
- Copy the install.img to /tmp on HD installs. (clumens)
- Fix a typo (dcantrell).
- Expert mode was disabled in 2004.  Remove it now. (clumens)
- Remove an extra "Local disk" option (#459128). (clumens)
- Clear up error reporting on upgrades when devices are listed by UUID.
  (clumens)
- If the UI was used to specify a repo, construct a repo param (#458899).
  (clumens)
- Fix a traceback calling createMapping. (clumens)
- First crack at upgrade of systems with encrypted block devices. (#437604)
  (dlehman)
- In kickstart, prompt for new LUKS dev passphrase if not specified.
  (#446930) (dlehman)
- Remove passphrase check hack from LUKSDevice.getScheme. (dlehman)
- Allow specification of a device string for display in passphrase dialog.
  (dlehman)
- Add encrypted device passphrase dialog for text mode. (dlehman)
- Fix PartitionDevice.getDevice to take asBoot into account. (dlehman)
- Make passphrase dialogs appear in the center of the screen. (#458114)
  (dlehman)
- Consider clearpart and ignoredisk when scanning for encrypted partitions.
  (dlehman)
- Correctly handle typos in the stage2 location when inferred from repo=.
  (clumens)
- Fix the loader UI when prompting for stage2.img on HDISO. (clumens)
- Rename stage2.img to install.img (dcantrell)
- Bring up the network before saving a bug via scp. (clumens)
- Make it more explicit we want the stage2.img URL, not the repo URL.
  (clumens)
- Add the match type so we don't find all bugs. (clumens)
- Make upd-updates create the updates.img you specify if it doesn't already
  exist. (pjones)
- Don't base mpath/dmraid/raid startup/stopping based on if lvm is activated
  yet, (pjones)
- Add diskset.devicesOpen boolean, so we can tell if devices should be
  started (pjones)
- Add dirCleanup back in so we don't leave install metadata behind. (clumens)
- Move betanag to after keyboard and language are setup. (clumens)
- Add module dependencies of qeth.ko (#431922). (clumens)
- Copy the changes from RHEL5 for the linuxrc.s390 over. (clumens)
- Disable SCSI devices so we can safely remove a LUN (bhinson, #249341).
  (dcantrell)

* Tue Aug 12 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.28-1
- More fixes to include udev rules in the initrd (#458570). (clumens)
- Catch the first non-generic-logo package that provides system-logos.
  (clumens)
- Remove extra ')' in install-buildrequires (dcantrell)

* Mon Aug 11 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.27-1
- Handle 'rescue' and %%post in rescue mode (atodorov)
- Delay the duplicate label error until the label is actually used
  (#458505). (clumens)
- Enable wireless modules again for now as a test (#443545). (clumens)
- udev rules have changed location (#458570). (clumens)
- Add install-buildrequires target. (dcantrell)

* Fri Aug 08 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.26-1
- Remove a bunch of cachedir setting code that is no longer needed. (clumens)
- Fix segfaults on interactive NFS installs (#458416). (clumens)
- Fix LVM error handling so the exceptions actually get into the namespace.
  (pjones)
- yuminstall: don't look for kernel-xen anymore (markmc)
- console: kill the /proc/xen hack (markmc)
- yuminstall: don't ever stop people installing the virt group (markmc)
- lang: kill xen keymap hack (markmc)
- bootloader: remove old kernel-xen-{guest, hypervisor} handling (markmc)
- Preserve baseurl/mirrorlist and mirrorlist checkbox settings across loads.
  (clumens)
- It's BETANAG, not betanag. (clumens)
- Various string fixes (clumens).
- Wrap spec file changelog lines. (dcantrell)
- mk-images: replace kernel-xen with pv_ops kernel (markmc)
- Use a temporary location for yum cache data (#457632). (clumens)
- Remove extra newtPopWindow() call that was causing a crash (#260621).
  (dcantrell)
- Add /sbin/sfdisk (#224297). (dcantrell)
- Do not call _isys.vtActivate() on s390 or s390x platforms (#217563).
  (dcantrell)
- Change the maximum recommended swap size to "2000 + (current
  ram)".(#447372) (jgranado)
- Make it >= not > for the memory size comparison (#207573) (pjones)
- Allow float comparison between nic names in isys.py. (#246135) (joel)
- Fix formatting on disk sizes >1TB (pjones)
- Don't traceback when trying to remove /mnt/sysimage (#227650). (dcantrell)
- If we're booting off the boot.iso, don't prompt for lang or kbd (#457595).
  (clumens)
- Don't mention images/diskboot.img anymore (#441092). (clumens)
- Remove iSeries image generation (#456878) (dcantrell)
- Display capslock status correctly (#442258) (dcantrell)

* Mon Aug 04 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.25-1
- Eject the CD/DVD if we booted off a boot.iso as well (#442088). (clumens)
- Fix a GTK warning that only appears with s-c-ks running from a
  shell (#431844). (clumens)
- Break a few functions out of yuminstall.py into their own file. (clumens)
- We're not actually activating new filesystems quite yet. (clumens)
- Fix a typo in the initial partitioning screen. (clumens)
- Use system-logos instead of hardcoding fedora-logos (#457378). (clumens)
- anaconda can no longer be None when we create a DiskSet instance. (clumens)
- Remove LabelFactory since we now rely on UUIDs for everything. (clumens)
- Filter out repos that aren't enabled when running in betanag mode. (clumens)
- Close the transaction between CDs (#457126). (clumens)
- Split media fixes. (clumens)
- Handling (ask user) of invalid timezone value in kickstart added
  (#404323) (rvykydal)

* Thu Jul 31 2008 Jeremy Katz <katzj@redhat.com> - 11.4.1.24-1
- Don't try to use self.tree as the mode to open .discinfo. (clumens)
- Remove all the RPM lock files before creating a new
  transaction (#456949). (clumens)
- Support VDSK devices on s390x (#264061) (dcantrell)

* Wed Jul 30 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.23-1
- Fix mke2fs argument passing (#457285). (clumens)
- Disable logging in the firmware loader, since it clobbers other
  log messages. (pjones)

* Wed Jul 30 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.22-1
- udevsettle takes forever, so display a waitWindow. (clumens)
- Leave anaconda-runtime around for mk-images run. (dcantrell)

* Tue Jul 29 2008 Jeremy Katz <katzj@redhat.com> - 11.4.1.21-1
- Remove an instance of NEEDGR still existing to fix graphical
  isolinux (#457144) (katzj)
- use newer mke2fs arguments for different filesystems (sandeen)
- Use attributes to tell us whether filesystems are
  bootable (#457037). (clumens)
- Make sure we drag in gzip, used by the image creation stuff. (jkeating)

* Fri Jul 25 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.20-1
- Clean up some mistakes in the minstg2 removal. (dcantrell)
- Fix passing the language to anaconda (katzj)

* Thu Jul 24 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.19-1
- Fix another NFS kickstart segfault (#456461). (clumens)
- Remove support for generating a minstg2.img image. (dcantrell)
- If the xconfig command is given, do something with it (#455938). (clumens)
- METHOD_CDROM is now supported on s390 (jgranado). (clumens)
- Fix test for if we could access stage2.img on the CD (wwoods).
- Look for updates.img and product.img on the boot.iso. (clumens)
- Suspend the curses interface before calling scripts and resume afterwards
  (#435314) (msivak)

* Wed Jul 23 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.18-1
- MD_NEW_SIZE_BLOCKS no longer exists in newer kernel headers. (clumens)

* Wed Jul 23 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.17-1
- Add support for filing bugs straight into bugzilla. (clumens)
- Running git-tag -f from a makefile rule is a bad idea (katzj)
- A text message in rescue.py is not gettext-ized (atodorov)
- Code cleanup - handling of --serial (atodorov)
- Offer physical NIC identification in stage 1 (#261101) (dcantrell)
- Specify a default cio_ignore parameter for s390x (#253075) (dcantrell)
- Fix getting the stage2 image when doing kickstart installs. (clumens)
- Convert package names to unicode before displaying the error message
  (#446826). (clumens)
- When there is text mode specified in the kickstart file, disable the vnc
  question (#455612) (msivak)
- We no longer add the fstype to the hd: method in loader. (clumens)
- Check DHCP by default on the text network configurator screen. (clumens)
- Support booting from FCP-attached CD/DVD drive on s390 (#184648) (dcantrell)

* Thu Jul 17 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.16-1
- Support xdriver= again (katzj)
- Fix loadkeys on serial console (niels.devos)
- don't change from cmdline to textmode on lowmem systems (niels.devos)
- Update the VNC over text mode patch, so it correctly passes the password
  to VNC server (#455612) (msivak)
- Set interface MTU if user specified mtu= param (#435874) (dcantrell)
- Bring up the network before attempting to mount the NFSISO source. (clumens)
- Catch mount errors when adding NFS repos (#455645). (clumens)
- Fix a traceback when trying to save exceptiona via scp. (clumens)
- Give a progress bar when cleaning up after upgrades (#208725). (clumens)
- Look for repo config files in /etc/anaconda.repos.d. (clumens)
- baseurl should be a list, mirrorlist should not. (clumens)
- It's called crypto_blkcipher.ko these days. (clumens)

* Tue Jul 15 2008 David Cantrell <dcantrell@redhat.com> - 11.4.1.15-1
- Add a text-mode network config dialog so default installs can work. (clumens)
- Use the right format for the NFS methodstr, but harder this time. (clumens)
- Ask the user if he wants to use VNC instead of text mode (#453551) (msivak)
- Fix a segfault when displaying the wrong CD message. (clumens)
- Use the right format for the NFS methodstr. (clumens)
- Use correct path for FAK plugins in upd-instroot (jgranado)

* Fri Jul 11 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.14-1
- Remove an extra tab that was causing problems with the Iloko
  translation. (clumens)
- Use the right stage2.img path for kickstart URL installs (#452140). (clumens)
- Convert package errors to unicode before displaying them (#441200). (clumens)
- Display a status message while waiting for the CD to become ready. (clumens)
- Fix window title to be the same as all others. (clumens)
- In cmdline mode, give some feedback when transferring loader files. (clumens)
- If network config info isn't provided for cmdline, abort. (clumens)
- If we're not given a method in cmdline mode, we have to quit. (clumens)
- In cmdline mode, set language to the default if none is provided. (clumens)
- Don't stop on the method screen if stage2= is provided. (clumens)
- Add support for NFS to the repo editor (#443733). (clumens)
- Fix whitespace silliness. (pjones)
- Fix closing the drive door so that if the kernel happens to start giving us
  the right error code, we'll handle it correctly... (pjones)
- Fix the mysterious Error: OK message. (clumens)
- The return value from mediaCheckCdrom is totally useless. (clumens)
- Add better error handling when initializing yum (#453695). (clumens)
- Add functions for creating repos as well. (clumens)
- Don't handle all possible exceptions as if they were repo errors. (clumens)
- Reorganize to make it easier to reset the "base" repository. (clumens)
- Remove the pkgSack when a repo is disabled. (clumens)
- Use the new method of calling the NetworkConfigurator. (clumens)
- Add an updated repo editor. (clumens)
- Don't suggest text mode to the poor, poor user. (pjones)

* Wed Jul 09 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.13-1
- Filter out source and debuginfo repos from the UI. (clumens)
- Add the MD5 sum to the boot.iso to avoid errors in loader
  (#453698). (clumens)
- Don't strip too much off the NFS directory path. (clumens)
- Log stage2 url better. (pjones)
- Fix minor whitespace nits. (pjones)
- Use %%m rather than strerror() where appropriate. (pjones)
- Make setupCdrom() actually return the path to the stage2 image it
  found. (pjones)
- Don't unconditionally pass --lang for live installs (#454101) (katzj)
- Set up rhgb for plymouth on live.  And conditionalize rhgb + runlevel 5 (katzj)
- Set up rhgb if plymouth is installed as well as rhgb (katzj)
- Get the math right on how many usec per second... (pjones)
- Import missing module "network". (pjones)
- Wait up to 45 seconds for "No medium found" to stop happening (pjones)

* Thu Jul 03 2008 Peter Jones <pjones@redhat.com> - 11.4.1.12-1
- Add dmraid-libs to PACKAGES so new dmraid won't break installs.

* Thu Jul 03 2008 Peter Jones <pjones@redhat.com> - 11.4.1.11-1
- Fix double free in setupCdrom
- Fix missing psudo->pseudo spelling fix (katzj, #453843)
- Include missing X libraries in stage2.img

* Tue Jul 01 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.10-1
- Remove old livecd flag (katzj)
- Explicitly setup livecd install by passing --liveinst to anaconda (katzj)
- Check return value of asprintf() consistently (dcantrell)
- Per strtol(3) man page, set errno=0 before call. (dcantrell)
- Rescue mode no longer needs access to a methodstr (#453044). (clumens)
- Use strtol() instead of atoi() (dcantrell)
- Spell pseudo correctly. (pjones)

* Wed Jun 25 2008 Chris Lumens <clumens@redhat.com> 11.4.1.9-1
- Query for anaconda rather than anaconda-runtime in buildinstall (jkeating).

* Mon Jun 23 2008 Jeremy Katz <katzj@redhat.com> - 11.4.1.8-1
- Remove from being installed too (katzj)
- Remove anaconda-runtime as a separate subpackage (katzj)
- Remove the stuff we're not calling. (pjones)
- Remove this since we don't use it anymore (katzj)
- Don't continue on using the base installclass if we can't find one (katzj)
- Get rid of wlite and unicode-lite; these were necessary to support (pjones)
- Remove pkgorder and splittree; these should be in pungi (katzj)
- Add the .treeinfo file into the exception report. (clumens)
- Fix a typo (#452140). (clumens)

* Fri Jun 20 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.7-1
- Remove ancient block of code to upgrade Netscape Communicator. (clumens)
- Move enableNetwork into the interface.  Bring network up for scp. (clumens)
- If we can't mount for some reason, don't traceback (#452159). (clumens)
- Fix the upgrade button traceback (#374891). (clumens)

* Wed Jun 18 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.6-1
- Enable media check again, and let it check the boot.iso. (clumens)
- Substitute the version from buildstamp for $releasever if needed. (clumens)
- Remove the askmethod cmdline option. (clumens)
- Lots of work to make loader only look for stage2.img, and stage2 do
  all the install method configuration. (clumens)
- Add the --stage2= and --repo= options, deprecate --method=. (clumens)
- Fix pkgorder to include deps of kernel early. (pjones)
- Deal with udev losing udevcontrol/udevtrigger (katzj)
- Boot in graphical mode if /usr/bin/kdm exists. (clumens)
- bootProto isn't a global variable (#451689). (clumens)

* Fri Jun 13 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.5-1
- Add a mirrorlist option. (jkeating)
- Don't display garbage when prompting for the updates device. (clumens)
- Don't write out yum repo config files in kickstart.py. (clumens)
- It doesn't make sense to insert a disk into a partition, so don't
  ask. (clumens)
- Unmount /mnt/sysimage/dev manually since it doesn't get an entry. (clumens)
- Link ld-linux.so.2 to ld-*.*.*.so (dcantrell)
- Quote the repo name in anaconda-ks.cfg in case it includes spaces. (clumens)
- Move all the exception classes into a single file. (clumens)
- And import iutil a the end as well. (clumens)
- Don't display obsoleted packages in the UI. (clumens)

* Thu Jun 05 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.4-1
- Fix text mode button translations (#450176). (clumens)
- Remove a rogue call to textdomain. (clumens)
- Make "upd-updates /tmp/updates.img" update everything newer in the
  current (pjones)
- _xmltrans is undefined.  Try xmltrans instead. (clumens)
- Fix reference to cost vs. priority (#450168). (clumens)
- Don't do the "exec shell on tty1" thing in vnc if we've got virtual
  terminals. (pjones)
- Import N_ (#450163). (clumens)
- raise "NotImplementedError", not "NotImplemented" (pjones)
- Need to import iutil before we use it. (clumens)
- Don't reference PartitioningError.value . (pjones)

* Wed Jun 04 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.3-1
- Can't reference iutil.whatever from inside iutil.py. (clumens)
- When using the boot.iso and URL installs, download the .treeinfo
  file. (clumens)
- Fix a couple typos in the getArch commit. (clumens)
- Be consistent with data type. (dcantrell)
- Replace rhpl.getArch() calls with iutil calls. (dcantrell)
- Expand iutil.isX86() and added iutil.getArch() (dcantrell)
- Add isAlpha() test function to iutil. (dcantrell)
- Create architecture test functions in iutil (dcantrell)
- Removed mystrstr() function in loader2/init.c (dcantrell)
- Don't support Arabic in text mode installs since we don't even do
  RTL. (clumens)
- Removed old strace debugging in loader2/init (dcantrell)
- Keep only one copy of this code for group sorting/display around (katzj)
- Stop using rhpl.translate and use gettext directly (katzj)
- Add a descriptive comment to the top of /etc/fstab (#448966). (clumens)
- Use "message" instead of "value" on errors, and stringify on the front
  side. (pjones)
- Translate package descriptions (#449455). (clumens)
- Translate password error messages (#439981). (clumens)
- Fix traceback starting vnc (#449295) (katzj)
- Add Hewbrew to lang-table (oron)
- Fix errors in python string formatting (#449130). (clumens)

* Thu May 29 2008 Chris Lumens <clumens@redhat.com> - 11.4.1.2-1
- Allow ext4 migration again for testing at least (katzj)
- Remount filesystems after migration (#440055) (katzj)
- Add blkid to the keepfiles list so jkeating will whine less (pjones)
- Don't allow vfat /boot (katzj)
- Use the base yum doConfigSetup method. (clumens)
- Include the yum repo files from fedora-release in stage2. (clumens)
- No longer maintain our own list of extra repos. (clumens)
- Sort the repos in the UI. (clumens)
- Add cost, includepkgs, and excludepkgs to the ks repo
  objects (#448501). (clumens)
- Stop pretending to support Greek text mode (#208841) (katzj)
- Make it clear you need to reboot to use the installed
  system (#238297) (katzj)
- Activate LVM for when we do meta-resizing (#441706) (katzj)
- List Norweigian as Bokmål (#437355) (katzj)
- Simplify the install classes. (clumens)
- Don't show the EFI filesystem unless we're on an EFI platform (katzj)
- Add nfsv4 so that we don't nuke them on upgrades (#448145) (katzj)
- When there are errors reading the live CD, offer a retry. (clumens)
- Can't recover from buildTransaction errors on a per-repo
  basis (#447796). (clumens)
- Set default partition size to 200 MB in the custom partitioning
  UI. (clumens)
- Limit the size of things in exception dumps to 1k. (clumens)
- Catch IOErrors one place they seem to happen most. (clumens)
- Add a unique user agent for anaconda's grabbing in stage2 (katzj)
- Remove text mode help support as well. (clumens)
- Check for all the non-mkfs utilities required for each filesystem
  type. (clumens)
- More partitioning error handling fixes (#446453). (clumens)
- Require cracklib-python for the rootpassword screen. (notting)
- Use pykickstart's deprecated versions of the xconfig and monitor
  classes. (clumens)
- Fix tyop in upgrade migrate screen (#446363) (katzj)

* Tue May 13 2008 Jeremy Katz <katzj@redhat.com> - 11.4.1.1-1
- Just call the XStartupCB() function directly and randr to the
  desired resolution (katzj)
- Stop writing out an xorg.conf (katzj)
- Make the "dump to removable device" option work in anaconda. (jgranado)

* Mon May 12 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.79-1
- Stop neutering DRI (notting)
- make scripts/buildinstall take multiple repos (wwoods)
- Don't worry about telling people that interactive text mode is in
  wrong lang (katzj)
- Allow cpio updates.img in the tree for URL installs. (dlehman)
- Declare unpackCpioBall for use from within urlinstall.c. (dlehman)
- Don't unlink an image we retrieved but could not mount as it
  could be .cgz. (dlehman)
- Don't run lspci with an explicit path (katzj)
- Include lspci on all images (#445974) (katzj)
- Add support for attaching gdbserver to the loader early on. (clumens)
- Add virtio max partition count (markmc)
- Sort virtio devices first (markmc)
- Merge branch 'master' of ssh://git.fedorahosted.org/git/anaconda (andrewm)
- 2008-05-08  Andrew Martynov <andrewm)
- Look in the right place when ISO images are in a
  subdirectory (#443580). (clumens)
- And run in the root (#374921) (katzj)
- Don't crash when given URLs of the form ftp://user)
- Use 'yum clean all' when cleaning up after an upgrade, not
  preupgrade (#374921) (katzj)
- Kickstart flag is backwards (katzj)
- If we're given a language, don't warn about console fonts (#444258) (katzj)
- And actually include the bash binary too (#443700) (katzj)
- Search path rather than hard-coding path to mdadm (#444843) (katzj)
- Fix incorrect command name in error message. (clumens)
- Specify which protocol is used for remote saving (#440214). (clumens)
- Use bash for minstg2 shell (#443700) (katzj)
- Revert PS1 and PATH changes as they don't work with busybox as used
  in minstg2 (katzj)

* Mon Apr 28 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.78-1
- Write per-interface DNS info to ifcfg files (#443244) (dcantrell)
- Clean up sanityCheckHostname() in network.py (dcantrell)
- Activate autorepeat for GUI installs. (jgranado)

* Fri Apr 25 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.77-1
- Preserve 'set the hostname' setting when going Next/Back (#443414) (dcantrell)
- Avoid traceback on network configuration screen (#444184) (dcantrell)
- Add missing backslashes for the .profile here document. (dcantrell)
- Label the efi boot filesystem on ia64 as well. (pjones)
- Don't use size to determine if a partition is an EFI system
  partition; instead, (pjones)
- Handle the DVD having a disknumber of ALL. (443291) (jkeating)
- Make the LUKS passphrase prompt fit on an 80x25 screen. (#442100) (dlehman)
- Don't dd the image from /dev/zero _and_ use
  "mkdosfs -C <image> <blockcount>" (pjones)
- label the filesystem in efidisk.img so that HAL and such won't try to
  mount it. (pjones)
- fix testiso Makefile target - boot.iso, not netinst.iso (wwoods)

* Thu Apr 24 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.76-1
- Use the execWithCapture wrapper to be consistent. (jgranado)
- Call the mdadm with full path. (jgranado)
- Use the correct ls(1) alias. (dcantrell)
- Set PS1 and ls(1) alias for tty2 shell. (dcantrell)
- Lookinig for the capabilities file in xen is valid in more cases. (jgranado)
- Avoid putting virtualization option when in Xen or VMware.
  (#443373) (jgranado)
- If the stage2 image is on a CD, don't bother copying it (#441336). (clumens)
- Once we've found the stage2 media on CD, always use it (#443736). (clumens)
- Change mount point for CD to /mnt/stage2 when looking for stage2
  (#443755). (clumens)
- Switch to using 'yum clean all' to clean up after preupgrade
  (#374921) (katzj)
- Handle .utf8 vs .UTF-8 (#443408) (katzj)
- Avoid dividing by zero (#439160) (katzj)
- Changes related to BZ #230949 (dcantrell)
- $XORGDRIVERS no longer exists (markmc)
- Bump version. (katzj)
- Write IPv6 values to /etc/sysconfig/... correctly (#433290) (dcantrell)
- Use the right base class for autopart handler. (clumens)

* Fri Apr 18 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.75-1
- Listing the directories before expiring yum caches helps (katzj)

* Fri Apr 18 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.74-1
- Don't look for .discinfo on the rescue CD (#442098). (clumens)
- Use /var/cache/yum as the cachedir since /tmp might be
  too small (#443083). (clumens)
- Revert "Don't look for a .discinfo file in rescue
  mode (jvonau, #442098)." (clumens)
- Revert "Fix figuring out that the CD has stage2 on it and should
  be mounted." (clumens)
- We've always expected devices to be strings, not unicode (#443040) (katzj)
- Resizing lvs on top of RAID fails, make the error not a traceback (katzj)
- Don't put an extra slash on the error message (jgranado)
- Kernel changed howw the uevent API works for firmware
  loading *AGAIN*. (pjones)
- Expose the log file descriptors so fwloader can avoid closing
  them (pjones)
- Minor UI tweaks to passphrase dialogs (katzj)
- Nuke preupgrade cache once we're done (#442832) (katzj)
- Support bringing up the network if needed with preupgrade (#442610) (katzj)
- Use a real GtkDialog instead of some crazy hacked up dialog (katzj)
- Fix handling of pre-existing raids for the upgrade/rescue
  case (#441770) (katzj)
- Add missing / (Doug Chapman, #442751) (katzj)

* Wed Apr 16 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.73-1
- Fix figuring out that the CD has stage2 on it and should be mounted. (clumens)
- Don't copy the stage2 image on NFS installs (#438377). (clumens)

* Tue Apr 15 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.72-1
- Don't use megabytes for the livecd size for copying. (notting)
- find moved (katzj)
- Fix up silly syntax error that crept in to this commit (katzj)
- Back to using the raw version of the docs (#442540) (katzj)
- Expire yum caches on upgrade (#374921) (katzj)
- Include KERNEL== in udev rules (#440568) (dwmw2)
- Don't look for a .discinfo file in rescue
  mode (jvonau, #442098). (clumens)
- Slower machines may take more than five seconds for hal
  to start (#442113) (katzj)
- Pass the full device path (notting)
- Only include the parts of grub that will work without
  crazy tricks (#429785) (katzj)

* Thu Apr 10 2008 Peter Jones <pjones@redhat.com> - 11.4.0.71-1
- Fix destdir handling in upd-kernel (markmc)
- Get rid of module ball remnants in mk-images (markmc)
- Make upd-kernel handle version numbers the way we do them now (markmc)
- Fix ia64 kernel path problems (katzj, #441846)
- Don't tag more than one partRequest with mountpoint=/boot/efi (pjones)
- Don't treat tiny disks as EFI System Partitions during autopart (pjones)

* Thu Apr 10 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.70-1
- ide-cd_mod, not ide-cd_rom (thanks to jwb) (katzj)

* Wed Apr 09 2008 Peter Jones <pjones@redhat.com> - 11.4.0.69-1
- Ignore some warnings copying into /etc and /var (clumens)
- Try to mount the NFS source in the loader to verify it is correct (clumens)
- Be as clean as possible when looking for files/directories (jgranado, #431392)
- More ia64 kernel finding fixage (katzj, #441708)
- Fix read permissions on efidisk.img (pjones)
- Use the mount flags passed to isys.mount() (pjones)

* Wed Apr 09 2008 Peter Jones <pjones@redhat.com> - 11.4.0.68-2
- Fix device-mapper dep.

* Tue Apr 08 2008 Peter Jones <pjones@redhat.com> - 11.4.0.68-1
- Handle EFI partitions somewhat better (pjones)
- Fix typo in mk-images.efi's parted usage (pjones)

* Tue Apr 08 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.67-1
- Set the initial state of the auto-encrypt checkbutton (#441018) (katzj)
- Don't treat RAID devices as "disks" to avoid lots of odd
  behavior (#438358) (katzj)
- Log a message if we disable selinux on upgrade (katzj)
- Build efiboot.img on x86_64 and i386 . (pjones)
- When splitting srpms, only link srpms, nothing else. (jkeating)
- Don't cause the text to flicker between installed packages. (clumens)
- Don't cause the screen to jump up and down between
  packages (#441160). (clumens)
- Fix zooming and centering in the timezone screen (#439832). (clumens)
- Handle ia64 kernel path (katzj)
- And add nas to the list (#439255) (katzj)
- Set parent so that the dialog centers (#441361) (katzj)
- Don't show the label column (#441352) (katzj)
- Do string substitution after we've translated (#441053) (katzj)
- Set domain on glade file so translations show up (#441053) (katzj)
- fix compression of modules (notting)
- More build fixing due to translation breakage. (katzj)
- Add code to create efiboot.img on i386 and x86_64 (pjones)
- Remove gnome-panel too, it's no longer multilib. (jkeating)
- Fix raising new NoSuchGroup exception. (clumens)
- remove debugging print (notting)
- Support encrypted RAID member devices. (#429600) (dlehman)
- No longer require Amiga partitions on Pegasos (dwmw2)
- Don't copy the stage2 image every time or on the way back. (clumens)
- Make lukscb.get_data("encrypt") always return a valid value. (pjones)
- Set the scrollbar color so it doesn't surprise me the same way in
  the future. (pjones)
- Translation updates.

* Sun Apr 06 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.66-1
- Another day, another broken translation commit to fix. (katzj)
- Work around GL crashes in anaconda X by disabling them. (jkeating)
- Clean up "finishing upgrade" wait window (katzj)
- Stop refreshing like mad in text-mode on WaitWindow.refresh() (katzj)
- Avoid progress bars going off the end and making newt unhappy (katzj)
- Brute force hack to avoid the number of packages
  overflowing (#436588) (katzj)
- Revert "Change the default level in /etc/sysconfig/init now
  (#440058)." (notting)
- Add gnome-applets to the upgrade blacklist, fix kmymoney2 typo. (jkeating)
- Don't enable encryption by default (katzj)
- Print our mount commands to /dev/tty5 for easier debugging. (clumens)
- Change the default level in /etc/sysconfig/init now (#440058). (clumens)
- Make the Back button work when asking for tcp/ip information in
  loader.c. (#233655) (jgranado)
- Have <F12> work in the network configuration stage (#250982) (jgranado)
- Use a better test to see if a package group doesn't exist (#439922). (clumens)
- avoid behavior in (#208970) (jgranado)
- Correctly label the xen images in the .treeinfo file (jgranado)
- Translation updates

* Wed Apr 02 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.65-1
- Only do verbose hal logging if loglevel=debug (katzj)
- Avoid AttributeError in HardDriveDict (#432362) (pjones)
- Don't use %%n with gettext to avoid segfaults (#439861) (katzj)
- Require live installs to be to an ext2 or ext3 filesystem (#397871) (katzj)
- Don't allow migrations to ext4 for now (katzj)
- Change ext4 parameter to ext4, not iamanext4developer (katzj)
- Bootable requests can not be on logical volumes (#439270). (clumens)
- Don't allow /boot to be migrated to ext4 (#439944) (katzj)
- Fix for ia64 (#439876) (katzj)
- Update pkgorder group listings to match current Fedora defaults. (jkeating)
- Lame attempt to try to avoid race condition with udev creating device
  nodes (katzj)
- Don't traceback if stdout is an fd either (katzj)
- iutil doesn't need isys anymore (katzj)
- Free memory only after we're done using it (#439642). (clumens)
- Fix a segfault freeing memory on boot.iso+hdiso installs. (clumens)

* Mon Mar 31 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.64-1
- Fix my tyop (katzj)
- Fuzzy broken string again (katzj)

* Sun Mar 30 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.63-1
- Fix broken translations.  Again. (katzj)

* Sun Mar 30 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.62-1
- Translation updates
- Allow GPT disk labels on ppc/ppc64. (dcantrell)
- Tear down the right loopback device before going to stage2. (clumens)
- Don't pass None as stdout or stderr. (clumens)
- Make sure there's a stdout to write to. (clumens)
- Handle fstype munging in isys.readFSType instead of in various
  other places. (dlehman)
- Fix a typo in new encrypted LV code. (dlehman)
- Partitioning UI for handling of preexisting encrypted devices. (dlehman)
- Support discovery of preexisting rootfs on LV. (dlehman)
- Improve handling of logical volume device names when encrypted. (dlehman)
- Add support for discovery of preexisting LUKS encrypted devices. (dlehman)
- Add support for retrieving LUKS UUIDs. (dlehman)
- Refresh po files (katzj)
- Mark for translation based on feedback from translators (katzj)
- Just relabel all of /etc/sysconfig (#439315) (katzj)
- When dhcp is selected ensure that bootproto is set to
  dhcp (RPL-2301) (elliot)
- Fix for test mode repo bits (katzj)
- Try to make the size flow a little more for weird resolution
  screens (#439297) (katzj)
- Add kmymoney to upgrade remove list (#439255) (katzj)

* Thu Mar 27 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.61-1
- Fix broken translation. (clumens)

* Thu Mar 27 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.60-1
- Have a fallback empty description for devices (#432362) (katzj)
- os.path.join does not work the way we think it should. (clumens)
- Remove the stage2 in all cases now that we're copying it basically
  all the time (katzj)
- Add support for saving the exception to a local directory for live
  installs (katzj)
- Catch errors on resize and present a dialog to the user (katzj)
- Save resize output to a file (/tmp/resize.out) so that it's more
  useful (katzj)
- Make sure we give the command that's run on stdout so that it's
  logged (katzj)
- more mouse-related removals (notting)
- Fix up autopart resizing for the multiple partitions to resize case (katzj)
- Fix up the case where both method= and stage2= are given (katzj)
- Remove mouse screens that haven't been used in 4 years (katzj)

* Wed Mar 26 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.59-1
- Only remove duplicate slashes from the front of the prefix. (clumens)
- Ensure that we take into account new repos (katzj)
- Handle kernel variants a little better at install time too (katzj)
- Make a little bit more future proof for kernel version changing (katzj)
- Add confirmation of closing the installer window (#437772) (katzj)
- Fix SIGSEGV on all mounts without options (katzj)
- Add support for encrypted logical volumes in kickstart. (clumens)
- Add support for encrypted LVs. (dlehman)
- Put in some handling for redundant method calls and devices containing '/'.
  (dlehman)

* Tue Mar 25 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.58-1
- Fuzzy broken string (katzj)

* Tue Mar 25 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.57-1
- Use anaconda-upgrade dir in the preupgrade case (katzj)
- Have 'preupgrade' key doing an upgrade (katzj)
- Fix what we expect to be the message from ntfsprogs (katzj)
- Fix up compile error for new newt (katzj)
- Don't traceback if we have little freespace partitions (#438696) (katzj)
- Translation updates (ko, ru)

* Mon Mar 24 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.56-1
- Translation updates (hi, fr, kn, de, ml, es, mr, ko, te)
- Fix up more unicode shenanigans (#437993) (katzj)
- Move /tmp/stage2.img to /mnt/sysimage to free up some
  memory (#438377). (clumens)
- Be a little smarter about downloading repo metadata (#437972). (clumens)
- Make sure that devices are set up before using them. (#437858) (dlehman)
- Don't prepend /dev/ on bind mounts either. (clumens)
- Use the repo name instead of id in the group file error
  message (#437972). (clumens)
- Handle /dev being on hard drive devices in the second stage (katzj)
- Fix the build (katzj)
- The units for /sys/block/foo/size aren't bytes.  Fixes finding some
  disks (katzj)
- Remove the check for .discinfo on URL installs. (clumens)
- Always unmount /mnt/source on hdiso installs before starting
  stage2. (clumens)
- Always unmount /mnt/source on nfsiso installs before starting
  stage2. (clumens)
- Make sure the first disc image is mounted before setting up repos. (clumens)
- Fix $UPDATES for real (katzj)
- Avoid piling up slashes in the UI when retrying (#437516). (clumens)
- Require comps-extras now that we don't require pirut bringing it in (notting)
- Put "ide-cd_mod" in the list of modules to pull in. (pjones)

* Tue Mar 18 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.55-1
- Fix format of method=hd: parameter (#438075). (clumens)
- Work on support for NFSISO installs when using boot.iso. (clumens)
- If a file doesn't exist, don't continue trying to loopback mount
  it. (clumens)
- Make loopback mount error messages more useful. (clumens)
- Focus root password entry box (#436885). (dcantrell)
- Fix a traceback writing out the method string for hdiso installs. (clumens)
- Fix use of sizeof on a malloc()'d char ** (pjones)
- Fix up ppc boot check (#438005) (katzj)
- Support reading the UUID from the disk like we do with labels. (clumens)
- If the protected partition is not yet mounted, mount it now. (clumens)
- Don't add /dev/ to LABEL= or UUID= devices either. (clumens)
- Use arch instead of the name again in package nevra. (clumens)
- Fix traceback with preexisting LUKS partitions in setFromDisk.
  (part of #437858) (dlehman)

* Mon Mar 17 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.54-1
- Translation updates (de, fi, it, gu, ta, pa)
- Fix a typo. (clumens)
- Fix the build. (clumens)
- Make sure we return the same kind of exception in all cases. (clumens)
- Filter so we don't show LVM and RAID components when adding
  boot entry (#437501) (katzj)
- Only print the filename we're fetching, as newt doesn't like
  long names. (clumens)
- Fix off by one error reading .buildstamp (pjones)
- Use the right path when trying to fetch .discinfo. (clumens)
- Don't prepend /dev/ onto nfs devices.  Also log mount
  errors to tty5. (pjones)

* Sun Mar 16 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.53-1
- Update translations (pl, de)
- Use i586 kernel (#437641) (katzj)
- Give indication of success or failure for mediacheck (#437577) (katzj)
- Ensure the UUID for the rootfs is random and not the same for every
  live image (katzj)
- Make migration from ext3 -> ext4 saner on upgrade (#437567) (katzj)
- Force filesystem mount options on /boot/efi . (pjones)
- On HDISO installs, look for the stage2.img file in the right
  directory. (clumens)
- Accept devices with or without a leading /dev/. (clumens)
- .buildstamp no longer contains productPath, so change
  the default (#437509). (clumens)
- Remove references to an uninitialized variable. (clumens)
- Use shortname=winnt instead of shortname=win95 when
  mounting /boot/efi (pjones)
- Do not strip leading or trailing whiltespace from
  passphrases. (#437499) (dlehman)
- Set methodstr for nfsiso installs (#437541). (clumens)
- Create and check /boot/efi correctly, and use preexisting
  one if available. (pjones)
- Handle /boot/efi and /boot both as bootrequests (pjones)
- Emit "efi" as /boot/efi's filesystem type (pjones)
- Add EFI handling to the bootloader setup choices. (pjones)
- Add efi to the ignoreable filesystem list. (pjones)
- Add EFIFileSystem, and getMountName() to hide that it's really vfat. (pjones)
- Add isEfiSystemPartition(), and use it where appropriate (pjones)
- Call getAutoPartitionBoot with our partition list as an arg. (pjones)
- Don't show the epoch in package selection either (#437502). (clumens)
- Fix some errors on reporting which files are being downloaded. (clumens)
- Revert "Handle /boot and /boot/efi separately, plus fixes" (pjones)
- Handle /boot and /boot/efi separately, plus fixes (pjones)
- Get rid of unused >1024 cylindar check, fix text of boot
  check exceptions. (pjones)
- Make bootRequestCheck() check /each/ boot partition like it's
  supposed to, (pjones)
- Fix shell quoting on numbers > 9, and fix an error message. (pjones)
- Don't show the epoch in the progress bar (#437502). (clumens)
- Include efibootmgr in the instroot (pjones)

* Thu Mar 13 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.52-1
- Don't unmount NFS source so NFSISO will work. (clumens)
- Fix the format of the method=hd: parameter. (clumens)
- Fix creating new users in kickstart. (clumens)
- "gtk-edit" isn't valid in text mode. (clumens)
- Ignore LUKS headers on partitions containing RAID signatures.
  (#437051) (dlehman)
- The xconfig command with no X running doesn't make sense. (clumens)

* Wed Mar 12 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.51-1
- yum.remove removes installed packages, not to be installed
  packages (#436226) (katzj)
- Make the /tmp/updates vs RHupdates code at least a little readable. (pjones)
- Allow vfat update images. (pjones)
- Fix syntax error (pjones)
- Add a progress bar for when we're downloading headers (#186789). (clumens)
- mount will set up the loopback device if we let it. (clumens)
- Fix mounting problems with NFSISO images. (clumens)
- Simplify the logic for the upgrade arch check (katzj)
- Add a fallback method for determining the architecture of installed
  system during an upgrade (#430115) (msivak)
- Avoid a traceback (#436826) (katzj)
- Make sure host lookups work for manual net config (#435574). (dcantrell)

* Tue Mar 11 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.50-1
- Focus root password entry box (#436885). (dcantrell)
- Make sure default is SHA-512 for libuser.conf. (dcantrell)
- Fix detection of ISO images on a hard drive partition. (clumens)
- Devices names aren't prefixed with /dev/. (clumens)
- Filter out /dev/ram* devices from the list of hdiso partitions. (clumens)
- But make sure that we've activated the keymap now that X
  follows its defaults (katzj)
- Don't set a keyboard in the X config, we should just do this
  at runtime (katzj)
- Writing out the nfs method line is a lot simpler now. (clumens)
- Use /mnt/sysimage/tmp/cache for the yum cache, instead of the
  ramdisk. (clumens)
- Translation updates (nl, gu, ml, mr, pa)

* Mon Mar 10 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.49-1
- Use the full path to the .discinfo file (#436855). (clumens)
- List netinst.iso/boot.iso in .treeinfo (#436089) (katzj)
- Convinced to change the name back to boot.iso (katzj)
- Only pass the file path to {ftp,http}GetFileDesc. (clumens)
- Pass the correct NFS method parameter to stage2 (#436360). (clumens)
- Fix logging messages to not display the hostname twice. (clumens)
- Fix traceback with text mode adding iscsi (#436480) (katzj)

* Thu Mar 06 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.48-1
- Don't use the bits from $UPDATES unless $UPDATES exists (katzj)
- Fix horkage with busybox stuff.  There's now start-stop-daemon (katzj)
- Require new enough version of yum-utils (katzj)
- Pass the --archlist option to yumdownloader (jkeating)
- Update pt_BR translation

* Wed Mar 05 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.47-1
- Fix the build again (katzj)

* Wed Mar 05 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.46-1
- Don't require some things which we fall back gracefully when not there (katzj)
- Check for filesystem utilities to see if a filesystem is supported (katzj)
- Write out keyboard settings before installing packages. (related
  to #429358) (dlehman)
- Update pl translation
- Make sure http:// or ftp:// is specified (#436089) (katzj)
- Fix segfault when port is specified (#435219) (katzj)
- Use ntfsresize -m to get minimum size (#431124) (katzj)
- Use the right path to the .discinfo file when validating a tree. (clumens)

* Tue Mar 04 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.45-1
- Fix the build.

* Tue Mar 04 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.44-1
- Add --archlist to repoquery call. (jkeating)
- Translation updates (pl, nl, ja)
- Handle efibootmgr and grub.efi in upd-instroot. (pjones)
- Merge in branch to implement stage2= parameter. (clumens)
- Revert the memtest86 bits for EFI, since this gets run on
  multiple arches. (pjones)
- Use iutil.isEfi() instead of testing for ia64-ness. (pjones)
- Only do gptsync if we're not using EFI. (pjones)
- Don't do gptsync if we're using EFI. (pjones)
- Use gpt on all efi platforms. (pjones)
- Rework isEfi() to be slightly more conservative. (pjones)
- Test for using efi rather than arch==ia64 (pjones)
- Don't copy memtest86 in on EFI since it won't work. (pjones)
- Add comment regarding usage of elilo (pjones)
- Free some variables so we can http GET twice if needed. (clumens)
- Change the method config prompts. (clumens)
- Support stage2= for CD installs in loader. (clumens)
- Support stage2= for HD installs. (clumens)
- Support stage2= for NFS installs. (clumens)
- Support stage2= for URL installs. (clumens)
- Update the method string handling for NFS and URL installs. (clumens)
- mountStage2 now needs to take an extra argument for updates. (clumens)
- If stage2= is given, it overrides the check for a CD stage2 image. (clumens)
- Support the stage2= parameter, and add a flag for it. (clumens)

* Mon Mar 03 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.43-1
- Only use UUID= for devices we would have labeled.  Related to #435228 (katzj)
- If we don't find a kernel package, then give a better error (katzj)
- Translation updates (cs, de)

* Sun Mar 02 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.42-1
- Fix a traceback when we have an error.  Related to #433658 (katzj)
- Add virtio_pci in hopes of getting virtio working (katzj)
- Pull in the bits of pirut that we use so that we don't depend on pirut (katzj)
- Default to RAID1 instead of RAID0 (#435579) (katzj)
- Refresh po (katzj)
- Fix traceback leaving task selection screen (#435556) (katzj)
- More ext4 vs ext4dev nonsense.  (#435517) (katzj)
- Fix reverse name lookup. (pjones)

* Thu Feb 28 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.41-1
- Don't write out /etc/rpm/platform anymore. (katzj)
- anaconda-runtime now needs yum-utils (katzj)
- Add 'testiso' target (katzj)
- Remove rescue cd creation scripts (katzj)
- Take --updates with location of additional updates beyond the package
  set used (katzj)
- Change the ISOs we build (katzj)
- Take advantage of yum repos being available (katzj)
- Allow recovery from some missing repodata conditions. (clumens)
- Rework the repo editor screen to be more modular. (clumens)
- Move doPostImages to be run after the second stage build (katzj)
- Ensure that group info for txmbrs is accurate after we reset (katzj)
- Fix backwards logic for yum verbosity (katzj)
- No more arc (#435175) (katzj)
- Remove an unused method. (clumens)

* Tue Feb 26 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.40-1
- Use non-deprecated HAL properties. (notting)
- More crud to deal with the fact that rawhide trees are composed weird (katzj)
- Gtk does not have the error type, use custom with proper
  icons. (#224636) (msivak)

* Mon Feb 25 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.39-1
- Fix up symlinks that could be broken with our movement here (#434882) (wwoods)
- pvops xen uses hvc as its console (#434763) (katzj)
- Follow symlinks when looking for the anaconda-runtime package. (jkeating)

* Sun Feb 24 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.38-1
- Write out UUID in the fstab (#364441) (katzj)
- Add support for getting UUID using libblkid (katzj)
- Fix calculation of sizes of LVs when resizing (#433024) (katzj)
- Add back some bits for text mode (katzj)
- Remove advanced bootloader bits (katzj)
- Add support for actually changing where the boot loader gets
  installed as well (katzj)
- Less text. (katzj)
- Reorder things a little, clean up spacing (katzj)
- Use a tooltip instead of a long bit of text that most people
  don't read (katzj)
- Remove advanced checkbox (katzj)
- Switch the grub installation radio to be a checkbutton.  Cleanups for
  grub only (katzj)
- Lets redirect to /dev/null to ensure that what we get in DIR is the
  result of pwd. (jgranado)
- Catch the error emmited by lvm tools during logical volume
  creation process (#224636). (msivak)
- Don't try to lock /etc/mtab, fix error detection when mount fails. (clumens)
- Don't append (null) to the NFS mount options. (clumens)
- There's no need to wait if the last download retry failed. (clumens)
- the '-o' is appended to the mount command in imount.c (jgranado)
- Use full path to device for mount in findExistingRootPartitions. (dlehman)
- Map preexisting encrypted devs before mounting everything
  in mountRootPartition. (dlehman)
- Fix traceback on test mount in findExistingRootPartitions. (dlehman)
- Use SHA-512 by default for password encryption. (dcantrell)
- Clean up root password user interfaces. (dcantrell)

* Tue Feb 19 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.37-1
- Default to the right timezone when language is changed (#432158). (clumens)
- Fix another text mode network config traceback (#433475). (clumens)
- More scripts cleanups. (jgranado)
- Remove more references to ARC (#433229). (clumens)
- Mount flags should be an optional argument (#433279, #433280). (clumens)
- We don't need productpath anymore, so stop taking it as an option (katzj)
- Set yum output level based on whether or not we've passed --debug or
  not (katzj)
- Clean up invocation of mk-images from buildinstall (katzj)
- Clean up invocation of upd-instroot from buildinstall (katzj)
- Remove some legacy stuff that's no longer relevant from
  .discinfo/.treeinfo (katzj)
- Don't depend on product path for finding the anaconda-runtime
  package (katzj)
- Make buildinstall a little clearer (katzj)
- Use $LIBDIR instead of lib globbing to avoid problems with chroots (katzj)
- Add some error handling around populateTs. (clumens)

* Thu Feb 14 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.36-1
- Fix up firmware inclusion.  This didn't actually ever work. (katzj)
- Fix up the groff related stuff for man pages to be done in the correct
  place (katzj)
- remove yumcache (katzj)
- Don't do fixmtimes anymore (katzj)
- Don't compress translations (katzj)
- Don't manually duplicate things from package %%post scripts (katzj)
- Remove some unused options (--discs and --buildinstdir) (katzj)
- Keep /etc/nsswitch.conf and /etc/shells (katzj)
- Stop forcing passive mode for FTP by patching urllib (katzj)
- We don't use timezones.gz anymore anywhere (katzj)
- We shouldn't need to remove files that are only in -devel packages (katzj)
- Remove some obsolete files from the list to clean up noise in the
  output (katzj)
- We want nss bits on all arches these days (katzj)
- Just use default /etc/nsswitch.conf and /etc/shells (katzj)
- alpha should have translations probably (katzj)
- Remove some things that aren't used anymore (katzj)
- Don't run pkgorder as a part of buildinstall anymore (katzj)
- Remove duplicate file from the file lists (katzj)
- Don't use the static versions of these anymore as they're likely to go
  away (katzj)
- Remove weird s390 hack that shouldn't be needed any more (katzj)
- Make makebootfat less noisy (katzj)
- Get rid of dangling fobpath stuff; now that we're not mounting to
  create (katzj)
- Ignore .bak files created by glade (katzj)
- Get rid of duplication for yaboot stuff to make scripts less noisy (katzj)
- Correct internationalization of exception handler text (msw)
- More fixing of mount paths (#432720) (katzj)
- securitylevel -> firewall in the spec file. (clumens)
- Include util-linux-ng, which contains mount (#432720). (clumens)
- When mounting stage2 on loopback, add -o loop to mount opts. (clumens)

* Tue Feb 12 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.35-1
- Fix the build (katzj)

* Tue Feb 12 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.34-1
- Handle modules with more than one description (#432414) (katzj)
- Finish HDISO installs, at least for DVDs (#431132). (clumens)
- Move migration to before mounting filesystems (katzj)
- Fix silly thinko in Eric's patch (katzj)
- Allow ext3->ext4 upgrades (sandeen)
- Do the man pages in rescue mode the right way. (jgranado)
- Merge branch 'master' of ssh://git.fedorahosted.org/git/anaconda (notting)
- Use /etc/adjtime as the configuration file for UTC/not-UTC. (notting)
- Remove all our own mount code. (clumens)
- Use the mount program instead of our own code. (clumens)
- Add the real mount programs to stage1. (clumens)
- Use the correct variables to get the ipv6 info. (#432035) (jgranado)
- Update error messages to match function names. (dcantrell)
- Rename nl.c to iface.c and functions to iface_* (dcantrell)
- In rescue mode, show interface configuration (#429953) (dcantrell)
- Add qla2xxx firmware (#377921) (katzj)
- Rename base repo (#430806). (clumens)
- Remove dep on anaconda from pkgorder (katzj)
- Remove no longer used dumphdrlist script (katzj)

* Thu Feb 07 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.33-1
- Fix error message on continuing after changing cds with mediacheck (katzj)
- Fix the progress bar during mediacheck (#431138) (katzj)
- Ensure we disable SELinux if the live image isn't using it (#417601) (katzj)
- Correct nl_ip2str() cache iteration. (dcantrell)
- Check the fstype of the live image (katzj)
- Check for device existence rather than starting with /dev (katzj)
- The FL_TEXT flag has no reason to be here. (#207657) (jgranado)
- Don't traceback when getLabels is called with DiskSet.anaconda set
  to None. (dlehman)
- Pass arguments correctly to anaconda (katzj)
- Cancel on escape being pressed with autopart resizing (katzj)

* Wed Feb 06 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.32-1
- Make passwordEntry appear on the exn saving screen. (clumens)
- Don't allow disabling default repositories. (clumens)
- Make loopback device purposes line up with what stage2 expects. (clumens)
- Fix methodstr handling for hdiso installs (#431132). (clumens)
- Remove our own DNS functions, since glibc's are available now. (clumens)

* Tue Feb 05 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.31-1
- Copy over repodata from media after the install is done (#381721) (katzj)
- Add resizing support in autopartitioning (katzj)
- Fix test mode with python-fedora installed (katzj)
- Add support for encrypted devices in rescue mode (dlehman).
- Allow creation of LUKSDevice with no passphrase. (dlehman)
- Fix hdiso installs in loader and in methodstr (#431132). (clumens)
- Avoid infinite loop in nl_ip2str(). (dcantrell)
- Force users to set a hostname (#408921) (dcantrell)
- Forward-port RHEL-5 fixes for s390x issues. (dcantrell)
- fsset.py tweaks for ext4dev & xfs (sandeen)
- When editing the raid partitions show raid memebers. (#352721) (jgranado)
- mdadm to create the mdadm.conf (#395881) (jgranado)

* Wed Jan 30 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.30-1
- Initialize int in doConfigNetDevice() to fix compiler warnings. (dcantrell)

* Wed Jan 30 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.29-1
- Handle putting updates ahead of anaconda in the updates= case too. (clumens)
- Make sure the device name starts with /dev (#430811). (clumens)
- Revert "Initial support for network --bootproto=ask (#401531)." (clumens)
- (#186439)  handle lv names with "-" when doing kickstart. (jgranado)
- Remove the last references to makeDevInode (#430784). (clumens)
- Don't traceback trying to raise an exception when making
  users (#430772). (clumens)

* Mon Jan 28 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.28-1
- Go back to the method screen if back is hit on nfs config (#430477). (clumens)
- Fix dmidecode dependency (#430394, Josh Boyer <jwboyer)

* Fri Jan 25 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.27-1
- Fix generation of stage1 images. (notting)
- Fix a typo in mk-images. (clumens)
- Allow removing packages by glob now that yum supports it. (clumens)

* Thu Jan 24 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.26-1
- Fix a traceback on the driver selection screen (#428810). (clumens)
- Map 'nousb', 'nofirewire', etc. to be proper module blacklists. (notting)
- Clean off leading and trailing whitespace from descriptions. (notting)
- Write out /etc/rpm/platform on livecd installs. (clumens)

* Wed Jan 23 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.25-1
- Include new firstboot module. (clumens)
- Conditionalize ntfsprogs as not all arches include it. (clumens)
- Remove kudzu-probe-stub. (clumens)
- Remove rogue references to kudzu. (clumens)
- Add dogtail support (#172891, #239024). (clumens)
- Fix some error reporting tracebacks. (clumens)

* Tue Jan 22 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.24-1
- Avoid possible SIGSEGV from empty loaderData values. (dcantrell)
- Do not require glib2-devel for building. (dcantrell)
- Use libnl to get interface MAC and IP addresses (dcantrell)
- Don't refer to the libuser.conf when creating users (#428891). (clumens)
- pcspkr works (or isn't even present), per testing on #fedora-devel (notting)
- Inline spufs loading for ppc. (notting)
- Load iscsi_tcp, so that iSCSI actually works (notting)
- inline ipv6 module loading (notting)
- If we execWith a program, require the package containing it. (clumens)
- Add a repository editor. (clumens)
- Add the default repo to the UI so it can be edited later. (clumens)
- Fix non-latin-1 locale display in the loader. (notting)
- Make sure anaconda has precedence in the search path (#331091). (clumens)
- When starting RAID arrays, the device node may not already exist. (notting)
- Fix a typo that's breaking kickstart network installs. (clumens)
- Don't allow backing up to partitioning (#429618). (clumens)
- Update font paths. (clumens)

* Mon Jan 21 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.23-1
- Try to fix a problem creating users via kickstart (#428891, clumens)
- Fix a loader segfault doing kickstart nfs installs (clumens)
- Move more interactive steps ahead of partitioning (clumens)
- If we can't possibly add advanced devices, don't offer it (#429210, clumens)
- Don't flush after rescanning so recently attached disks are
  available (clumens)
- If bootproto is dhcp, unset any static settings (#218489, dcantrell)
- Add some groups to pkgorder to make the CDs come out right (pjones)
- Fix traceback when using non-encrypted RAID (notting)
- Complete the patch for dhcptimeout (#198147, #254032, msivak)

* Wed Jan 16 2008 David L. Cantrell Jr. <dcantrell@redhat.com> - 11.4.0.22-1
- Require the latest libdhcp (dcantrell)
- Don't set currentMedia when we're on a network install (#428927, clumens)
- Don't offer two reboot options (clumens)
- Remove fsopts that are already defaults (#429039, clumens)
- Remove isofs module to get rid of a FATAL message (clumens)
- Add the crc32c kernel module for iscsi (#405911, clumens)
- Add MAC address to the network device selection screen (#428229, clumens)
- Initial support for network --bootproto=ask (#401531, clumens)
- Remove an extra newline (clumens)
- Add firstaidkit to the rescue image (jgranado)
- Fix the progress bar to hit 100%% on the last package (#428790, clumens)
- Add some output so the startup delay doesn't seem quite so long (clumens)
- Initial kickstart support for encrypted partitions (clumens)

* Mon Jan 14 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.21-1
- Inherit from the right versions of pykickstart classes (clumens)
- Update for nss files moving to /lib (clumens)
- Remove unneeded arguments from detectHardware function (notting)
- Symlink all udev support binaries to udevadm (notting)
- /sbin/restorecon on /etc/modprobe.d (notting)
- Add the kickstart syntax version to the kickstart file (clumens)
- Require latest libdhcp to fix x86_64 SIGABRT problems

* Sun Jan 13 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.20-1
- Install new udev paths so HAL can talk to it (notting)
- Also get DSO deps for setuid binaries (like X). (clumens)
- Fix a bunch of pychecker errors. (clumens)

* Fri Jan 11 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.19-1
- Make sure the arch is listedat the top of all loader screens. (clumens)
- Add the version number really early in the log file too. (clumens)
- Require latest libdhcp (dcantrell)
- Add nicdelay parameter to loader, so we can wait before sending DHCP
  requests. (msivak)
- Add dhcpdelay to loader so we can modify the default dhcp timeout
  (#198147, #254032). (msivak)
- Fix the selected device when disabling entries in Add advanced drive
  dialog. (#248447) (msivak)
- Include mkfs.gfs2 (#356661). (clumens)
- Use the new default Japanese font (#428070). (clumens)
- More urlinstall loader fixes. (clumens)

* Wed Jan 09 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.18-1
- Fix encrypted autopart traceback. (dlehman)
- Allow for better recovery if the CD/DVD is bad. (clumens)
- If downloading the updates image fails, prompt for a new location. (clumens)
- X now relies on libpciaccess, so add it to our list. (clumens)
- Erase temporary packages after installing them on all methods. (clumens)

* Mon Jan 07 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.17-1
- Make text mode root password dialog default match GUI. (clumens)
- Fix a segfault in making the URL dialog box. (clumens)

* Sun Jan 06 2008 Chris Lumens <clumens@redhat.com> - 11.4.0.16-1
- Fix checking the timestamps on split media installs. (clumens)
- Fix reference to isodir to avoid a post-install traceback. (clumens)
- Use a better test when populating the URL panel in loader. (clumens)
- Don't use error messages from dosfslabel as the label (#427457). (clumens)
- No longer require kudzu (#427680). (clumens)

* Thu Jan 03 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.15-1
- Require latest libdhcp (#378641) (dcantrell)

* Thu Jan 03 2008 David Cantrell <dcantrell@redhat.com> - 11.4.0.14-1
- Precreate /etc/modprobe.d in installroot (jkeating)
- 'import sets' in image.py (jkeating)
- Fix traceback when displaying required media (clumens)

* Tue Jan 01 2008 Jeremy Katz <katzj@redhat.com> - 11.4.0.13-1
- Make it obvious which partitions are being formatted and encrypted (katzj)
- Set initial sensitivity of encrypt button correctly (katzj)
- Fix traceback on invalid passphrase (#426887) (katzj)
- Use mkstemp() instead of tempnam() (katzj)
- Don't resize filesystems which are being formatted (#426466) (katzj)
- Add cracklib-dicts (#426444) (katzj)
- Fix build (notting)
