Summary: The libraries needed to run the GNU Emacs text editor.
Name: emacs
Version: 21.2
Release: 2
License: GPL
URL: http://www.gnu.org/software/emacs/
Group: Applications/Editors
Source0: ftp://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/emacs/leim-%{version}.tar.bz2
Source3: emacs.desktop
Source4: emacs.png
Source5: dotemacs
Source6: site-start.el
Source7: python-mode.el
Source8: http://www.tihlde.org/~stigb/rpm-spec-mode.el
Source9: emacs-asian.tar.bz2
Source10: ftp://ftp.gnu.org/gnu/emacs/elisp-manual-21-2.7.tar.bz2
# 1.0.0 - http://prdownloads.sourceforge.net/php-mode/php-mode-100.el
Source11: php-mode.el
Source12: php-mode-init.el
Source13: ssl.el
Source14: po-mode.el
Source15: po-mode-init.el
Patch50: emacs-20.7-s390.patch
Buildroot: %{_tmppath}/%{name}-%{version}-root
Prereq: /sbin/install-info
BuildRequires: Xaw3d-devel glibc-devel gcc XFree86-devel bzip2 ncurses-devel
BuildRequires: zlib-devel libpng-devel libjpeg-devel libungif-devel libtiff-devel 
Obsoletes: emacs-nox emacs-X11
Conflicts: gettext < 0.10.40

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package includes the libraries you need to run the Emacs editor,
You also need to install the actual Emacs program package (emacs-nox or
emacs-X11). Install emacs-nox if you are not going to use the X
Window System; install emacs-X11 if you will be using X.

%package el
Summary: The sources for elisp programs included with Emacs.
Group: Applications/Editors
Requires: emacs

%description el
Emacs-el contains the emacs-elisp sources for many of the elisp
programs included with the main Emacs text editor package.

You need to install emacs-el only if you intend to modify any of the
Emacs packages or see some elisp examples.

%package leim
Summary: Emacs Lisp code for input methods for international characters.
Group: Applications/Editors
Requires: emacs

%description leim
The emacs-leim package contains Emacs Lisp code for input methods for
various international character scripts. Basically, the Lisp code
provided by this package describes the consecutive keystrokes that a
user must press in order to input a particular character in a
non-English character set. Input methods for many different character
sets are included in this package.

%prep

%setup -q -b 1


%ifarch s390 s390x
%patch50 -p1 -b .s390
%endif

%build

export CFLAGS="-DMAIL_USE_LOCKF $RPM_OPT_FLAGS"
#to find installinfo
export PATH="$PATH:/sbin:/usr/sbin"

%configure --with-gcc --with-pop --with-sound
make


%define recompile src/emacs -batch --no-init-file --no-site-file -f batch-byte-compile

# recompile patched .el files
%{recompile} lisp/mail/mh-utils.el lisp/progmodes/make-mode.el

# bytecompile python-mode, ssl, php-mode and rpm-spec-mode
cp %SOURCE7 %SOURCE8  %SOURCE11 %SOURCE13 %SOURCE14 .
%{recompile} python-mode.el rpm-spec-mode.el php-mode.el ssl.el po-mode.el



%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d

mkdir -p $RPM_BUILD_ROOT/%{_infodir}

%makeinstall

#install lisp files for Japanese and other Asian languages
pushd $RPM_BUILD_ROOT
tar --use-compress-program=bzip2 -xf %{SOURCE9}
popd

rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
gzip -9nf $RPM_BUILD_ROOT/%{_infodir}/*

install -m 644 %SOURCE6 $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.el

mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp

mv $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1 $RPM_BUILD_ROOT%{_mandir}/man1/gctags.1
mv $RPM_BUILD_ROOT/usr/bin/ctags $RPM_BUILD_ROOT/usr/bin/gctags


# GNOME / KDE files
mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Applications
install -c -m 0644 %SOURCE3 $RPM_BUILD_ROOT/etc/X11/applnk/Applications/
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
install -c -m 0644 %SOURCE4 $RPM_BUILD_ROOT/usr/share/pixmaps/

mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/%{version}/etc
install -c -m644 etc/DOC-* $RPM_BUILD_ROOT/usr/share/emacs/%{version}/etc

# Python mode, php mode and rpm-spec mode

install -c -m0644 po-mode.el po-mode.elc php-mode.el php-mode.elc python-mode.el python-mode.elc rpm-spec-mode.el rpm-spec-mode.elc ssl.el ssl.elc $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/
install -m0644 %SOURCE12 $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d/php-mode-init.el
install -m0644 %SOURCE15 $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d/po-mode-init.el

# default initialization file
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m0644 %SOURCE5 $RPM_BUILD_ROOT/etc/skel/.emacs

#
# create file lists
#

# Remove ctags

rm -f $RPM_BUILD_ROOT/usr/bin/ctags
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/*ctags*
rm -f $RPM_BUILD_ROOT/usr/share/emacs/%{version}/etc/ctags*

# The elisp reference manual
bzcat %{SOURCE10} | tar xf -
pushd elisp-manual-21-2.7
install -m 644 elisp elisp-? elisp-?? $RPM_BUILD_ROOT/%{_infodir}
popd

find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp -type f\
  -not -name '*.el' -print | sed "s^$RPM_BUILD_ROOT^^" > core-filelist
find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
  -type d -printf "%%%%dir %%p\n" | sed "s^$RPM_BUILD_ROOT^^" >> core-filelist

# Include .el files which lack a corresponding byte compiled form
for I in `find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
          -name '*.el'`; do
  if [ ! -e `dirname $I`/`basename $I .el`.elc ]; then 
    echo $I | sed "s^$RPM_BUILD_ROOT^^"
  fi
done >> core-filelist

# Include all non elisp files which emacs installs
#find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp -type f | \
#  sed "s^$RPM_BUILD_ROOT^^" | grep -v "\.el\(c\)\?$" >> core-filelist


find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/leim \
  -name '*.elc' -print | sed "s^$RPM_BUILD_ROOT^^" > leim-filelist
find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/leim \
  -mindepth 1 -type d -printf "%%%%dir %%p\n" | \
  sed "s^$RPM_BUILD_ROOT^^" >> leim-filelist

#
# be sure to exclude some files which are needed in the core package
#
for I in `find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
          -name '*.el'`; do
  if [ -e `dirname $I`/`basename $I .el`.elc ]; then 
    echo $I | sed "s^$RPM_BUILD_ROOT^^"
  fi
done >> el-filelist

find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/leim \
  -name '*.el' -print | sed "s^$RPM_BUILD_ROOT^^" |\
  grep -v "leim\/leim-list.el" >> el-filelist

%clean
rm -rf $RPM_BUILD_ROOT
   
%define info_files ccmode cl dired-x ediff emacs forms gnus info message mh-e reftex sc vip viper widget elisp
%post
for f in %{info_files}; do
  /sbin/install-info %{_infodir}/$f.gz %{_infodir}/dir --section="GNU Emacs" 2> /dev/null || :
done

%preun
if [ "$1" = 0 ]; then
for f in %{info_files}; do
  /sbin/install-info --delete %{_infodir}/$f.gz %{_infodir}/dir \
    --section="GNU Emacs" 2> /dev/null || :
done
fi


%files -f core-filelist
%defattr(-,root,root)
%config(noreplace) /etc/skel/.emacs
%doc etc/NEWS BUGS README 
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/*
/usr/share/emacs/site-lisp/python-mode.elc
/usr/share/emacs/site-lisp/php-mode.elc
/usr/share/emacs/site-lisp/po-mode.elc
/usr/share/emacs/site-lisp/rpm-spec-mode.elc
/usr/share/emacs/site-lisp/ssl.elc
/usr/share/emacs/site-lisp/subdirs.el
/usr/share/emacs/site-lisp/site-start.d/lang.emacs.el
/usr/share/emacs/site-lisp/site-start.d/php-mode-init.el
/usr/share/emacs/site-lisp/site-start.d/po-mode-init.el
/usr/share/emacs/site-lisp/lang
%dir /usr/share/emacs
%dir /usr/share/emacs/site-lisp
%dir /usr/share/emacs/%{version}
%dir /usr/share/emacs/%{version}/*
/usr/share/emacs/%{version}/etc/*
/usr/libexec/emacs/%{version}/*/*
%attr(0755,root,root) /usr/libexec/emacs/%{version}/*/movemail
%attr(0644,root,root) %config /usr/share/emacs/site-lisp/site-start.el
%dir /usr/share/emacs/site-lisp/site-start.d
%config(noreplace) /etc/X11/applnk/Applications/emacs.desktop
/usr/share/pixmaps/emacs.png 

%files -f el-filelist el
%defattr(-,root,root)
/usr/share/emacs/site-lisp/python-mode.el
/usr/share/emacs/site-lisp/php-mode.el
/usr/share/emacs/site-lisp/po-mode.el
/usr/share/emacs/site-lisp/ssl.el
/usr/share/emacs/site-lisp/rpm-spec-mode.el

%files -f leim-filelist leim
%defattr(-,root,root)
/usr/share/emacs/%{version}/leim/leim-list.el
%dir /usr/share/emacs/%{version}/leim

%changelog
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
