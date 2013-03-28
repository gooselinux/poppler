
Summary: PDF rendering library
Name: poppler
Version: 0.12.4
Release: 3%{?dist}.1
License: GPLv2
Group: Development/Libraries
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=557812
Patch0: poppler-0.12.3-text-selection.patch
Patch1: poppler-0.12.3-text-selection-tables.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=559604
Patch2: poppler-0.12.3-actualize-fcconfig.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=587678
Patch3: poppler-0.12.3-downscale.patch
Patch4: poppler-0.12.3-rotated-downscale.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=588723
Patch5: poppler-0.12.4-table-overlap.patch

## upstream patches
# for texlive/pdftex, make ObjStream class public
Patch100: poppler-0.12.1-objstream.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=595245
Patch101: poppler-0.12.4-CVE-2010-3702.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=639356
Patch102: poppler-0.12.4-CVE-2010-3703.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=638960
Patch103: poppler-0.12.4-CVE-2010-3704.patch

Requires: poppler-data >= 0.4.0
BuildRequires: automake libtool
BuildRequires: cairo-devel >= 1.8.4
BuildRequires: gtk2-devel
BuildRequires: lcms-devel
BuildRequires: libjpeg-devel
BuildRequires: openjpeg-devel >= 1.3-5
BuildRequires: qt3-devel
BuildRequires: qt4-devel


%description
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%package devel
Summary: Libraries and headers for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary: Glib wrapper for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary: Development files for glib wrapper
Group: Development/Libraries
Requires: %{name}-glib = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description glib-devel
%{summary}.

%package qt
Summary: Qt3 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description qt
%{summary}.

%package qt-devel
Summary: Development files for Qt3 wrapper
Group:   Development/Libraries
Requires: %{name}-qt = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt3-devel

%description qt-devel
%{summary}.

%package qt4
Summary: Qt4 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description qt4
%{summary}.

%package qt4-devel
Summary: Development files for Qt4 wrapper
Group:   Development/Libraries
Requires: %{name}-qt4 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: qt4-devel

%description qt4-devel
%{summary}.

%package utils
Summary: Command line utilities for converting PDF files
Group: Applications/Text
Requires: %{name} = %{version}-%{release}
%if 0%{?fedora} < 11 && 0%{?rhel} < 6
#  last seen in fc8
Provides: pdftohtml = 0.36-11
Obsoletes: pdftohtml < 0.36-11
#  last seen in fc7
Provides: xpdf-utils = 1:3.01-27
Obsoletes: xpdf-utils <= 1:3.01-26
# even earlier?
Conflicts: xpdf <= 1:3.01-8
%endif
%description utils
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%prep
%setup -q 

%patch0 -p1 -b .text-selection
%patch1 -p1 -b .text-selection-tables
%patch2 -p1 -b .fcconfig
%patch3 -p1 -b .downscale
%patch4 -p1 -b .rotated-downscale
%patch5 -p1 -b .cell-overlap
%patch100 -p1 -b .objstream
%patch101 -p1 -b .CVE-2010-3702
%patch102 -p1 -b .CVE-2010-3703
%patch103 -p1 -b .CVE-2010-3704

chmod -x goo/GooTimer.h

iconv -f iso-8859-1 -t utf-8 < "utils/pdftohtml.1" > "utils/pdftohtml.1.utf8"
mv "utils/pdftohtml.1.utf8" "utils/pdftohtml.1"

# hammer to nuke rpaths, recheck on new releases
autoreconf -i -f


%build
%configure \
  --disable-static \
  --enable-cairo-output \
  --enable-libjpeg \
  --enable-libopenjpeg \
  --enable-poppler-qt \
  --enable-poppler-qt4 \
  --enable-xpdf-headers \
  --disable-zlib

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 

rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post glib -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig

%post qt -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%post qt4 -p /sbin/ldconfig

%postun qt4 -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libpoppler.so.5*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/libpoppler.so
%{_includedir}/poppler/
%{_datadir}/gtk-doc/html/poppler

%files glib
%defattr(-,root,root,-)
%{_libdir}/libpoppler-glib.so.4*

%files glib-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/libpoppler-glib.so

%files qt
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt.so.2*

%files qt-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt.so
%{_libdir}/pkgconfig/poppler-qt.pc
%{_includedir}/poppler/qt3/

%files qt4
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so.3*

%files qt4-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Wed Oct  6 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-3.el6.1
- Add poppler-0.12.4-CVE-2010-3702.patch
    (Properly initialize parser)
- Add poppler-0.12.4-CVE-2010-3703.patch
    (Properly initialize stack)
- Add poppler-0.12.4-CVE-2010-3704.patch
    (Fix crash in broken pdf (code < 0))
- Resolves: #639859

* Wed May  5 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-3
- Don't detect overlaping cells as table
- Resolves: #588723

* Mon May  3 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-2
- Downscale images better
- Resolves: #587678

* Mon Mar 22 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-1
- Update to poppler-0.12.4
- Resolves: #575892

* Thu Jan 28 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-5
- Get current FcConfig before using it
- Resolves: #559604

* Fri Jan 22 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-4
- Fix text selection
- Add patch poppler-0.12.3-text-selection.patch by Brian Ewins
- Add patch poppler-0.12.3-text-selection-tables.patch by Marek Kasik
- Make Provides/Obsoletes versioned
- Add requirement of poppler-data
- Resolves: #557812

* Thu Jan 14 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-3
- Correct %%changelog
- Correct permissions of goo/GooTimer.h
- Convert pdftohtml.1 to utf8
- Related: #543948

* Mon Jan 11 2010 Warren Togami <wtogami@fedoraproject.org> - 0.12.3-2
- Actualize system version check.

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-1
- poppler-0.12.3

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.2-1
- poppler-0.12.2

* Sun Oct 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-3
- CVE-2009-3607 poppler: create_surface_from_thumbnail_data
  integer overflow (#526924)

* Mon Oct 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-1
- poppler-0.12.1
- deprecate xpdf/pdftohtml Conflicts/Obsoletes

* Wed Sep 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Tue Aug 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.3-1
- Update to 0.11.3

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-2
- omit poppler-data (#507675)

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-1
- poppler-0.11.1

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-6
- reduce lib deps in qt/qt4 pkg-config support

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-5
- --enable-libjpeg
- (explicitly) --disable-zlib

* Fri Jun 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-3
- --enable-libopenjpeg, --disable-zlib

* Sun May 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-2
- update changelog
- track sonames

* Tue May 19 2009 Bastien Nocera <bnocera@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.5-1
- Update to 0.10.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.4-1
- Update to 0.10.4

* Tue Jan 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-2
- add needed scriptlets
- nuke rpaths

* Tue Jan 13 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.2-1
- Update to 0.10.2

* Tue Nov 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1 and  -data 0.2.1

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.7-2
- cleanup qt3 hack
- %%description cosmetics

* Sun Sep  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Tue Aug 05 2008 Colin Walters <walters@redhat.com> - 0.8.5-1
- Update to 0.8.5

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Mon Apr 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Sun Apr 06 2008 Adam Jackson <ajax@redhat.com> 0.8.0-3
- poppler-0.8.0-ocg-crash.patch: Fix a crash when no optional content
  groups are defined.
- Mangle configure to account for the new directory for qt3 libs.
- Fix grammar in %%description.

* Tue Apr 01 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- -qt-devel: Requires: qt3-devel

* Sun Mar 30 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Sun Mar 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Mar 12 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Thu Feb 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Thu Feb 21 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.4-4
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Jindrich Novy <jnovy@redhat.com> - 0.6.4-3
- apply ObjStream patch (#433090)

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-2
- Add some required inter-subpackge deps

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-1
- Update to 0.6.4
- Split off poppler-glib

* Sun Dec  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-3
- Fix the qt3 checks some more

* Thu Nov 28 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-2
- package xpdf headers in poppler-devel (Jindrich Novy)
- Fix qt3 detection (Denis Leroy)

* Thu Nov 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Thu Oct 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.6-2
- include qt4 wrapper

* Tue Sep  4 2007 Kristian Høgsberg <krh@redhat.com> - 0.6-1
- Update to 0.6

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-2
- Remove debug spew

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-1
- Update to 0.5.91

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-2
- Update the license field

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-1
- Update to 0.5.9

* Thu Mar  1 2007 Bill Nottingham <notting@redhat.com> - 0.5.4-7
- fix it so the qt pkgconfig/.so aren't in the main poppler-devel

* Fri Dec 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-5
- Include epoch in the Provides/Obsoletes for xpdf-utils

* Wed Dec 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-4
- Add Provides/Obsoletes for xpdf-utils (#219033)

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.5.4-3
- drop hard-wired: Req: gtk2
- --disable-static
- enable qt wrapper
- -devel: Requires: pkgconfig

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.5.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.4-1.fc6
- Rebase to 0.5.4, drop poppler-0.5.3-libs.patch, fixes #205813,
  #205549, #200613, #172137, #172138, #161293 and more.

* Wed Sep 13 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.3-3.fc6
- Move .so to -devel (#203637).

* Mon Aug 14 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-2.fc6
- link against fontconfig (see bug 202256)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.3-1.1
- rebuild

* Wed May 31 2006 Kristian Høgsberg <krh@redhat.com> 0.5.3-1
- Update to 0.5.3.

* Mon May 22 2006 Kristian Høgsberg <krh@redhat.com> 0.5.2-1
- Update to 0.5.2.

* Wed Mar  1 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-2
- Rebuild the get rid of old soname dependency.

* Tue Feb 28 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-1
- Update to version 0.5.1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- change xpdf conflict version to be <= instead of <

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- update conflicts: xpdf line to be versioned

* Wed Jan 11 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.0-2.0
- Update to 0.5.0 and add poppler-utils subpackage.
- Flesh out poppler-utils subpackage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Sep  4 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.2-1
- Update to 0.4.2 and disable splash backend so we don't build it.

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-2
- Rebuild

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Wed Aug 17 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.0-2
- Bump release and rebuild.

* Wed Aug 17 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-2
- Rebuild to pick up new cairo soname.

* Mon Jun 20 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-1
- Update to 0.3.3 and change to build cairo backend.

* Sun May 22 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May  7 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.1
- Update to 0.3.1

* Sat Apr 23 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.0
- Update to 0.3.0

* Wed Apr 13 2005 Florian La Roche <laroche@redhat.com>
- remove empty post/postun scripts

* Wed Apr  6 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Sat Mar 12 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Use tar.gz because there are not bz of poppler

* Sat Mar  2 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.1-1
- Initial build
