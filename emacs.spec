Summary: The libraries needed to run the GNU Emacs text editor.
Name: emacs
Version: 20.7
Release: 40
License: GPL
Group: Applications/Editors
Source0: ftp://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/emacs/leim-%{version}.tar.bz2
Source3: emacs.desktop
Source4: emacs.png
Source5: dotemacs
Source6: site-start.el
Source7: http://www.python.org/emacs/python-mode/python-mode.el
# From /usr/X11R6/lib/X11/locale/locale.alias
Source8: emacs.locale.alias
Source11: http://www.tihlde.org/~stigb/rpm-spec-mode.el
Source12: mwheel.el
Source13: lisp-startup-localealias.patch
Source14: ftp://ftp.gnus.org/pub/gnus/gnus-5.8.8.tar.bz2
Source15: emacs-asian.tar.bz2
Source16: ftp://ftp.gnu.org/gnus/emacs/elisp-manual-21-2.6.tar.bz2
Patch0: emacs-20.7-xaw3d.patch
Patch2: emacs-20.3-tmprace.patch
Patch3: emacs-20.3-linkscr.patch
Patch4: emacs-20.4-nmhlocation.patch
Patch5: emacs-20.5-loadup.patch
Patch6: emacs-20.6-kbdbuffer.patch
Patch7: emacs-20.6-ia64.patch
Patch8: emacs-20.6-ia64-2.patch
Patch9: emacs-20.6-ia64-3.patch
Patch10: emacs-20.7-manboption.patch
Patch11: emacs-20.7-proto.patch
Patch12: emacs-cpp-Makefile.patch

Patch50: emacs-20.7-s390.patch

Buildroot: %{_tmppath}/%{name}-%{version}-root
Prereq: /sbin/install-info
BuildRequires: Xaw3d-devel glibc-devel gcc XFree86-devel bzip2 ncurses-devel
BuildRequires: zlib-devel libpng-devel libjpeg-devel libungif-devel libtiff-devel
# temporary hack.  roll tamago into base emacs package
#Requires: tamago

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news and more without
leaving the editor.

This package includes the libraries you need to run the Emacs editor, so
you need to install this package if you intend to use Emacs.  You also
need to install the actual Emacs program package (emacs-nox or emacs-X11).
Install emacs-nox if you are not going to use the X Window System; install
emacs-X11 if you will be using X.

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
non-English character set. Input methods for many different language's
character sets are included in this package.

%package nox
Summary: The Emacs text editor without support for the X Window System.
Group: Applications/Editors
Requires: emacs
Prereq: fileutils

%description nox
Emacs-nox is the Emacs text editor program without support for
the X Window System.

You need to install this package only if you plan on exclusively using
Emacs without the X Window System (emacs-X11 will work both in X and out
of X, but emacs-nox will only work outside of X).  You'll also need to
install the emacs package in order to run Emacs.

%package X11
Summary: The Emacs text editor for the X Window System.
Group: Applications/Editors
Requires: emacs

%description X11
Emacs-X11 includes the Emacs text editor program for use with the X
Window System (it provides support for the mouse and other GUI
elements). Emacs-X11 will also run Emacs outside of X, but it has a
larger memory footprint than the 'non-X' Emacs package (emacs-nox).

Install emacs-X11 if you're going to use Emacs with the X Window
System.  You should also install emacs-X11 if you're going to run
Emacs both with and without X (it will work fine both ways). You'll
also need to install the emacs package in order to run Emacs.


%prep

%setup -q -b 1

%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%ifarch s390 s390x
%patch50 -p1 -b .s390
%endif

%build

PUREDEF="-DNCURSES_OSPEED_T"
XPUREDEF="-DNCURSES_OSPEED_T"
libtoolize --force --copy
autoconf
CONFOPTS="--mandir=%{_mandir} --infodir=%{_infodir} --prefix=/usr --libexecdir=/usr/lib --sharedstatedir=/var --with-gcc --with-pop"

BuildEmacs() {
    dir=$1
    configflags=$2
    [ -d build-$1 ] && rm -rf build-$1
    mkdir build-$1 && cd build-$1
    CFLAGS="-DMAIL_USE_LOCKF $RPM_OPT_FLAGS $PUREDEF" LDFLAGS=-s \
      ../configure ${CONFOPTS} $2 ${RPM_ARCH}-redhat-linux-gnu
    # blarg
    echo "#include <string.h>"  >> src/config.h
    make 
    cd ..
}


#Build binary with X support
BuildEmacs withx "--with-x-toolkit"

%define recompile build-withx/src/emacs -batch --no-init-file --no-site-file -f batch-byte-compile

#change the locale.alias for the nox builds
#patch lisp/startup.el %SOURCE10
#rm -fv lisp/startup.elc
#%{recompile} lisp/startup.el

#Build binary without X support
BuildEmacs nox "--with-x=no"

#change the locale.alias back for packaging
#patch -R lisp/startup.el %SOURCE10
#rm -fv lisp/startup.elc
#%{recompile} lisp/startup.el

# recompile patched .el files
%{recompile} lisp/mail/mh-utils.el

# bytecompile python-mode, mwheel and rpm-spec-mode
cp %SOURCE7 %SOURCE11 %SOURCE12 .
%{recompile} python-mode.el mwheel.el rpm-spec-mode.el



%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d

mkdir -p $RPM_BUILD_ROOT/%{_infodir}
make install  -C build-withx \
	prefix=$RPM_BUILD_ROOT/usr \
	libexecdir=$RPM_BUILD_ROOT/usr/lib \
	sharedstatedir=$RPM_BUILD_ROOT/var \
	mandir=$RPM_BUILD_ROOT/%{_mandir} \
	infodir=$RPM_BUILD_ROOT/%{_infodir}

# install the locale file
install -m 644 %SOURCE8 $RPM_BUILD_ROOT/usr/share/emacs/locale.alias

#install lisp files for Japanese and other Asian languages
pushd $RPM_BUILD_ROOT
tar --use-compress-program=bzip2 -xf %{SOURCE15}
popd

# We want a newer gnus
tar --use-compress-program=bzip2 -xf %{SOURCE14}
pushd gnus-5.8.8
PATH=$RPM_BUILD_ROOT/usr/bin:$PATH ./configure 
make

rm -f $RPM_BUILD_ROOT//usr/share/emacs/%{version}/lisp/gnus/*
install -m 644 lisp/* $RPM_BUILD_ROOT//usr/share/emacs/%{version}/lisp/gnus/
rm -f $RPM_BUILD_ROOT/%{_infodir}/gnus*
install -m 644 texi/{gnus,gnus-?,gnus-??} $RPM_BUILD_ROOT/%{_infodir}
popd

rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
gzip -9nf $RPM_BUILD_ROOT/%{_infodir}/*


#change the locale.alias for this one and regenerate
# Do it this way, using the macro here seems to confuse RPM
patch lisp/startup.el %SOURCE13

rm -fv lisp/startup.elc
%{recompile} lisp/startup.el
rm -f build-nox/src/emacs-%{version}*
make -C build-nox
install -c -m755 build-nox/src/emacs $RPM_BUILD_ROOT/usr/bin/emacs-nox

install -c -m755 build-nox/src/emacs $RPM_BUILD_ROOT/usr/bin/emacs-nox
install -m 644 %SOURCE6 $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.el

mkdir -p $RPM_BUILD_ROOT/usr/lib/emacs/site-lisp

mv $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1 $RPM_BUILD_ROOT%{_mandir}/man1/gctags.1
mv $RPM_BUILD_ROOT/usr/bin/ctags $RPM_BUILD_ROOT/usr/bin/gctags


# GNOME / KDE files
mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Applications
install -c -m 0644 %SOURCE3 $RPM_BUILD_ROOT/etc/X11/applnk/Applications/
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
install -c -m 0644 %SOURCE4 $RPM_BUILD_ROOT/usr/share/pixmaps/

install -c -m644 build-nox/etc/DOC-* $RPM_BUILD_ROOT/usr/share/emacs/%{version}/etc

# Python mode, mwheel and rpm-spec mode

install -c -m0644 python-mode.el python-mode.elc mwheel.el mwheel.elc rpm-spec-mode.el rpm-spec-mode.elc $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/

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
bzcat %{SOURCE16} | tar xf -
pushd elisp-manual-21-2.6
install -m 644 elisp elisp-? elisp-?? $RPM_BUILD_ROOT/%{_infodir}
popd

find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
  -name '*.elc' -print | sed "s^$RPM_BUILD_ROOT^^" > core-filelist
find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
  -type d -printf "%%%%dir %%p\n" | sed "s^$RPM_BUILD_ROOT^^" >> core-filelist
find $RPM_BUILD_ROOT/usr/lib/emacs/%{version} -type f | \
  sed "s^$RPM_BUILD_ROOT^^" | grep -v movemail >> core-filelist

# Include .el files which lack a corresponding byte compiled form
for I in `find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp \
          -name '*.el'`; do
  if [ ! -e `dirname $I`/`basename $I .el`.elc ]; then 
    echo $I | sed "s^$RPM_BUILD_ROOT^^"
  fi
done >> core-filelist

# Include all non elisp files which emacs installs
find $RPM_BUILD_ROOT/usr/share/emacs/%{version}/lisp -type f | \
  sed "s^$RPM_BUILD_ROOT^^" | grep -v "\.el\(c\)\?$" >> core-filelist


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
rm -rf build-nox
rm -rf build-withx
   
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

%triggerin nox -- emacs-X11
if [ -L /usr/bin/emacs ]; then
  rm /usr/bin/emacs
fi

%triggerpostun nox -- emacs-X11
[ $2 = 0 ] || exit 0
if [ ! -L /usr/bin/emacs ]; then
  ln -sf emacs-nox /usr/bin/emacs
fi

%post nox
if [ ! -x /usr/bin/emacs -a ! -L /usr/bin/emacs ]; then
  ln -sf emacs-nox /usr/bin/emacs
fi

%postun nox
[ $1 = 0 ] || exit 0
if [ -L /usr/bin/emacs ]; then
  rm /usr/bin/emacs
fi

%files -f core-filelist
%defattr(-,root,root)
%config(noreplace) /etc/skel/.emacs
%doc etc/NEWS BUGS README etc/FAQ
/usr/bin/b2m
/usr/bin/emacsclient
/usr/bin/etags
/usr/bin/rcs-checkin
%{_mandir}/*/*
%{_infodir}/*
/usr/share/emacs/locale.alias
/usr/share/emacs/site-lisp/python-mode.elc
/usr/share/emacs/site-lisp/mwheel.elc
/usr/share/emacs/site-lisp/rpm-spec-mode.elc
/usr/share/emacs/site-lisp/subdirs.el

/usr/share/emacs/site-lisp/site-start.d/lang.emacs.el
/usr/share/emacs/site-lisp/lang

%dir /usr/lib/emacs
%dir /usr/lib/emacs/site-lisp
%dir /usr/lib/emacs/%{version}
%dir /usr/lib/emacs/%{version}/*
%attr(0755,root,root) /usr/lib/emacs/%{version}/*/movemail

%dir /usr/share/emacs/site-lisp
%attr(0644,root,root) %config /usr/share/emacs/site-lisp/site-start.el
%dir /usr/share/emacs/site-lisp/site-start.d
%dir /usr/share/emacs/%{version}
%dir /usr/share/emacs/%{version}/site-lisp
%dir /usr/share/emacs/%{version}/leim
/usr/share/emacs/%{version}/etc

%files -f el-filelist el
%defattr(-,root,root)
/usr/share/emacs/site-lisp/python-mode.el
/usr/share/emacs/site-lisp/mwheel.el
/usr/share/emacs/site-lisp/rpm-spec-mode.el

%files -f leim-filelist leim
%defattr(-,root,root)
/usr/share/emacs/%{version}/leim/leim-list.el

%files nox
%defattr(-,root,root)
/usr/bin/emacs-nox

%files X11
%defattr(-,root,root)
%attr(755,root,root) /usr/bin/emacs
%attr(755,root,root) /usr/bin/emacs-%{version}
%config(noreplace) /etc/X11/applnk/Applications/emacs.desktop
/usr/share/pixmaps/emacs.png 

%changelog
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
