# This file is encoded in UTF-8.  -*- coding: utf-8 -*-

%define muleucs_ver current
%define tramp_ver 2.1.3

Summary: GNU Emacs text editor
Name: emacs
Version: 21.4
Release: 1
License: GPL
URL: http://www.gnu.org/software/emacs/
Group: Applications/Editors
Source0: ftp://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/emacs/leim-%{version}.tar.gz
Source3: emacs.desktop
Source4: emacs.png
Source5: dotemacs.el
Source6: site-start.el
Source7: http://www.python.org/emacs/python-mode/python-mode.el
Source8: http://cvs.xemacs.org/viewcvs.cgi/XEmacs/packages/xemacs-packages/prog-modes/rpm-spec-mode.el
Source10: ftp://ftp.gnu.org/gnu/emacs/elisp-manual-21-2.8.tar.bz2
Source11: http://prdownloads.sourceforge.net/php-mode/php-mode-1.1.0.tgz
Source12: php-mode-init.el
Source13: ssl.el
Source16: python-mode-init.el
Source17: rpm-spec-mode-init.el
Source18: rpm-spec-mode.el-0.14-xemacs-compat.patch
Source20: po-mode.el
Source21: po-compat.el
Source22: po-mode-init.el
Source23: po-mode-auto-replace-date-71264.patch
Source24: ftp://ftp.m17n.org/pub/mule/Mule-UCS/test/Mule-UCS-%{muleucs_ver}.tar.gz
Source25: lang-coding-systems-init.el
Source26: default.el
Source27: rfc1345.el
Source28: http://ftp.gnu.org/gnu/tramp/tramp-%{tramp_ver}.tar.gz
Source29: tramp-init.el
Source30: wrapper
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: glibc-devel, gcc, bzip2, ncurses-devel, zlib-devel, autoconf213
Buildrequires: xorg-x11-devel, Xaw3d-devel, libpng-devel, libjpeg-devel, libungif-devel, libtiff-devel
Requires: fonts-xorg-75dpi
%ifarch %{ix86}
BuildRequires: setarch
%endif
Requires: emacs-common = %{version}-%{release}
Obsoletes: emacs-X11
Conflicts: gettext < 0.10.40

# Non-lisp patches
Patch2: emacs-21.2-s390.patch
Patch3: emacs-21.2-x86_64.patch
Patch4: emacs-21.2-sticky-bit-80049.patch
Patch5: emacs-21.2-s390x.patch
Patch7: emacs-21.2-alloc-blockinput-83600.patch
Patch9: emacs-21.3-ppc64.patch
Patch10: editfns.c-Fformat-multibyte-davej.patch
Patch11: emacs-21.3-no-rpath.patch
Patch14: emacs-xim-status-under-window-125413.patch
Patch15: emacs-21.3-xterm-modifiers-137868.patch
Patch17: emacs-21.3-gcc4.patch
Patch19: emacs-21.4-21.4a-diff.patch
Patch20: bzero-and-have-stdlib.dpatch
Patch21: coding-region-leak.dpatch
Patch22: detect-coding-iso2022.dpatch
Patch23: fix-batch-mode-signal-handling.dpatch
Patch24: fix-x-vs-no-x-diffs.dpatch
Patch25: scroll-margin.dpatch
Patch26: xfree86-4.3-modifiers.dpatch

# Lisp patches
Patch106: emacs-21.2-menubar-games.patch
Patch108: browse-url-htmlview-84262.patch
Patch112: emacs-21.3-lisp-textmodes-ispell-languages.patch
Patch113: emacs-21.3-gud-libtool-fix.patch
Patch118: emacs-21.3-latex-mode-hook-144083.patch
Patch119: battery-acpi-support.dpatch
Patch120: pcl-cvs-format.dpatch
Patch121: python-completion-ignored-extensions.dpatch
Patch122: save-buffer.dpatch

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with support for X windows.

%package nox
Summary: GNU Emacs text editor without X support
Group: Applications/Editors
Requires: emacs-common = %{version}-%{release}

%description nox
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with no X windows support for running
on a terminal.

%package common
Summary: Emacs common files
Group: Applications/Editors
PreReq: /sbin/install-info, dev, %{_sbindir}/alternatives

%description common
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package contains all the common files needed by emacs or emacs-nox.

%package el
Summary: Emacs Lisp source files included with Emacs.
Group: Applications/Editors

%description el
Emacs-el contains the emacs-elisp sources for many of the elisp
programs included with the main Emacs text editor package.

You need to install emacs-el only if you intend to modify any of the
Emacs packages or see some elisp examples.

%package leim
Summary: Emacs Lisp files for input methods for international characters.
Group: Applications/Editors

%description leim
The emacs-leim package contains Emacs Lisp code for input methods for
various international character scripts. Basically, the Lisp code
provided by this package describes the consecutive keystrokes that a
user must press in order to input a particular character in a
non-English character set. Input methods for many different character
sets are included in this package.

%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}

%prep
%setup -q -b 1 -a 24 -a 28

%patch2 -p1 -b .2-s390
%patch3 -p1 -b .3-hammer
%patch4 -p1 -b .4-sticky
%patch5 -p1 -b .5-s390x
# block input in `allocate_vectorlike' (alloc.c)
%patch7 -p1 -b .7-block
%patch9 -p1 -b .9-ppc64
%patch10 -p1 -b .10-multibyte
%patch11 -p1 -b .11-rpath
%patch14 -p1 -b .14-StatusArea
%patch15 -p0 -b .15-modifier
%patch17 -p1 -b .17-getcwd
%patch19 -p1 -b .19-fedora
%patch20 -p1 -b .20-bzero
%patch21 -p1 -b .21-leak
%patch22 -p1 -b .22-iso2022
%patch23 -p1 -b .23-batch
%patch24 -p1 -b .24-x-nox
%patch25 -p1 -b .25-scroll-margin
%patch26 -p1 -b .26-xmodifier

# patches 2 and 3 touch configure.in
autoconf-2.13

## Lisp patches
# remove game we can't ship
%patch106 -p1
rm lisp/finder-inf.el lisp/play/tetris.el*
# make browse-url default to htmlview not netscape
%patch108 -p1
# fix names of aspell language dictionaries
%patch112 -p1
# fix running gdb with libtool
%patch113 -p1
# run latex-mode-hook
%patch118 -p1
# battery acpi
%patch119 -p1
# pcl-cvs format
%patch120 -p1
# .pyc completion
%patch121 -p1
# save-buffer
%patch122 -p1

# install rest of site-lisp files
( cd site-lisp
  cp %SOURCE7 %SOURCE8 %SOURCE13 %SOURCE20 %SOURCE21 .
  # xemacs compat patch for rpm-spec-mode
  patch < %SOURCE18
  # fix po-auto-replace-revision-date nil
  patch < %SOURCE23
  tar zxvf %SOURCE11
)

# add rfc1345 input method (default for UTF-8 lang env)
cp -pi %SOURCE27 leim/quail

%build
export CFLAGS="-DMAIL_USE_LOCKF $RPM_OPT_FLAGS"
%configure --with-pop --with-sound

# workaround #101818 (vm/break dumper problem)
%ifarch %{ix86}
%define __make setarch i386 make
%endif

%__make %{?_smp_mflags}

# remove versioned file so that we end up with .1 suffix and only one DOC file
rm src/emacs-%{version}.*

TOPDIR=${PWD}
%define emacsbatch ${TOPDIR}/src/emacs -batch --no-init-file --no-site-file

# make sure patched lisp files get byte-compiled
%emacsbatch -f batch-byte-recompile-directory lisp
%emacsbatch -f batch-byte-compile leim/quail/rfc1345.el site-lisp/*.el

%__make %{?_smp_mflags} -C lisp updates

( cd Mule-UCS-%{muleucs_ver}
  %{emacsbatch} -l mucs-comp.el )

( cd tramp-%{tramp_ver}
  ./configure --with-emacs=${TOPDIR}/src/emacs
  make )

%install
rm -rf $RPM_BUILD_ROOT

# workaround #101818 (vm/break dumper problem)
%ifarch %{ix86}
%define makeinstall %{__make} prefix=%{?buildroot:%{buildroot}}%{_prefix} exec_prefix=%{?buildroot:%{buildroot}}%{_exec_prefix} bindir=%{?buildroot:%{buildroot}}%{_bindir} sbindir=%{?buildroot:%{buildroot}}%{_sbindir} sysconfdir=%{?buildroot:%{buildroot}}%{_sysconfdir} datadir=%{?buildroot:%{buildroot}}%{_datadir} includedir=%{?buildroot:%{buildroot}}%{_includedir} libdir=%{?buildroot:%{buildroot}}%{_libdir} libexecdir=%{?buildroot:%{buildroot}}%{_libexecdir} localstatedir=%{?buildroot:%{buildroot}}%{_localstatedir} sharedstatedir=%{?buildroot:%{buildroot}}%{_sharedstatedir} mandir=%{?buildroot:%{buildroot}}%{_mandir} infodir=%{?buildroot:%{buildroot}}%{_infodir} install
%endif

%makeinstall
# suffix binaries with -x
mv $RPM_BUILD_ROOT%{_bindir}/emacs{,-x}
mv $RPM_BUILD_ROOT%{_bindir}/emacs-%{version}{,-x}
mv $RPM_BUILD_ROOT%{emacs_libexecdir}/fns-%{version}.1{,-x}.el

# rebuild without X support
# remove the versioned binary with X support so that we end up with .1 suffix for emacs-nox too
rm src/emacs-%{version}.*
%configure --without-x
%__make %{?_smp_mflags}

# install the emacs without X
install -m 0755 src/emacs-%{version}.1 $RPM_BUILD_ROOT%{_bindir}/emacs-%{version}-nox
ln $RPM_BUILD_ROOT%{_bindir}/emacs{-%{version},}-nox
install -m 0644 lib-src/fns-%{version}.1.el $RPM_BUILD_ROOT%{emacs_libexecdir}/fns-%{version}.1-nox.el

# install wrapper script
install -m 0755 %SOURCE30 $RPM_BUILD_ROOT%{_bindir}/emacs-%{version}
ln -s %{_bindir}/emacs-%{version} $RPM_BUILD_ROOT%{_bindir}/emacs

# make sure movemail isn't setgid
chmod 755 $RPM_BUILD_ROOT%{emacs_libexecdir}/movemail

%define site_lisp $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

mkdir -p %{site_lisp}
install -m 0644 %SOURCE6 %{site_lisp}/site-start.el
install -m 0644 %SOURCE26 %{site_lisp}

mv $RPM_BUILD_ROOT%{_bindir}/{etags,etags.emacs}
mv $RPM_BUILD_ROOT%{_mandir}/man1/{ctags.1,gctags.1}
mv $RPM_BUILD_ROOT%{_bindir}/{ctags,gctags}

# GNOME / KDE files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m 0644 %SOURCE3 $RPM_BUILD_ROOT%{_datadir}/applications/gnu-emacs.desktop
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 0644 %SOURCE4 $RPM_BUILD_ROOT%{_datadir}/pixmaps/

# install site-lisp files
install -m 0644 site-lisp/*.el{,c} %{site_lisp}

mkdir -p %{site_lisp}/site-start.d
install -m 0644 $RPM_SOURCE_DIR/*-init.el %{site_lisp}/site-start.d

# default initialization file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 0644 %SOURCE5 $RPM_BUILD_ROOT%{_sysconfdir}/skel/.emacs

( cd Mule-UCS-%{muleucs_ver}/lisp
  mkdir %{site_lisp}/Mule-UCS
  cp -p *.el *.elc %{site_lisp}/Mule-UCS )

( cd tramp-%{tramp_ver}
  %makeinstall lispdir=%{site_lisp}/tramp )

# elisp reference manual
tar jxf %{SOURCE10}
( cd elisp-manual-21-2.8
  install -m 644 elisp elisp-* $RPM_BUILD_ROOT%{_infodir} )

# after everything is installed, remove info dir
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

#
# create file lists
#
rm -f *-filelist {common,el,leim}-*-files
( TOPDIR=${PWD}
  cd $RPM_BUILD_ROOT

  find .%{_datadir}/emacs/%{version}/lisp .%{_datadir}/emacs/site-lisp \( -type f -not -name '*.el' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el' ! -name site-start.el \( -exec test -e '{}'c \; -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \) \)

  find .%{_datadir}/emacs/%{version}/leim \( -name '*.elc' -fprint $TOPDIR/leim-elc-files \) -o \( -type d -fprintf $TOPDIR/leim-dir-files "%%%%dir %%p\n" -fprintf $TOPDIR/el-leim-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el' \( -exec test -e '{}'c \; -fprint $TOPDIR/el-leim-bytecomped-files -o -fprint $TOPDIR/leim-not-comped-files \) \)
)

# put the lists together after filtering  ./usr to /usr
sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
cat common-*-files > common-filelist
cat el-*-files common-lisp-dir-files > el-filelist
cat leim-*-files > leim-filelist

%clean
rm -rf $RPM_BUILD_ROOT
   
%define info_files ada-mode autotype ccmode cl dired-x ebrowse ediff efaq elisp emacs eshell eudc forms gnus idlwave info message mh-e pcl-cvs reftex sc speedbar vip viper widget woman

%post common
for f in %{info_files}; do
  /sbin/install-info %{_infodir}/$f.gz %{_infodir}/dir --section="GNU Emacs" 2> /dev/null || :
done
alternatives --install %{_bindir}/etags etags %{_bindir}/etags.emacs 80

%preun common
if [ "$1" = 0 ]; then
  for f in %{info_files}; do
    /sbin/install-info --delete %{_infodir}/$f.gz %{_infodir}/dir \
      --section="GNU Emacs" 2> /dev/null || :
  done
  alternatives --remove etags %{_bindir}/etags.emacs
fi

%files
%defattr(-,root,root)
%{_bindir}/emacs
%{_bindir}/emacs-%{version}
%{_bindir}/emacs-x
%{_bindir}/emacs-%{version}-x
%dir %{_libexecdir}/emacs
%dir %{_libexecdir}/emacs/%{version}
%dir %{emacs_libexecdir}
%{emacs_libexecdir}/fns-%{version}.1-x.el
%{_datadir}/applications/gnu-emacs.desktop
%{_datadir}/pixmaps/emacs.png 

%files nox
%defattr(-,root,root)
%{_bindir}/emacs
%{_bindir}/emacs-%{version}
%{_bindir}/emacs-nox
%{_bindir}/emacs-%{version}-nox
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/%{version}
%dir %{_datadir}/emacs/%{version}/etc
%dir %{_libexecdir}/emacs
%dir %{_libexecdir}/emacs/%{version}
%dir %{emacs_libexecdir}
%{emacs_libexecdir}/fns-%{version}.1-nox.el

%files -f common-filelist common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/skel/.emacs
%doc etc/NEWS BUGS README 
%exclude %{_bindir}/emacs*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
# quieten startup when -leim and -el aren't installed
%dir %{_datadir}/emacs/%{version}/leim
%{_datadir}/emacs/%{version}/site-lisp
%{_libexecdir}/emacs
%exclude %{emacs_libexecdir}/fns-%{version}.*.el
%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/default.el
%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/site-start.el

%files -f el-filelist el
%defattr(-,root,root)

%files -f leim-filelist leim
%defattr(-,root,root)

%changelog
* Fri Apr  8 2005 Jens Petersen <petersen@redhat.com> - 21.4-1
- update to 21.4 movemail vulnerability release
  - no longer need movemail-CAN-2005-0100.patch
- replace %{_bindir}/emacs alternatives with a wrapper script (Warren Togami)
  to prevent it from disappearing when upgrading (Michal Jaegermann, 154326)
  - suffix the X emacs binaries with -x and the no X binaries with -nox
  - the wrapper script %{_bindir}/emacs-%%version runs emacs-x if installed or
    otherwise emacs-nox.  %{_bindir}/emacs is a symlink to the wrapper
- make emacs and emacs-nox own the subdirs in %{_libexecdir}
- add a bunch of fixes from debian's emacs21_21.4a-1 patch:
    battery-acpi-support.dpatch, bzero-and-have-stdlib.dpatch,
    coding-region-leak.dpatch, detect-coding-iso2022.dpatch,
    fix-batch-mode-signal-handling.dpatch, pcl-cvs-format.dpatch,
    python-completion-ignored-extensions.dpatch,
    remote-files-permissions.dpatch, save-buffer.dpatch, scroll-margin.dpatch,
    xfree86-4.3-modifiers.dpatch
  - add fix-x-vs-no-x-diffs.dpatch
    - define emacs_libexecdir
    - build both emacs and emacs-nox as %%{version}.1 and move common DOC file
      to emacs-common
    - suffix version in fns-%%{version}.1.el with -x and -nox respectively
- add 100 to elisp patches

* Wed Apr  6 2005 Jens Petersen <petersen@redhat.com> - 21.3-27
- use alternatives to switch _bindir/emacs between emacs and emacs-nox
  (Henning Schmiedehausen, #151067)
  - remove emacs and emacs-nox from bindir
  - prereq alternatives for emacs and emacs-nox
  - add post and postun scripts to handle alternatives
- buildrequire xorg-x11-devel instead of XFree86-devel
- really include and apply emacs-21.3-latex-mode-hook-144083.patch
- make emacs and emacs-nox own _datadir/emacs/version too

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 21.3-26
- rebuild with gcc 4.0
  - add emacs-21.3-gcc4.patch for emacsclient

* Mon Feb 28 2005 Jens Petersen <petersen@redhat.com> - 21.3-25
- add tramp-2.1.3 to site-lisp (David Woodhouse, 149703)
  - move removal of info dir to after its installation
  - add tramp-init.el to put tramp into load-path

* Thu Feb 24 2005 Jens Petersen <petersen@redhat.com> - 21.3-24
- mark default.el as a noreplace config file (Pawel Salek, 149310)
- only set keyboard-coding-system in xterms to fix problem with input
  Latin characters becoming prefixes and making emacs loop
  (Eddahbi Karim, 126007)
- make emacs-el own its lisp directories
- run latex-mode-hook in latex-mode (Martin Biely, 144083)
  - add emacs-21.3-latex-mode-hook-144083.patch

* Fri Feb 18 2005 Jens Petersen <petersen@redhat.com> - 21.3-23
- install %{_bindir}/emacs-nox as a hardlink of the versioned binary
- drop explicit lib requirements
- use sed instead of perl to fix up filelists

* Mon Feb 14 2005 Jens Petersen <petersen@redhat.com> - 21.3-22
- use prereq instead of contexts for common script requirements
  (Axel Thimm, 147791)
- move emacs.png from common to main package

* Fri Feb  4 2005 Jens Petersen <petersen@redhat.com> - 21.3-21
- fix CAN-2005-0100 movemail vulnerability with movemail-CAN-2005-0100.patch
  (Max Vozeler, 146701)

* Fri Jan 14 2005 Jens Petersen <petersen@redhat.com> - 21.3-20
- workaround xorg-x11 modifier key problem with
  emacs-21.3-xterm-modifiers-137868.patch (Thomas Woerner, 137868)

* Mon Nov 29 2004 Jens Petersen <petersen@redhat.com> - 21.3-19
- prefer XIM status under-the-window for now to stop xft httx from dying
  (125413): add emacs-xim-status-under-window-125413.patch
- default diff to unified format in .emacs

* Thu Nov  4 2004 Jens Petersen <petersen@redhat.com> - 21.3-18
- show emacs again in the desktop menu (132567)
- require fonts-xorg-75dpi to prevent empty boxes at startup due to missing
  fonts (Johannes Kaiser, 137060)

* Mon Oct 18 2004 Jens Petersen <petersen@redhat.com> - 21.3-17
- fix etag alternatives removal when uninstalling (Karsten Hopp, 136137)

* Fri Oct 15 2004 Jens Petersen <petersen@redhat.com> - 21.3-16
- do not setup frame-title-format in default.el, since it will override
  setting by users (Henrik Bakken, 134520)
- emacs-el no longer requires emacs for the sake of -nox users
  (Lars Hupfeldt Nielsen, 134479)
- condition calling of global-font-lock-mode in default .emacs
  in case xemacs should happen to load it

* Wed Sep 29 2004 Jens Petersen <petersen@redhat.com> - 21.3-15
- cleanup and update .desktop file
- make emacs not appear in the desktop menu (Seth Nickell,132567)
- move the desktop file from -common to main package
- go back to using just gctags for ctags
- etags is now handled by alternatives (92256)
- improve the default frame title by prefixing the buffer name
  (Christopher Beland, 128110)
- fix the names of some European aspell languages with
  emacs-21.3-lisp-textmodes-ispell-languages.patch (David Jansen, 122618)
- fixing running "libtool gdb program" in gud with
  emacs-21.3-gud-libtool-fix.patch (Dave Malcolm, 130955)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 30 2004 Jens Petersen <petersen@redhat.com> - 21.3-13
- unset focus-follows-mouse in default.el to make switching frames work for
  click-to-focus (Theodore Belding,114736)

* Thu Apr 15 2004 Jens Petersen <petersen@redhat.com> - 21.3-12
- update php-mode to 1.1.0
- add emacs-21.3-no-rpath.patch so that /usr/X11R6/lib is not rpath'ed
- require /bin/ln for %%post (Tim Waugh, 119817)
- move prereq for dev and /sbin/install-info to emacs-common
- leim no longer requires emacs
- use source site-lisp dir in %%prep to setup site files
- define and use site_lisp for buildroot in %%install
- default ispell dictionary to "english" for CJK locale
- add comment to top of site-start.el about load order
- turn on auto-compression-mode in default.el (114808)
- set require-final-newline with setq (David Olsson,119141)
  and remove redundant next-line-add-newlines setting
- update info_file list (Reuben Thomas,114729)

* Wed Mar 16 2004 Mike A. Harris <mharris@redhat.com> 21.3-11
- Removed bogus Requires: XFree86-libs that was added in 21.3-8, as rpm
  find-requires will automatically pick up the dependancies on any runtime
  libraries, and such hard coded requires is not X11 implementation
  agnostic (#118471)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 24 2004 Jens Petersen <petersen@redhat.com> - 21.3-9
- bring back emacs-nox subpackage (emacs built without X support) (#113001)
  [suggested by Frank Kruchio]
- base emacs package now only contains emacs binary built with X support
  and no longer obsoletes emacs-nox
- all the common files required by emacs and emacs-nox are now in emacs-common
- update php-mode.el to 1.0.5
- add missing rfc1345.el leim input method
- update po-compat.el to version in gettext-0.13.1
- update base package summary
- add url for python-mode.el and php-mode.el
- gctags is now a symlink to ctags.emacs

* Wed Jan 14 2004 Jens Petersen <petersen@redhat.com> - 21.3-8
- comment out setting transient-mark-mode in skel .emacs (#102441,#90193)
  [reported by mal@gromco.com, Jonathan Kamens]
- improve lang-coding-systems-init.el to set-language-environment for CJK
  utf-8 locale too and use utf-8 for default-coding-systems and
  terminal-coding-system (#111172) [Yoshinori Kuniga]
- update rpm-spec-mode.el to newer one in xemacs package cvs (#105888) [Dams]
- rename etags to etags.emacs and make etags a symlink to it at install time
  if it doesn't exist (#92256) [marc_soft@merlins.org]
- apply editfns.c-Fformat-multibyte-davej.patch to fix multibyte code typo
  in Fformat [patch from Dave Jones]
- add runtime requirements for XFree86-libs, image libraries, ncurses and zlib
- improve -el and -leim package summaries
- no longer configure build with redundant --with-gcc

* Tue Nov 25 2003 Jens Petersen <petersen@redhat.com>
- buildrequire autoconf213 (#110741) [reported by mvd@mylinux.com.ua]

* Mon Oct 27 2003 Jens Petersen <petersen@redhat.com> - 21.3-7
- use "setarch i386" to build on ix86 (#101818) [reported by Michael Redinger]
- use __make to %%build and %%install
- set keyboard coding-system for utf-8 in lang-coding-systems-init.el (#106929)
  [reported with fix by Axel Thimm]
- add source url for MuleUCS
- update base package description (#103551) [reported by Tim Landscheidt]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Jens Petersen <petersen@redhat.com> - 21.3-5
- move transient-mark-mode and global-font-lock-mode setting from default.el
  back to dotemacs, so as not to surprise old users (#90193)
  [reported by jik@kamens.brookline.ma.us]
- change require-final-newline to query (default.el)
- don't make a backup when applying browse-url-htmlview-84262.patch (#90226)
  [reported by mitr@volny.cz]

* Fri May  2 2003 Elliot Lee <sopwith@redhat.com>
- Add emacs-21.3-ppc64.patch

* Fri Apr 25 2003 Jens Petersen <petersen@redhat.com> - 21.3-3
- use Mule-UCS utf-8 coding-system for CJK subprocess IO
- no need to set fontset anymore in CJK locale

* Wed Apr 16 2003 Jens Petersen <petersen@redhat.com> - 21.3-2
- add Mule-UCS for CJK utf-8 support (suggested by Akira Tagoh)
  and use it by default in CJK UTF-8 locale
- move emacs-asian startup files into new lang-coding-systems-init.el
- utf-8 setup in site-start.el is no longer needed in Emacs 21.3
- generate filelist for site-lisp automatically like base lisp and leim
- don't setup aspell in site-start.el
- rename dotemacs to dotemacs.el and move former contents to new default.el

* Mon Apr  7 2003 Jens Petersen <petersen@redhat.com> - 21.3-1
- update to 21.3
- no longer set compound-text-with-extensions in dotemacs, since it is now
  the default
- emacs-21.2-pop.patch is no longer needed
- update php-mode to 1.0.4

* Thu Feb 20 2003 Jens Petersen <petersen@redhat.com> - 21.2-33
- default browse-url to use htmlview (#84262)
- remove info dir file rather than excluding it

* Sat Feb  8 2003 Jens Petersen <petersen@redhat.com> - 21.2-32
- set X copy'n'paste encoding to extended compound-text (#74100)
  by default in .emacs file [suggested by olonho@hotmail.com]
- .emacs file cleanup (xemacs now has a separate init file)

* Fri Feb  7 2003 Jens Petersen <petersen@redhat.com> - 21.2-31
- block input in allocate_vectorlike to prevent malloc hangs (#83600)
  [thanks to Jim Blandy]
- set startup wmclass notify in desktop file

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 21.2-29
- update to newer po-mode.el and po-compat.el from gettext-0.11.4
- patch po-mode's po-replace-revision-date for when
  po-auto-replace-revision-date is nil (#71264)
- update po-mode-init.el
- examine LC_ALL before LC_CTYPE in site-start.el for utf-8 (#79535)
- don't install etc/DOC files explicitly by hand
- make sure all lisp .elc files are up to date
- pass _smp_mflags to make
- remove games that we shouldn't ship

* Mon Jan 13 2003 Karsten Hopp <karsten@redhat.de> 21.2-28
- s390x lib64 fix

* Fri Jan  3 2003 Jens Petersen <petersen@redhat.com> 21.2-27
- look at LANG after LC_CTYPE when checking for UTF-8 locale encoding
  in site-start.el (#79535)
- don't set desktop file config(noreplace)

* Fri Dec 20 2002 Jens Petersen <petersen@redhat.com> 21.2-26
- unset the sticky bit of emacs in bindir (#80049)

* Wed Dec 18 2002 Jens Petersen <petersen@redhat.com> 21.2-25
- no need to patch config.{sub,guess}

* Tue Dec  3 2002 Tim Waugh <twaugh@redhat.com>
- Fix python-mode-init.el (bug #78910).

* Sun Dec  1 2002 Jens Petersen <petersen@redhat.com> 21.2-24
- rpm-spec-mode update fixes
  - patch in XEmacs compat functions rather than defining them with apel
    macros in init file (#78764)
  - autoload "rpm-spec-mode" not "rpm-spec-mode.el" in same file
- let emacs base also own leim dir to avoid startup warning about missing dir
  when -el and -leim aren't installed (#78764)

* Thu Nov 28 2002 Jens Petersen <petersen@redhat.com>
- use LC_CTYPE rather than LANG to determine default encoding (#78678)
  [reported by starback@stp.ling.uu.se]

* Wed Nov 27 2002 Jens Petersen <petersen@redhat.com> 21.2-23
- set transient-mark-mode in dotemacs for Emacs not XEmacs (#75440)
- update rpm-spec-mode.el to 0.12
  - define needed XEmacs compat functions in new rpm-spec-mode-init.el
- tidy site-start.el
  - move python-mode setup to python-mode
- don't build with sbin in path
- use _libexecdir, _bindir and _sysconfdir
- don't gzip info files explicitly
- use tar's C and j options
- generate lisp file-lists in single find sweeps over lisp and leim dirs
  - use -fprint and -fprintf
  - correct more dir ownerships

* Sun Nov 24 2002 Florian La Roche <Florian.LaRoche@redhat.de> 21.2-22
- add correct alloca defines for s390

* Wed Nov  6 2002 Jens Petersen <petersen@redhat.com> 21.2-21
- uses patches for x86_64 and s390 support and config.{guess,sub} updating

* Tue Nov  5 2002 Jens Petersen <petersen@redhat.com> 21.2-20
- add support for x86_64 and merge in s390 support from cvs
- add alloca defines to amdx86-64.h (from SuSE)

* Wed Oct 30 2002 Jens Petersen <petersen@redhat.com> 21.2-19
- own our libexec dir (#73984)
- only set transient-mark-mode in dotemacs for Emacs (#75440)
- update to latest config.{guess,sub}
- use _datadir macro

* Wed Aug 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-18
- Desktop file fix - add Application to make it show up
- DNS lookup fix for pop (#64802)

* Tue Aug 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-17
- Fix gdb arrow when used in non-windowed mode (#56890)

* Fri Aug  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-16
- Handle UTF-8 input (#70855).

* Tue Aug  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-15
- Don't use canna by default (#70870)

* Thu Aug  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-14
- Fixes to desktop file (add encoding, add missing a ";")
- Update s390 patch

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-13
- rpm -> rpmbuild for rpmspec mode (#68185)

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-12
- desktop file changes (#69385)

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-11
- Fix php-mode to not initialize on e.g.  foophp.c (#67592)

* Thu Jun 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-10
- Downgrade po-mode

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-8
- #66808

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-7
- Rebuild

* Mon May 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-6
- Prereq dev

* Thu May 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-5
- Update the elisp manual and po-mode

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-4
- php-mode 1.0.2

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-3
- Update po-mode to the one from gettext 0.11.1

* Mon Apr  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-2
- Tweak mouse init process (#59757)

* Mon Mar 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-1
- 21.2

* Fri Mar  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.95-1
- 21.1.95

* Fri Feb  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.90-2
- Upgrade po-mode to the version bundled with gettext 0.11
- Upgrade rpm-spec-mode to 0.11h

* Thu Jan 31 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.90-1
- 21.1.90

* Fri Jan 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.80-2
- Add ebrowse
- Set transient-mode to t in /etc/skel/.emacs

* Mon Jan 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.80-1
- 21.1.80

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-3
- Increase recursive-load-depth-limit from 10 to 50

* Wed Dec  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-2
- Make it conflict with old versions of gettext

* Thu Nov 29 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-1
- rpm-spec-mode 0.11h, should fix #56748

* Tue Nov  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.4
- php mode 1.0.1. Should fix some speedbar problems.

* Tue Oct 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.3
- Minor cleanups
- add ssl.el

* Mon Oct 22 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.2
- Add more files from the libexec directory (#54874, #54875)

* Sun Oct 21 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.1
- 21.1
- Build on IA64 again - the default config now handles it
- Drop all old patches
- Misc cleanups
- Update the elisp manual to 21-2.7
- Deprecate the emacs-nox and emacs-X11 subpackages. 
  Simplify build procedure to match. 
- Update php-mode to 1.0.0

* Mon Oct 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 20.7-43
- Add php-mode 0.9.9
- Add URL (#54603)
- don't run autoconf/libtoolize during build - they're broken
- don't build on IA64 until they are fixed

* Sun Sep 16 2001 Trond Eivind Glomsrød <teg@redhat.com> 20.7-42
- Update python-mode to the version in the python 2.2a3
- Include po-mode in emacs, instead of including in gettext

* Mon Jul 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Minor fix to make-mode fontify regexp (#50010)
- Build without emacs being installed (#49085)

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Much cleaner site-start.d sourcing
- Add more build dependencies
- Add the emacs lisp reference info pages (RFE #44577)
- Don't require tamago - just plug it in for Japanese support

* Mon Jun 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add Xaw3d-devel to buildrequires (#44736)

* Mon Jun 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- merged s390x patch from <oliver.paukstadt@millenux.com>

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New rpm-spec-mode.el, which fixes #43323

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix linker problem on s390 (fix by Than Ngo than@redhat.com)

* Wed Apr 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make sure that mwheel is initialized for XEmacs (#37451)

* Fri Mar 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New locale.alias file for emacs-nox

* Tue Mar  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- update rpm-spec-mode.el to 0.11e - this should fix #30702

* Fri Feb 16 2001 Preston Brown <pbrown@redhat.com>
- require tamago, or japanese cannot be input (#27932).

* Sat Jan 27 2001 Jakub Jelinek <jakub@redhat.com>
- Preprocess Makefiles as if they were assembly, not C source.

* Thu Jan 24 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix the fontset problem when creating a new frame.

* Thu Jan 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add Japanese support from Yukihiro Nakai <ynakai@redhat.com>

* Thu Jan 04 2001 Preston Brown <pbrown@redhat.com>
- do not remove etags, only ctags, per Tom Tromey's suggestion.

* Wed Dec 27 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space

* Mon Dec 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/locale.alias , which had gone AWOL
- update rpm-spec-mode to 0.11a, fresh from the author
  (Stig Bjorlykke <stigb@tihlde.org>). The changes we made 
  are integrated.

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- prereq fileutils for emacs-nox

* Mon Dec 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- do locale.alias fix for emacs-nox only, as it somehow
  broke the subject line in gnus. Weird.
- update to gnus 5.8.7

* Fri Dec 08 2000 Than Ngo <than@redhat.com>
- add support s390 machine

* Thu Dec 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add rpm-spec-mode after modifying (use Red Hat groups,
  from /usr/share/doc/rpm-version/GROUPS) and fixing
  colours(don't specify "yellow" on "bright") Also, 
  use gpg, not pgp.
- use it (site-start.el)
- add mwheel 
- use it, in /etc/skel/.emacs

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/site-lisp/site-start.d
- change site-start.el so files in the above directory
  are automatically run on startup
- don't set the ispell name in site-start.el, use the
  above directory instead  

* Thu Oct 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix icon name in the .desktop file
- don't have site-start.el "noreplace"
- load psgml-init (if present) in the default site-start.el
  to avoid psgml modifying the file

* Tue Oct 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new and better emacs.desktop file

* Tue Oct 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove ctags.1 and etags.1 from the emacs etc directory
  (#18011)
- fix the emacs-nox not to use the locale.alias in XFree86
  (#18548)... copy it into /usr/share/emacs and patch
  the startup files to use it. Argh.

* Wed Oct 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix initialization of python mode (require it before
  customizing it)

* Fri Sep 22 2000 Bill Nottingham <notting@redhat.com>
- don't use bcopy without a prototype

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- define MAIL_USE_LOCKF 
- remove setgid on movemail

* Mon Aug 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/site-lisp/subdirs.el (#15639)

* Tue Jul 25 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove "-b" option from manpage

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove Japanese support

* Mon Jul 17 2000 Matt Wilson <msw@redhat.com>
- updated .desktop entry and icon

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix some typos in spec file

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make /etc/skel/.emacs 0644

* Wed Jun 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- include python mode and change in site-start.el related to this
- some changes to the default .emacs 

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- don't build with -O2 on alpha until we can track down the compiler
  bug that causes crashes in the garbage collector
- removed all the nox Japanese packages

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- include site-start.el as a a config file
- add aspell support via the above

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- (from MSW) different compression on IA64 to avoid hangs
- remove etags/ctags - use a separate package. Disable patch1

* Wed Jun 14 2000 Matt Wilson <msw@redhat.com>
- edited japanese patch not to patch configure
- fixed a missing escaped " in a wc string
- merge japanese support to head of development

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Version 20.7
- Add requirement for final newline to the default .emacs
- redid the Xaw3d patch
- checked all patches, discarded those we've upstreamed

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir} and %%{_infodir}

* Fri Jun  2 2000 Bill Nottingham <notting@redhat.com>
- add yet another ia64 patch

* Mon May 22 2000 Bill Nottingham <notting@redhat.com>
- add another ia64 patch

* Fri May 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Disabled the compile patch for 20.6

* Thu May 18 2000 Bill Nottingham <notting@redhat.com>
- add in ia64 patch

* Thu May 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't apply the unexelf patch - use a new unexelf.c file
  from the 21 source tree (this will go into the 20.7 tree)

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added patch by jakub to make it work with glibc2.2

* Mon May 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed a problem with ange-ftp and kerberized ftp

* Mon May 08 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new Xaw3d

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- let the build system handle gzipping man pages and stripping
- added patch to increase keyboard buffer size

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- gzip man pages

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added a security patch from RUS-CERT, which fixes 
  bugs mentioned in "Advisory 200004-01: GNU Emacs 20"

* Tue Apr 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patched to detect bash2 scripts. 

* Thu Apr 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- removed configuraton file status from /usr/share/pixmaps/emacs.png

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to 20.6 and make it compile

* Mon Feb 21 2000 Preston Brown <pbrown@redhat.com>
- add .emacs make the delete key work to delete forward character for X ver.

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #2988
- recompile patched .el files (suggested by Pavel.Janik@linux.cz)
- prereq /sbin/install-info

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig gone

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions and summary
- fix permissions for emacs niaries (what the hell does 1755 means for a
  binary?)
- added missing, as per emacs Changelog, NCURSES_OSPEED_T compilation
  flag; without it emacs on Linux is making global 'ospeed' short which
  is not the same as 'speed_t' expected by libraries. (reported by Michal
  Jaegermann <michal@harddata.com>)

* Mon Jan 10 2000 David S. Miller <davem@redhat.com>
- Revert src/unexecelf.c to 20.4 version, fixes SPARC problems.

* Sun Jan  9 2000 Matt Wilson <msw@redhat.com>
- strip emacs binary
- disable optimizations for now, they cause illegal instructions on SPARC.

* Sun Jan 09 2000 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.5a
- remove python-mode, wheelmouse support, and auctex menu
- import emacs.desktop with icon from GNOME

* Wed Dec 08 1999 Ngo Than <than@redhat.de>
- added python-mode, wheelmouse support and auctex menu
- added Comment[de] in emacs.desktop

* Sat Sep 25 1999 Preston Brown <pbrown@redhat.com>
- added desktop entry

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- tried to fix triggers, hopefully working now.

* Wed Sep 01 1999 Preston Brown <pbrown@redhat.com>
- added trigger for making symlink to /usr/bin/emacs in emacs-nox package

* Thu Jul 22 1999 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.4
- cleaned up spec

* Fri Apr 16 1999 Owen Taylor <otaylor@redhat.com>
- replace bad xemacs compiled .elc file for mh-e with one compiled
  on emacs

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- make sure movemail doesn't get %defattr()'d to root.root

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- patch to make it work with dxpc

* Wed Mar 31 1999 Preston Brown <pbrown@redhat.com>
- updated mh-utils emacs lisp file to match our nmh path locations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Fri Feb 26 1999 Cristian Gafton <gafton@redhat.com>
- linker scripts hack to make it build on the alpha

* Fri Jan  1 1999 Jeff Johnson <jbj@redhat.com>
- add leim package (thanks to Pavel.Janik@inet.cz).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- backed up changes to uncompress.el (it seems that the one from 20.2 works
  much better)

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- eliminate /tmp race in rcs2log

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to 20.3

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add --with-pop to X11 compile.
- include contents of /usr/share/.../etc with main package.

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- fix signals when linked with glibc on non-Intel architectures
  NOTE: This patch is not needed with emacs >20.2

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/lib/emacs/20.2/*-redhat-linux directory in the filelist

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- alpha started to like emacs-nox again :-)

* Thu Nov  6 1997 Michael Fulbright <msf@redhat.com>
- alpha just doesnt like emacs-nox, taking it out for now

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- added multibyte support back into emacs 20.2
- added wmconfig for X11 emacs
- fixed some errant buildroot references

* Thu Oct 23 1997 Michael Fulbright <msf@redhat.com>
- joy a new version of emacs! Of note - no lockdir any more.
- use post/preun sections to handle numerous GNU info files

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- stopped stripping it as it seems to break things

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- turned off ecoff support on the Alpha (which doesn't build anymore)

* Mon Jun 16 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved ctags to gctags to fit in the more powerful for C (but less
  general) exuberant ctags as the binary /usr/bin/ctags and the
  man page /usr/man/man1/ctags.1
